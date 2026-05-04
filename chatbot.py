import streamlit as st
from ai_service import ai_service   #  connect AI

def show():

    # =========================
    # HEADER
    # =========================
    st.markdown("""
    <div class="ai-page-title">
        <div>
            <h1>✨ Darrah AI Assistant</h1>
            <p>Your intelligent guide to procurement analytics</p>
        </div>
        <div class="ai-badge">🧠 AI Powered</div>
    </div>
    """, unsafe_allow_html=True)

    center, right = st.columns([2.6, 1.4], gap="large")

    # =========================
    # SESSION MEMORY (CHAT HISTORY)
    # =========================
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # =========================
    # CENTER PANEL
    # =========================
    with center:

        # HERO CARD
        st.markdown("""
        <div class="hero-card">
            <div class="bot-avatar">🤖</div>
            <div>
                <h2>Hello! I'm Darrah AI Assistant 👋</h2>
                <p>I can help you understand procurement data, explain key metrics, identify risks, and provide insights to support your analysis.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # =========================
        # QUICK QUESTIONS (CONNECTED)
        # =========================
        q1, q2, q3, q4 = st.columns(4)

        def quick_prompt(text):
            answer = ask_ai(text, context=get_context())
            st.session_state.messages.append(("user", text))
            st.session_state.messages.append(("bot", answer))

        with q1:
            if st.button("📊 HHI"):
                quick_prompt("What is HHI and how is it used in procurement?")

        with q2:
            if st.button("🛡️ Risk"):
                quick_prompt("Explain the procurement risk gauge")

        with q3:
            if st.button("🧠 ML"):
                quick_prompt("How does the machine learning model work?")

        with q4:
            if st.button("👥 Vendors"):
                quick_prompt("Who are the top vendors and what does it mean?")

        st.markdown("<br>", unsafe_allow_html=True)

        # =========================
        # CHAT DISPLAY
        # =========================
        for role, msg in st.session_state.messages:

            if role == "user":
                st.markdown(f"""
                <div class="user-bubble">
                    <b>You</b><br>{msg}
                </div>
                """, unsafe_allow_html=True)

            else:
                st.markdown(f"""
                <div class="bot-bubble">
                    <b>🤖 Darrah AI Assistant</b><br><br>{msg}
                </div>
                """, unsafe_allow_html=True)

        # =========================
        # INPUT (REAL)
        # =========================
        question = st.text_input("Ask anything about the project, data, or analysis...")

        if question:
            answer = ask_ai(question, context=get_context())

            st.session_state.messages.append(("user", question))
            st.session_state.messages.append(("bot", answer))

            st.rerun()

    # =========================
    # RIGHT PANEL
    # =========================
    with right:
        st.markdown("""
        <div class="side-card">
            <h3>📋 Project Overview</h3>
            <div class="mini-grid">
                <div><span>Total Records</span><b>153,269</b><small>Contracts</small></div>
                <div><span>Total Vendors</span><b>8,842</b><small>Vendors</small></div>
                <div><span>Departments</span><b>52</b><small>Departments</small></div>
            </div>
        </div>

        <div class="side-card">
            <h3>⚡ Quick Actions</h3>
            <div class="action-row">Explain Market Concentration (HHI) ›</div>
            <div class="action-row">Show Top Vendors by Spend ›</div>
            <div class="action-row">Explain NLP Classification ›</div>
            <div class="action-row">Explain ML Prediction Model ›</div>
            <div class="action-row">Summarize Key Findings ›</div>
        </div>

        <div class="side-card">
            <h3>📈 Risk Distribution</h3>
            <div class="risk-placeholder">Chart here</div>
            <div class="risk-level">Low Risk</div>
        </div>
        """, unsafe_allow_html=True)


# =========================
# CONTEXT FUNCTION (VERY IMPORTANT)
# =========================
def get_context():
    return """
    This system analyzes government procurement data.

    It includes:
    - Vendor intelligence and market concentration (HHI)
    - Risk scoring based on contract behavior
    - NLP classification of procurement descriptions
    - Machine learning prediction of contract values

    The system is designed as an AI-powered procurement intelligence platform.
    """