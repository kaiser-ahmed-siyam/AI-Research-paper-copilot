# 🤖 AI Research Paper Copilot 

> An AI-powered research assistant that automates academic paper discovery, semantic search, and Retrieval-Augmented Generation (RAG) over your personal research library.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-red?logo=streamlit)
![ChromaDB](https://img.shields.io/badge/Vector%20Database-ChromaDB-success)
![RAG](https://img.shields.io/badge/AI-Retrieval%20Augmented%20Generation-purple)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📖 Overview

**AI Research Paper Copilot** is an end-to-end research assistant designed to simplify academic literature exploration. It enables researchers and students to search papers from **arXiv**, download PDFs, extract text, build a local semantic knowledge base, and interact with research papers using **Large Language Models (LLMs)**.

Instead of manually reading hundreds of pages, users can ask natural language questions, retrieve relevant information from their document collection, and generate concise summaries powered by **Retrieval-Augmented Generation (RAG)**.

---

## ✨ Key Features

* 🔍 Search research papers directly from the **arXiv API**
* 📄 Download academic PDFs automatically
* 📚 Extract text from PDFs using **PyMuPDF**
* 🧠 Generate semantic embeddings using **Sentence Transformers**
* ⚡ Store and retrieve embeddings with **ChromaDB**
* 🤖 Ask questions over your research library using **RAG**
* 📝 Generate AI-powered summaries
* 💾 Store paper metadata in **SQLite**
* 🌐 Interactive web interface built with **Streamlit**
* 🧩 Modular architecture for easy extension

---

## 🏗️ Project Architecture

```
AI-Research-Paper-Copilot/
│
├── app.py                         # Streamlit application
│
├── research_copilot/
│   ├── arxiv_client.py            # arXiv API integration
│   ├── pdf_tools.py               # PDF download & extraction
│   ├── storage.py                 # SQLite database
│   ├── vector_store.py            # ChromaDB indexing
│   ├── rag.py                     # Retrieval-Augmented Generation
│   ├── summarize.py               # AI summarization
│   ├── llm_client.py              # Groq LLM integration
│   └── utils.py
│
├── data/
│   ├── papers/
│   ├── extracted_text/
│   └── chroma_db/
│
├── tests/
├── requirements.txt
├── .env.example
└── README.md
```

---

## ⚙️ Tech Stack

| Category        | Technologies          |
| --------------- | --------------------- |
| Language        | Python                |
| Frontend        | Streamlit             |
| LLM             | Groq API              |
| Embeddings      | Sentence Transformers |
| Vector Database | ChromaDB              |
| PDF Processing  | PyMuPDF               |
| Database        | SQLite                |
| Environment     | python-dotenv         |
| Testing         | pytest                |

---

## 🚀 How It Works

```text
User Search
      │
      ▼
arXiv API
      │
      ▼
Download PDF
      │
      ▼
Extract Text
      │
      ▼
Chunk Documents
      │
      ▼
Generate Embeddings
      │
      ▼
Store in ChromaDB
      │
      ▼
Retrieve Relevant Chunks
      │
      ▼
Groq LLM
      │
      ▼
Answer Questions / Generate Summaries
```

---

## 📦 Installation

Clone the repository

```bash
git clone https://github.com/yourusername/AI-Research-Paper-Copilot.git

cd AI-Research-Paper-Copilot
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment

**Windows**

```bash
.venv\Scripts\activate
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```env
GROQ_API_KEY=your_api_key_here
```

Run the application

```bash
streamlit run app.py
```

---

## Web Deployment 

[AI-Research-paper-copilot](https://ai-research-paper-copilot.onrender.com)

## 💡 Usage

1. Search academic papers by keyword.
2. Download selected papers.
3. Automatically extract PDF text.
4. Build a semantic vector index.
5. Ask questions about your papers.
6. Generate concise AI-powered summaries.

---

## 🎯 Example Use Cases

* Literature review
* Research paper exploration
* Academic Q&A
* Paper summarization
* Semantic document search
* Research knowledge management

---

## 🔮 Future Improvements

* Multi-paper reasoning
* Literature review generation
* Citation generation (BibTeX/APA)
* Research paper comparison
* Cross-document insight extraction
* Export to PDF, Word, and Markdown
* Multi-source support (Semantic Scholar, PubMed, IEEE Xplore)

---

## 📸 Screenshots

> Add screenshots of:
>
> * Home Page
> * Paper Search
> * Semantic Search
> * AI Chat
> * Summary Generation

---

## 🤝 Contributing

Contributions, feature requests, and bug reports are welcome. Feel free to fork the repository and submit a pull request.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

[**Kaiser Ahmed**](https://github.com/kaiser-ahmed-siyam)

**Aspiring ML & AI Engineer | AI Researcher**

Specializing in **Machine Learning**, **Retrieval-Augmented Generation (RAG)**, **LLMs**, **Natural Language Processing**, and **AI-powered research tools**.

If you find this project useful, consider giving it a ⭐ to support future development.

<!-- # AI Research Paper Copilot  
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

