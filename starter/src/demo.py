"""Interactive CLI demo to query the persisted Chroma vector store across strategies A, B, and C."""
import argparse
import sys
from pathlib import Path

from dotenv import load_dotenv

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from src.embeddings import OpenAIEmbedder
    from src.store import ChromaVectorStore
else:
    from .embeddings import OpenAIEmbedder
    from .store import ChromaVectorStore


def run_query(
    store: ChromaVectorStore,
    embedder: OpenAIEmbedder,
    strategy: str,
    question: str,
    section: str | None = None,
    author_role: str | None = None,
    top_k: int = 3,
) -> None:
    filters: dict[str, str] = {}
    if section:
        filters["section"] = section
    if author_role:
        filters["author_role"] = author_role

    query_vec = embedder.embed_query(question)
    hits = store.search(
        strategy=strategy,
        query_vector=query_vec,
        top_k=top_k,
        filters=filters or None,
    )

    print(f"\n=== DEMO RETRIEVAL | Strategy {strategy} | Filter={filters or 'None'} ===")
    print(f"Query: {question}\n")
    if not hits:
        print("Không tìm thấy kết quả phù hợp.")
        return

    for idx, hit in enumerate(hits, start=1):
        meta = hit["metadata"]
        print(
            f"[Top-{idx}] score={hit['score']:.4f} | pdf_page={meta.get('page')} "
            f"(book_page={meta.get('book_page')}) | section={meta.get('section')} | author={meta.get('author_role')}"
        )
        print(f"  chunk_id: {hit['chunk_id']}")
        print(f"  text    : {hit['text']}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Demo truy vấn ChromaDB cho Day 06 Lab")
    parser.add_argument("--strategy", default="C", choices=["A", "B", "C"], help="Chiến lược (A, B, C)")
    parser.add_argument("--query", type=str, default=None, help="Câu hỏi truy vấn (bỏ trống để nhập tương tác)")
    parser.add_argument("--section", type=str, default=None, help="Filter theo section (vd: chapter_1, commentary_ch1)")
    parser.add_argument("--author", type=str, default=None, help="Filter theo author_role (graham, zweig, buffett)")
    parser.add_argument("--top-k", type=int, default=3, help="Số lượng kết quả trả về")
    args = parser.parse_args()

    starter_dir = Path(__file__).resolve().parents[1]
    load_dotenv(starter_dir / ".env")

    embedder = OpenAIEmbedder()
    store = ChromaVectorStore(persist_dir=starter_dir / "results" / "chroma_db", dimensions=embedder.dimensions)

    if args.query:
        run_query(store, embedder, args.strategy, args.query, args.section, args.author, args.top_k)
        return

    print(f"Chế độ Demo tương tác (Strategy {args.strategy} | gõ 'exit' để thoát).\n")
    while True:
        try:
            q = input("Nhập câu hỏi: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not q or q.lower() in {"exit", "quit"}:
            break
        run_query(store, embedder, args.strategy, q, args.section, args.author, args.top_k)


if __name__ == "__main__":
    main()

