import streamlit as st
import pandas as pd
import plotly.express as px
import utils
import overview as overview
import vendor as vendor
import department as department 
import risk as risk
import nlp as nlp
import prediction as prediction

import streamlit as st
import chatbot





# =========================
# CONFIG
# =========================


# =========================
# LOAD CSS
# =========================
def load_css():
    try:
        with open("style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("style.css not found — using default styling")

load_css()

# =========================
# LOAD DATA (GOOGLE DRIVE)
# =========================
@st.cache_data
def load_data():
    url = "https://drive.google.com/uc?id=1t2HYI1D3QWH2okLOrpYg81MZRJI4cI-k"
    return pd.read_csv(url)

df = load_data()


# =========================
# UTILS
# =========================


df = load_data()

df = utils.add_risk_columns(df)

kpis = utils.get_kpis(df)
trend = utils.get_spending_trend(df)


# =========================
# SIDEBAR
# =========================
st.sidebar.title("Procurement Intelligence System")

page = st.sidebar.radio(
    "Navigation",
    [
    
        "Darrah AI Assistant",
        "Executive Overview",
        "Vendor Intelligence",
        "Department Analysis",
        "Risk Dashboard",
        "NLP Analysis",
        "ML Prediction"
    ]
)

# =========================
# READ ME
# =========================


# =========================
# CHATBOT 
# =========================


# =========================
# EXECUTIVE OVERVIEW
# =========================
if page == "Executive Overview":
    overview.show(df, kpis, trend)

# =========================
# Vendor Intelligence
# =========================
elif page == "Vendor Intelligence":
    vendor.show(df)

# =========================
# Department Analysis
# =========================
elif page == "Department Analysis":
    department.show(df)

# =========================
# Risk Dashboard
# =========================
elif page == "Risk Dashboard":
    risk.show(df)


# =========================
# NLP Analysis
# =========================
elif page == "NLP Analysis":
    nlp.show(df)

# =========================
# ML Prediction
# =========================
elif page == "ML Prediction":
    prediction.show(df)

# =========================
# PLACEHOLDER PAGES
# =========================
elif page == "Vendor Intelligence":
    st.title(" Vendor Intelligence")
    st.info("Coming next...")

elif page == "Department Analysis":
    st.title(" Department Analysis")
    st.info("Coming next...")

elif page == "Risk Dashboard":
    st.title(" Risk Dashboard")
    st.info("Coming next...")

elif page == "NLP Analysis":
    st.title(" NLP Analysis")
    st.info("Coming next...")

elif page == "ML Prediction":
    st.title(" ML Prediction")
    st.info("Coming next...")


# =========================
# FOOTER
# =========================
st.divider()
st.caption("Developed by Darrah Borinaga • University of Toronto • AI Procurement Intelligence System")