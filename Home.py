import streamlit as st
import os

st.set_page_config(
    page_title="Movie Recommender Home",
    page_icon="🎨",
    layout="wide"
)

img_path = os.path.join("assets", "Home_movie2.png")
st.image(img_path)

st.title("Movie Recommender")

st.markdown(
    """
    Welcome to the Movie Recommender app!  
    Explore movie data, get recommendations, and discover your next favorite film.  
    Use the sidebar to navigate through the app's features.
    """
)