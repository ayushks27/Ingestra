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


# -------------------- DB Helpers --------------------
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


def bigram_analysis(df):
    df = df[df["label"] == "True"]

    labels = change_label(df["Stars"].tolist())

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(2, 2)
    )

    X = vectorizer.fit_transform(df["Review"])
    clf = LinearSVC()
    clf.fit(X, labels)

    coef = clf.coef_.ravel()
    top_pos = np.argsort(coef)[-10:]
    top_neg = np.argsort(coef)[:10]
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
zipcode = st.text_input("Enter Zipcode")
business_name = st.text_input("Enter Restaurant Name")

if st.button("Analyze"):
    conn = get_connection()
    cursor = conn.cursor()

    business_id = get_business_id(cursor, zipcode, business_name)

    if not business_id:
        st.error("Business not found.")
    else:
        df = load_reviews(conn, business_id)

        st.metric(
            "Fake Review Ratio",
            f"{fake_ratio(df):.2%}"
        )

        fig = bigram_analysis(df)
        st.pyplot(fig)
