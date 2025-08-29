import streamlit as st
from backend.prediction import movie_recommendations, display_recommendations

st.set_page_config(page_title="Movie Recommender", layout="wide")

st.title("🎬 Movie Recommender")

st.markdown(
    """
    Describe the type of movie you want to watch and get your top recommendations!
    You can be as detailed as you like, e.g., genre, mood, or actors.
    """
)

with st.form(key="recommendation_form"):
    query = st.text_area(
        label="What kind of movie are you in the mood for?",
        height=80,
        placeholder="E.g., a funny family adventure movie with talking animals..."
    )
    submit_button = st.form_submit_button(label="Get Recommendations")

if submit_button:
    recommendations_df = movie_recommendations(query)
    display_recommendations(recommendations_df)
