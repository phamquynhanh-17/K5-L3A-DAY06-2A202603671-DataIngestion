"""Real embedding provider adapter supporting Gemini, OpenAI, and OpenRouter APIs."""
import os
import time
from typing import Protocol

import requests
from openai import OpenAI


class Embedder(Protocol):
    model_name: str
    dimensions: int
    total_tokens: int

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Return one vector per input text, in the same order."""
        ...

    def embed_query(self, question: str) -> list[float]:
        """Return a query vector compatible with the stored document vectors."""
        ...


class OpenAIEmbedder:
    """Real embedding adapter supporting Gemini, OpenAI, and OpenRouter APIs (no mock fallback)."""

    def __init__(self, model_name: str | None = None, batch_size: int = 32) -> None:
        gemini_key = (os.getenv("GEMINI_API_KEY") or "").strip()
        openai_key = (os.getenv("OPENAI_API_KEY") or "").strip()
        openrouter_key = (os.getenv("OPENROUTER_API_KEY") or "").strip()

        self.batch_size = batch_size
        self.total_tokens = 0
        self.dimensions = 0

        if gemini_key:
            self.provider = "gemini"
            self.api_key = gemini_key
            self.client = None
            default_model = "gemini-embedding-001"
            self.model_name = (model_name or os.getenv("EMBEDDING_MODEL") or default_model).strip()
        elif openai_key:
            self.provider = "openai"
            self.api_key = openai_key
            self.client = OpenAI(api_key=openai_key)
            default_model = "text-embedding-3-small"
            self.model_name = (model_name or os.getenv("EMBEDDING_MODEL") or default_model).strip()
            self.dimensions = 1536 if "3-small" in self.model_name else 0
        elif openrouter_key:
            self.provider = "openrouter"
            self.api_key = openrouter_key
            self.client = OpenAI(
                api_key=openrouter_key,
                base_url="https://openrouter.ai/api/v1",
            )
            default_model = "openai/text-embedding-3-small"
            self.model_name = (model_name or os.getenv("EMBEDDING_MODEL") or default_model).strip()
            self.dimensions = 1536 if "3-small" in self.model_name else 0
        else:
            raise RuntimeError(
                "Missing API key: set GEMINI_API_KEY, OPENAI_API_KEY, or OPENROUTER_API_KEY in starter/.env. "
                "Do not fall back to mock vectors."
            )

    def _gemini_batch_embed(self, texts: list[str], task_type: str) -> list[list[float]]:
        model_id = self.model_name.removeprefix("models/")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_id}:batchEmbedContents"
        payload = {
            "requests": [
                {
                    "model": f"models/{model_id}",
                    "content": {"parts": [{"text": t}]},
                    "taskType": task_type,
                }
                for t in texts
            ]
        }
        for attempt in range(6):
            resp = requests.post(url, params={"key": self.api_key}, json=payload, timeout=60)
            if resp.status_code == 429 and attempt < 5:
                wait_s = 38
                print(f"Gemini rate limit (429), waiting {wait_s}s before retry ({attempt + 1}/5)...", flush=True)
                time.sleep(wait_s)
                continue
            if not resp.ok:
                raise RuntimeError(f"Gemini embedding error {resp.status_code}: {resp.text}")
            data = resp.json()
            vectors = [list(item["values"]) for item in data["embeddings"]]
            if vectors and self.dimensions == 0:
                self.dimensions = len(vectors[0])
            return vectors
        raise RuntimeError("Gemini embedding failed after retries due to rate limit.")

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        vectors: list[list[float]] = []
        for start in range(0, len(texts), self.batch_size):
            batch = texts[start : start + self.batch_size]
            if self.provider == "gemini":
                vectors.extend(self._gemini_batch_embed(batch, task_type="RETRIEVAL_DOCUMENT"))
            else:
                assert self.client is not None
                resp = self.client.embeddings.create(model=self.model_name, input=batch)
                if resp.usage and resp.usage.total_tokens:
                    self.total_tokens += int(resp.usage.total_tokens)
                sorted_data = sorted(resp.data, key=lambda item: item.index)
                for item in sorted_data:
                    vec = list(item.embedding)
                    if self.dimensions == 0:
                        self.dimensions = len(vec)
                    vectors.append(vec)
        return vectors

    def embed_query(self, question: str) -> list[float]:
        if self.provider == "gemini":
            return self._gemini_batch_embed([question], task_type="RETRIEVAL_QUERY")[0]
        assert self.client is not None
        resp = self.client.embeddings.create(model=self.model_name, input=[question])
        if resp.usage and resp.usage.total_tokens:
            self.total_tokens += int(resp.usage.total_tokens)
        vec = list(resp.data[0].embedding)
        if self.dimensions == 0:
            self.dimensions = len(vec)
        return vec
