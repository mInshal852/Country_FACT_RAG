"""
Country FACT RAG — Streamlit Frontend
A production-grade AI assistant UI for country knowledge retrieval.
"""

import time
import streamlit as st

try:
    import requests
except ImportError:  # requests may not be installed in all environments
    requests = None

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Country FACT RAG",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CONSTANTS
# ============================================================

COLORS = {
    "background": "#0D1117",
    "surface": "#161B22",
    "card": "#1C2128",
    "border": "#30363D",
    "text_primary": "#F0F6FC",
    "text_secondary": "#8B949E",
    "accent": "#D4A017",
    "accent_soft": "#3FB68B",
}

COUNTRIES = [
    "Japan",
    "Germany",
    "Pakistan",
    "Saudi Arabia",
    "Malaysia",
]

TOPICS = [
    "History",
    "Introduction",
    "Economy",
    "Culture",
]

SUGGESTION_TOPICS = ["History", "Economy", "Culture", "Introduction"]

BACKEND_URL = "http://backend:8000"
BACKEND_HEALTH_URL = "http://backend:8000/health"
REPOSITORY_URL = None


def get_suggestions(country: str) -> list:
    """Generate suggested questions dynamically based on the selected country."""
    return [f"{topic} of {country}" for topic in SUGGESTION_TOPICS]


# ============================================================
# SESSION STATE
# ============================================================


def init_session_state():
    defaults = {
        "messages": [],
        "selected_country": COUNTRIES[0],
        "backend_status": None,
        "pending_input": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def new_chat():
    st.session_state.messages = []
    st.session_state.pending_input = None


def clear_chat():
    st.session_state.messages = []


def queue_suggestion(text: str):
    st.session_state.pending_input = text


def check_backend_status() -> str:
    """
    Check backend health by calling GET /health.
    Returns "online" or "offline". Falls back to "offline" when
    BACKEND_HEALTH_URL is not configured or the request fails.
    """
    if not BACKEND_HEALTH_URL or requests is None:
        return "offline"
    try:
        response = requests.get(BACKEND_HEALTH_URL, timeout=2)
        return "online" if response.status_code == 200 else "offline"
    except requests.RequestException:
        return "offline"


# ============================================================
# STYLES
# ============================================================


def inject_css():
    st.markdown(
        f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

            html, body, [class*="css"] {{
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            }}

            .stApp {{
                background-color: {COLORS['background']};
                background-image:
                    radial-gradient(circle at 20% 0%, rgba(212, 160, 23, 0.03) 0%, transparent 40%),
                    radial-gradient(circle at 80% 100%, rgba(63, 182, 139, 0.025) 0%, transparent 40%);
                background-attachment: fixed;
                color: {COLORS['text_primary']};
            }}

            #MainMenu, footer {{visibility: hidden;}}

            /* Keep the header element (it contains the sidebar
               expand/collapse arrow) but make it blend into the
               background instead of hiding it outright. */
            header[data-testid="stHeader"] {{
                background-color: transparent;
                box-shadow: none;
            }}

            [data-testid="collapsedControl"] {{
                color: {COLORS['text_primary']};
            }}

            section[data-testid="stSidebar"] {{
                background-color: {COLORS['surface']};
                border-right: 1px solid {COLORS['border']};
            }}

            section[data-testid="stSidebar"] .block-container {{
                padding-top: 1.5rem;
            }}

            .block-container {{
                padding-top: 2rem;
                padding-bottom: 6rem;
                max-width: 1050px;
            }}

            /* Sidebar brand */
            .sidebar-brand-title {{
                font-size: 1.15rem;
                font-weight: 700;
                color: {COLORS['text_primary']};
                letter-spacing: -0.02em;
                margin-bottom: 0.15rem;
            }}
            .sidebar-brand-sub {{
                font-size: 0.82rem;
                color: {COLORS['text_secondary']};
                margin-bottom: 1.4rem;
                line-height: 1.4;
            }}

            .sidebar-section-label {{
                font-size: 0.72rem;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.06em;
                color: {COLORS['text_secondary']};
                margin: 1.1rem 0 0.5rem 0;
            }}

            .status-pill {{
                display: inline-flex;
                align-items: center;
                gap: 0.45rem;
                background-color: {COLORS['card']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
                padding: 0.45rem 0.7rem;
                font-size: 0.82rem;
                color: {COLORS['text_primary']};
                width: 100%;
                box-sizing: border-box;
            }}
            .status-dot {{
                width: 8px;
                height: 8px;
                border-radius: 50%;
                flex-shrink: 0;
            }}
            .status-dot.online {{ background-color: {COLORS['accent_soft']}; }}
            .status-dot.offline {{ background-color: #F85149; }}

            .about-box {{
                background-color: {COLORS['card']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
                padding: 0.75rem 0.85rem;
                font-size: 0.8rem;
                color: {COLORS['text_secondary']};
                line-height: 1.5;
            }}

            /* Hero */
            .hero-title {{
                font-size: 2.4rem;
                font-weight: 700;
                letter-spacing: -0.03em;
                color: {COLORS['text_primary']};
                margin-bottom: 0.4rem;
            }}
            .hero-subtitle {{
                font-size: 1.05rem;
                color: {COLORS['text_secondary']};
                margin-bottom: 1.4rem;
                font-weight: 400;
            }}

            .topics-label {{
                font-size: 0.8rem;
                color: {COLORS['text_secondary']};
                margin-bottom: 0.6rem;
            }}

            .topic-pill-row {{
                display: flex;
                flex-wrap: wrap;
                gap: 0.5rem;
                margin-bottom: 1.6rem;
            }}

            .topic-pill {{
                background-color: transparent;
                border: 1px solid {COLORS['border']};
                color: {COLORS['text_secondary']};
                border-radius: 20px;
                padding: 0.3rem 0.8rem;
                font-size: 0.8rem;
            }}

            /* Buttons */
            .stButton > button {{
                background-color: {COLORS['card']};
                border: 1px solid {COLORS['border']};
                color: {COLORS['text_primary']};
                border-radius: 10px;
                padding: 0.55rem 1rem;
                font-size: 0.88rem;
                font-weight: 500;
                transition: border-color 0.15s ease, background-color 0.15s ease;
                width: 100%;
            }}
            .stButton > button:hover {{
                border-color: {COLORS['accent']};
                color: {COLORS['accent']};
                background-color: {COLORS['card']};
            }}
            .stButton > button:active {{
                border-color: {COLORS['accent']};
            }}

            section[data-testid="stSidebar"] .stButton > button {{
                text-align: left;
                justify-content: flex-start;
            }}

            /* Chat messages */
            [data-testid="stChatMessage"] {{
                background-color: transparent;
                border: none;
                border-bottom: 1px solid rgba(48, 54, 61, 0.5);
                border-radius: 0;
                padding: 1.1rem 0.2rem;
                margin-bottom: 0.2rem;
            }}

            [data-testid="stChatMessage"]:last-child {{
                border-bottom: none;
            }}

            [data-testid="stChatMessage"] p {{
                line-height: 1.65;
                font-size: 0.95rem;
                color: {COLORS['text_primary']};
            }}

            [data-testid="stChatInput"] {{
                background-color: {COLORS['surface']};
                border-top: 1px solid {COLORS['border']};
            }}

            [data-testid="stChatInput"] textarea {{
                background-color: {COLORS['card']} !important;
                border: 1px solid {COLORS['border']} !important;
                border-radius: 12px !important;
                color: {COLORS['text_primary']} !important;
            }}

            /* Select box */
            div[data-baseweb="select"] > div {{
                background-color: {COLORS['card']};
                border-color: {COLORS['border']};
                border-radius: 8px;
            }}

            hr {{
                border-color: {COLORS['border']};
            }}

            ::-webkit-scrollbar {{
                width: 8px;
            }}
            ::-webkit-scrollbar-thumb {{
                background: {COLORS['border']};
                border-radius: 4px;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# SIDEBAR
# ============================================================


def render_sidebar():
    with st.sidebar:
        st.markdown(
            '<div class="sidebar-brand-title">Country FACT RAG</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="sidebar-brand-sub">Retrieval-augmented answers on country knowledge.</div>',
            unsafe_allow_html=True,
        )

        st.session_state.backend_status = check_backend_status()
        status = st.session_state.backend_status
        status_label = "Online" if status == "online" else "Offline"
        st.markdown(
            '<div class="sidebar-section-label">Backend Status</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div class="status-pill">
                <span class="status-dot {status}"></span>
                <span>{status_label}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="sidebar-section-label">Country</div>', unsafe_allow_html=True
        )
        st.session_state.selected_country = st.selectbox(
            "Country selector",
            options=COUNTRIES,
            index=COUNTRIES.index(st.session_state.selected_country),
            label_visibility="collapsed",
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("New Chat", use_container_width=True):
                new_chat()
                st.rerun()
        with col2:
            if st.button("Clear Chat", use_container_width=True):
                clear_chat()
                st.rerun()

        st.markdown(
            '<div class="sidebar-section-label">About</div>', unsafe_allow_html=True
        )
        st.markdown(
            """
            <div class="about-box">
                Country FACT RAG retrieves grounded facts from a curated
                knowledge base and generates concise, cited answers about
                any country's history, economy, culture, and more.
            </div>
            """,
            unsafe_allow_html=True,
        )

        if REPOSITORY_URL:
            st.markdown(
                '<div class="sidebar-section-label">Repository</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="about-box">{REPOSITORY_URL}</div>',
                unsafe_allow_html=True,
            )


# ============================================================
# HERO + SUGGESTIONS
# ============================================================


def render_header():
    """Title and subtitle — remain visible for the entire session."""
    st.markdown(
        '<div class="hero-title">Country FACT RAG</div>', unsafe_allow_html=True
    )
    st.markdown(
        '<div class="hero-subtitle">AI-powered Retrieval-Augmented Generation for country knowledge.</div>',
        unsafe_allow_html=True,
    )


def render_empty_state():
    """Suggestions and topic helper — shown only before the first message."""
    country = st.session_state.selected_country
    suggestions = get_suggestions(country)

    cols = st.columns(len(suggestions))
    for col, suggestion in zip(cols, suggestions):
        with col:
            if st.button(
                suggestion, key=f"suggestion_{suggestion}", use_container_width=True
            ):
                queue_suggestion(suggestion)

    st.markdown(
        '<div class="topics-label">You can ask about:</div>', unsafe_allow_html=True
    )
    pills = "".join(f'<span class="topic-pill">{topic}</span>' for topic in TOPICS)
    st.markdown(f'<div class="topic-pill-row">{pills}</div>', unsafe_allow_html=True)


# ============================================================
# RAG BACKEND CALL (placeholder retrieval logic)
# ============================================================


def get_rag_response(query: str) -> str:
    """
    Send the user's question to the FastAPI backend and return the generated answer.
    """

    try:
        response = requests.post(
            f"{BACKEND_URL}/ask",
            json={"question": query},
            timeout=60,
        )

        response.raise_for_status()

        data = response.json()

        return data["answer"]

    except requests.exceptions.ConnectionError:
        return "Unable to connect to the backend server."

    except requests.exceptions.Timeout:
        return "The request timed out."

    except requests.exceptions.HTTPError as e:
        return f"Backend returned an error: {e}"

    except Exception as e:
        return f"Unexpected error: {e}"


# ============================================================
# CHAT RENDERING
# ============================================================


def render_conversation():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def handle_user_input(user_text: str):
    st.session_state.messages.append({"role": "user", "content": user_text})

    with st.chat_message("user"):
        st.markdown(user_text)

    with st.chat_message("assistant"):
        with st.status("Searching knowledge base...", expanded=False) as status:
            time.sleep(0.4)
            status.update(label="Generating grounded response...")
            answer = get_rag_response(user_text)
            status.update(label="Answer ready", state="complete")
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})


# ============================================================
# MAIN
# ============================================================


def main():
    init_session_state()
    inject_css()
    render_sidebar()
    render_header()

    if not st.session_state.messages:
        render_empty_state()

    render_conversation()

    prompt = st.chat_input("Ask about any country's history, economy, or culture...")

    if st.session_state.pending_input:
        prompt = st.session_state.pending_input
        st.session_state.pending_input = None

    if prompt:
        handle_user_input(prompt)
        st.rerun()


if __name__ == "__main__":
    main()
