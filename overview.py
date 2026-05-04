import streamlit as st
import plotly.express as px


def show(df, kpis, trend):

    # =========================
    # SAFE COLUMN HANDLING
    # =========================
    df.columns = df.columns.str.strip().str.lower()

    vendor_col = "vendor_name" if "vendor_name" in df.columns else df.columns[0]
    org_col = "owner_org_title" if "owner_org_title" in df.columns else df.columns[1]
    value_col = "contract_value" if "contract_value" in df.columns else df.columns[2]

    if "risk_level" not in df.columns:
        df["risk_level"] = "Low Risk"

    # =========================
    # HEADER
    # =========================
    st.markdown("<div class='big-title'>Executive Overview</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Procurement performance and risk insights</div>", unsafe_allow_html=True)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # =========================
    # KPI STRIP
    # =========================
    col1, col2, col3, col4 = st.columns(4)

    def kpi(title, value):
        st.markdown(f"""
        <div class="kpi-box">
            <div class="kpi-label">{title}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

    total_value = df[value_col].sum()
    total_contracts = len(df)
    total_vendors = df[vendor_col].nunique()
    high_risk = df[df["risk_level"] == "High Risk"].shape[0]

    with col1:
        kpi("Total Value", f"${total_value/1e9:.1f}B")

    with col2:
        kpi("Contracts", f"{total_contracts:,}")

    with col3:
        kpi("Vendors", f"{total_vendors:,}")

    with col4:
        kpi("High Risk", f"{high_risk:,}")

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # =========================
    # SPENDING TREND
    # =========================
    st.markdown("#### Spending Trend")

    if "year" in df.columns:
        trend_data = df.groupby("year")[value_col].sum().reset_index()

        fig = px.line(
            trend_data,
            x="year",
            y=value_col,
            template="plotly_dark"
        )

        fig.update_traces(
            mode="lines+markers",
            line=dict(width=2, color="#C9D9F9"),
            marker=dict(size=9, color="#B141DA"),
            hovertemplate="<b>Year:</b> %{x}<br><b>Value:</b> %{y:,.0f}<extra></extra>",
            hoverlabel=dict(
                bgcolor="#010A10",
                font_size=13,
                font_color="white"
            )
        )

        fig.update_layout(
            height=320,
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis=dict(showgrid=False),
            yaxis=dict(gridcolor="rgba(255,255,255,0.08)")
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("Missing 'year' column for trend analysis.")

    # =========================
    # TOP VENDORS (GRADIENT)
    # =========================
    st.markdown("#### Top Vendors")

    top_vendors = (
        df.groupby(vendor_col)[value_col]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )

    top_vendors["normalized"] = top_vendors[value_col] / top_vendors[value_col].max()

    fig2 = px.bar(
        top_vendors,
        x=value_col,
        y=vendor_col,
        orientation="h",
        color="normalized",
        color_continuous_scale=[
            "#B480DB",
            "#BD22DF",
            "#B12CD6",
            "#E056DE"
        ]
    )

    fig2.update_layout(coloraxis_showscale=False)

    fig2.update_traces(
        marker=dict(line=dict(width=0)),
        hovertemplate="<b>%{y}</b><br>Value: %{x:,.0f}<extra></extra>"
    )

    fig2.update_layout(
        height=300,
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis=dict(showgrid=False),
        yaxis=dict(categoryorder="total ascending", showgrid=False)
    )

    st.plotly_chart(fig2, use_container_width=True)

    # =========================
    # RISK DISTRIBUTION
    # =========================
    





    # =========================
    # ORGANIZATION SPEND (MODERN BAR)
    # =========================
    st.markdown("#### Organization Spend")

    org = (
        df.groupby(org_col)[value_col]
        .sum()
        .sort_values(ascending=False)
        .head(8)
        .reset_index()
    )

    total = org[value_col].sum()

    for _, row in org.iterrows():
        value = row[value_col]
        pct = (value / total) * 100

        st.markdown(f"""
        <div style="margin-bottom:12px;">
            <div style="display:flex; justify-content:space-between; font-size:12px;">
                <span>{row[org_col]}</span>
                <span>${value/1e6:.1f}M · {pct:.1f}%</span>
            </div>
            <div style="background:#111827; height:6px; border-radius:6px;">
                <div style="width:{pct}%; background:#4F46E5; height:6px; border-radius:6px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)