import streamlit as st
import plotly.express as px

def show(df):

    # =========================
    # HEADER
    # =========================
    st.markdown("<div class='big-title'>Risk Dashboard</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Monitor and investigate high-risk contracts across vendors and departments</div>", unsafe_allow_html=True)
    st.divider()

    # =========================
    #  FILTER — HIGH RISK VENDOR
    # =========================
    high_risk_df = df[df["risk_level"] == "High Risk"]

    vendor_list = sorted(high_risk_df["vendor_name"].dropna().unique())

    st.markdown("<div class='section-title'> Select High-Risk Vendor</div>", unsafe_allow_html=True)

    selected_vendor = st.selectbox(
        "",
        ["Vendors"] + vendor_list
    )

    # =========================
    # FILTER LOGIC
    # =========================
    if selected_vendor != "Vendors":
        filtered_df = high_risk_df[high_risk_df["vendor_name"] == selected_vendor]
    else:
        filtered_df = high_risk_df.copy()

    # =========================
    # KPI CALCULATIONS
    # =========================
    total_contracts = len(df)
    total_high_risk = len(high_risk_df)
    selected_count = len(filtered_df)

    risk_percentage = (total_high_risk / total_contracts) * 100 if total_contracts > 0 else 0

    #  Vendor Risk %
    if selected_vendor != "Vendors":
        vendor_df = df[df["vendor_name"] == selected_vendor]

        total_vendor_contracts = len(vendor_df)
        high_risk_vendor = vendor_df[vendor_df["risk_level"] == "High Risk"].shape[0]

        risk_rate = (
            (high_risk_vendor / total_vendor_contracts) * 100
            if total_vendor_contracts > 0 else 0
        )
    else:
        risk_rate = 0

    # =========================
    # KPI ROW
    # =========================
    col1, col2, col3, col4 = st.columns(4)

    def kpi(title, value, subtitle="", highlight=False):
        extra = "kpi-risk" if highlight else ""
        st.markdown(f"""
        <div class="kpi-card {extra}">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-subtitle">{subtitle}</div>
        </div>
        """, unsafe_allow_html=True)

    with col1:
        kpi("High-Risk Contracts", f"{total_high_risk:,}", "Total exposure", True)

    with col2:
        kpi("Selected Vendor Risk", f"{selected_count:,}", "Filtered result")

    with col3:
        kpi("Vendor Risk %", f"{risk_rate:.1f}%", "Risk level of vendor")

    with col4:
        kpi("Overall Risk %", f"{risk_percentage:.2f}%", "System risk")

    st.markdown("<br>", unsafe_allow_html=True)

    # =========================
    #  MAIN — RISK DISTRIBUTION
    # =========================
    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Risk Distribution</div>", unsafe_allow_html=True)

    risk_counts = df["risk_level"].value_counts().reset_index()
    risk_counts.columns = ["risk_level", "count"]

    fig = px.bar(
        risk_counts,
        x="risk_level",
        y="count",
        color="risk_level",
        template="plotly_dark",
        color_discrete_map={
            "High Risk": "#7F1D1D",   #  dark red
            "Medium Risk": "#B45309", #  muted
            "Low Risk": "#010746"     #  dark green
        }
    )

    fig.update_layout(
        height=350,
        xaxis_title=None,
        yaxis_title=None
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # =========================
    #  HIGH-RISK VENDORS
    # =========================
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>High-Risk Vendors</div>", unsafe_allow_html=True)

        vendor_risk = (
            filtered_df.groupby("vendor_name")
            .size()
            .reset_index(name="risk_count")
            .sort_values(by="risk_count", ascending=False)
            .head(10)
        )

        fig2 = px.bar(
            vendor_risk,
            x="risk_count",
            y="vendor_name",
            orientation="h",
            template="plotly_dark",
            color="risk_count",
            color_continuous_scale=["#7F1D1D", "#DC2626"]
        )

        fig2.update_layout(
            height=350,
            xaxis_title=None,
            yaxis_title=None,
            yaxis={"categoryorder": "total ascending"}
        )

        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # =========================
    #  HIGH-RISK DEPARTMENTS
    # =========================
    with col2:
        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>High-Risk Departments</div>", unsafe_allow_html=True)

        dept_risk = (
            filtered_df.groupby("owner_org_title")
            .size()
            .reset_index(name="risk_count")
            .sort_values(by="risk_count", ascending=False)
            .head(10)
        )

        fig3 = px.bar(
            dept_risk,
            x="risk_count",
            y="owner_org_title",
            orientation="h",
            template="plotly_dark",
            color="risk_count",
            color_continuous_scale=["#7F1D1D", "#DC2626"]
        )

        fig3.update_layout(
            height=350,
            xaxis_title=None,
            yaxis_title=None,
            yaxis={"categoryorder": "total ascending"}
        )

        st.plotly_chart(fig3, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # =========================
    #  SMART INSIGHT
    # =========================
    st.markdown("<br>", unsafe_allow_html=True)

    if selected_vendor != "All High-Risk Vendors":
        if risk_rate < 10:
            st.success(f" {selected_vendor} is a low-risk vendor ({risk_rate:.1f}%)")
        elif risk_rate < 30:
            st.warning(f" {selected_vendor} has moderate risk ({risk_rate:.1f}%)")
        else:
            st.error(f" {selected_vendor} is a high-risk vendor ({risk_rate:.1f}%)")
    else:
        if risk_percentage < 10:
            st.success("Low overall system risk")
        elif risk_percentage < 25:
            st.warning("Moderate system risk — monitor vendors")
        else:
            st.error("High system risk — immediate action needed")