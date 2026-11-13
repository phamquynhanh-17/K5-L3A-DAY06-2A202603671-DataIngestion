"""Read and normalize source data with full page/section traceability."""
import json
import re
import unicodedata
from pathlib import Path
from typing import Any

from pypdf import PdfReader

from .models import DocumentPage


def normalize_text(text: str) -> str:
    """Normalize Unicode to NFC and clean whitespace while keeping paragraph breaks."""
    text = unicodedata.normalize("NFC", text or "")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # Clean trailing spaces on each line and collapse multiple spaces within lines
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.split("\n")]
    # Collapse 3+ consecutive newlines into double newline
    cleaned = "\n".join(lines)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


def _load_manifest_page_map(manifest_path: Path | None) -> tuple[dict[int, dict[str, Any]], set[int]]:
    """Build lookup maps from pdf_page -> section metadata and excluded pages."""
    page_meta: dict[int, dict[str, Any]] = {}
    excluded: set[int] = set()
    if not manifest_path or not manifest_path.exists():
        return page_meta, excluded

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for item in manifest.get("excluded_pages", []):
        excluded.add(int(item["pdf_page"]))

    for sec in manifest.get("sections", []):
        pdf_pages = sec.get("pdf_pages", [])
        book_pages = sec.get("book_pages", [])
        for idx, pdf_page in enumerate(pdf_pages):
            book_page = book_pages[idx] if idx < len(book_pages) else None
            page_meta[int(pdf_page)] = {
                "section": sec["section_id"],
                "author_role": sec["author_role"],
                "section_title": sec["title"],
                "book_page": int(book_page) if book_page is not None else 0,
            }
    return page_meta, excluded


def load_pdf(
    path: Path,
    document_id: str,
    source: str,
    manifest_path: Path | None = None,
    min_chars: int = 100,
) -> tuple[list[DocumentPage], list[dict[str, Any]]]:
    """Extract each physical PDF page, normalize text, attach metadata, and log skipped pages."""
    reader = PdfReader(str(path))
    page_meta_map, excluded_pages = _load_manifest_page_map(manifest_path)

    pages: list[DocumentPage] = []
    skipped_logs: list[dict[str, Any]] = []

    for idx, raw_page in enumerate(reader.pages, start=1):
        raw_text = raw_page.extract_text() or ""
        norm_text = normalize_text(raw_text)

        if idx in excluded_pages or len(norm_text) < min_chars:
            skipped_logs.append(
                {
                    "pdf_page": idx,
                    "char_count": len(norm_text),
                    "reason": "excluded_in_manifest" if idx in excluded_pages else f"below_min_chars({min_chars})",
                    "preview": norm_text[:100],
                }
            )
            continue

        meta = dict(page_meta_map.get(idx, {}))
        meta["pdf_page"] = idx
        pages.append(
            DocumentPage(
                document_id=document_id,
                source=source,
                page=idx,
                text=norm_text,
                metadata=meta,
            )
        )

    return pages, skipped_logs
