import os
import sys
from sentence_transformers import SentenceTransformer
import numpy as np

# Add project root (two levels up from this file)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.data_loader import sql_connection, get_movies

engine = sql_connection()

def embed_movies():
    movies = get_movies(engine)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    movies_encoded = model.encode(movies.description)

    # Ensure embeddings folder exists
    save_dir = os.path.join("embeddings")
    os.makedirs(save_dir, exist_ok=True)

    save_path = os.path.join(save_dir, "movie_embeddings.npy")
    np.save(save_path, movies_encoded)

embed_movies()