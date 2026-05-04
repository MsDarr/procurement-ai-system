import streamlit as st
import plotly.express as px
import utils

def show(df):

    # =========================
    # HEADER
    # =========================
    st.markdown("<div class='big-title'>Vendor Intelligence</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Analyze vendor dominance, performance, and competition</div>", unsafe_allow_html=True)
    st.divider()

    # =========================
    #  FILTER (POWER BI STYLE)
    # =========================
    vendor_list = sorted(df["vendor_name"].dropna().unique())

    selected_vendor = st.selectbox(
        " Select Vendor",
        ["All Vendors"] + vendor_list
    )

    if selected_vendor != "All Vendors":
        filtered_df = df[df["vendor_name"] == selected_vendor]
    else:
        filtered_df = df.copy()

    # =========================
    # KPI ROW (DYNAMIC)
    # =========================
    hhi = utils.calculate_hhi(filtered_df)
    total_vendors = filtered_df["vendor_name"].nunique()
    total_value = filtered_df["contract_value"].sum()

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
        kpi("Total Spend", f"${total_value:,.0f}", "Filtered value")

    with col2:
        kpi("Total Vendors", f"{total_vendors:,}", "After filter")

    with col3:
        kpi("HHI Score", f"{hhi:.4f}", "Market concentration")

    st.markdown("<br>", unsafe_allow_html=True)

    # =========================
    #  TOP VENDORS (MAIN STORY)
    # =========================
    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Top Vendors by Contract Value</div>", unsafe_allow_html=True)

    top_vendors = utils.get_top_vendors(filtered_df, 10)

    fig = px.bar(
        top_vendors,
        x="contract_value",
        y="vendor_name",
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
    #  SECONDARY ANALYSIS
    # =========================
    col1, col2 = st.columns(2)

    #  MARKET SHARE
    with col1:
        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)

        st.markdown("<div class='section-title'>Market Share (Top 5 Vendors)</div>", unsafe_allow_html=True)

        market = utils.get_top_vendors(filtered_df, 5)

        total_market = market["contract_value"].sum()

        fig2 = px.pie(
            market,
            names="vendor_name",
            values="contract_value",
            hole=0.65,
            template="plotly_dark"
        )

        #  Dynamic center value
        fig2.update_layout(
            height=350,
            annotations=[
                dict(
                    text=f"${total_market/1e9:.1f}B",
                    x=0.5,
                    y=0.5,
                    font_size=18,
                    showarrow=False
                )
            ]
        )

        st.plotly_chart(fig2, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    #  CONTRACT COUNT
    with col2:
        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)

        st.markdown("<div class='section-title'>Vendor Contract Activity</div>", unsafe_allow_html=True)

        vendor_count = (
            filtered_df.groupby("vendor_name")
            .size()
            .reset_index(name="contract_count")
            .sort_values(by="contract_count", ascending=False)
            .head(10)
        )

        fig3 = px.bar(
            vendor_count,
            x="contract_count",
            y="vendor_name",
            orientation="h",
            template="plotly_dark",
            color="contract_count",
            color_continuous_scale="Purples"
        )

        fig3.update_layout(
            height=350,
            yaxis={"categoryorder": "total ascending"},
            coloraxis_showscale=False
        )

        st.plotly_chart(fig3, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # =========================
    #  SMART INSIGHT
    # =========================
    st.markdown("<br>", unsafe_allow_html=True)

    if hhi < 0.15:
        st.success("Competitive market — low vendor concentration")
    elif hhi < 0.25:
        st.warning("Moderate concentration — watch dominant vendors")
    else:
        st.error("High concentration — strong vendor dominance risk")