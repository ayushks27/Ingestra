# -------------------- Config --------------------
DB_PATH = "yelp_demo.db"

import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer


# -------------------- Page Config --------------------
st.set_page_config(
    page_title="Ingestra",
    layout="centered"
)

st.title("Ingestra")
st.caption("Data Ingestion & Processing Pipeline")


# -------------------- Database Helpers --------------------
@st.cache_resource
def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def get_business_id(cursor, zipcode, business_name):
    cursor.execute(
        """
        SELECT DISTINCT b_id
        FROM business
        WHERE postal_code = ? AND name = ?
        """,
        (zipcode, business_name)
    )
    result = cursor.fetchone()
    return result[0] if result else None


def load_reviews(conn, business_id):
    query = """
        SELECT 
            Review,
            Stars,
            authenticity_label AS label
        FROM predicted_reviews
        WHERE business_id = ?
    """
    return pd.read_sql_query(query, conn, params=(business_id,))


# -------------------- Analytics --------------------
def change_label(stars):
    return [1 if s >= 3.0 else 0 for s in stars]


def fake_ratio(df):
    total = len(df)
    fake = (df["label"] == 0).sum()
    return fake / total if total > 0 else 0


def average_ratings(df):
    overall_avg = df["Stars"].mean()
    authentic_avg = df[df["label"] == 1]["Stars"].mean()
    return overall_avg, authentic_avg


def bigram_analysis(df):
    # Only authentic reviews
    df = df[df["label"] == 1]

    # Guard: empty or too small
    if df.empty or df["Review"].nunique() < 2:
        return None

    labels = change_label(df["Stars"].tolist())

    # Guard: ML needs at least 2 classes
    if len(set(labels)) < 2:
        return None

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(2, 2),
        min_df=1
    )

    try:
        X = vectorizer.fit_transform(df["Review"])
    except ValueError:
        return None

    clf = LinearSVC()
    clf.fit(X, labels)

    coef = clf.coef_.ravel()
    top_pos = np.argsort(coef)[-5:]
    top_neg = np.argsort(coef)[:5]
    idx = np.hstack([top_neg, top_pos])

    features = np.array(vectorizer.get_feature_names_out())

    plt.figure(figsize=(8, 4))
    colors = ["red" if c < 0 else "blue" for c in coef[idx]]
    plt.bar(range(len(idx)), coef[idx], color=colors)
    plt.xticks(range(len(idx)), features[idx], rotation=45, ha="right")
    plt.title("Key Phrases Influencing Ratings")
    plt.tight_layout()

    return plt


# -------------------- UI --------------------
st.subheader("Analyze Reviews")

zipcode = st.text_input(
    "Enter Zipcode",
    value="226021",
    key="zip"
)

business_name = st.text_input(
    "Enter Restaurant Name",
    value="Demo Cafe",
    key="biz"
)

analyze = st.button("Analyze", key="analyze_btn")

if analyze:
    conn = get_connection()
    cursor = conn.cursor()

    business_id = get_business_id(cursor, zipcode, business_name)

    if not business_id:
        st.error("Business not found. Try: 226021 / Demo Cafe")
    else:
        df = load_reviews(conn, business_id)

        # ---- Metrics ----
        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Fake Review Ratio",
            f"{fake_ratio(df):.2%}"
        )

        overall_avg, authentic_avg = average_ratings(df)

        col2.metric(
            "Avg Rating (All)",
            f"{overall_avg:.2f}" if not np.isnan(overall_avg) else "N/A"
        )

        col3.metric(
            "Avg Rating (Authentic)",
            f"{authentic_avg:.2f}" if not np.isnan(authentic_avg) else "N/A"
        )

        # ---- Bigram Analysis ----
        fig = bigram_analysis(df)

        if fig is None:
            st.info(
                "Not enough authentic reviews to perform phrase analysis "
                "(demo dataset limitation)."
            )
        else:
            st.pyplot(fig)
