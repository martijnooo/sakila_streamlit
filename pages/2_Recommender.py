import streamlit as st
import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.prediction import movie_recommendations, display_recommendation

st.header("Movie Recommender")

with st.form(key="recommendation_form"):
    query = st.text_area(label="Describe what you would like to watch", height=80)
    submit_button = st.form_submit_button(label="Get Your Recommendation")

    if submit_button:
        st.write("🎬 **Top 3 Recommendations:**")
        recommendations_df = movie_recommendations(query)

        for idx, row in recommendations_df.iterrows():
            display_recommendation (idx, row)





