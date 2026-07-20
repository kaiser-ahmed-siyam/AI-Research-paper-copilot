from dataclasses import dataclass


@dataclass(frozen=True)
class Paper:
    arxiv_id: str
    title: str
    authors: str
    year: int | None
    abstract: str
    pdf_url: str
    source_url: str
    published: str
    local_path: str | None = None
    text_path: str | None = None

