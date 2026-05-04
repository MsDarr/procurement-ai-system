import streamlit as st


def show(df=None):

    # =========================
    # HEADER
    # =========================
    st.markdown("""
    <div class="ai-header">
        <div>
            <h1>Darrah AI Assistant</h1>
            <p>Your intelligent guide to procurement analytics</p>
        </div>
        <div class="ai-badge">AI Powered</div>
    </div>
    """, unsafe_allow_html=True)

    # =========================
    # LAYOUT (CENTER + RIGHT)
    # =========================
    center, right = st.columns([2.6, 1.4], gap="large")

    # =========================
    # CENTER PANEL
    # =========================
    with center:

        # HERO CARD
        st.markdown("""
        <div class="hero-card">
            <div class="bot-avatar"></div>
            <div>
                <h2>Hello! I'm Darrah AI Assistant</h2>
                <p>
                    I can help you understand procurement data, explain key metrics,
                    identify risks, and provide insights to support your analysis.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # =========================
        # QUICK QUESTIONS
        # =========================
        st.markdown('<div class="section-title">Quick Questions</div>', unsafe_allow_html=True)

        q1, q2, q3, q4 = st.columns(4)

        with q1:
            st.markdown('<div class="q-card">What is HHI and how is it used?</div>', unsafe_allow_html=True)

        with q2:
            st.markdown('<div class="q-card">Explain the risk gauge</div>', unsafe_allow_html=True)

        with q3:
            st.markdown('<div class="q-card">How does the ML model work?</div>', unsafe_allow_html=True)

        with q4:
            st.markdown('<div class="q-card">Who are the top vendors?</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # =========================
        # CHAT SAMPLE (STATIC UI)
        # =========================
        st.markdown("""
        <div class="chat-user">
            <b>You</b><br>
            What does the risk gauge mean?
        </div>

        <div class="chat-bot">
            <b>Darrah AI Assistant</b><br><br>
            The risk gauge represents the overall procurement risk level based on our scoring model.<br><br>
            ✔ High contract value<br>
            ✔ Emergency procurement<br>
            ✔ Sole-source contracts<br>
            ✔ Vendor concentration<br>
            ✔ Unusual spending patterns<br><br>
            It provides a quick overview of whether the environment is Low, Moderate, or High Risk.
        </div>
        """, unsafe_allow_html=True)

        # =========================
        # INPUT BAR (UI ONLY)
        # =========================
        st.markdown("""
        <div class="input-bar">
            Ask anything about the project, data, or analysis...
        </div>
        """, unsafe_allow_html=True)

        # =========================
        # KPI STRIP
        # =========================
        st.markdown("""
        <div class="kpi-strip">
            <div><span>Total Contract Value</span><b>$2.45B</b></div>
            <div><span>Avg Contract Value</span><b>$15,978</b></div>
            <div><span>Emergency Procurements</span><b>1,248</b></div>
            <div><span>Sole-Source Contracts</span><b>2,156</b></div>
            <div><span>Vendor Concentration (HHI)</span><b>0.14</b></div>
        </div>
        """, unsafe_allow_html=True)

    # =========================
    # RIGHT PANEL
    # =========================
    with right:

        # PROJECT OVERVIEW
        st.markdown("""
        <div class="side-card">
            <h3>Project Overview</h3>
            <div class="mini-grid">
                <div><span>Total Records</span><b>153,269</b></div>
                <div><span>Total Vendors</span><b>8,842</b></div>
                <div><span>Departments</span><b>52</b></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # QUICK ACTIONS
        st.markdown("""
        <div class="side-card">
            <h3>Quick Actions</h3>
            <div class="action">Explain Market Concentration (HHI)</div>
            <div class="action">Show Top Vendors by Spend</div>
            <div class="action">Explain NLP Classification</div>
            <div class="action">Explain ML Prediction Model</div>
            <div class="action">Summarize Key Findings</div>
        </div>
        """, unsafe_allow_html=True)

        # RISK DISTRIBUTION
        st.markdown("""
        <div class="side-card">
            <h3>Risk Distribution</h3>
            <div class="risk-chart">Chart Area</div>
            <div class="risk-level">Low Risk</div>
        </div>
        """, unsafe_allow_html=True)