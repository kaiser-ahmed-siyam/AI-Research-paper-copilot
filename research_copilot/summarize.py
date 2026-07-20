from __future__ import annotations

from pathlib import Path

from . import llm_client
from .models import Paper


# Keep the prompt small: enough of the paper to ground the summary without
# blowing past a small/free model's context window.
MAX_SOURCE_CHARS = 12000

STYLE_INSTRUCTIONS = {
    "one_sentence": "Summarize the paper in exactly one clear sentence.",
    "short": "Summarize the paper in a short paragraph of 3-5 sentences covering the problem, approach, and key result.",
    "detailed": (
        "Write a detailed structured summary with these sections: Problem, Approach, "
        "Key Results, and Limitations. Use short headers and bullet points."
    ),
    "eli5": "Explain the paper like I'm five years old, using simple language and an analogy. No jargon.",
}


def summarize_paper(paper: Paper, style: str = "short") -> str:
    if style not in STYLE_INSTRUCTIONS:
        raise ValueError(f"Unknown style '{style}'. Choose from {list(STYLE_INSTRUCTIONS)}.")

    source_text = paper.abstract
    if paper.text_path and Path(paper.text_path).exists():
        full_text = Path(paper.text_path).read_text(encoding="utf-8")
        source_text = f"Abstract:\n{paper.abstract}\n\nFull text (may be truncated):\n{full_text}"
    source_text = source_text[:MAX_SOURCE_CHARS]

    messages = [
        {
            "role": "system",
            "content": "You are a research assistant that writes accurate, faithful summaries of academic papers.",
        },
        {
            "role": "user",
            "content": (
                f"Paper title: {paper.title}\n\n{source_text}\n\n"
                f"Instruction: {STYLE_INSTRUCTIONS[style]}"
            ),
        },
    ]
    return llm_client.chat_completion(messages, max_tokens=700)
