import os
import sys
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st


# Add parent folder of the current working directory
sys.path.append(os.path.abspath(".."))

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
embeddings = load_embeddings("../embeddings/movie_embeddings.npy")

def movie_recommendations(query, top_n=3):
    query_vector = model.encode([query])
    sims = cosine_similarity(query_vector, embeddings)[0]
    top_indices = np.argsort(sims)[::-1][:top_n]
    
    # Select movies and add similarity score column
    top_movies = movies.iloc[top_indices].copy()
    top_movies['score'] = sims[top_indices]  # Add similarity score
    return top_movies.reset_index(drop=True)
