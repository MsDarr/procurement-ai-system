import streamlit as st


def show():
    st.title("✨ Darrah AI Assistant")
    st.markdown("Your intelligent guide to procurement analytics")

    st.info("Hello! I'm Darrah AI Assistant ")
    st.write(
        "I can help explain procurement concepts, dashboard metrics, "
        "vendor intelligence, risk indicators, and thesis findings."
    )

    st.markdown("### Quick Questions")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("What is HHI?"):
            st.success(
                "HHI means Herfindahl-Hirschman Index. "
                "It measures vendor concentration. A high HHI means spending is dominated by fewer vendors."
            )

        if st.button("Explain risk gauge"):
            st.success(
                "The risk gauge shows the overall procurement risk level based on contract value, "
                "vendor concentration, sole-source contracts, emergency procurement, and unusual spending patterns."
            )

    with col2:
        if st.button("How does the ML model work?"):
            st.success(
                "The ML model analyzes historical procurement data to predict future contract values "
                "and identify patterns that may signal risk or unusual spending."
            )

        if st.button("Who are the top vendors?"):
            st.success(
                "Top vendors will be shown here once we connect the dashboard to your dataset."
            )

    st.markdown("---")

    question = st.text_input(" Ask anything about the project")

    if question:
        q = question.lower()

        if "hhi" in q or "market concentration" in q:
            answer = (
                "HHI measures how concentrated spending is among vendors. "
                "If only a few vendors receive most of the spending, the HHI becomes high."
            )

        elif "risk" in q:
            answer = (
                "Risk is based on factors such as high contract value, vendor dominance, "
                "emergency procurement, sole-source contracts, and unusual spending behavior."
            )

        elif "ml" in q or "machine learning" in q:
            answer = (
                "The machine learning model uses historical procurement patterns to help predict "
                "contract value and detect possible risk signals."
            )

        elif "vendor" in q:
            answer = (
                "Vendor intelligence helps identify top vendors, vendor concentration, "
                "market dominance, and dependency risk."
            )

        else:
            answer = (
                "This assistant currently uses fixed project knowledge. "
                "Later, we will connect it to BigQuery and Gemini AI."
            )

        st.markdown("###  Answer")
        st.success(answer)