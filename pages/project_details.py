import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Project Details — PDF Assistant RAG",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }

.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    min-height: 100vh;
}
section[data-testid="stSidebar"] { display: none !important; }

::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: rgba(255,255,255,0.02); }
::-webkit-scrollbar-thumb { background: rgba(102,126,234,0.35); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Back link ──────────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding: 18px 0 0 4px;">
  <a href="/" target="_self" style="
    color: rgba(102,126,234,0.9);
    text-decoration: none;
    font-size: 0.88rem;
    font-weight: 500;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    transition: color 0.2s;
  ">← Back to PDF Assistant</a>
</div>
""", unsafe_allow_html=True)

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="
  background: linear-gradient(135deg, #1a1a4e 0%, #2d1b6e 50%, #1e1040 100%);
  border: 1px solid rgba(102,126,234,0.25);
  border-radius: 20px;
  padding: 42px 48px 36px;
  margin: 20px 0 36px;
  box-shadow: 0 8px 40px rgba(0,0,0,0.4);
  position: relative;
  overflow: hidden;
">
  <div style="
    position: absolute; top: -60px; right: -60px;
    width: 260px; height: 260px;
    background: radial-gradient(circle, rgba(118,75,162,0.25) 0%, transparent 70%);
    pointer-events: none;
  "></div>
  <div style="font-size: 0.8rem; font-weight: 600; letter-spacing: 2px; color: rgba(102,126,234,0.8); text-transform: uppercase; margin-bottom: 10px;">Architecture Overview</div>
  <div style="font-size: 2.4rem; font-weight: 800; color: white; letter-spacing: -0.6px; line-height: 1.15; margin-bottom: 12px;">
    PDF Assistant<br><span style="background: linear-gradient(135deg,#667eea,#a78bfa); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">RAG Pipeline</span>
  </div>
  <div style="font-size: 0.97rem; color: rgba(255,255,255,0.6); max-width: 600px; line-height: 1.7;">
    A Retrieval-Augmented Generation system that lets you upload any PDF and ask natural-language questions about its content.
    Documents are chunked, embedded locally, stored in a vector index, and retrieved at query time to ground LLM responses in factual content.
  </div>
  <div style="margin-top: 22px; display: flex; flex-wrap: wrap; gap: 10px;">
    <span style="background:rgba(102,126,234,0.15);border:1px solid rgba(102,126,234,0.35);border-radius:20px;padding:5px 14px;font-size:0.8rem;color:rgba(180,180,255,0.9);font-weight:500;">🦜 LangChain</span>
    <span style="background:rgba(52,211,153,0.1);border:1px solid rgba(52,211,153,0.3);border-radius:20px;padding:5px 14px;font-size:0.8rem;color:rgba(100,230,180,0.9);font-weight:500;">🧠 HuggingFace Embeddings</span>
    <span style="background:rgba(251,191,36,0.1);border:1px solid rgba(251,191,36,0.3);border-radius:20px;padding:5px 14px;font-size:0.8rem;color:rgba(251,210,100,0.9);font-weight:500;">⚡ FAISS Vector Store</span>
    <span style="background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.3);border-radius:20px;padding:5px 14px;font-size:0.8rem;color:rgba(255,150,150,0.9);font-weight:500;">🤖 OpenRouter LLMs</span>
    <span style="background:rgba(96,165,250,0.1);border:1px solid rgba(96,165,250,0.3);border-radius:20px;padding:5px 14px;font-size:0.8rem;color:rgba(150,200,255,0.9);font-weight:500;">🎈 Streamlit</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Pipeline flow diagram ──────────────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom: 12px;">
  <div style="font-size: 0.75rem; font-weight: 600; letter-spacing: 2px; color: rgba(102,126,234,0.7); text-transform: uppercase; margin-bottom: 16px;">End-to-End Pipeline</div>
</div>
""", unsafe_allow_html=True)

components.html("""
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: transparent; font-family: 'Inter', sans-serif; }

  .pipeline {
    display: flex;
    align-items: stretch;
    gap: 0;
    overflow-x: auto;
    padding: 8px 0 16px;
    scrollbar-width: thin;
    scrollbar-color: rgba(102,126,234,0.4) transparent;
  }

  .step-wrap {
    display: flex;
    align-items: center;
    flex-shrink: 0;
  }

  .step {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 14px;
    padding: 18px 16px;
    width: 148px;
    cursor: pointer;
    transition: transform 0.2s, background 0.2s, border-color 0.2s, box-shadow 0.2s;
    text-align: center;
    position: relative;
  }
  .step:hover, .step.active {
    background: rgba(102,126,234,0.15);
    border-color: rgba(102,126,234,0.5);
    transform: translateY(-3px);
    box-shadow: 0 8px 28px rgba(102,126,234,0.25);
  }
  .step-icon { font-size: 1.7rem; margin-bottom: 8px; }
  .step-num {
    position: absolute; top: 9px; left: 12px;
    font-size: 0.65rem; font-weight: 700;
    color: rgba(102,126,234,0.7);
    background: rgba(102,126,234,0.12);
    border-radius: 10px; padding: 1px 6px;
  }
  .step-title { font-size: 0.78rem; font-weight: 600; color: rgba(255,255,255,0.88); line-height: 1.35; }
  .step-sub   { font-size: 0.68rem; color: rgba(255,255,255,0.42); margin-top: 4px; line-height: 1.35; }

  .arrow {
    font-size: 1.2rem; color: rgba(102,126,234,0.5);
    margin: 0 4px; flex-shrink: 0; align-self: center;
  }

  .detail-panel {
    margin-top: 14px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(102,126,234,0.2);
    border-radius: 14px;
    padding: 22px 26px;
    animation: fadeIn 0.25s ease;
    min-height: 110px;
  }
  @keyframes fadeIn { from { opacity:0; transform:translateY(6px); } to { opacity:1; transform:translateY(0); } }

  .detail-title { font-size: 1rem; font-weight: 700; color: white; margin-bottom: 8px; }
  .detail-body  { font-size: 0.85rem; color: rgba(255,255,255,0.65); line-height: 1.7; }
  .detail-body strong { color: rgba(180,180,255,0.95); }
  .detail-body code {
    background: rgba(102,126,234,0.15); border-radius: 4px;
    padding: 1px 6px; font-size: 0.8rem; color: rgba(160,200,255,0.9);
    font-family: 'Fira Code', monospace;
  }
  .detail-pills { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 12px; }
  .pill {
    background: rgba(102,126,234,0.12); border: 1px solid rgba(102,126,234,0.25);
    border-radius: 20px; padding: 3px 12px; font-size: 0.74rem; color: rgba(180,180,255,0.85);
  }
</style>

<div class="pipeline" id="pipeline">

  <div class="step-wrap">
    <div class="step active" data-idx="0" onclick="select(0)">
      <span class="step-num">01</span>
      <div class="step-icon">📄</div>
      <div class="step-title">Document<br>Ingestion</div>
      <div class="step-sub">PDF / URL</div>
    </div>
  </div>
  <div class="arrow">›</div>

  <div class="step-wrap">
    <div class="step" data-idx="1" onclick="select(1)">
      <span class="step-num">02</span>
      <div class="step-icon">✂️</div>
      <div class="step-title">Text<br>Splitting</div>
      <div class="step-sub">Chunks</div>
    </div>
  </div>
  <div class="arrow">›</div>

  <div class="step-wrap">
    <div class="step" data-idx="2" onclick="select(2)">
      <span class="step-num">03</span>
      <div class="step-icon">🧠</div>
      <div class="step-title">Embedding<br>Generation</div>
      <div class="step-sub">384-dim vectors</div>
    </div>
  </div>
  <div class="arrow">›</div>

  <div class="step-wrap">
    <div class="step" data-idx="3" onclick="select(3)">
      <span class="step-num">04</span>
      <div class="step-icon">🗄️</div>
      <div class="step-title">Vector<br>Index</div>
      <div class="step-sub">FAISS store</div>
    </div>
  </div>
  <div class="arrow">›</div>

  <div class="step-wrap">
    <div class="step" data-idx="4" onclick="select(4)">
      <span class="step-num">05</span>
      <div class="step-icon">🔍</div>
      <div class="step-title">Similarity<br>Search</div>
      <div class="step-sub">Top-k retrieval</div>
    </div>
  </div>
  <div class="arrow">›</div>

  <div class="step-wrap">
    <div class="step" data-idx="5" onclick="select(5)">
      <span class="step-num">06</span>
      <div class="step-icon">🤖</div>
      <div class="step-title">LLM<br>Generation</div>
      <div class="step-sub">Grounded answer</div>
    </div>
  </div>

</div>

<div class="detail-panel" id="detail-panel">
  <div class="detail-title" id="d-title">📄 Document Ingestion</div>
  <div class="detail-body" id="d-body"></div>
  <div class="detail-pills" id="d-pills"></div>
</div>

<script>
const steps = [
  {
    title: "📄 Document Ingestion",
    body: `PDF documents are loaded using <strong>PyPDFLoader</strong> from LangChain Community.
    The loader reads each page of the PDF, extracts raw text, and attaches page-level metadata
    (source path, page number). It also supports <strong>remote URLs</strong> — if a URL is provided instead of a
    local file path, the PDF is fetched over HTTP before parsing.`,
    pills: ["PyPDFLoader", "LangChain Community", "PDF + URL support", "Page metadata"]
  },
  {
    title: "✂️ Text Splitting",
    body: `Loaded pages are split into smaller, overlapping chunks using <strong>RecursiveCharacterTextSplitter</strong>.
    It tries to split on paragraph breaks <code>\\n\\n</code>, then newlines <code>\\n</code>, then spaces, then characters —
    preserving semantic coherence as much as possible.
    Each chunk is <strong>100 characters</strong> with a <strong>10-character overlap</strong> so that context
    isn't lost at chunk boundaries.`,
    pills: ["RecursiveCharacterTextSplitter", "chunk_size=100", "chunk_overlap=10", "Semantic-aware splits"]
  },
  {
    title: "🧠 Embedding Generation",
    body: `Each chunk is converted into a dense numerical vector using <strong>HuggingFace all-MiniLM-L6-v2</strong>,
    a lightweight sentence-transformer model that runs <strong>100% locally</strong> — no API key required, no data leaves your machine.
    It produces <strong>384-dimensional embeddings</strong> that capture semantic meaning, so similar
    sentences land close together in vector space even if they use different words.`,
    pills: ["all-MiniLM-L6-v2", "384 dimensions", "Runs locally", "Sentence Transformers", "HuggingFace"]
  },
  {
    title: "🗄️ FAISS Vector Index",
    body: `Embeddings are stored in a <strong>FAISS</strong> (Facebook AI Similarity Search) in-memory index.
    FAISS uses highly optimised approximate nearest-neighbour (ANN) algorithms to make similarity
    search fast even across millions of vectors. The index is rebuilt fresh each time a new
    document is selected, ensuring the knowledge base always reflects the current source.
    LangChain's <strong>VectorstoreIndexCreator</strong> wires the splitter, embedder, and store together.`,
    pills: ["FAISS", "In-memory ANN index", "VectorstoreIndexCreator", "LangChain"]
  },
  {
    title: "🔍 Similarity Search (Retrieval)",
    body: `At query time the user's question is embedded with the same <strong>all-MiniLM-L6-v2</strong> model.
    FAISS computes <strong>cosine / L2 distance</strong> against every stored chunk vector and returns the
    top-k most relevant chunks in milliseconds. These retrieved chunks form the <em>context</em> that
    is injected into the LLM prompt, anchoring the answer to actual document content.`,
    pills: ["Cosine similarity", "Top-k retrieval", "Same embedding model", "Zero hallucination grounding"]
  },
  {
    title: "🤖 LLM Answer Generation",
    body: `The retrieved context chunks and the original question are combined into a prompt and sent
    to a <strong>free LLM via OpenRouter</strong> (e.g. <code>arcee-ai/trinity-large-thinking:free</code>,
    <code>deepseek/deepseek-r1:free</code>, <code>meta-llama/llama-3.1-8b-instruct:free</code>).
    OpenRouter is an API gateway that routes to many providers. The LLM is accessed through
    LangChain's <strong>ChatOpenAI</strong> wrapper pointed at the OpenRouter base URL.
    Temperature is configurable to trade off factual precision vs. creativity.`,
    pills: ["OpenRouter API", "ChatOpenAI wrapper", "Temperature control", "Free-tier LLMs", "Context-grounded"]
  }
];

function select(idx) {
  document.querySelectorAll('.step').forEach((s, i) => {
    s.classList.toggle('active', i === idx);
  });
  document.getElementById('d-title').textContent = steps[idx].title;
  document.getElementById('d-body').innerHTML    = steps[idx].body;
  const pills = document.getElementById('d-pills');
  pills.innerHTML = steps[idx].pills.map(p => `<span class="pill">${p}</span>`).join('');
  // re-trigger animation
  const panel = document.getElementById('detail-panel');
  panel.style.animation = 'none';
  panel.offsetHeight;
  panel.style.animation = '';
}

// init
select(0);
</script>
""", height=420, scrolling=False)

# ── Component cards ────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin: 36px 0 16px;">
  <div style="font-size: 0.75rem; font-weight: 600; letter-spacing: 2px; color: rgba(102,126,234,0.7); text-transform: uppercase; margin-bottom: 4px;">Key Components</div>
  <div style="font-size: 1.4rem; font-weight: 700; color: white;">Tech Stack Deep Dive</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
<div style="
  background: linear-gradient(145deg, rgba(52,211,153,0.08), rgba(16,185,129,0.04));
  border: 1px solid rgba(52,211,153,0.2);
  border-radius: 16px;
  padding: 24px;
  height: 100%;
  min-height: 260px;
">
  <div style="font-size: 1.8rem; margin-bottom: 10px;">🧠</div>
  <div style="font-size: 1rem; font-weight: 700; color: white; margin-bottom: 6px;">Embedding Model</div>
  <div style="font-size: 0.82rem; font-weight: 600; color: rgba(52,211,153,0.8); margin-bottom: 12px;">all-MiniLM-L6-v2</div>
  <div style="font-size: 0.83rem; color: rgba(255,255,255,0.6); line-height: 1.7;">
    A <strong style="color:rgba(255,255,255,0.82)">Sentence Transformer</strong> from HuggingFace.
    Only 22M parameters — fast to run on CPU.
    Maps text to <strong style="color:rgba(255,255,255,0.82)">384-dimensional</strong> semantic vectors.
    Trained on 1B+ sentence pairs for superior semantic similarity.
  </div>
  <div style="margin-top: 14px; display: flex; gap: 6px; flex-wrap: wrap;">
    <span style="background:rgba(52,211,153,0.12);border:1px solid rgba(52,211,153,0.25);border-radius:10px;padding:2px 9px;font-size:0.72rem;color:rgba(100,230,180,0.85);">Local / offline</span>
    <span style="background:rgba(52,211,153,0.12);border:1px solid rgba(52,211,153,0.25);border-radius:10px;padding:2px 9px;font-size:0.72rem;color:rgba(100,230,180,0.85);">384 dims</span>
    <span style="background:rgba(52,211,153,0.12);border:1px solid rgba(52,211,153,0.25);border-radius:10px;padding:2px 9px;font-size:0.72rem;color:rgba(100,230,180,0.85);">22M params</span>
  </div>
</div>
""", unsafe_allow_html=True)

with col2:
    st.markdown("""
<div style="
  background: linear-gradient(145deg, rgba(251,191,36,0.08), rgba(245,158,11,0.04));
  border: 1px solid rgba(251,191,36,0.2);
  border-radius: 16px;
  padding: 24px;
  height: 100%;
  min-height: 260px;
">
  <div style="font-size: 1.8rem; margin-bottom: 10px;">⚡</div>
  <div style="font-size: 1rem; font-weight: 700; color: white; margin-bottom: 6px;">Vector Store</div>
  <div style="font-size: 0.82rem; font-weight: 600; color: rgba(251,191,36,0.8); margin-bottom: 12px;">FAISS (Facebook AI)</div>
  <div style="font-size: 0.83rem; color: rgba(255,255,255,0.6); line-height: 1.7;">
    <strong style="color:rgba(255,255,255,0.82)">Facebook AI Similarity Search</strong> —
    an in-memory index optimised for high-speed nearest-neighbour lookup.
    Uses flat L2/cosine indexes for exact search on small corpora.
    Rebuilt on every new document so the knowledge base stays fresh.
  </div>
  <div style="margin-top: 14px; display: flex; gap: 6px; flex-wrap: wrap;">
    <span style="background:rgba(251,191,36,0.12);border:1px solid rgba(251,191,36,0.25);border-radius:10px;padding:2px 9px;font-size:0.72rem;color:rgba(251,210,100,0.85);">In-memory</span>
    <span style="background:rgba(251,191,36,0.12);border:1px solid rgba(251,191,36,0.25);border-radius:10px;padding:2px 9px;font-size:0.72rem;color:rgba(251,210,100,0.85);">ANN search</span>
    <span style="background:rgba(251,191,36,0.12);border:1px solid rgba(251,191,36,0.25);border-radius:10px;padding:2px 9px;font-size:0.72rem;color:rgba(251,210,100,0.85);">Sub-ms lookup</span>
  </div>
</div>
""", unsafe_allow_html=True)

with col3:
    st.markdown("""
<div style="
  background: linear-gradient(145deg, rgba(239,68,68,0.08), rgba(220,38,38,0.04));
  border: 1px solid rgba(239,68,68,0.2);
  border-radius: 16px;
  padding: 24px;
  height: 100%;
  min-height: 260px;
">
  <div style="font-size: 1.8rem; margin-bottom: 10px;">🤖</div>
  <div style="font-size: 1rem; font-weight: 700; color: white; margin-bottom: 6px;">LLM Gateway</div>
  <div style="font-size: 0.82rem; font-weight: 600; color: rgba(239,68,68,0.8); margin-bottom: 12px;">OpenRouter API</div>
  <div style="font-size: 0.83rem; color: rgba(255,255,255,0.6); line-height: 1.7;">
    Routes to dozens of <strong style="color:rgba(255,255,255,0.82)">free-tier LLMs</strong> from a single API key.
    Models include Arcee Trinity, DeepSeek R1, Meta Llama 3.1, Gemma 3.
    Accessed via LangChain's <strong style="color:rgba(255,255,255,0.82)">ChatOpenAI</strong>
    wrapper with a custom base URL.
  </div>
  <div style="margin-top: 14px; display: flex; gap: 6px; flex-wrap: wrap;">
    <span style="background:rgba(239,68,68,0.12);border:1px solid rgba(239,68,68,0.25);border-radius:10px;padding:2px 9px;font-size:0.72rem;color:rgba(255,150,150,0.85);">Free tier</span>
    <span style="background:rgba(239,68,68,0.12);border:1px solid rgba(239,68,68,0.25);border-radius:10px;padding:2px 9px;font-size:0.72rem;color:rgba(255,150,150,0.85);">50+ models</span>
    <span style="background:rgba(239,68,68,0.12);border:1px solid rgba(239,68,68,0.25);border-radius:10px;padding:2px 9px;font-size:0.72rem;color:rgba(255,150,150,0.85);">OpenAI-compatible</span>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("""
<div style="
  background: linear-gradient(145deg, rgba(102,126,234,0.1), rgba(118,75,162,0.06));
  border: 1px solid rgba(102,126,234,0.22);
  border-radius: 16px;
  padding: 24px;
  min-height: 220px;
">
  <div style="font-size: 1.8rem; margin-bottom: 10px;">🦜</div>
  <div style="font-size: 1rem; font-weight: 700; color: white; margin-bottom: 6px;">Orchestration</div>
  <div style="font-size: 0.82rem; font-weight: 600; color: rgba(102,126,234,0.8); margin-bottom: 12px;">LangChain</div>
  <div style="font-size: 0.83rem; color: rgba(255,255,255,0.6); line-height: 1.7;">
    Glues every stage together. <code style="background:rgba(102,126,234,0.15);border-radius:4px;padding:1px 5px;font-size:0.78rem;color:rgba(160,200,255,0.9)">VectorstoreIndexCreator</code>
    wires splitter + embedder + store in one call.
    <code style="background:rgba(102,126,234,0.15);border-radius:4px;padding:1px 5px;font-size:0.78rem;color:rgba(160,200,255,0.9)">index.query()</code> handles
    retrieval + prompt construction + LLM call transparently.
  </div>
</div>
""", unsafe_allow_html=True)

with col5:
    st.markdown("""
<div style="
  background: linear-gradient(145deg, rgba(96,165,250,0.1), rgba(59,130,246,0.05));
  border: 1px solid rgba(96,165,250,0.22);
  border-radius: 16px;
  padding: 24px;
  min-height: 220px;
">
  <div style="font-size: 1.8rem; margin-bottom: 10px;">📄</div>
  <div style="font-size: 1rem; font-weight: 700; color: white; margin-bottom: 6px;">Document Loader</div>
  <div style="font-size: 0.82rem; font-weight: 600; color: rgba(96,165,250,0.8); margin-bottom: 12px;">PyPDFLoader</div>
  <div style="font-size: 0.83rem; color: rgba(255,255,255,0.6); line-height: 1.7;">
    Parses PDF files using <strong style="color:rgba(255,255,255,0.82)">pypdf</strong> under the hood.
    Each PDF page becomes a LangChain Document object with text content and source/page metadata.
    Supports both local file paths and remote HTTPS URLs.
  </div>
</div>
""", unsafe_allow_html=True)

with col6:
    st.markdown("""
<div style="
  background: linear-gradient(145deg, rgba(167,139,250,0.1), rgba(139,92,246,0.05));
  border: 1px solid rgba(167,139,250,0.22);
  border-radius: 16px;
  padding: 24px;
  min-height: 220px;
">
  <div style="font-size: 1.8rem; margin-bottom: 10px;">🎈</div>
  <div style="font-size: 1rem; font-weight: 700; color: white; margin-bottom: 6px;">Frontend</div>
  <div style="font-size: 0.82rem; font-weight: 600; color: rgba(167,139,250,0.8); margin-bottom: 12px;">Streamlit</div>
  <div style="font-size: 0.83rem; color: rgba(255,255,255,0.6); line-height: 1.7;">
    Pure-Python reactive UI. Sidebar manages document sources, model selection, and temperature.
    Main area renders a chat interface. Custom CSS layers a dark gradient theme.
    Session state persists the vector index across reruns.
  </div>
</div>
""", unsafe_allow_html=True)

# ── Data flow diagram ──────────────────────────────────────────────────────────
st.markdown("""
<div style="margin: 40px 0 16px;">
  <div style="font-size: 0.75rem; font-weight: 600; letter-spacing: 2px; color: rgba(102,126,234,0.7); text-transform: uppercase; margin-bottom: 4px;">Two Phases</div>
  <div style="font-size: 1.4rem; font-weight: 700; color: white;">Indexing vs. Query Time</div>
</div>
""", unsafe_allow_html=True)

components.html("""
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: transparent; font-family: 'Inter', sans-serif; }

  .phases { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }

  .phase-card {
    border-radius: 16px;
    padding: 22px 24px;
  }
  .phase-card.index {
    background: linear-gradient(145deg, rgba(52,211,153,0.08), rgba(16,185,129,0.03));
    border: 1px solid rgba(52,211,153,0.2);
  }
  .phase-card.query {
    background: linear-gradient(145deg, rgba(102,126,234,0.1), rgba(118,75,162,0.05));
    border: 1px solid rgba(102,126,234,0.25);
  }

  .phase-label {
    font-size: 0.7rem; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase;
    margin-bottom: 10px;
  }
  .phase-card.index .phase-label { color: rgba(52,211,153,0.8); }
  .phase-card.query .phase-label { color: rgba(102,126,234,0.8); }

  .phase-title {
    font-size: 1.05rem; font-weight: 700; color: white; margin-bottom: 14px;
  }

  .flow-list { list-style: none; display: flex; flex-direction: column; gap: 10px; }
  .flow-item {
    display: flex; align-items: flex-start; gap: 12px;
    font-size: 0.82rem; color: rgba(255,255,255,0.65); line-height: 1.55;
  }
  .flow-dot {
    width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; margin-top: 5px;
  }
  .phase-card.index .flow-dot { background: rgba(52,211,153,0.7); }
  .phase-card.query .flow-dot { background: rgba(102,126,234,0.7); }
  .flow-item strong { color: rgba(255,255,255,0.88); }
</style>

<div class="phases">
  <div class="phase-card index">
    <div class="phase-label">Phase 1 — runs once per document</div>
    <div class="phase-title">📥 Indexing Pipeline</div>
    <ul class="flow-list">
      <li class="flow-item"><span class="flow-dot"></span><div>Upload or select a <strong>PDF / URL</strong></div></li>
      <li class="flow-item"><span class="flow-dot"></span><div><strong>PyPDFLoader</strong> extracts text page by page</div></li>
      <li class="flow-item"><span class="flow-dot"></span><div><strong>RecursiveCharacterTextSplitter</strong> cuts text into 100-char chunks with 10-char overlap</div></li>
      <li class="flow-item"><span class="flow-dot"></span><div><strong>all-MiniLM-L6-v2</strong> encodes each chunk → 384-dim vector</div></li>
      <li class="flow-item"><span class="flow-dot"></span><div>Vectors stored in a <strong>FAISS</strong> in-memory index (cached in session state)</div></li>
    </ul>
  </div>

  <div class="phase-card query">
    <div class="phase-label">Phase 2 — runs on every question</div>
    <div class="phase-title">🔎 Query Pipeline</div>
    <ul class="flow-list">
      <li class="flow-item"><span class="flow-dot"></span><div>User types a <strong>natural-language question</strong></div></li>
      <li class="flow-item"><span class="flow-dot"></span><div>Question embedded by same <strong>all-MiniLM-L6-v2</strong> model</div></li>
      <li class="flow-item"><span class="flow-dot"></span><div><strong>FAISS similarity search</strong> retrieves top-k most relevant chunks</div></li>
      <li class="flow-item"><span class="flow-dot"></span><div>Chunks injected as <strong>context</strong> into LLM prompt</div></li>
      <li class="flow-item"><span class="flow-dot"></span><div><strong>OpenRouter LLM</strong> generates a grounded, cited answer</div></li>
    </ul>
  </div>
</div>
""", height=310, scrolling=False)

# ── Config summary ─────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin: 40px 0 16px;">
  <div style="font-size: 0.75rem; font-weight: 600; letter-spacing: 2px; color: rgba(102,126,234,0.7); text-transform: uppercase; margin-bottom: 4px;">Configuration</div>
  <div style="font-size: 1.4rem; font-weight: 700; color: white;">Current Defaults</div>
</div>
""", unsafe_allow_html=True)

components.html("""
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: transparent; font-family: 'Inter', sans-serif; }

  .config-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 12px;
  }
  .cfg {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 12px;
    padding: 16px 18px;
    transition: background 0.2s, border-color 0.2s;
  }
  .cfg:hover {
    background: rgba(102,126,234,0.08);
    border-color: rgba(102,126,234,0.3);
  }
  .cfg-key   { font-size: 0.72rem; color: rgba(255,255,255,0.38); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px; }
  .cfg-val   { font-size: 0.92rem; font-weight: 600; color: rgba(180,180,255,0.92); }
  .cfg-note  { font-size: 0.73rem; color: rgba(255,255,255,0.38); margin-top: 4px; }
</style>

<div class="config-grid">
  <div class="cfg">
    <div class="cfg-key">Embedding Model</div>
    <div class="cfg-val">all-MiniLM-L6-v2</div>
    <div class="cfg-note">HuggingFace · local</div>
  </div>
  <div class="cfg">
    <div class="cfg-key">Vector Dimensions</div>
    <div class="cfg-val">384</div>
    <div class="cfg-note">Dense float32 vectors</div>
  </div>
  <div class="cfg">
    <div class="cfg-key">Chunk Size</div>
    <div class="cfg-val">100 chars</div>
    <div class="cfg-note">RecursiveCharacterTextSplitter</div>
  </div>
  <div class="cfg">
    <div class="cfg-key">Chunk Overlap</div>
    <div class="cfg-val">10 chars</div>
    <div class="cfg-note">Prevents boundary loss</div>
  </div>
  <div class="cfg">
    <div class="cfg-key">Default Temperature</div>
    <div class="cfg-val">0.10</div>
    <div class="cfg-note">Factual / low creativity</div>
  </div>
  <div class="cfg">
    <div class="cfg-key">Max Tokens</div>
    <div class="cfg-val">5,000</div>
    <div class="cfg-note">LLM response cap</div>
  </div>
  <div class="cfg">
    <div class="cfg-key">LLM Gateway</div>
    <div class="cfg-val">OpenRouter</div>
    <div class="cfg-note">openrouter.ai/api/v1</div>
  </div>
  <div class="cfg">
    <div class="cfg-key">Vector Store</div>
    <div class="cfg-val">FAISS</div>
    <div class="cfg-note">In-memory · per-session</div>
  </div>
</div>
""", height=220, scrolling=False)

st.markdown("<div style='height: 48px'></div>", unsafe_allow_html=True)
