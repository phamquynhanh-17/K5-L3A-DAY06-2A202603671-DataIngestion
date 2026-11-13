"""Persistent Chroma local vector store with cosine search and metadata filtering."""
from pathlib import Path
from typing import Any

import chromadb

from .models import Chunk


class ChromaVectorStore:
    """Persistent local Chroma store supporting strategy isolation and idempotent upsert."""

    def __init__(self, persist_dir: Path, dimensions: int) -> None:
        self.persist_dir = Path(persist_dir)
        self.persist_dir.mkdir(parents=True, exist_ok=True)
        self.dimensions = dimensions
        self.client = chromadb.PersistentClient(path=str(self.persist_dir))
        self._collections: dict[str, Any] = {}

    def _get_collection(self, strategy: str):
        name = f"day06_{strategy.lower()}"
        if name not in self._collections:
            self._collections[name] = self.client.get_or_create_collection(
                name=name,
                metadata={"hnsw:space": "cosine"},
            )
        return self._collections[name]

    def upsert(self, strategy: str, chunks: list[Chunk], vectors: list[list[float]]) -> None:
        if len(chunks) != len(vectors):
            raise ValueError(f"Mismatch: {len(chunks)} chunks vs {len(vectors)} vectors")
        if not chunks:
            return
        if self.dimensions > 0 and len(vectors[0]) != self.dimensions:
            raise ValueError(f"Expected {self.dimensions} dims, got {len(vectors[0])}")

        collection = self._get_collection(strategy)

        # Idempotent re-ingestion: remove only obsolete IDs for the same document_id(s)
        new_id_set = {c.chunk_id for c in chunks}
        doc_ids = sorted({c.document_id for c in chunks})
        for doc_id in doc_ids:
            existing = collection.get(where={"document_id": doc_id}, include=[])
            if existing and existing.get("ids"):
                obsolete = [eid for eid in existing["ids"] if eid not in new_id_set]
                if obsolete:
                    collection.delete(ids=obsolete)

        ids = [c.chunk_id for c in chunks]
        documents = [c.text for c in chunks]
        metadatas = []
        for c in chunks:
            meta: dict[str, Any] = {
                "document_id": c.document_id,
                "source": c.source,
                "page": int(c.page),
            }
            for k, v in c.metadata.items():
                if isinstance(v, (str, int, float, bool)):
                    meta[k] = v
            metadatas.append(meta)

        batch_size = 100
        for start in range(0, len(chunks), batch_size):
            end = start + batch_size
            collection.upsert(
                ids=ids[start:end],
                embeddings=vectors[start:end],
                documents=documents[start:end],
                metadatas=metadatas[start:end],
            )

    def count(self, strategy: str) -> int:
        return self._get_collection(strategy).count()

    def search(
        self,
        strategy: str,
        query_vector: list[float],
        top_k: int = 3,
        filters: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        collection = self._get_collection(strategy)
        where_clause: dict[str, Any] | None = None
        if filters:
            if len(filters) == 1:
                where_clause = dict(filters)
            else:
                where_clause = {"$and": [{k: v} for k, v in filters.items()]}

        result = collection.query(
            query_embeddings=[query_vector],
            n_results=top_k,
            where=where_clause,
            include=["documents", "metadatas", "distances"],
        )

        ids = result.get("ids", [[]])[0]
        docs = result.get("documents", [[]])[0]
        metas = result.get("metadatas", [[]])[0]
        dists = result.get("distances", [[]])[0]

        hits: list[dict[str, Any]] = []
        for cid, doc, meta, dist in zip(ids, docs, metas, dists):
            hits.append(
                {
                    "chunk_id": cid,
                    "text": doc,
                    "score": round(1.0 - float(dist), 6),
                    "metadata": meta,
                }
            )
        return hits
