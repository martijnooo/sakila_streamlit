import streamlit as st
import sys
import os

# Add parent folder of the current working directory
sys.path.append(os.path.abspath(".."))

from backend.prediction import movie_recommendations

st.header("Movie Recommender")

with st.form(key="recommendation_form"):
    query = st.text_area(label="Describe what you would like to watch", height=80)
    submit_button = st.form_submit_button(label="Get Your Recommendation")

    if submit_button:
        st.write("🎬 **Top 3 Recommendations:**")
        recommendations_df = movie_recommendations(query)

        for idx, row in recommendations_df.iterrows():
            # Columns for title+year and score
            col1, col2 = st.columns([4, 1])
            
            # Title + year
            col1.markdown(f"### {row['title']} ({row['release_year']})")

            # Color-code the score
            if row['score'] > 0.8:
                color = "green"
            elif row['score'] > 0.5:
                color = "orange"
            else:
                color = "red"
            
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





