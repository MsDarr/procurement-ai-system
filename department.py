import streamlit as st
import plotly.express as px
import utils

def show(df):

    # =========================
    # HEADER
    # =========================
    st.markdown("<div class='big-title'>Department Analysis</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Analyze spending, contract volume, and risk across departments</div>", unsafe_allow_html=True)
    st.divider()

    # =========================
    #  FILTER
    # =========================
    departments = sorted(df["owner_org_title"].dropna().unique())

    selected_dept = st.selectbox(
        "Select Department",
        ["All Departments"] + departments
    )

    if selected_dept != "All Departments":
        filtered_df = df[df["owner_org_title"] == selected_dept]
    else:
        filtered_df = df.copy()

    # =========================
    # KPI ROW
    # =========================
    total_spend = filtered_df["contract_value"].sum()
    total_contracts = len(filtered_df)
    high_risk = filtered_df[filtered_df["risk_level"] == "High Risk"].shape[0]

    col1, col2, col3 = st.columns(3)

    def kpi(title, value, subtitle=""):
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-subtitle">{subtitle}</div>
        </div>
        """, unsafe_allow_html=True)

    with col1:
        kpi("Total Spend", f"${total_spend:,.0f}", "Filtered value")

    with col2:
        kpi("Total Contracts", f"{total_contracts:,}", "Number of contracts")

    with col3:
        kpi("High-Risk Contracts", f"{high_risk:,}", "Risk exposure")

    st.markdown("<br>", unsafe_allow_html=True)

    # =========================
    #  MAIN — SPEND BY DEPARTMENT
    # =========================
    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Spend by Department</div>", unsafe_allow_html=True)

    dept_spend = utils.get_department_spend(filtered_df).head(10)

    fig = px.bar(
        dept_spend,
        x="contract_value",
        y="owner_org_title",
        orientation="h",
        template="plotly_dark",
        color="contract_value",
        color_continuous_scale="Blues"
    )

    fig.update_layout(
        height=420,
        yaxis={"categoryorder": "total ascending"},
        coloraxis_showscale=False
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # =========================
    #  SECONDARY — CONTRACTS + RISK
    # =========================
    col1, col2 = st.columns(2)

    #  Contracts by Department
    with col1:
        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)

        st.markdown("<div class='section-title'>Contracts by Department</div>", unsafe_allow_html=True)

        dept_contracts = utils.get_department_contracts(filtered_df).head(10)

        fig2 = px.bar(
            dept_contracts,
            x="contract_count",
            y="owner_org_title",
            orientation="h",
            template="plotly_dark",
            color="contract_count",
            color_continuous_scale="Purples"
        )

        fig2.update_layout(
            height=350,
            yaxis={"categoryorder": "total ascending"},
            coloraxis_showscale=False
        )

        st.plotly_chart(fig2, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    #  High Risk Departments
    with col2:
        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)

        st.markdown("<div class='section-title'>High Risk by Department</div>", unsafe_allow_html=True)

        risk_dept = (
            filtered_df[filtered_df["risk_level"] == "High Risk"]
            .groupby("owner_org_title")
            .size()
            .reset_index(name="high_risk_count")
            .sort_values(by="high_risk_count", ascending=False)
            .head(10)
        )

        fig3 = px.bar(
            risk_dept,
            x="high_risk_count",
            y="owner_org_title",
            orientation="h",
            template="plotly_dark",
            color="high_risk_count",
            color_continuous_scale="Reds"
        )

        fig3.update_layout(
            height=350,
            yaxis={"categoryorder": "total ascending"},
            coloraxis_showscale=False
        )

        st.plotly_chart(fig3, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # =========================
    #  INSIGHT (SMART TOUCH)
    # =========================
    st.markdown("<br>", unsafe_allow_html=True)

    top_dept = dept_spend.iloc[-1]["owner_org_title"]

    st.info(f" Insight: '{top_dept}' has the highest spending among departments.")