import os
import json
import requests
import streamlit as st
import rag_backend as backend

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Q&A — OpenRouter RAG",
    page_icon="🤖",
    layout="wide",
)

_BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(_BASE_DIR, "uploaded_pdfs")
URLS_FILE  = os.path.join(_BASE_DIR, "saved_urls.json")
os.makedirs(UPLOAD_DIR, exist_ok=True)

FALLBACK_FREE_MODELS = {
    "Meta Llama 3.1 8B Instruct": "meta-llama/llama-3.1-8b-instruct:free",
    "Google Gemma 3 27B":         "google/gemma-3-27b-it:free",
    "DeepSeek R1":                "deepseek/deepseek-r1:free",
}

# ── Helpers ────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def fetch_free_models():
    try:
        resp = requests.get("https://openrouter.ai/api/v1/models", timeout=10)
        resp.raise_for_status()
        models = resp.json().get("data", [])
        free = {
            m["name"]: m["id"]
            for m in models
            if str(m.get("pricing", {}).get("prompt", "1")) == "0"
            and str(m.get("pricing", {}).get("completion", "1")) == "0"
        }
        return dict(sorted(free.items())) if free else FALLBACK_FREE_MODELS
    except Exception:
        return FALLBACK_FREE_MODELS

def load_urls():
    if os.path.exists(URLS_FILE):
        with open(URLS_FILE) as f:
            return json.load(f)
    return {}

def save_urls(data: dict):
    with open(URLS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def list_all_sources():
    """Combined dict of {display_label: path_or_url} for the query selector."""
    sources = {}
    default = os.path.join(_BASE_DIR, "LeavePolicy-2026.pdf")
    if os.path.exists(default):
        sources["📄 LeavePolicy-2026.pdf (default)"] = default
    for fname in sorted(os.listdir(UPLOAD_DIR)):
        if fname.lower().endswith(".pdf"):
            sources[f"📄 {fname}"] = os.path.join(UPLOAD_DIR, fname)
    for label, url in load_urls().items():
        sources[f"🌐 {label}"] = url
    return sources

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("⚙️ OpenRouter Config")
    st.markdown("---")

    # ── API Key ────────────────────────────────────────────────────────────────
    env_key = os.environ.get("OPENROUTER_API_KEY", "")
    api_key_input = st.text_input(
        "API Key", value=env_key, type="password",
        placeholder="sk-or-v1-...", help="Get a free key at openrouter.ai",
    )
    if not api_key_input:
        st.warning("Paste your OpenRouter API key above.")
    else:
        st.success("API key loaded ✓")

    st.markdown("---")

    # ── Knowledge Base ─────────────────────────────────────────────────────────
    st.subheader("📂 Knowledge Base")
    pdf_tab, url_tab = st.tabs(["📄 PDF Upload", "🌐 URL"])

    # ── PDF tab ────────────────────────────────────────────────────────────────
    with pdf_tab:
        uploaded_file = st.file_uploader("Choose a PDF", type="pdf", label_visibility="collapsed")

        if uploaded_file:
            save_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
            already_saved = os.path.exists(save_path)
            if already_saved:
                st.info(f"Already saved: **{uploaded_file.name}**")
            if st.button("💾 Save PDF", use_container_width=True, disabled=already_saved):
                with open(save_path, "wb") as f:
                    f.write(uploaded_file.read())
                st.success(f"✅ Saved: **{uploaded_file.name}**")
                st.rerun()

        # Saved PDFs list with delete
        saved_pdfs = sorted(
            f for f in os.listdir(UPLOAD_DIR) if f.lower().endswith(".pdf")
        )
        if saved_pdfs:
            st.markdown("**Saved PDFs**")
            for fname in saved_pdfs:
                col1, col2 = st.columns([5, 1])
                col1.caption(fname)
                if col2.button("🗑️", key=f"del_pdf_{fname}", help=f"Delete {fname}"):
                    fpath = os.path.join(UPLOAD_DIR, fname)
                    os.remove(fpath)
                    # Clear index if this PDF was active
                    if st.session_state.get("indexed_source") == fpath:
                        st.session_state.pop("vector_index", None)
                        st.session_state.pop("indexed_source", None)
                    st.rerun()
        else:
            st.caption("No PDFs uploaded yet.")

    # ── URL tab ────────────────────────────────────────────────────────────────
    with url_tab:
        st.caption("Add a direct link to a PDF document.")
        url_label = st.text_input("Label", placeholder="e.g. UPL India Leave Policy")
        url_value = st.text_input("URL",   placeholder="https://example.com/policy.pdf")

        if st.button("➕ Add URL", use_container_width=True):
            if url_label.strip() and url_value.strip():
                urls = load_urls()
                urls[url_label.strip()] = url_value.strip()
                save_urls(urls)
                st.success(f"✅ Saved: **{url_label.strip()}**")
                st.rerun()
            else:
                st.warning("Please fill in both Label and URL.")

        # Saved URLs list with delete
        saved_urls = load_urls()
        if saved_urls:
            st.markdown("**Saved URLs**")
            for label, url in saved_urls.items():
                col1, col2 = st.columns([5, 1])
                col1.caption(f"{label}")
                if col2.button("🗑️", key=f"del_url_{label}", help=f"Delete {label}"):
                    del saved_urls[label]
                    save_urls(saved_urls)
                    if st.session_state.get("indexed_source") == url:
                        st.session_state.pop("vector_index", None)
                        st.session_state.pop("indexed_source", None)
                    st.rerun()
        else:
            st.caption("No URLs saved yet.")

    st.markdown("---")

    # ── Source selector ────────────────────────────────────────────────────────
    all_sources = list_all_sources()
    if not all_sources:
        st.error("No sources available. Upload a PDF or add a URL.")
        selected_label  = None
        selected_source = None
    else:
        selected_label  = st.selectbox("Select source to query", list(all_sources.keys()))
        selected_source = all_sources[selected_label]
        st.caption(f"`{selected_source}`")

    st.markdown("---")

    # ── Model selector ─────────────────────────────────────────────────────────
    free_models = fetch_free_models()
    model_label = st.selectbox("Model (free tier)", list(free_models.keys()))
    selected_model = free_models[model_label]
    st.caption(f"`{selected_model}`")

    st.markdown("---")

    # ── Temperature ────────────────────────────────────────────────────────────
    temperature = st.slider("Temperature", 0.0, 1.0, 0.1, 0.05,
                            help="Lower = more factual, Higher = more creative")

    st.markdown("---")

    if st.button("🔄 Reload Knowledge Base", use_container_width=True):
        st.session_state.pop("vector_index", None)
        st.session_state.pop("indexed_source", None)
        st.rerun()

    st.caption("🧠 Embeddings: HuggingFace all-MiniLM-L6-v2 (local)")

# ── Main area ──────────────────────────────────────────────────────────────────
st.title("🤖 HR Q&A with RAG")
st.markdown(f"Powered by **OpenRouter** · Model: `{selected_model}`")
st.markdown("---")

# Rebuild index when source changes
if selected_source and (
    "vector_index" not in st.session_state
    or st.session_state.get("indexed_source") != selected_source
):
    with st.spinner(f"Building knowledge base from **{selected_label}**..."):
        st.session_state.vector_index  = backend.hr_index(pdf_path=selected_source)
        st.session_state.indexed_source = selected_source
    st.success(f"Knowledge base ready for **{selected_label}**!", icon="✅")

# Question input
question = st.text_area(
    "Ask a question about the selected source:",
    placeholder="e.g. How many casual leaves are employees entitled to?",
    height=100,
)

ask_button = st.button("Ask", type="primary", disabled=not api_key_input or not selected_source)

if ask_button and question.strip():
    with st.spinner(f"Querying {model_label}..."):
        try:
            answer = backend.hr_rag_response(
                index=st.session_state.vector_index,
                question=question,
                model_id=selected_model,
                api_key=api_key_input,
                temperature=temperature,
            )
            st.markdown("### Answer")
            st.write(answer)
        except Exception as e:
            st.error(f"Error: {e}")

elif ask_button and not question.strip():
    st.warning("Please enter a question before submitting.")
