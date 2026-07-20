from __future__ import annotations

import xml.etree.ElementTree as ET
from urllib.parse import quote_plus
from urllib.request import Request, urlopen

from .http_utils import SSL_CONTEXT
from .models import Paper


ARXIV_API_URL = "https://export.arxiv.org/api/query"
ATOM_NS = {"atom": "http://www.w3.org/2005/Atom"}


def search_arxiv(query: str, max_results: int = 10) -> list[Paper]:
    """Search arXiv using its official Atom API."""
    cleaned_query = query.strip()
    if not cleaned_query:
        return []

    url = (
        f"{ARXIV_API_URL}?search_query=all:{quote_plus(cleaned_query)}"
        f"&start=0&max_results={int(max_results)}"
        "&sortBy=relevance&sortOrder=descending"
    )
    request = Request(url, headers={"User-Agent": "ai-research-paper-copilot/0.1"})
    with urlopen(request, timeout=30, context=SSL_CONTEXT) as response:
        xml_body = response.read()

    root = ET.fromstring(xml_body)
    papers: list[Paper] = []
    for entry in root.findall("atom:entry", ATOM_NS):
        arxiv_id = _text(entry, "atom:id").rsplit("/", 1)[-1]
        title = " ".join(_text(entry, "atom:title").split())
        abstract = " ".join(_text(entry, "atom:summary").split())
        authors = ", ".join(
            _text(author, "atom:name")
            for author in entry.findall("atom:author", ATOM_NS)
            if _text(author, "atom:name")
        )
        published = _text(entry, "atom:published")
        papers.append(
            Paper(
                arxiv_id=arxiv_id,
                title=title,
                authors=authors,
                year=_year_from_published(published),
                abstract=abstract,
                pdf_url=_pdf_url(entry) or f"https://arxiv.org/pdf/{arxiv_id}",
                source_url=_text(entry, "atom:id"),
                published=published,
            )
        )
    return papers


def _text(element: ET.Element, selector: str) -> str:
    found = element.find(selector, ATOM_NS)
    return found.text.strip() if found is not None and found.text else ""


def _year_from_published(published: str) -> int | None:
    try:
        return int(published[:4])
    except (TypeError, ValueError):
        return None


def _pdf_url(entry: ET.Element) -> str | None:
    for link in entry.findall("atom:link", ATOM_NS):
        if link.attrib.get("title") == "pdf":
            return link.attrib.get("href")
    return None

