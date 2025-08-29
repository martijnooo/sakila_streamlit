import streamlit as st
import sys
import os

# Add parent folder of the current working directory
sys.path.append(os.path.abspath(".."))

from backend.eda_utils import rental_over_time_chart, revenue_by_store_chart, top_movies_df, city_options, date_options

st.header("Exploratory Data Analysis")

col1, col2 = st.columns(2, gap="large")
with col1:
    all_cities = city_options()
    cities = st.multiselect(label="**Store**", options=all_cities, default=all_cities)
with col2:
    min_date, max_date = date_options()
    dates = st.slider("**Date Range**", min_date, max_date, (min_date,max_date))

tab1, tab2, tab3 = st.tabs(["Rentals Over Time", "Revenue by Store", "Top Movies"])
with tab1:
    rental_over_time_chart(cities, dates)
with tab2:
    revenue_by_store_chart(cities, dates)
with tab3:
    st.write("**Top Movies per Store**")
    top_movies_df(cities, dates)

