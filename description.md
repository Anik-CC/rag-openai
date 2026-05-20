# PDF Assistant — RAG Q&A

Upload any PDF and ask natural-language questions. Answers are grounded in the document via Retrieval-Augmented Generation — no hallucinations from general training data.

## Stack

| Layer | Module |
|---|---|
| Frontend | Streamlit |
| Document loading | LangChain `PyPDFLoader` |
| Text splitting | `RecursiveCharacterTextSplitter` — 100 char chunks, 10 char overlap |
| Embeddings | HuggingFace `all-MiniLM-L6-v2` — 384-dim, runs locally |
| Vector store | FAISS (in-memory) |
| LLM | OpenRouter API — free-tier models (Arcee, DeepSeek, Llama, Gemma) |
| Orchestration | LangChain `VectorstoreIndexCreator` |

## How it works

1. PDF is loaded and split into chunks
2. Chunks are embedded locally (no data sent externally)
3. On each question, the top matching chunks are retrieved via cosine similarity
4. Retrieved context + question are sent to the LLM
5. LLM returns a grounded answer
