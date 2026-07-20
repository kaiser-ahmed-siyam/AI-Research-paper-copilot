import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
PAPER_DIR = DATA_DIR / "papers"
TEXT_DIR = DATA_DIR / "texts"
CHROMA_DIR = DATA_DIR / "chroma"
DB_PATH = DATA_DIR / "papers.sqlite3"

# Embeddings: a small local sentence-transformers model (free, offline, no API key).
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")
CHROMA_COLLECTION_NAME = "papers"

# Generation: Groq's free-tier Llama models (OpenAI-compatible, no local GPU needed).
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

# Chunking defaults for RAG indexing (word-based, ~ token-proportional).
CHUNK_SIZE_WORDS = int(os.getenv("CHUNK_SIZE_WORDS", "220"))
CHUNK_OVERLAP_WORDS = int(os.getenv("CHUNK_OVERLAP_WORDS", "40"))


def ensure_data_dirs() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    PAPER_DIR.mkdir(parents=True, exist_ok=True)
    TEXT_DIR.mkdir(parents=True, exist_ok=True)
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)

