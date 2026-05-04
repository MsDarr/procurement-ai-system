import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
import joblib

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import r2_score


MODEL_PATH = "model.pkl"


def show(df):

    # =========================
    # HEADER
    # =========================
    st.markdown("<div class='big-title'>ML Contract Prediction</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>AI-powered contract value prediction with model explainability</div>", unsafe_allow_html=True)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # =========================
    # DATA PREP
    # =========================
    model_df = df.copy()

    required_cols = ["vendor_name", "owner_org_title", "contract_value", "month"]

    for col in required_cols:
        if col not in model_df.columns:
            st.error(f"Missing column: {col}")
            return

    model_df = model_df.dropna(subset=required_cols)

    # =========================
    # ENCODING
    # =========================
    le_vendor = LabelEncoder()
    le_dept = LabelEncoder()

    model_df["vendor_encoded"] = le_vendor.fit_transform(model_df["vendor_name"])
    model_df["dept_encoded"] = le_dept.fit_transform(model_df["owner_org_title"])

    X = model_df[["vendor_encoded", "dept_encoded", "month"]]
    y = model_df["contract_value"]

    # =========================
    # TRAIN OR LOAD MODEL
    # =========================
    if os.path.exists(MODEL_PATH):
        model, r2 = joblib.load(MODEL_PATH)
    else:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = RandomForestRegressor(
            n_estimators=150,
            max_depth=12,
            random_state=42
        )

        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        r2 = r2_score(y_test, y_pred)

        joblib.dump((model, r2), MODEL_PATH)

    # =========================
    # KPI — MODEL PERFORMANCE
    # =========================
    col1, col2 = st.columns(2)

    def kpi(title, value, subtitle=""):
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-subtitle">{subtitle}</div>
        </div>
        """, unsafe_allow_html=True)

    with col1:
        kpi("Model Accuracy (R²)", f"{r2:.3f}", "Prediction performance")

    with col2:
        kpi("Model Status", "Trained & Loaded", "Ready for predictions")

    st.markdown("<br>", unsafe_allow_html=True)

    # =========================
    # INPUT PANEL
    # =========================
    st.markdown("<div class='section-title'> Prediction Inputs</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        vendor_input = st.selectbox("Vendor", sorted(model_df["vendor_name"].unique()))

    with col2:
        dept_input = st.selectbox("Department", sorted(model_df["owner_org_title"].unique()))

    with col3:
        month_input = st.slider("Month", 1, 12, 6)

    # Encode
    vendor_encoded = le_vendor.transform([vendor_input])[0]
    dept_encoded = le_dept.transform([dept_input])[0]

    input_data = np.array([[vendor_encoded, dept_encoded, month_input]])

    # =========================
    #  PREDICTION + CONFIDENCE
    # =========================
    tree_preds = np.array([tree.predict(input_data)[0] for tree in model.estimators_])

    prediction = tree_preds.mean()
    std_dev = tree_preds.std()

    confidence = max(0, 100 - (std_dev / prediction * 100)) if prediction != 0 else 0

    # =========================
    # OUTPUT
    # =========================
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Predicted Contract Value</div>", unsafe_allow_html=True)

    st.markdown(f"""
        <div style='font-size:36px; font-weight:700; color:#636EFA;'>
            ${prediction:,.0f}
        </div>
        <div style='font-size:14px; color:#9CA3AF;'>
            Confidence: {confidence:.1f}% (lower variance = higher confidence)
        </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # =========================
    # FEATURE IMPORTANCE
    # =========================
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Feature Importance</div>", unsafe_allow_html=True)

    importance_df = pd.DataFrame({
        "Feature": ["Vendor", "Department", "Month"],
        "Importance": model.feature_importances_
    })

    fig = px.bar(
        importance_df,
        x="Importance",
        y="Feature",
        orientation="h",
        template="plotly_dark",
        color="Importance",
        color_continuous_scale="Blues"
    )

    fig.update_layout(height=300, xaxis_title=None, yaxis_title=None)

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # =========================
    # INSIGHT
    # =========================
    st.markdown("<br>", unsafe_allow_html=True)

    st.info(
        f" Insight: The model achieves an R² score of {r2:.3f}, meaning it explains approximately {r2*100:.1f}% of the variation in contract values."
    )