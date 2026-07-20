from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from urllib.request import Request, urlopen

from .config import PAPER_DIR, TEXT_DIR, ensure_data_dirs
from .http_utils import SSL_CONTEXT
from .models import Paper


def download_pdf(paper: Paper) -> Paper:
    ensure_data_dirs()
    target = PAPER_DIR / f"{_safe_filename(paper.arxiv_id)}.pdf"
    if not target.exists():
        request = Request(
            paper.pdf_url,
            headers={"User-Agent": "ai-research-paper-copilot/0.1"},
        )
        with urlopen(request, timeout=60, context=SSL_CONTEXT) as response:
            target.write_bytes(response.read())
    return replace(paper, local_path=str(target))


def extract_text(paper: Paper) -> Paper:
    if not paper.local_path:
        raise ValueError("PDF must be downloaded before text extraction.")

    ensure_data_dirs()
    target = TEXT_DIR / f"{_safe_filename(paper.arxiv_id)}.txt"
    text = _extract_with_pymupdf(Path(paper.local_path))
    target.write_text(text, encoding="utf-8")
    return replace(paper, text_path=str(target))


def _extract_with_pymupdf(pdf_path: Path) -> str:
    try:
        import fitz
    except ImportError as error:
        raise RuntimeError(
            "PyMuPDF is required for PDF extraction. Install dependencies with "
            "`python -m pip install -r requirements.txt`."
        ) from error

    chunks: list[str] = []
    with fitz.open(pdf_path) as document:
        for index, page in enumerate(document, start=1):
            page_text = page.get_text("text").strip()
            if page_text:
                chunks.append(f"\n\n--- Page {index} ---\n{page_text}")
    return "\n".join(chunks).strip()


def _safe_filename(value: str) -> str:
    return "".join(character if character.isalnum() or character in ".-" else "_" for character in value)

