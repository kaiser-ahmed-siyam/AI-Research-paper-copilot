import streamlit as st

from research_copilot.arxiv_client import search_arxiv
from research_copilot.llm_client import LLMNotConfiguredError
from research_copilot.pdf_tools import download_pdf, extract_text
from research_copilot.rag import answer_question
from research_copilot.storage import list_papers, row_to_paper, upsert_paper
from research_copilot.summarize import STYLE_INSTRUCTIONS, summarize_paper
from research_copilot.vector_store import index_paper


st.set_page_config(page_title="AI Research Paper Copilot", layout="wide")

st.title("AI Research Paper Copilot")

with st.sidebar:
    st.header("Library")
    stored = list_papers()
    st.metric("Saved papers", len(stored))
    if stored:
        for row in stored[:8]:
            st.caption(f"{row['year'] or 'n.d.'} - {row['title'][:72]}")
    st.divider()
    st.caption(
        "Ask & Summarize need a free Groq API key. Add `GROQ_API_KEY` to a "
        "`.env` file (see `.env.example`)."
    )

tab_search, tab_ask, tab_summarize = st.tabs(
    ["🔎 Search & Save", "💬 Ask your library", "📝 Summarize"]
)

with tab_search:
    query = st.text_input("Search arXiv", placeholder="retrieval augmented generation evaluation")
    limit = st.slider("Results", min_value=3, max_value=25, value=10)

    if st.button("Search", type="primary", disabled=not query.strip()):
        with st.spinner("Searching arXiv..."):
            st.session_state["results"] = search_arxiv(query, limit)

    results = st.session_state.get("results", [])
    if results:
        st.subheader("Results")

    for paper in results:
        with st.container(border=True):
            st.markdown(f"### {paper.title}")
            st.caption(f"{paper.authors} - {paper.year or 'n.d.'} - arXiv:{paper.arxiv_id}")
            st.write(paper.abstract)

            col1, col2, _ = st.columns([1, 1, 4])
            with col1:
                st.link_button("Open", paper.source_url)
            with col2:
                if st.button("Save PDF", key=f"save-{paper.arxiv_id}"):
                    try:
                        with st.spinner("Downloading and extracting text..."):
                            saved = extract_text(download_pdf(paper))
                            upsert_paper(saved)
                        try:
                            with st.spinner("Indexing for search..."):
                                chunk_count = index_paper(saved)
                            st.success(f"Saved and indexed ({chunk_count} chunks).")
                        except Exception as index_error:
                            st.warning(
                                f"Saved, but indexing for Ask/RAG failed: {index_error}"
                            )
                    except Exception as error:
                        st.error(str(error))

with tab_ask:
    st.write("Ask a question answered from the papers you've saved and indexed.")
    library = list_papers()
    if not library:
        st.info("Save at least one paper in the Search & Save tab first.")
    else:
        scope_options = {"All saved papers": None}
        scope_options.update(
            {f"{row['title'][:60]} (arXiv:{row['arxiv_id']})": row["arxiv_id"] for row in library}
        )
        scope_label = st.selectbox("Scope", list(scope_options.keys()))
        question = st.text_area("Question", placeholder="What evaluation metrics does this paper use?")
        top_k = st.slider("Chunks to retrieve", min_value=2, max_value=10, value=5)

        if st.button("Ask", type="primary", disabled=not question.strip()):
            try:
                with st.spinner("Retrieving context and asking the model..."):
                    result = answer_question(
                        question, arxiv_id=scope_options[scope_label], top_k=top_k
                    )
                st.markdown("#### Answer")
                st.write(result["answer"])
                if result["sources"]:
                    with st.expander(f"Sources ({len(result['sources'])})"):
                        for source in result["sources"]:
                            st.caption(
                                f"{source['title']} - arXiv:{source['arxiv_id']} - chunk {source['chunk_index']}"
                            )
                            st.text(source["document"][:500])
            except LLMNotConfiguredError as error:
                st.error(str(error))
            except Exception as error:
                st.error(f"Could not answer the question: {error}")

with tab_summarize:
    st.write("Generate a summary of a saved paper at your preferred depth.")
    library = list_papers()
    if not library:
        st.info("Save at least one paper in the Search & Save tab first.")
    else:
        paper_options = {
            f"{row['title'][:60]} (arXiv:{row['arxiv_id']})": row for row in library
        }
        paper_label = st.selectbox("Paper", list(paper_options.keys()))
        style_labels = {
            "one_sentence": "One sentence",
            "short": "Short paragraph",
            "detailed": "Detailed (structured)",
            "eli5": "Explain like I'm five",
        }
        style = st.radio(
            "Style",
            list(style_labels.keys()),
            format_func=lambda key: style_labels[key],
            horizontal=True,
        )

        if st.button("Summarize", type="primary"):
            try:
                paper = row_to_paper(paper_options[paper_label])
                with st.spinner("Summarizing..."):
                    summary = summarize_paper(paper, style=style)
                st.markdown("#### Summary")
                st.write(summary)
            except LLMNotConfiguredError as error:
                st.error(str(error))
            except Exception as error:
                st.error(f"Could not summarize: {error}")
