import os
import json
import requests
import streamlit as st
import streamlit.components.v1 as components
import rag_backend as backend

st.set_page_config(
    page_title="PDF Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Inject CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

#MainMenu, footer, header { visibility: hidden; }

/* ── Background ── */
.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    min-height: 100vh;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: rgba(10, 8, 30, 0.97) !important;
    border-right: 1px solid rgba(255,255,255,0.07) !important;
}
section[data-testid="stSidebar"] * { color: rgba(255,255,255,0.85) !important; }
section[data-testid="stSidebar"] .stMarkdown h1 { font-size: 1.1rem !important; font-weight: 700; }

/* ── Sidebar inputs ── */
section[data-testid="stSidebar"] .stTextInput input,
section[data-testid="stSidebar"] .stTextInput input[type="password"] {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 8px !important;
    color: white !important;
    font-size: 0.88rem !important;
}
section[data-testid="stSidebar"] .stTextInput input:focus {
    border-color: rgba(102,126,234,0.5) !important;
    box-shadow: 0 0 0 2px rgba(102,126,234,0.12) !important;
}
section[data-testid="stSidebar"] .stSelectbox > div > div {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 8px !important;
}
section[data-testid="stSidebar"] .stFileUploader {
    background: rgba(255,255,255,0.03) !important;
    border: 2px dashed rgba(102,126,234,0.25) !important;
    border-radius: 10px !important;
}

/* ── Slider thumb ── */
.stSlider [data-baseweb="slider"] div[role="slider"] {
    background: #667eea !important;
}

/* ── Sidebar Tabs ── */
section[data-testid="stSidebar"] .stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.05) !important;
    border-radius: 8px !important;
    padding: 3px !important;
    gap: 3px !important;
}
section[data-testid="stSidebar"] .stTabs [data-baseweb="tab"] {
    border-radius: 6px !important;
    font-size: 0.82rem !important;
    padding: 5px 10px !important;
}
section[data-testid="stSidebar"] .stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
}

/* ── All buttons ── */
.stButton > button {
    border-radius: 8px !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    transition: all 0.18s !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    border: none !important;
    color: white !important;
    padding: 10px 32px !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 14px rgba(102,126,234,0.35) !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(102,126,234,0.5) !important;
}
.stButton > button[kind="primary"]:active { transform: translateY(0) !important; }
.stButton > button[kind="primary"]:disabled,
.stButton > button[kind="primary"][disabled] {
    opacity: 0.38 !important;
    cursor: not-allowed !important;
    box-shadow: none !important;
    transform: none !important;
    filter: grayscale(30%) !important;
}
.stButton > button:not([kind="primary"]) {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    color: rgba(255,255,255,0.75) !important;
}
.stButton > button:not([kind="primary"]):hover {
    background: rgba(255,255,255,0.11) !important;
    border-color: rgba(255,255,255,0.22) !important;
    color: white !important;
}

/* ── Main text area ── */
.stTextArea textarea {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 12px !important;
    color: rgba(255,255,255,0.9) !important;
    font-size: 0.95rem !important;
    line-height: 1.6 !important;
    resize: none !important;
    transition: border-color 0.2s !important;
}
.stTextArea textarea:focus {
    border-color: rgba(102,126,234,0.55) !important;
    box-shadow: 0 0 0 3px rgba(102,126,234,0.1) !important;
}
.stTextArea textarea::placeholder { color: rgba(255,255,255,0.28) !important; }
.stTextArea label { color: rgba(255,255,255,0.6) !important; font-size: 0.85rem !important; }

/* ── Alerts ── */
.stSuccess > div {
    background: rgba(52,211,153,0.08) !important;
    border: 1px solid rgba(52,211,153,0.25) !important;
    border-radius: 10px !important;
    color: rgba(52,211,153,0.9) !important;
}
.stWarning > div {
    background: rgba(251,191,36,0.08) !important;
    border: 1px solid rgba(251,191,36,0.25) !important;
    border-radius: 10px !important;
}
.stError > div {
    background: rgba(239,68,68,0.08) !important;
    border: 1px solid rgba(239,68,68,0.25) !important;
    border-radius: 10px !important;
}
.stInfo > div {
    background: rgba(96,165,250,0.08) !important;
    border: 1px solid rgba(96,165,250,0.25) !important;
    border-radius: 10px !important;
}

/* ── Divider ── */
hr { border-color: rgba(255,255,255,0.08) !important; margin: 12px 0 !important; }

/* ── Caption ── */
.stCaption, .stCaption p { color: rgba(255,255,255,0.38) !important; font-size: 0.76rem !important; }

/* ── Spinner ── */
.stSpinner > div { border-top-color: #667eea !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: rgba(255,255,255,0.02); }
::-webkit-scrollbar-thumb { background: rgba(102,126,234,0.35); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(102,126,234,0.55); }

/* ── Sidebar PDF/URL row — vertically centre name + delete button ── */
section[data-testid="stSidebar"] div[data-testid="column"] {
    display: flex !important;
    align-items: center !important;
}

/* ── Delete icon button: small, red-tinted, centred ── */
section[data-testid="stSidebar"] div[data-testid="column"]:last-child .stButton > button {
    padding: 2px 7px !important;
    min-height: 26px !important;
    height: 26px !important;
    font-size: 0.82rem !important;
    line-height: 1 !important;
    background: rgba(239,68,68,0.09) !important;
    border: 1px solid rgba(239,68,68,0.22) !important;
    color: rgba(255,120,120,0.85) !important;
    border-radius: 6px !important;
    width: 100% !important;
    justify-content: center !important;
}
section[data-testid="stSidebar"] div[data-testid="column"]:last-child .stButton > button:hover {
    background: rgba(239,68,68,0.2) !important;
    border-color: rgba(239,68,68,0.4) !important;
    color: rgba(255,150,150,1) !important;
}

</style>
""", unsafe_allow_html=True)

# ── Floating sidebar toggle (JS injected into parent window) ──────────────────
components.html("""
<script>
(function() {
    var pd = window.parent.document;
    if (pd.getElementById('_cc_sidebar_tab')) return;

    var tab = pd.createElement('div');
    tab.id = '_cc_sidebar_tab';
    tab.title = 'Open settings';
    tab.style.cssText = [
        'position:fixed;left:0;top:50%;transform:translateY(-50%);',
        'z-index:2147483647;cursor:pointer;',
        'background:linear-gradient(180deg,#667eea,#764ba2);',
        'border-radius:0 14px 14px 0;width:24px;height:80px;',
        'display:flex;align-items:center;justify-content:center;',
        'box-shadow:4px 0 20px rgba(102,126,234,0.65);',
        'border:1px solid rgba(255,255,255,0.2);border-left:none;',
        'transition:width 0.18s ease,box-shadow 0.18s ease,opacity 0.22s ease;',
        'opacity:1;'
    ].join('');
    tab.innerHTML = '<svg width="9" height="15" viewBox="0 0 9 15" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M1.5 1.5L7.5 7.5L1.5 13.5" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>';

    // Use sidebar pixel width as the ground truth — reliable across Streamlit versions
    function sidebarWidth() {
        var s = pd.querySelector('section[data-testid="stSidebar"]');
        return s ? s.getBoundingClientRect().width : 0;
    }

    function updateTab() {
        var open = sidebarWidth() > 60;
        tab.style.opacity        = open ? '0' : '1';
        tab.style.pointerEvents  = open ? 'none' : 'auto';
    }

    tab.addEventListener('mouseenter', function(){ this.style.width='32px'; this.style.boxShadow='6px 0 28px rgba(102,126,234,0.85)'; });
    tab.addEventListener('mouseleave', function(){ this.style.width='24px'; this.style.boxShadow='4px 0 20px rgba(102,126,234,0.65)'; });
    tab.addEventListener('click', function(){
        var btn = pd.querySelector('[data-testid="collapsedControl"] button')
                || pd.querySelector('[data-testid="stSidebarCollapseButton"] button')
                || pd.querySelector('button[aria-label="Open sidebar"]')
                || pd.querySelector('button[aria-label="Close sidebar"]');
        if (btn) btn.click();
    });

    pd.body.appendChild(tab);

    // ResizeObserver tracks sidebar width changes (open/close animation)
    function attachObserver() {
        var sidebar = pd.querySelector('section[data-testid="stSidebar"]');
        if (sidebar) {
            new ResizeObserver(updateTab).observe(sidebar);
            updateTab();
        } else {
            // Sidebar not in DOM yet — wait for it
            setTimeout(attachObserver, 200);
        }
    }
    attachObserver();
})();
</script>
""", height=0, scrolling=False)

# ── Constants ──────────────────────────────────────────────────────────────────
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

def validate_pdf_url(url: str) -> tuple[bool, str]:
    """Return (ok, error_message). Checks Content-Type via a HEAD request."""
    try:
        r = requests.head(url, timeout=8, allow_redirects=True)
        ct = r.headers.get("Content-Type", "")
        if "pdf" in ct.lower():
            return True, ""
        if url.lower().split("?")[0].endswith(".pdf"):
            return True, ""
        return False, (
            f"The URL doesn't appear to serve a PDF "
            f"(Content-Type: `{ct or 'unknown'}`). "
            "Please use a direct link to a .pdf file."
        )
    except requests.exceptions.Timeout:
        return False, "Request timed out. Check that the URL is reachable."
    except Exception as exc:
        return False, f"Could not reach the URL: {exc}"

def list_all_sources():
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
    st.markdown("### ⚙️ Configuration")
    st.markdown("---")

    api_key_input = os.environ.get("OPENROUTER_API_KEY", "") or st.secrets.get("OPENROUTER_API_KEY", "")
    if api_key_input:
        st.caption("🔑 API key loaded ✓")

    st.markdown("---")
    st.markdown("##### 📂 Knowledge Base")
    pdf_tab, url_tab = st.tabs(["📄 PDF", "🌐 URL"])

    with pdf_tab:
        uploaded_file = st.file_uploader("Upload PDF", type="pdf", label_visibility="collapsed")
        if uploaded_file:
            save_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
            already_saved = os.path.exists(save_path)
            if already_saved:
                st.info(f"Already saved: **{uploaded_file.name}**")
            if st.button("💾 Save PDF", use_container_width=True, disabled=already_saved):
                with open(save_path, "wb") as f:
                    f.write(uploaded_file.read())
                st.success(f"Saved: **{uploaded_file.name}**")
                st.rerun()

        saved_pdfs = sorted(f for f in os.listdir(UPLOAD_DIR) if f.lower().endswith(".pdf"))
        if saved_pdfs:
            st.markdown("<small style='color:rgba(255,255,255,0.45);text-transform:uppercase;letter-spacing:.5px;font-size:.72rem'>Saved PDFs</small>", unsafe_allow_html=True)
            for fname in saved_pdfs:
                c1, c2 = st.columns([5, 1])
                c1.caption(fname)
                if c2.button("🗑️", key=f"del_pdf_{fname}", help=f"Delete {fname}"):
                    fpath = os.path.join(UPLOAD_DIR, fname)
                    os.remove(fpath)
                    if st.session_state.get("indexed_source") == fpath:
                        st.session_state.pop("vector_index", None)
                        st.session_state.pop("indexed_source", None)
                    st.rerun()
        else:
            st.caption("No PDFs uploaded yet.")

    with url_tab:
        st.caption("Link to a remote PDF document.")
        url_label = st.text_input("Label", placeholder="e.g. Leave Policy 2026")
        url_value = st.text_input("URL",   placeholder="https://example.com/policy.pdf")
        if st.button("➕ Add URL", use_container_width=True):
            if not url_label.strip() or not url_value.strip():
                st.warning("Fill in both Label and URL.")
            else:
                with st.spinner("Checking URL…"):
                    ok, err = validate_pdf_url(url_value.strip())
                if ok:
                    urls = load_urls()
                    urls[url_label.strip()] = url_value.strip()
                    save_urls(urls)
                    st.success(f"Saved: **{url_label.strip()}**")
                    st.rerun()
                else:
                    st.error(f"**Invalid PDF URL** — {err}")

        saved_urls = load_urls()
        if saved_urls:
            st.markdown("<small style='color:rgba(255,255,255,0.45);text-transform:uppercase;letter-spacing:.5px;font-size:.72rem'>Saved URLs</small>", unsafe_allow_html=True)
            for label, url in saved_urls.items():
                c1, c2 = st.columns([5, 1])
                c1.caption(label)
                if c2.button("🗑️", key=f"del_url_{label}", help=f"Delete {label}"):
                    del saved_urls[label]
                    save_urls(saved_urls)
                    if st.session_state.get("indexed_source") == url:
                        st.session_state.pop("vector_index", None)
                        st.session_state.pop("indexed_source", None)
                    st.rerun()
        else:
            st.caption("No URLs saved yet.")

    st.markdown("---")

    all_sources = list_all_sources()
    if not all_sources:
        st.error("No sources available. Upload a PDF or add a URL.")
        selected_label  = None
        selected_source = None
    else:
        selected_label  = st.selectbox("Active source", list(all_sources.keys()))
        selected_source = all_sources[selected_label]
        st.caption(selected_source)

    st.markdown("---")

    free_models  = fetch_free_models()
    model_label  = st.selectbox("Model", list(free_models.keys()))
    selected_model = free_models[model_label]
    st.caption(selected_model)

    st.markdown("---")

    temperature = st.slider("Temperature", 0.0, 1.0, 0.1, 0.05,
                            help="Lower = more factual · Higher = more creative")

    st.markdown("---")

    col_reload, col_clear = st.columns(2)
    if col_reload.button("🔄 Reload KB", use_container_width=True):
        st.session_state.pop("vector_index", None)
        st.session_state.pop("indexed_source", None)
        st.rerun()
    if col_clear.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.pop("chat_history", None)
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("🧠 Embeddings: HuggingFace all-MiniLM-L6-v2 (local)")

# ── Hero header ────────────────────────────────────────────────────────────────
_ps = "background:rgba(255,255,255,0.18);border:1px solid rgba(255,255,255,0.25);border-radius:20px;padding:3px 12px;font-size:0.78rem;color:rgba(255,255,255,0.9);display:inline-block;margin-right:6px;"
_badges = (
    '<span style="' + _ps + '">⚡ ' + selected_model + '</span>'
    + '<span style="' + _ps + '">🌡️ temp ' + str(temperature) + '</span>'
    + ('<span style="' + _ps + '">' + selected_label + '</span>' if selected_label else '')
)
_hero = (
    '<div style="background:linear-gradient(135deg,#667eea,#764ba2);border-radius:16px;padding:28px 36px;margin-bottom:20px;box-shadow:0 8px 32px rgba(102,126,234,0.28);position:relative;">'
    + '<div style="font-size:1.9rem;font-weight:700;color:white;letter-spacing:-0.4px;margin-bottom:6px;">🤖 PDF Assistant</div>'
    + '<div style="font-size:0.9rem;color:rgba(255,255,255,0.72);margin-bottom:14px;">Retrieval-Augmented Generation · Ask anything about your uploaded PDF</div>'
    + '<div style="margin-top:4px;">' + _badges + '</div>'
    + '<a href="/project_details" target="_self" style="'
        'position:absolute;top:20px;right:28px;'
        'background:rgba(255,255,255,0.15);'
        'border:1px solid rgba(255,255,255,0.3);'
        'border-radius:20px;padding:6px 16px;'
        'font-size:0.8rem;font-weight:600;color:white;'
        'text-decoration:none;letter-spacing:0.2px;'
        'backdrop-filter:blur(6px);'
        'transition:background 0.2s,border-color 0.2s;'
        '" onmouseover="this.style.background=\'rgba(255,255,255,0.25)\'" onmouseout="this.style.background=\'rgba(255,255,255,0.15)\'">🔬 Project Details ↗</a>'
    + '</div>'
)
st.markdown(_hero, unsafe_allow_html=True)

# ── Empty state: no API key ───────────────────────────────────────────────────
if not api_key_input:
    st.markdown(
        '<div style="text-align:center;padding:60px 20px 12px;">'
        '<div style="font-size:3.5rem;margin-bottom:14px;">🔑</div>'
        '<div style="font-size:1.25rem;font-weight:600;color:rgba(255,255,255,0.75);margin-bottom:8px;">OpenRouter API key required</div>'
        '<div style="font-size:0.9rem;color:rgba(255,255,255,0.38);max-width:420px;margin:0 auto;line-height:1.7;">'
        'Open the <strong style="color:rgba(255,255,255,0.55);">Settings panel</strong> and paste your free OpenRouter API key to get started. '
        'Get one at <strong style="color:rgba(255,255,255,0.55);">openrouter.ai</strong> — no credit card needed.'
        '</div></div>',
        unsafe_allow_html=True,
    )
    components.html("""
<div style="text-align:center;padding:16px 0 0;font-family:Inter,sans-serif;">
  <button
    style="background:linear-gradient(135deg,#667eea,#764ba2);color:white;border:none;border-radius:10px;padding:10px 24px;cursor:pointer;font-size:0.9rem;font-weight:600;box-shadow:0 4px 14px rgba(102,126,234,0.4);letter-spacing:0.2px;transition:transform 0.15s,box-shadow 0.15s;"
    onmouseover="this.style.transform='translateY(-1px)';this.style.boxShadow='0 6px 22px rgba(102,126,234,0.6)';"
    onmouseout="this.style.transform='none';this.style.boxShadow='0 4px 14px rgba(102,126,234,0.4)';"
    onclick="
      var pd=window.parent.document;
      var btn=pd.querySelector('[data-testid=\\'collapsedControl\\'] button')
             ||pd.querySelector('[data-testid=\\'stSidebarCollapseButton\\'] button')
             ||pd.querySelector('button[aria-label=\\'Open sidebar\\']');
      if(btn){btn.click();}
    ">
    ⚙️ &nbsp;Open Settings Panel
  </button>
</div>
""", height=80, scrolling=False)
    st.stop()

# ── Empty state: no source ────────────────────────────────────────────────────
if not selected_source:
    st.markdown(
        '<div style="text-align:center;padding:60px 20px 12px;">'
        '<div style="font-size:3.5rem;margin-bottom:14px;">📂</div>'
        '<div style="font-size:1.25rem;font-weight:600;color:rgba(255,255,255,0.75);margin-bottom:8px;">No knowledge base loaded</div>'
        '<div style="font-size:0.9rem;color:rgba(255,255,255,0.38);max-width:380px;margin:0 auto 0;line-height:1.6;">'
        'Upload a PDF or add a URL in the settings panel, then pick it from the <strong style="color:rgba(255,255,255,0.55);">Active source</strong> dropdown.'
        '</div></div>',
        unsafe_allow_html=True,
    )
    components.html("""
<div style="text-align:center;padding:16px 0 0;font-family:Inter,sans-serif;">
  <button
    style="background:linear-gradient(135deg,#667eea,#764ba2);color:white;border:none;border-radius:10px;padding:10px 24px;cursor:pointer;font-size:0.9rem;font-weight:600;box-shadow:0 4px 14px rgba(102,126,234,0.4);letter-spacing:0.2px;transition:transform 0.15s,box-shadow 0.15s;"
    onmouseover="this.style.transform='translateY(-1px)';this.style.boxShadow='0 6px 22px rgba(102,126,234,0.6)';"
    onmouseout="this.style.transform='none';this.style.boxShadow='0 4px 14px rgba(102,126,234,0.4)';"
    onclick="
      var pd=window.parent.document;
      var btn=pd.querySelector('[data-testid=\\'collapsedControl\\'] button')
             ||pd.querySelector('[data-testid=\\'stSidebarCollapseButton\\'] button')
             ||pd.querySelector('button[aria-label=\\'Open sidebar\\']');
      if(btn){btn.click();}
    ">
    ⚙️ &nbsp;Open Settings Panel
  </button>
  
</div>
""", height=80, scrolling=False)
    st.stop()

# ── Build / refresh index ──────────────────────────────────────────────────────
_index_error = None
if (
    "vector_index" not in st.session_state
    or st.session_state.get("indexed_source") != selected_source
):
    with st.spinner(f"Building knowledge base from **{selected_label}**…"):
        try:
            st.session_state.vector_index   = backend.hr_index(pdf_path=selected_source)
            st.session_state.indexed_source = selected_source
        except Exception as _exc:
            st.session_state.pop("vector_index", None)
            st.session_state.pop("indexed_source", None)
            _index_error = _exc

    if _index_error is None:
        st.success(f"Knowledge base ready — **{selected_label}**", icon="✅")
    else:
        _raw = str(_index_error)
        if "PdfStream" in _raw or "stream" in _raw.lower() or "unexpected" in _raw.lower():
            _msg = "This source doesn't appear to be a valid PDF. If it's a URL, make sure it points directly to a <strong>.pdf</strong> file — not a webpage or redirect."
        elif "404" in _raw or "not found" in _raw.lower():
            _msg = "The file or URL could not be found (404). The link may be broken or the file deleted."
        elif "timeout" in _raw.lower() or "timed out" in _raw.lower():
            _msg = "The request timed out while fetching the document. Check your connection and try again."
        else:
            _msg = _raw

        st.markdown(
            '<div style="background:rgba(239,68,68,0.09);border:1px solid rgba(239,68,68,0.3);'
            'border-radius:14px;padding:22px 26px;margin:8px 0 16px;">'
            '<div style="font-size:1.05rem;font-weight:700;color:rgba(255,110,110,1);margin-bottom:8px;">⚠️ Could not load this source</div>'
            '<div style="font-size:0.9rem;color:rgba(255,195,195,0.85);line-height:1.65;">' + _msg + '</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        _is_url = selected_source.startswith("http")
        _c1, _c2, _c3 = st.columns([1.6, 1.4, 4])

        if _is_url:
            if _c1.button("🗑️ Remove URL", use_container_width=True):
                _urls = load_urls()
                for _k, _v in list(_urls.items()):
                    if _v == selected_source:
                        del _urls[_k]
                save_urls(_urls)
                st.session_state.pop("vector_index", None)
                st.session_state.pop("indexed_source", None)
                st.rerun()
        else:
            if _c1.button("🗑️ Remove File", use_container_width=True):
                if os.path.exists(selected_source):
                    os.remove(selected_source)
                st.session_state.pop("vector_index", None)
                st.session_state.pop("indexed_source", None)
                st.rerun()

        if _c2.button("🔄 Try Again", use_container_width=True):
            st.session_state.pop("vector_index", None)
            st.session_state.pop("indexed_source", None)
            st.rerun()

        st.stop()

# ── Chat history ───────────────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Render past messages
for turn in st.session_state.chat_history:
    # User bubble
    st.markdown(f"""
    <div style="display:flex;justify-content:flex-end;margin-bottom:6px;">
        <div style="
            background:linear-gradient(135deg,#667eea,#764ba2);
            color:white;border-radius:18px 18px 4px 18px;
            padding:11px 16px;max-width:72%;
            font-size:0.93rem;line-height:1.55;
            box-shadow:0 4px 12px rgba(102,126,234,0.28);
        ">{turn['question']}</div>
    </div>
    """, unsafe_allow_html=True)

    # Bot bubble
    st.markdown(f"""
    <div style="display:flex;gap:10px;align-items:flex-start;margin-bottom:16px;">
        <div style="
            width:34px;height:34px;flex-shrink:0;
            background:linear-gradient(135deg,#11998e,#38ef7d);
            border-radius:50%;display:flex;align-items:center;
            justify-content:center;font-size:16px;
        ">🤖</div>
        <div style="
            background:rgba(255,255,255,0.07);
            backdrop-filter:blur(8px);
            border:1px solid rgba(255,255,255,0.1);
            color:rgba(255,255,255,0.88);
            border-radius:4px 18px 18px 18px;
            padding:13px 17px;max-width:75%;
            font-size:0.93rem;line-height:1.65;
            box-shadow:0 4px 12px rgba(0,0,0,0.18);
            white-space:pre-wrap;
        ">{turn['answer']}</div>
    </div>
    """, unsafe_allow_html=True)

# ── Divider between history and input ─────────────────────────────────────────
if st.session_state.chat_history:
    st.markdown("---")

# ── Question input ─────────────────────────────────────────────────────────────
question = st.text_area(
    "Ask a question",
    placeholder="e.g.  What are the key points covered in this document?",
    height=100,
    label_visibility="collapsed",
    key="question_input",
)

col_ask, col_hint = st.columns([1, 4])
ask_button = col_ask.button(
    "Ask ➜", type="primary",
    disabled=not selected_source,
    use_container_width=True,
)
col_hint.markdown(
    "<span style='color:rgba(255,255,255,0.3);font-size:0.82rem;line-height:2.5'>"
    "Press <b>Ask</b> or <kbd style='background:rgba(255,255,255,0.1);border-radius:4px;padding:1px 5px'>Ctrl+Enter</kbd>"
    "</span>",
    unsafe_allow_html=True,
)

if ask_button and not api_key_input:
    st.warning("Enter your OpenRouter API key in the Settings panel (⚙️) to ask questions.")
elif ask_button and question.strip():
    with st.spinner(f"Thinking…"):
        try:
            answer = backend.hr_rag_response(
                index=st.session_state.vector_index,
                question=question,
                model_id=selected_model,
                api_key=api_key_input,
                temperature=temperature,
            )
            st.session_state.chat_history.append({"question": question, "answer": answer})
            st.session_state.question_input = ""
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

elif ask_button and not question.strip():
    st.warning("Please type a question first.")
