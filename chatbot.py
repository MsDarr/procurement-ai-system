import streamlit as st

def show():

    # =========================
    # LAYOUT (3 PANEL)
    # =========================
    left, center, right = st.columns([1.2, 3.5, 1.8])

    # =========================
    # CENTER PANEL (AI UI)
    # =========================
    with center:

        # HEADER
        st.markdown("""
        <div>
            <p class="big-title">✨ Darrah AI Assistant</p>
            <p class="subtitle">Your intelligent guide to procurement analytics</p>
        </div>
        """, unsafe_allow_html=True)

        # =========================
        # AI CARD (FIXED)
        # =========================
        st.markdown("""
        <div class="ai-card">
            <div style="display:flex; gap:15px; align-items:center;">
                <div style="font-size:30px;">🤖</div>
                <div>
                    <h3 style="margin:0;">Hello! I'm Darrah AI Assistant 👋</h3>
                    <p style="margin:0; font-size:14px;">
                        I can help explain procurement concepts, dashboard metrics, vendor intelligence, and risk indicators.
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # =========================
        # QUICK QUESTIONS
        # =========================
        if "quick_answer" not in st.session_state:
            st.session_state.quick_answer = ""

        q1, q2, q3, q4 = st.columns(4)

        with q1:
            if st.button("📊 HHI"):
                st.session_state.quick_answer = "HHI measures vendor concentration. High HHI = few vendors dominate spending."

        with q2:
            if st.button("⚠️ Risk"):
                st.session_state.quick_answer = "Risk is based on contract value, vendor dominance, emergency procurement, and unusual spending."

        with q3:
            if st.button("🤖 ML"):
                st.session_state.quick_answer = "The ML model predicts contract values using historical procurement patterns."

        with q4:
            if st.button("🏆 Vendors"):
                st.session_state.quick_answer = "Top vendors are those with highest total contract value and frequency."

        st.markdown("<br>", unsafe_allow_html=True)

        # =========================
        # CHAT DISPLAY (FIXED BLOCKS)
        # =========================
        if st.session_state.quick_answer:
            st.markdown(f"""
            <div class="chat-bot">
                {st.session_state.quick_answer}
            </div>
            """, unsafe_allow_html=True)

        # =========================
        # USER INPUT
        # =========================
        question = st.text_input("Ask anything about the project...")

        if question:
            q = question.lower()

            if "hhi" in q or "market concentration" in q:
                answer = "HHI measures how concentrated spending is among vendors."

            elif "risk" in q:
                answer = "Risk is based on contract value, vendor dominance, emergency procurement, and unusual spending."

            elif "ml" in q:
                answer = "The ML model predicts contract value using historical procurement data."

            elif "vendor" in q:
                answer = "Vendor intelligence identifies top vendors and market dominance."

            else:
                answer = "This assistant currently uses project knowledge. Next step: connect to AI."

            # USER MESSAGE (RIGHT)
            st.markdown(f"""
            <div class="chat-user">
                {question}
            </div>
            """, unsafe_allow_html=True)

            # BOT MESSAGE (LEFT)
            st.markdown(f"""
            <div class="chat-bot">
                {answer}
            </div>
            """, unsafe_allow_html=True)

    # =========================
    # RIGHT PANEL
    # =========================
    with right:

        st.markdown("### 📊 Project Overview")

        c1, c2, c3 = st.columns(3)
        c1.metric("Records", "153,269")
        c2.metric("Vendors", "8,842")
        c3.metric("Departments", "52")

        st.markdown("<hr>", unsafe_allow_html=True)

        st.markdown("### ⚡ Quick Actions")
        st.button("Explain HHI")
        st.button("Top Vendors")
        st.button("Explain NLP")
        st.button("ML Model")

        st.markdown("<hr>", unsafe_allow_html=True)

        st.markdown("### 📈 Risk Distribution")
        st.write("Chart here")

        st.success("Low Risk")