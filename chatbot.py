import streamlit as st

def show():

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

    with center:
        st.markdown("""
        <div class="hero-card">
            <div class="bot-avatar">🤖</div>
            <div>
                <h2>Hello! I'm Darrah AI Assistant 👋</h2>
                <p>I can help you understand procurement data, explain key metrics, identify risks, and provide insights to support your analysis.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        q1, q2, q3, q4 = st.columns(4)
        with q1:
            st.button("📊 What is HHI?")
        with q2:
            st.button("🛡️ Explain risk gauge")
        with q3:
            st.button("🧠 How does ML work?")
        with q4:
            st.button("👥 Top vendors")

        st.markdown("""
        <div class="user-bubble">
            <b>You</b><br>
            What does the risk gauge mean?
        </div>

        <div class="bot-bubble">
            <b>🤖 Darrah AI Assistant</b><br><br>
            The risk gauge represents the overall procurement risk level based on the risk scoring model.<br><br>
            ✅ High contract value<br>
            ✅ Emergency procurement<br>
            ✅ Sole-source contracts<br>
            ✅ Vendor concentration<br>
            ✅ Unusual spending patterns<br><br>
            The gauge gives a quick overview of whether the procurement environment is Low Risk, Moderate Risk, or High Risk.
        </div>

        <div class="input-shell">
            Ask anything about the project, data, or analysis... <span>🎤 ➤</span>
        </div>
        """, unsafe_allow_html=True)

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
            <div class="risk-placeholder">Risk chart here</div>
            <div class="risk-level">Low Risk</div>
        </div>
        """, unsafe_allow_html=True)