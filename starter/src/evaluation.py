"""Evaluate retrieved top-3 chunks against verified gold evidence."""
import re
from typing import Any


def _norm_for_match(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip().lower()


def _matches_filter(metadata: dict[str, Any], filters: dict[str, Any] | None) -> bool:
    if not filters:
        return True
    return all(metadata.get(k) == v for k, v in filters.items())


def _is_evidence_hit(question: dict[str, Any], hit: dict[str, Any]) -> bool:
    meta = hit.get("metadata", {})
    if meta.get("document_id") != question["gold_source_id"]:
        return False
    if int(meta.get("page", -1)) != int(question["gold_page"]):
        return False

    chunk_norm = _norm_for_match(hit.get("text", ""))
    quote_norm = _norm_for_match(question["evidence_quote"])
    if quote_norm in chunk_norm:
        return True

    # Handle slight boundary clipping where at least 60% contiguous core of the quote appears
    words = quote_norm.split()
    if len(words) >= 8:
        window = max(6, int(len(words) * 0.6))
        for start in range(0, len(words) - window + 1):
            sub = " ".join(words[start : start + window])
            if sub in chunk_norm:
                return True
    return False


def evaluate_query(
    question: dict[str, Any],
    hits: list[dict[str, Any]],
    applied_filter: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Compute Hit@1, Evidence Hit@3, and filter compliance for one query."""
    hit_flags = [_is_evidence_hit(question, h) for h in hits]
    hit_at_1 = bool(hit_flags and hit_flags[0])
    hit_at_3 = any(hit_flags[:3])

    filter_compliant: bool | None = None
    if applied_filter:
        filter_compliant = all(_matches_filter(h.get("metadata", {}), applied_filter) for h in hits)

    return {
        "question_id": question["id"],
        "split": question["split"],
        "type": question.get("type", ""),
        "question": question["question"],
        "gold_source_id": question["gold_source_id"],
        "gold_page": question["gold_page"],
        "evidence_quote": question["evidence_quote"],
        "applied_filter": applied_filter,
        "hit_at_1": hit_at_1,
        "hit_at_3": hit_at_3,
        "filter_compliant": filter_compliant,
        "top_k": [
            {
                "rank": idx + 1,
                "chunk_id": h["chunk_id"],
                "score": h["score"],
                "metadata": h["metadata"],
                "is_hit": hit_flags[idx],
                "text": h["text"],
            }
            for idx, h in enumerate(hits)
        ],
    }


def summarize(traces: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate Hit@1 and Evidence Hit@3 by split (dev/test/all)."""
    summary: dict[str, Any] = {}
    for split_name in ("dev", "test", "all"):
        subset = traces if split_name == "all" else [t for t in traces if t["split"] == split_name]
        n = len(subset)
        h1 = sum(1 for t in subset if t["hit_at_1"])
        h3 = sum(1 for t in subset if t["hit_at_3"])
        filtered = [t for t in subset if t["filter_compliant"] is not None]
        fc_ok = sum(1 for t in filtered if t["filter_compliant"])
        summary[split_name] = {
            "total": n,
            "hit_at_1_count": h1,
            "hit_at_1": round(h1 / n, 4) if n else 0.0,
            "hit_at_3_count": h3,
            "hit_at_3": round(h3 / n, 4) if n else 0.0,
            "filter_queries": len(filtered),
            "filter_compliant_count": fc_ok,
        }
    return summary
