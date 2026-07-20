from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from .chunking import chunk_text
from .config import CHROMA_COLLECTION_NAME, CHROMA_DIR, EMBEDDING_MODEL_NAME, ensure_data_dirs
from .models import Paper


@lru_cache(maxsize=1)
def _embedding_function():
    # Imported lazily: sentence-transformers/torch are slow to import and only
    # needed once we actually touch the vector store.
    from chromadb.utils import embedding_functions

    return embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL_NAME)


@lru_cache(maxsize=1)
def _client():
    import chromadb

    ensure_data_dirs()
    return chromadb.PersistentClient(path=str(CHROMA_DIR))


def get_collection():
    return _client().get_or_create_collection(
        name=CHROMA_COLLECTION_NAME,
        embedding_function=_embedding_function(),
    )


def index_paper(paper: Paper) -> int:
    """Chunk a paper's extracted text and (re)index it in the vector store.

    Returns the number of chunks indexed. Re-indexing the same paper is safe:
    chunk ids are deterministic, so Chroma upserts in place.
    """
    if not paper.text_path:
        raise ValueError("Paper has no extracted text to index.")

    text = Path(paper.text_path).read_text(encoding="utf-8")
    chunks = chunk_text(text)
    if not chunks:
        return 0

    collection = get_collection()
    ids = [f"{paper.arxiv_id}-{index}" for index in range(len(chunks))]
    metadatas = [
        {"arxiv_id": paper.arxiv_id, "title": paper.title, "chunk_index": index}
        for index in range(len(chunks))
    ]
    collection.upsert(ids=ids, documents=chunks, metadatas=metadatas)
    return len(chunks)


def delete_paper(arxiv_id: str) -> None:
    get_collection().delete(where={"arxiv_id": arxiv_id})


def query_similar(query: str, top_k: int = 5, arxiv_id: str | None = None) -> list[dict]:
    """Return the top_k most relevant chunks for a query.

    Each result is {"document", "title", "arxiv_id", "chunk_index", "distance"}.
    """
    query = query.strip()
    if not query:
        return []

    collection = get_collection()
    where = {"arxiv_id": arxiv_id} if arxiv_id else None
    result = collection.query(
        query_texts=[query],
        n_results=top_k,
        where=where,
    )

    documents = (result.get("documents") or [[]])[0]
    metadatas = (result.get("metadatas") or [[]])[0]
    distances = (result.get("distances") or [[]])[0]

    hits: list[dict] = []
    for document, metadata, distance in zip(documents, metadatas, distances):
        hits.append(
            {
                "document": document,
                "title": metadata.get("title"),
                "arxiv_id": metadata.get("arxiv_id"),
                "chunk_index": metadata.get("chunk_index"),
                "distance": distance,
            }
        )
    return hits
