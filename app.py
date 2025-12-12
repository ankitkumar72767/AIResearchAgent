import streamlit as st
from memory import HistoryManager
from utils import extract_pdf_text
from graph_builder import build_graph

# ==========================
# 🧠 PAGE CONFIG
# ==========================
st.set_page_config(
    page_title="Open Deep Research Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

memory = HistoryManager()

# -------- Session State Init --------
if "last_query" not in st.session_state:
    st.session_state.last_query = None

if "last_report" not in st.session_state:
    st.session_state.last_report = None

if "pending_query" not in st.session_state:
    st.session_state.pending_query = None

if "pdf_context" not in st.session_state:
    st.session_state.pdf_context = ""

if "pdf_name" not in st.session_state:
    st.session_state.pdf_name = None

if "search_focus" not in st.session_state:
    st.session_state.search_focus = "General Web"

if "summary_length" not in st.session_state:
    st.session_state.summary_length = "Detailed"

if "openai_api_key" not in st.session_state:
    st.session_state.openai_api_key = ""

if "tavily_api_key" not in st.session_state:
    st.session_state.tavily_api_key = ""

# Provider fixed to OpenAI ChatGPT for this UI
if "provider" not in st.session_state:
    st.session_state.provider = "openai"

# ==========================
# 🎨 GLOBAL CSS (hero + clean)
# ==========================
st.markdown(
    """
    <style>
    .stApp {
        background: #050816;
        color: #e5e7eb;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1100px;
    }
    section[data-testid="stSidebar"] {
        background: #020617;
        border-right: 1px solid #1f2937;
    }
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #e5e7eb !important;
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        text-align: center;
        color: #f9fafb;
        margin-bottom: 0.2rem;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        text-align: center;
        color: #9ca3af;
        margin-bottom: 1.5rem;
    }
    /* Chat input look like long search bar */
    div[data-testid="stChatInput"] > div {
        max-width: 900px;
        margin: 0 auto;
    }
    div[data-testid="stChatInput"] textarea {
        font-size: 0.95rem;
    }
    /* Smooth bottom transition */
    div[data-testid="stBottom"] {
        transition: bottom 0.3s ease;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================
# 📚 SIDEBAR (Search Focus, Output Length, PDF, Keys)
# ==========================
with st.sidebar:
    st.markdown("### 🔍 Search Focus")
    st.session_state.search_focus = st.radio(
        "Target:",
        ["General Web", "Academic Papers"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("### 📏 Output Length")
    detail = st.radio(
        "Detail Level:",
        ["Detailed Report", "Short Summary"],
        index=0,
    )
    length_map = {"Detailed Report": "Detailed", "Short Summary": "Short"}
    st.session_state.summary_length = length_map[detail]

    st.markdown("---")
    st.markdown("### 📎 Document Upload")
    if not st.session_state.pdf_name:
        uploaded_file = st.file_uploader(
            "Upload PDF context",
            type=["pdf"],
            help="Optional: The agent will also use this document as context.",
        )
        if uploaded_file:
            with st.spinner("📖 Extracting text from PDF..."):
                raw_text = extract_pdf_text(uploaded_file)
                st.session_state.pdf_context = raw_text
                st.session_state.pdf_name = uploaded_file.name
                st.rerun()
    else:
        st.info(f"📄 *{st.session_state.pdf_name}* attached as context.")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Remove PDF"):
                st.session_state.pdf_context = ""
                st.session_state.pdf_name = None
                st.rerun()
        with col2:
            if st.button("Replace PDF"):
                st.session_state.pdf_context = ""
                st.session_state.pdf_name = None
                st.rerun()

    st.markdown("---")
    with st.expander("🔐 API Keys (required once)", expanded=False):
        st.session_state.openai_api_key = st.text_input(
            "OpenAI (ChatGPT) API Key",
            type="password",
            value=st.session_state.openai_api_key,
            help="Get it from https://platform.openai.com",
        )
        st.session_state.tavily_api_key = st.text_input(
            "Tavily API Key",
            type="password",
            value=st.session_state.tavily_api_key,
            help="Get it from https://app.tavily.com",
        )

    st.markdown("---")
    if st.button("🧹 Clear Last Result"):
        st.session_state.last_query = None
        st.session_state.last_report = None
        st.rerun()

# ==========================
# 🧠 HERO HEADER
# ==========================
st.markdown('<div class="hero-title">🧠 Open Deep Research Agent</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-subtitle">What would you like to research today?</div>',
    unsafe_allow_html=True,
)

# ==========================
# 💬 INPUT (single bar at bottom)
# ==========================
placeholder = 'Type a topic like "Natural Language Processing", "Blockchain in Healthcare", etc.'

user_prompt = st.chat_input(placeholder)

if user_prompt:
    # Check keys first
    if not st.session_state.openai_api_key or not st.session_state.tavily_api_key:
        st.error("⚠️ Please set your *OpenAI* and *Tavily* API keys in the sidebar (API Keys section).")
    else:
        st.session_state.pending_query = user_prompt
        st.rerun()

# ==========================
# ⚙️ BACKEND EXECUTION (if pending_query set)
# ==========================
if st.session_state.pending_query:
    query = st.session_state.pending_query
    st.session_state.pending_query = None

    # Build final topic string including search focus + PDF context
    final_topic = f"User Query: {query}\n\nSearch Focus: {st.session_state.search_focus}"
    mode = "Text"

    if st.session_state.pdf_context:
        final_topic += (
            f"\n\nReference PDF Content (truncated):\n"
            f"{st.session_state.pdf_context[:9000]}"
        )
        mode = "PDF"

    try:
        app_graph = build_graph(
            provider="openai",
            openrouter_api_key="",  # not used in this UI
            openai_api_key=st.session_state.openai_api_key,
            tavily_api_key=st.session_state.tavily_api_key,
        )

        # ⭐ Agent status card (Planner / Searcher / Writer)
        status_box = st.status("🤖 Agent Working...", expanded=True)
     
        final_state = app_graph.invoke(
            {
                "topic": final_topic,
                "summary_length": st.session_state.summary_length,
            }
        )

        report = final_state["final_report"]

        status_box.update(
            label="✅ Research Complete",
            state="complete",
            expanded=False,
        )

        # Save to session + history
        st.session_state.last_query = query
        st.session_state.last_report = report
        memory.save_entry(query, mode, report)

    except Exception as e:
        st.error(f"❌ Error while generating report:\n\n`{e}`")

# ==========================
# 📄 SHOW RESULT (Markdown like paper)
# ==========================
if st.session_state.last_report:
    st.markdown("---")
    st.markdown(f"### 📘 {st.session_state.last_query}")
    st.markdown(st.session_state.last_report)