import os
import sys
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st


# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.data_loader import sql_connection, get_movie_info

engine = sql_connection()

@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

@st.cache_data
def load_movies():
    return get_movie_info(engine)

@st.cache_data
def load_embeddings(path):
    return np.load(path)

model = load_model()
movies = load_movies()
BASE_DIR = os.path.dirname(__file__)
embeddings_path = os.path.join(BASE_DIR, "..", "embeddings", "movie_embeddings.npy")
embeddings = np.load(embeddings_path, allow_pickle=True)

def movie_recommendations(query, top_n=3):
    query_vector = model.encode([query])
    sims = cosine_similarity(query_vector, embeddings)[0]
    top_indices = np.argsort(sims)[::-1][:top_n]
    
    # Select movies and add similarity score column
    top_movies = movies.iloc[top_indices].copy()
    top_movies['score'] = sims[top_indices]  # Add similarity score
    return top_movies.reset_index(drop=True)

def color_for_score(score):
    if score > 0.8: return "green"
    if score > 0.5: return "orange"
    return "red"

def display_recommendation(idx, row):
        # Columns for title+year and score
        col1, col2 = st.columns([4, 1])
        
        # Title + year
        col1.markdown(f"### {idx + 1}. {row['title']} ({row['release_year']})")

        color = color_for_score(row["score"])
        
        col2.markdown(
            f"<span style='font-size:16px; font-weight:bold; color:{color};'>Match: {row['score']:.2f}</span>",
            unsafe_allow_html=True
        )
        # Description
        st.write(row['description'])

        # Other info in small gray text
        st.markdown(
            f"<span style='font-size:14px; color: gray;'>"
            f"Category: {row['category']} | Language: {row['language']} | Length: {row['length']} min"
            f"</span>",
            unsafe_allow_html=True
        )

        st.markdown("---")


