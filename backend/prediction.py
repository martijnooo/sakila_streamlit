import os
import numpy as np
import pandas as pd
from typing import Optional

import streamlit as st
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from backend.data_loader import sql_connection, get_movie_info

# -----------------------------
# Database connection and engine
# -----------------------------
engine = sql_connection()

# -----------------------------
# Load resources with caching
# -----------------------------
@st.cache_resource
def load_model() -> SentenceTransformer:
    """Load the SentenceTransformer model."""
    return SentenceTransformer('all-MiniLM-L6-v2')

@st.cache_data
def load_movies() -> pd.DataFrame:
    """Load movie information from the database."""
    return get_movie_info(engine)

@st.cache_data
def load_embeddings(path: str) -> np.ndarray:
    """Load precomputed movie embeddings."""
    return np.load(path)

# -----------------------------
# Initialize resources
# -----------------------------
model = load_model()
movies = load_movies()
EMBED_PATH = os.path.join(os.path.dirname(__file__), "../embeddings/movie_embeddings.npy")
embeddings = load_embeddings(EMBED_PATH)

# -----------------------------
# Recommendation logic
# -----------------------------
def movie_recommendations(query: str, top_n: int = 3) -> pd.DataFrame:
    """
    Generate top-N movie recommendations based on a text query.

    Args:
        query (str): User query describing desired movie.
        top_n (int): Number of recommendations to return.

    Returns:
        pd.DataFrame: Top-N movies with similarity scores.
    """
    if not query.strip():
        return pd.DataFrame(columns=movies.columns.tolist() + ['score'])

    query_vector = model.encode([query])
    sims = cosine_similarity(query_vector, embeddings)[0]
    top_indices = np.argsort(sims)[::-1][:top_n]

    top_movies = movies.iloc[top_indices].copy()
    top_movies['score'] = sims[top_indices]  # Add similarity score
    return top_movies.reset_index(drop=True)

# -----------------------------
# Display helpers
# -----------------------------
def color_for_score(score: float) -> str:
    """Return a color based on similarity score."""
    if score > 0.8:
        return "green"
    if score > 0.5:
        return "orange"
    return "red"

def display_recommendation(idx: int, row: pd.Series):
    """Display a single movie recommendation in Streamlit."""
    col1, col2 = st.columns([4, 1])
    col1.markdown(f"### {idx + 1}. {row['title']} ({row['release_year']})")
    color = color_for_score(row["score"])
    col2.markdown(
        f"<span style='font-size:16px; font-weight:bold; color:{color};'>Match: {row['score']:.2f}</span>",
        unsafe_allow_html=True
    )

    # Description
    st.write(row['description'])

    # Other info
    st.markdown(
        f"<span style='font-size:14px; color: gray;'>"
        f"Category: {row['category']} | Language: {row['language']} | Length: {row['length']} min"
        f"</span>",
        unsafe_allow_html=True
    )
    st.markdown("---")

def display_recommendations(df: pd.DataFrame):
    """Display all recommendations in a DataFrame using Streamlit."""
    if df.empty:
        st.warning("No recommendations found. Please enter a valid query.")
        return

    for idx, row in df.iterrows():
        display_recommendation(idx, row)
