"""End-to-end Day 06 pipeline: ingest, chunk (A/B/C), embed, store in Chroma, and evaluate."""
import csv
import json
import re
import statistics
import time
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from .chunking import by_paragraph, fixed_size
from .embeddings import OpenAIEmbedder
from .evaluation import evaluate_query, summarize
from .ingestion import load_pdf
from .store import ChromaVectorStore


def _verify_benchmark_quotes(pages, questions: list[dict[str, Any]]) -> None:
    """Verify every gold evidence_quote exists on its gold_page after normalization."""
    page_map = {p.page: re.sub(r"\s+", " ", p.text).strip().lower() for p in pages}
    missing = []
    for q in questions:
        gp = int(q["gold_page"])
        quote = re.sub(r"\s+", " ", q["evidence_quote"]).strip().lower()
        if gp not in page_map or quote not in page_map[gp]:
            missing.append((q["id"], gp))
    if missing:
        raise RuntimeError(f"Unverified gold evidence quotes on pages: {missing}")


def _export_manual_audit_template(
    out_path: Path,
    chunks_by_strategy: dict[str, list[Any]],
    traces_by_strategy: dict[str, list[dict[str, Any]]],
) -> None:
    """Generate a structured markdown template for manual Coherence, Metadata, and Grounding audits."""
    # Fixed 10 source pages (first 10 sorted content pages) selected prior to seeing scores
    sample_pages = sorted({c.page for c in chunks_by_strategy["A"]})[:10]
    lines = [
        "# Manual Audit Template",
        "",
        "## 1. Chunk Coherence (10 fixed source pages, scale 0-2)",
        "",
        "| Page (PDF) | Strategy A (first chunk preview) | Score A | Strategy B/C (first chunk preview) | Score B/C | Reason |",
        "|---:|---|---:|---|---:|---|",
    ]
    for p in sample_pages:
        ca = next((c for c in chunks_by_strategy["A"] if c.page == p), None)
        cb = next((c for c in chunks_by_strategy["B"] if c.page == p), None)
        pa = (ca.text[:120].replace("\n", " ") + "...") if ca else ""
        pb = (cb.text[:120].replace("\n", " ") + "...") if cb else ""
        lines.append(f"| {p} | `{pa}` | | `{pb}` | | |")

    lines.extend([
        "",
        "## 2. Test Set Grounding & Metadata Audit (5 test questions x top-3)",
        "",
    ])
    for strat in ("A", "B", "C"):
        lines.append(f"### Strategy {strat}")
        test_traces = [t for t in traces_by_strategy[strat] if t["split"] == "test"]
        for t in test_traces:
            lines.append(f"- **{t['question_id']}** (gold page {t['gold_page']}, Hit@3={t['hit_at_3']}, Filter={t['applied_filter']}): Grounding score (0-2): ___ | Metadata ok (x/3): ___ | Notes: ")
            for rank_item in t["top_k"]:
                meta = rank_item["metadata"]
                preview = rank_item["text"][:100].replace("\n", " ")
                lines.append(
                    f"  - Top-{rank_item['rank']} (score={rank_item['score']}, page={meta.get('page')}, section={meta.get('section')}, author={meta.get('author_role')}): `{preview}...`"
                )
        lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")


def _update_experiment_log(
    csv_path: Path,
    embedder_name: str,
    stats_by_strategy: dict[str, dict[str, Any]],
) -> None:
    """Update artifacts/experiment_log.csv with measured dev/test metrics."""
    rows = [
        {
            "strategy": "A",
            "chunking": "fixed_size",
            "chunk_size": "500",
            "overlap": "50",
            "metadata": "document_id,source,page,book_page,section,author_role",
            "filter": "none",
            "vectorizer": embedder_name,
            "hypothesis": "Chunk co dinh 500 ky tu de bi cat ngang cau/y, lam giam coherence va do chinh xac.",
            "dev_hit1": f"{stats_by_strategy['A']['summary']['dev']['hit_at_1_count']}/{stats_by_strategy['A']['summary']['dev']['total']} ({stats_by_strategy['A']['summary']['dev']['hit_at_1']:.2%})",
            "dev_hit3": f"{stats_by_strategy['A']['summary']['dev']['hit_at_3_count']}/{stats_by_strategy['A']['summary']['dev']['total']} ({stats_by_strategy['A']['summary']['dev']['hit_at_3']:.2%})",
            "test_hit1": f"{stats_by_strategy['A']['summary']['test']['hit_at_1_count']}/{stats_by_strategy['A']['summary']['test']['total']} ({stats_by_strategy['A']['summary']['test']['hit_at_1']:.2%})",
            "test_hit3": f"{stats_by_strategy['A']['summary']['test']['hit_at_3_count']}/{stats_by_strategy['A']['summary']['test']['total']} ({stats_by_strategy['A']['summary']['test']['hit_at_3']:.2%})",
            "notes": f"chunks={stats_by_strategy['A']['chunk_count']}, ingest_s={stats_by_strategy['A']['ingest_seconds']}",
        },
        {
            "strategy": "B",
            "chunking": "by_paragraph",
            "chunk_size": "800",
            "overlap": "0",
            "metadata": "document_id,source,page,book_page,section,author_role",
            "filter": "none",
            "vectorizer": embedder_name,
            "hypothesis": "Gom theo doan logic giup giu tron y (coherence cao hon A) va cai thien retrieval.",
            "dev_hit1": f"{stats_by_strategy['B']['summary']['dev']['hit_at_1_count']}/{stats_by_strategy['B']['summary']['dev']['total']} ({stats_by_strategy['B']['summary']['dev']['hit_at_1']:.2%})",
            "dev_hit3": f"{stats_by_strategy['B']['summary']['dev']['hit_at_3_count']}/{stats_by_strategy['B']['summary']['dev']['total']} ({stats_by_strategy['B']['summary']['dev']['hit_at_3']:.2%})",
            "test_hit1": f"{stats_by_strategy['B']['summary']['test']['hit_at_1_count']}/{stats_by_strategy['B']['summary']['test']['total']} ({stats_by_strategy['B']['summary']['test']['hit_at_1']:.2%})",
            "test_hit3": f"{stats_by_strategy['B']['summary']['test']['hit_at_3_count']}/{stats_by_strategy['B']['summary']['test']['total']} ({stats_by_strategy['B']['summary']['test']['hit_at_3']:.2%})",
            "notes": f"chunks={stats_by_strategy['B']['chunk_count']}, ingest_s={stats_by_strategy['B']['ingest_seconds']}",
        },
        {
            "strategy": "C",
            "chunking": "by_paragraph",
            "chunk_size": "800",
            "overlap": "0",
            "metadata": "document_id,source,page,book_page,section,author_role",
            "filter": "section/author_role when specified",
            "vectorizer": embedder_name,
            "hypothesis": "Ket hop chunk theo doan voi metadata filter giup thu hep pham vi va giam nhieu giua Graham/Zweig.",
            "dev_hit1": f"{stats_by_strategy['C']['summary']['dev']['hit_at_1_count']}/{stats_by_strategy['C']['summary']['dev']['total']} ({stats_by_strategy['C']['summary']['dev']['hit_at_1']:.2%})",
            "dev_hit3": f"{stats_by_strategy['C']['summary']['dev']['hit_at_3_count']}/{stats_by_strategy['C']['summary']['dev']['total']} ({stats_by_strategy['C']['summary']['dev']['hit_at_3']:.2%})",
            "test_hit1": f"{stats_by_strategy['C']['summary']['test']['hit_at_1_count']}/{stats_by_strategy['C']['summary']['test']['total']} ({stats_by_strategy['C']['summary']['test']['hit_at_1']:.2%})",
            "test_hit3": f"{stats_by_strategy['C']['summary']['test']['hit_at_3_count']}/{stats_by_strategy['C']['summary']['test']['total']} ({stats_by_strategy['C']['summary']['test']['hit_at_3']:.2%})",
            "notes": f"chunks={stats_by_strategy['C']['chunk_count']}, ingest_s={stats_by_strategy['C']['ingest_seconds']}",
        },
    ]
    fieldnames = list(rows[0].keys())
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    starter_dir = Path(__file__).resolve().parents[1]
    repo_root = starter_dir.parent
    load_dotenv(starter_dir / ".env")

    pdf_path = starter_dir / "data" / "sách.pdf"
    manifest_path = repo_root / "data" / "manifest.json"
    questions_path = repo_root / "benchmark" / "questions.json"
    results_dir = starter_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    # 1. Load & validate corpus (>= 30 content pages)
    pages, skipped_logs = load_pdf(
        path=pdf_path,
        document_id="nha-dau-tu-thong-minh-excerpt",
        source="starter/data/sách.pdf",
        manifest_path=manifest_path,
    )
    if len(pages) < 30:
        raise RuntimeError(f"Corpus has only {len(pages)} content pages (< 30).")

    questions = json.loads(questions_path.read_text(encoding="utf-8"))
    _verify_benchmark_quotes(pages, questions)
    print(f"Loaded {len(pages)} content pages (skipped {len(skipped_logs)}). Verified {len(questions)} benchmark questions.")

    # 2. Initialize real embedder & persistent Chroma store
    embedder = OpenAIEmbedder()
    store = ChromaVectorStore(persist_dir=results_dir / "chroma_db", dimensions=embedder.dimensions)

    # 3. Build chunks for A, B, C (with local cache for real API vectors)
    chunks_a = [c for p in pages for c in fixed_size(p, size=500, overlap=50)]
    chunks_b = [c for p in pages for c in by_paragraph(p, max_size=800)]
    chunks_by_strategy = {"A": chunks_a, "B": chunks_b, "C": chunks_b}

    cache_path = results_dir / "embeddings_cache.json"
    disk_cache: dict[str, Any] = {}
    if cache_path.exists():
        loaded = json.loads(cache_path.read_text(encoding="utf-8"))
        if loaded.get("model") == embedder.model_name:
            disk_cache = loaded.get("vectors", {})

    def _get_doc_vectors(key: str, chunks_list: list[Any]) -> list[list[float]]:
        cached = disk_cache.get(key)
        if cached and len(cached) == len(chunks_list):
            if embedder.dimensions == 0 and cached:
                embedder.dimensions = len(cached[0])
            return cached
        vecs = embedder.embed_documents([c.text for c in chunks_list])
        disk_cache[key] = vecs
        cache_path.write_text(
            json.dumps({"model": embedder.model_name, "vectors": disk_cache}),
            encoding="utf-8",
        )
        return vecs

    vectors_cache: dict[str, list[list[float]]] = {}
    stats_by_strategy: dict[str, dict[str, Any]] = {}
    traces_by_strategy: dict[str, list[dict[str, Any]]] = {}

    for strat in ("A", "B", "C"):
        t0 = time.perf_counter()
        chunks = chunks_by_strategy[strat]
        vec_key = "A" if strat == "A" else "B"
        if vec_key not in vectors_cache:
            vectors_cache[vec_key] = _get_doc_vectors(vec_key, chunks)
        store.upsert(strategy=strat, chunks=chunks, vectors=vectors_cache[vec_key])
        count_after_first = store.count(strat)
        # Verify idempotent re-ingestion does not duplicate chunks
        store.upsert(strategy=strat, chunks=chunks, vectors=vectors_cache[vec_key])
        count_after_reingest = store.count(strat)
        ingest_s = round(time.perf_counter() - t0, 3)

        lengths = [len(c.text) for c in chunks]
        stats_by_strategy[strat] = {
            "chunk_count": len(chunks),
            "count_after_reingest": count_after_reingest,
            "idempotent_ok": count_after_first == count_after_reingest == len(chunks),
            "total_chars": sum(lengths),
            "min_len": min(lengths),
            "median_len": statistics.median(lengths),
            "max_len": max(lengths),
            "ingest_seconds": ingest_s,
        }

    # 4. Run evaluation queries (reuse query vectors across A, B, C for fairness)
    if "queries" in disk_cache and len(disk_cache["queries"]) == len(questions):
        query_vectors = {q["id"]: disk_cache["queries"][q["id"]] for q in questions}
    else:
        query_vectors = {q["id"]: embedder.embed_query(q["question"]) for q in questions}
        disk_cache["queries"] = query_vectors
        cache_path.write_text(
            json.dumps({"model": embedder.model_name, "vectors": disk_cache}),
            encoding="utf-8",
        )

    for strat in ("A", "B", "C"):
        traces: list[dict[str, Any]] = []
        for q in questions:
            applied_filter = q.get("filter") if strat == "C" else None
            hits = store.search(
                strategy=strat,
                query_vector=query_vectors[q["id"]],
                top_k=3,
                filters=applied_filter,
            )
            traces.append(evaluate_query(q, hits, applied_filter=applied_filter))

        traces_by_strategy[strat] = traces
        summary = summarize(traces)
        stats_by_strategy[strat]["summary"] = summary
        (results_dir / f"traces_{strat}.json").write_text(
            json.dumps(traces, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(
            f"Strategy {strat} | Dev Hit@1={summary['dev']['hit_at_1_count']}/{summary['dev']['total']}, "
            f"Hit@3={summary['dev']['hit_at_3_count']}/{summary['dev']['total']} | "
            f"Test Hit@1={summary['test']['hit_at_1_count']}/{summary['test']['total']}, "
            f"Hit@3={summary['test']['hit_at_3_count']}/{summary['test']['total']}"
        )

    # 5. Save overall summary, skipped logs, audit template, and experiment_log.csv
    overall = {
        "model": embedder.model_name,
        "provider": embedder.provider,
        "dimensions": embedder.dimensions,
        "total_tokens": embedder.total_tokens,
        "content_pages": len(pages),
        "skipped_pages": skipped_logs,
        "strategies": stats_by_strategy,
    }
    (results_dir / "summary.json").write_text(
        json.dumps(overall, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    _export_manual_audit_template(
        results_dir / "manual_audit_template.md",
        chunks_by_strategy,
        traces_by_strategy,
    )
    _update_experiment_log(
        repo_root / "artifacts" / "experiment_log.csv",
        embedder.model_name,
        stats_by_strategy,
    )
    print(f"Done! Total embedding tokens used: {embedder.total_tokens}")


if __name__ == "__main__":
    main()
