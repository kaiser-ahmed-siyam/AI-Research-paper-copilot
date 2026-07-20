from __future__ import annotations

from functools import lru_cache

from .config import GROQ_API_KEY, GROQ_MODEL


class LLMNotConfiguredError(RuntimeError):
    """Raised when a chat completion is requested without a Groq API key."""


@lru_cache(maxsize=1)
def _client():
    if not GROQ_API_KEY:
        raise LLMNotConfiguredError(
            "GROQ_API_KEY is not set. Get a free key at https://console.groq.com/keys "
            "and add it to a .env file (see .env.example)."
        )
    from groq import Groq

    return Groq(api_key=GROQ_API_KEY)


def chat_completion(
    messages: list[dict],
    model: str | None = None,
    temperature: float = 0.2,
    max_tokens: int = 900,
) -> str:
    """Send a chat completion request to Groq and return the reply text."""
    response = _client().chat.completions.create(
        model=model or GROQ_MODEL,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content.strip()
