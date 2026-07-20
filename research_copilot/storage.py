from __future__ import annotations

from contextlib import closing
import sqlite3
from pathlib import Path

from .config import DB_PATH, ensure_data_dirs
from .models import Paper


SCHEMA = """
CREATE TABLE IF NOT EXISTS papers (
    arxiv_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    authors TEXT NOT NULL,
    year INTEGER,
    abstract TEXT NOT NULL,
    pdf_url TEXT NOT NULL,
    source_url TEXT NOT NULL,
    published TEXT NOT NULL,
    local_path TEXT,
    text_path TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


def get_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    ensure_data_dirs()
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    connection.execute(SCHEMA)
    return connection


def upsert_paper(paper: Paper, db_path: Path = DB_PATH) -> None:
    with closing(get_connection(db_path)) as connection:
        connection.execute(
            """
            INSERT INTO papers (
                arxiv_id, title, authors, year, abstract, pdf_url, source_url,
                published, local_path, text_path
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(arxiv_id) DO UPDATE SET
                title = excluded.title,
                authors = excluded.authors,
                year = excluded.year,
                abstract = excluded.abstract,
                pdf_url = excluded.pdf_url,
                source_url = excluded.source_url,
                published = excluded.published,
                local_path = COALESCE(excluded.local_path, papers.local_path),
                text_path = COALESCE(excluded.text_path, papers.text_path),
                updated_at = CURRENT_TIMESTAMP
            """,
            (
                paper.arxiv_id,
                paper.title,
                paper.authors,
                paper.year,
                paper.abstract,
                paper.pdf_url,
                paper.source_url,
                paper.published,
                paper.local_path,
                paper.text_path,
            ),
        )
        connection.commit()


def list_papers(db_path: Path = DB_PATH) -> list[sqlite3.Row]:
    with closing(get_connection(db_path)) as connection:
        return connection.execute(
            """
            SELECT *
            FROM papers
            ORDER BY COALESCE(year, 0) DESC, updated_at DESC
            """
        ).fetchall()


def get_paper(arxiv_id: str, db_path: Path = DB_PATH) -> sqlite3.Row | None:
    with closing(get_connection(db_path)) as connection:
        return connection.execute(
            "SELECT * FROM papers WHERE arxiv_id = ?",
            (arxiv_id,),
        ).fetchone()


def row_to_paper(row: sqlite3.Row) -> Paper:
    """Convert a stored SQLite row back into a Paper for downstream tools."""
    return Paper(
        arxiv_id=row["arxiv_id"],
        title=row["title"],
        authors=row["authors"],
        year=row["year"],
        abstract=row["abstract"],
        pdf_url=row["pdf_url"],
        source_url=row["source_url"],
        published=row["published"],
        local_path=row["local_path"],
        text_path=row["text_path"],
    )
