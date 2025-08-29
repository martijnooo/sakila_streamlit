import sys
import os
import plotly.express as px
import streamlit as st

# Add parent folder of the current working directory
sys.path.append(os.path.abspath(".."))

from backend.data_loader import sql_connection, daily_rentals_by_store, top_n_rented_movies_by_store, revenue_by_store

engine = sql_connection()

def rental_over_time_chart(cities, dates):
    df = daily_rentals_by_store(engine).reset_index()
    df = df[df.city.isin(cities)]
    df = df[(df.rental_date > dates[0]) & (df.rental_date < dates[1])]

    fig = px.line(
        df, 
        x="rental_date", 
        y="rental_id", 
        color="city",
        title='Rentals over Time',
        labels={
            "rental_date": "Rental Date", 
            "rental_id": "Number of Rentals",
            "city": "Store"  
        }
    )

    return st.plotly_chart(fig, use_container_width=True)

def revenue_by_store_chart(cities, dates):
    df = revenue_by_store(engine)
    df["rental_date"] = df["rental_date"].dt.date
    
    df = df[df.city.isin(cities)]
    df = df[(df.rental_date > dates[0]) & (df.rental_date < dates[1])]
    df = df.groupby(["city"]).agg({"amount":"sum"}).reset_index()
    fig = px.bar(
        df,
        x= "city",
        y="amount",
        color="city",
        title="Revenue per Store",
        labels={
            "city": "Store",
            "amount":"Revenue"
        }
    )

    return st.plotly_chart(fig, use_container_width=True)

def top_movies_df(cities, dates, n=5):
    df = top_n_rented_movies_by_store(engine).reset_index()
    df["rental_date"] = df["rental_date"].dt.date
    df = df[df.city.isin(cities)]
    df = df[(df.rental_date > dates[0]) & (df.rental_date < dates[1])]
    df = (
        df.groupby(["city", "title"])
        .agg({"rental_id": "count"}).sort_values(["city","rental_id"], ascending=[True, False])
        .groupby(level="city")
        .head(n)
        ).reset_index()
    # Rename columns
    df = df.rename(columns={
        "title": "Movie Title",
        "rental_id": "Number of Rentals",
        "city": "City"
    })
    # Add rank per city
    df["Rank"] = df.groupby("City")["Number of Rentals"].rank(method="first", ascending=False).astype(int)

    # Combine movie title and number of rentals into one string
    df["Movie & Rentals"] = df["Movie Title"] + " (" + df["Number of Rentals"].astype(str) + ")"

    # Pivot table: rows = Rank, columns = City, values = combined string
    pivot_df = df.pivot(index="Rank", columns="City", values="Movie & Rentals")

    # Reset index so Rank is a column
    pivot_df = pivot_df.reset_index()


    return st.dataframe(pivot_df, hide_index=True)

def city_options():
    df = top_n_rented_movies_by_store(engine).reset_index()
    return df.city.unique()

def date_options():
    df = daily_rentals_by_store(engine).reset_index()
    min_date = df.rental_date.min()
    max_date = df.rental_date.max()
    return min_date, max_date

