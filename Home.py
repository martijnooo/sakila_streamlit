import streamlit as st
import os

# Page configuration
st.set_page_config(
    page_title="Movie Recommender Home",
    page_icon="🎬",
    layout="wide"
)

# Hero image
img_path = os.path.join("assets", "Home_movie2.png")
st.image(img_path, use_column_width=True)

# Title with style
st.markdown(
    """
    <h1 style='text-align: center; color: #C1462C;'>🎥 Movie Recommender</h1>
    """,
    unsafe_allow_html=True
)

# Intro text
st.markdown(
    """
    <div style='text-align: center; font-size: 18px;'>
    Welcome to the Movie Recommender app! <br>
    Explore movie data, get personalized recommendations, and discover your next favorite film. <br>
    Use the sidebar or the buttons below to navigate through the app's features.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# Navigation buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("📊 Explore Data (EDA)"):
        st.session_state.page = "1_EDA"

with col2:
    if st.button("🤖 Get Recommendations"):
        st.session_state.page = "2_Recommender"

# Optional footer
st.markdown(
    """
    <div style='text-align: center; margin-top: 20px; color: grey; font-size: 12px;'>
    Made with ❤️ for movie lovers
    </div>
    """,
    unsafe_allow_html=True
)
