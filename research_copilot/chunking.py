from __future__ import annotations

from .config import CHUNK_OVERLAP_WORDS, CHUNK_SIZE_WORDS


def chunk_text(
    text: str,
    chunk_size: int = CHUNK_SIZE_WORDS,
    overlap: int = CHUNK_OVERLAP_WORDS,
) -> list[str]:
    """Split text into overlapping, word-bounded chunks for embedding.

    Word-based windows avoid pulling in a tokenizer dependency while staying
    roughly proportional to token count, which is good enough for chunking.
    """
    words = text.split()
    if not words:
        return []
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if overlap < 0 or overlap >= chunk_size:
        overlap = min(max(overlap, 0), chunk_size - 1)

    stride = chunk_size - overlap
    chunks: list[str] = []
    for start in range(0, len(words), stride):
        window = words[start : start + chunk_size]
        if not window:
            break
        chunks.append(" ".join(window))
        if start + chunk_size >= len(words):
            break
    return chunks
