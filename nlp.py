import streamlit as st
import plotly.express as px
import pandas as pd
import re

from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation


def show(df):

    # =========================
    # HEADER
    # =========================
    st.markdown("<div class='big-title'>NLP Contract Intelligence</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='subtitle'>Topic modeling, keyword trends, and AI-style contract classification</div>",
        unsafe_allow_html=True
    )
    st.divider()

    # =========================
    # SAFETY CHECK
    # =========================
    if "description_en" not in df.columns:
        st.error("Missing column: description_en")
        return

    nlp_df = df.copy()
    nlp_df["description_en"] = nlp_df["description_en"].fillna("")

    # =========================
    # TEXT CLEANING
    # =========================
    def clean_text(text):
        text = str(text).lower()
        text = re.sub(r"[^a-zA-Z\s]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    nlp_df["clean_description"] = nlp_df["description_en"].apply(clean_text)

    # =========================
    # AI CATEGORY DETECTION
    # =========================
    def detect_category(text):
        text = str(text).lower()

        category_keywords = {
            "IT": ["software", "cloud", "database", "cyber", "technology", "system", "network", "digital", "data"],
            "Construction": ["construction", "building", "renovation", "repair", "maintenance", "infrastructure"],
            "Consulting": ["consulting", "advisory", "consultant", "strategy", "professional"],
            "Healthcare": ["health", "medical", "hospital", "clinical", "vaccine", "pharmaceutical"],
            "Engineering": ["engineering", "engineer", "design", "technical", "architecture"],
            "Equipment": ["equipment", "machinery", "device", "hardware", "vehicle"],
            "Transportation": ["transportation", "vehicle", "fleet", "shipping", "logistics"],
            "Professional Services": ["training", "management", "administrative", "support", "services"]
        }

        for category, keywords in category_keywords.items():
            if any(word in text for word in keywords):
                return category

        return "Other"

    nlp_df["ai_category"] = nlp_df["clean_description"].apply(detect_category)

    # =========================
    # STOPWORDS + KEYWORDS
    # =========================
    stopwords = {
        "the", "and", "for", "with", "this", "that", "from", "are", "was", "were",
        "contract", "contracts", "service", "services", "supply", "provide", "provided",
        "project", "work", "support", "related", "including", "required", "requirement",
        "canada", "government", "department"
    }

    all_words = []
    for text in nlp_df["clean_description"]:
        words = text.split()
        all_words.extend([w for w in words if w not in stopwords and len(w) > 3])

    word_counts = Counter(all_words)
    top_words = word_counts.most_common(15)

    top_keyword = top_words[0][0] if top_words else "N/A"
    unique_keywords = len(word_counts)
    total_categories = nlp_df["ai_category"].nunique()

    # =========================
    # KPI ROW
    # =========================
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
        kpi("Unique Keywords", f"{unique_keywords:,}", "Extracted from descriptions")

    with col2:
        kpi("Top Keyword", top_keyword, "Most frequent term")

    with col3:
        kpi("AI Categories", f"{total_categories:,}", "Detected contract groups")

    st.markdown("<br>", unsafe_allow_html=True)

    # =========================
    # ROW 1 — CATEGORY + KEYWORDS
    # =========================
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>AI Contract Category Detection</div>", unsafe_allow_html=True)

        category_df = (
            nlp_df["ai_category"]
            .value_counts()
            .reset_index()
        )
        category_df.columns = ["category", "count"]

        fig = px.bar(
            category_df,
            x="count",
            y="category",
            orientation="h",
            template="plotly_dark",
            color="count",
            color_continuous_scale="Blues"
        )

        fig.update_layout(
            height=380,
            xaxis_title=None,
            yaxis_title=None,
            yaxis={"categoryorder": "total ascending"},
            coloraxis_showscale=False
        )

        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Top Keywords from Contract Descriptions</div>", unsafe_allow_html=True)

        word_df = pd.DataFrame(top_words, columns=["keyword", "count"])

        fig2 = px.bar(
            word_df,
            x="count",
            y="keyword",
            orientation="h",
            template="plotly_dark",
            color="count",
            color_continuous_scale="Purples"
        )

        fig2.update_layout(
            height=380,
            xaxis_title=None,
            yaxis_title=None,
            yaxis={"categoryorder": "total ascending"},
            coloraxis_showscale=False
        )

        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # =========================
    # TOPIC MODELING — LDA
    # =========================
    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Topic Modeling using LDA</div>", unsafe_allow_html=True)

    sample_text = nlp_df["clean_description"]
    sample_text = sample_text[sample_text.str.len() > 10]

    if len(sample_text) < 10:
        st.warning("Not enough text data for topic modeling.")
    else:
        vectorizer = CountVectorizer(
            max_features=500,
            stop_words="english",
            min_df=2
        )

        text_matrix = vectorizer.fit_transform(sample_text)

        lda = LatentDirichletAllocation(
            n_components=5,
            random_state=42,
            learning_method="batch"
        )

        lda.fit(text_matrix)

        feature_names = vectorizer.get_feature_names_out()

        topics = []

        for topic_idx, topic in enumerate(lda.components_):
            top_indices = topic.argsort()[-8:][::-1]
            keywords = [feature_names[i] for i in top_indices]

            topics.append({
                "Topic": f"Topic {topic_idx + 1}",
                "Top Keywords": ", ".join(keywords)
            })

        topic_df = pd.DataFrame(topics)

        st.dataframe(topic_df, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # =========================
    # KEYWORD GROWTH TRENDS
    # =========================
    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Keyword Growth Trends by Year</div>", unsafe_allow_html=True)

    if "year" not in nlp_df.columns:
        st.warning("Missing year column. Cannot create keyword trend.")
    else:
        trend_keywords = [w[0] for w in top_words[:5]]

        trend_rows = []

        for year in sorted(nlp_df["year"].dropna().unique()):
            year_text = " ".join(
                nlp_df[nlp_df["year"] == year]["clean_description"].tolist()
            )

            for keyword in trend_keywords:
                trend_rows.append({
                    "year": year,
                    "keyword": keyword,
                    "count": year_text.count(keyword)
                })

        trend_df = pd.DataFrame(trend_rows)

        fig3 = px.line(
            trend_df,
            x="year",
            y="count",
            color="keyword",
            markers=True,
            template="plotly_dark"
        )

        fig3.update_layout(
            height=400,
            xaxis_title=None,
            yaxis_title=None
        )

        st.plotly_chart(fig3, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # =========================
    # SAMPLE CONTRACT TEXT
    # =========================
    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Sample AI-Classified Contracts</div>", unsafe_allow_html=True)

    sample_cols = ["description_en", "ai_category"]

    if "contract_value" in nlp_df.columns:
        sample_cols.append("contract_value")

    if "vendor_name" in nlp_df.columns:
        sample_cols.append("vendor_name")

    st.dataframe(
        nlp_df[sample_cols].head(50),
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # =========================
    # SMART INSIGHT
    # =========================
    st.markdown("<br>", unsafe_allow_html=True)

    st.info(
        f" Insight: The most frequent keyword is '{top_keyword}', while the AI category detection shows that procurement activity is concentrated across {total_categories} major contract groups."
    )
    