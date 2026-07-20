from __future__ import annotations

from . import llm_client
from .vector_store import query_similar


SYSTEM_PROMPT = (
    "You are a research assistant answering questions about a personal library of "
    "academic papers. Answer strictly using the provided excerpts. If the excerpts "
    "don't contain the answer, say so plainly instead of guessing. When you use a "
    "fact, mention which paper it came from by title."
)


def answer_question(query: str, arxiv_id: str | None = None, top_k: int = 5) -> dict:
    """Answer a question via retrieval-augmented generation over indexed papers.

    Returns {"answer": str, "sources": list[dict]}. If nothing is indexed yet,
    or nothing relevant is found, "sources" is empty and "answer" explains why.
    """
    query = query.strip()
    if not query:
        return {"answer": "Please enter a question.", "sources": []}

    hits = query_similar(query, top_k=top_k, arxiv_id=arxiv_id)
    if not hits:
        return {
            "answer": (
                "No indexed content matches this question yet. Save and index at "
                "least one paper first."
            ),
            "sources": [],
        }

    context = "\n\n".join(
        f"[Source {index + 1} - {hit['title']} (arXiv:{hit['arxiv_id']}, chunk {hit['chunk_index']})]\n{hit['document']}"
        for index, hit in enumerate(hits)
    )
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"Excerpts:\n\n{context}\n\nQuestion: {query}",
        },
    ]
    answer = llm_client.chat_completion(messages)
    return {"answer": answer, "sources": hits}
