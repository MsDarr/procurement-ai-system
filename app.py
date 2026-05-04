import streamlit as st
import pandas as pd
import plotly.express as px
import os

import utils
import overview
import vendor
import department 
import risk
import nlp
import prediction
import chatbot
from ai_service import ai_service



# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Procurement Intelligence System",
    layout="wide"
)

# =========================
# LOAD CSS
# =========================
def load_css():
    with open("style.css") as f:
        css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

        # FORCE BODY STYLE
        st.markdown("""
        <style>
        html, body, [class*="css"]  {
            background-color: #0B0F19 !important;
            color: #E5E7EB !important;
        }
        </style>
        """, unsafe_allow_html=True)

#  CALL IT (THIS WAS MISSING)
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
# FEATURE ENGINEERING
# =========================
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
# PAGES
# =========================
if page == "Darrah AI Assistant":
    chatbot.show()

elif page == "Executive Overview":
    overview.show(df, kpis, trend)

elif page == "Vendor Intelligence":
    vendor.show(df)

elif page == "Department Analysis":
    department.show(df)

elif page == "Risk Dashboard":
    risk.show(df)

elif page == "NLP Analysis":
    nlp.show(df)

elif page == "ML Prediction":
    prediction.show(df)

# =========================
# FOOTER
# =========================
st.divider()
st.caption("Developed by Darrah Borinaga • University of Toronto • AI Procurement Intelligence System")
