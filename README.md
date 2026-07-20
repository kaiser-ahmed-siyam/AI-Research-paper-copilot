# AI Research Paper Copilot  
A research assistant for finding arXiv papers, downloading PDFs, extracting text,
indexing them for retrieval, and asking questions or generating summaries over
your personal library.

## Current scope

**Phase 1 - core pipeline**
- Search arXiv through the official API
- Save title, authors, year, abstract, arXiv URL, PDF URL, local PDF path, and extracted text path in SQLite
- Download PDFs into `data/papers`
- Extract text with PyMuPDF into `data/texts`

**Phase 2 - RAG core**
- Chunk extracted text and embed it locally with `sentence-transformers` (`all-MiniLM-L6-v2`, free, offline)
- Persist embeddings in a local ChromaDB store (`data/chroma`)
- "Ask your library" - retrieval-augmented Q&A over all saved papers or one paper, answered by a free Groq-hosted Llama model
- Auto-summary in four styles: one-sentence, short paragraph, detailed (structured), and ELI5

All of the above is available through the Streamlit app.

## Setup

```powershell
..\venv\Scripts\python.exe -m pip install -r requirements.txt
copy .env.example .env
# then edit .env and add a free Groq API key from https://console.groq.com/keys
..\venv\Scripts\python.exe -m streamlit run app.py
```

The app stores its local library in `data/papers.sqlite3` and its vector index in `data/chroma`.
Saving a paper automatically chunks and indexes it; searching arXiv and downloading PDFs
work without any API key, but "Ask your library" and "Summarize" require `GROQ_API_KEY`.

## Roadmap

1. Paper comparison, methodology extraction, and citation generation (APA/MLA/IEEE/BibTeX).
2. Literature review generation, research gap finder, knowledge graph, trend analysis, and recommendations.
3. Per-document paper chat, exports (Markdown/PDF/Word/PPTX), and polish.

## [Web](https://ai-research-paper-copilot.onrender.com)

