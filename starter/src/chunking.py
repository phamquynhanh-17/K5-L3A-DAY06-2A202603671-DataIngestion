"""Fixed-size and structure/paragraph-aware chunking strategies."""
import re
from .models import Chunk, DocumentPage


def fixed_size(page: DocumentPage, size: int = 500, overlap: int = 50) -> list[Chunk]:
    """Split flattened page text into fixed-size overlapping windows."""
    if size <= 0:
        raise ValueError("size must be positive")
    if overlap < 0 or overlap >= size:
        raise ValueError("overlap must be >= 0 and < size")

    flat_text = re.sub(r"\s+", " ", page.text).strip()
    if not flat_text:
        return []

    chunks: list[Chunk] = []
    step = size - overlap
    start = 0
    idx = 0
    while start < len(flat_text):
        end = min(start + size, len(flat_text))
        piece = flat_text[start:end].strip()
        if piece:
            meta = dict(page.metadata)
            meta["chunk_index"] = idx
            meta["char_len"] = len(piece)
            chunks.append(
                Chunk(
                    chunk_id=f"{page.document_id}_p{page.page}_fixed_{idx}",
                    document_id=page.document_id,
                    source=page.source,
                    page=page.page,
                    text=piece,
                    metadata=meta,
                )
            )
            idx += 1
        if end == len(flat_text):
            break
        start += step
    return chunks


def _reconstruct_paragraphs(text: str) -> list[str]:
    """Reconstruct logical paragraphs from PDF line breaks."""
    raw_lines = [line.strip() for line in text.split("\n") if line.strip()]
    if not raw_lines:
        return []

    paragraphs: list[str] = []
    buffer: list[str] = []

    for line in raw_lines:
        # Skip standalone page number at the top of the page
        if not buffer and line.isdigit() and len(line) <= 3:
            continue

        buffer.append(line)
        # Heuristic: a line ending with sentence punctuation and shorter than typical wrap
        # or ending with quote/bracket after punctuation marks a paragraph boundary.
        if re.search(r'[.!?]["”\'\]]*(\[\d+\])?$', line) and len(line) < 78:
            paragraphs.append(" ".join(buffer))
            buffer = []

    if buffer:
        paragraphs.append(" ".join(buffer))
    return paragraphs


def _split_oversized_paragraph(para: str, max_size: int) -> list[str]:
    """Split an oversized paragraph along sentence boundaries when possible."""
    sentences = re.split(r"(?<=[.!?])\s+", para)
    parts: list[str] = []
    current = ""
    for sent in sentences:
        if not current:
            current = sent
        elif len(current) + 1 + len(sent) <= max_size:
            current = f"{current} {sent}"
        else:
            parts.append(current)
            current = sent
    if current:
        parts.append(current)

    # Hard split if a single sentence still exceeds max_size
    final_parts: list[str] = []
    for part in parts:
        if len(part) <= max_size:
            final_parts.append(part)
        else:
            for i in range(0, len(part), max_size):
                final_parts.append(part[i : i + max_size].strip())
    return [p for p in final_parts if p]


def by_paragraph(page: DocumentPage, max_size: int = 800) -> list[Chunk]:
    """Group logical paragraphs up to max_size, splitting oversized paragraphs cleanly."""
    paragraphs = _reconstruct_paragraphs(page.text)
    if not paragraphs:
        return []

    grouped_texts: list[str] = []
    current = ""

    for para in paragraphs:
        if len(para) > max_size:
            if current:
                grouped_texts.append(current)
                current = ""
            grouped_texts.extend(_split_oversized_paragraph(para, max_size))
            continue

        if not current:
            current = para
        elif len(current) + 2 + len(para) <= max_size:
            current = f"{current}\n\n{para}"
        else:
            grouped_texts.append(current)
            current = para

    if current:
        grouped_texts.append(current)

    chunks: list[Chunk] = []
    for idx, piece in enumerate(grouped_texts):
        meta = dict(page.metadata)
        meta["chunk_index"] = idx
        meta["char_len"] = len(piece)
        chunks.append(
            Chunk(
                chunk_id=f"{page.document_id}_p{page.page}_para_{idx}",
                document_id=page.document_id,
                source=page.source,
                page=page.page,
                text=piece,
                metadata=meta,
            )
        )
    return chunks
