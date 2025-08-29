import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
import pandas as pd
import streamlit as st


db_connection_string = st.secrets["SUPABASE_CONNECTION_STRING"]

@st.cache_resource 
def sql_connection():
    # Create SQL engine
    engine = create_engine(db_connection_string)
    return engine

def daily_rentals_by_store(engine, year=2005):
    with engine.connect() as conn:
        result = conn.execute(text(f"""
            SELECT c.city, s.store_id, r.rental_id, r.rental_date
            FROM rental r
            JOIN inventory i
                ON i.inventory_id = r.inventory_id
            JOIN store s
                ON s.store_id = i.store_id
            JOIN address a
                ON s.address_id = a.address_id
            JOIN city c
                ON a.city_id = c.city_id
            WHERE EXTRACT(YEAR FROM r.rental_date) = {year}
        """))
        df = pd.DataFrame(result.mappings().all())
        df["rental_date"] = pd.to_datetime(df["rental_date"]).dt.date
        return df.groupby(["city", "rental_date"]).agg({"rental_id": "count"})

    

def revenue_by_store(engine):
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT c.city, p.amount, r.rental_date
            FROM payment p
            JOIN rental r 
                ON r.rental_id = p.rental_id
            JOIN inventory i 
                ON i.inventory_id = r.inventory_id
            JOIN store s
                ON i.store_id = s.store_id
            JOIN address a
                ON s.address_id = a.address_id
            JOIN city c
                ON a.city_id = c.city_id;
        """))
        df = pd.DataFrame(result.mappings().all())

        return df



def top_n_rented_movies_by_store(engine, n=5, year=2005):
    with engine.connect() as conn:
        result = conn.execute(text(f"""
            SELECT f.title, r.rental_id, r.rental_date, c.city
            FROM rental r 
            JOIN inventory i 
                ON i.inventory_id = r.inventory_id
            JOIN film f
                ON i.film_id = f.film_id
            JOIN store s
                ON i.store_id = s.store_id
            JOIN address a
                ON s.address_id = a.address_id
            JOIN city c
                ON a.city_id = c.city_id
            WHERE EXTRACT(YEAR FROM r.rental_date) = {year};
        """))
        df = pd.DataFrame(result.mappings().all())

        return df

    
def get_movie_info(engine):
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT 
                f.title,
                f.description,
                MIN(l.name) AS language,          -- replaces ANY_VALUE
                MIN(c.name) AS category,          -- replaces ANY_VALUE
                f.release_year,
                f.length,
                ARRAY_AGG(DISTINCT a.first_name || ' ' || a.last_name) AS actors
            FROM film f
            JOIN language l 
                ON f.language_id = l.language_id
            JOIN film_category fc 
                ON f.film_id = fc.film_id
            JOIN category c 
                ON fc.category_id = c.category_id
            JOIN film_actor fa 
                ON f.film_id = fa.film_id
            JOIN actor a 
                ON fa.actor_id = a.actor_id
            LEFT JOIN inventory i 
                ON f.film_id = i.film_id
            LEFT JOIN rental r 
                ON i.inventory_id = r.inventory_id
            GROUP BY f.film_id;
        """))
        df = pd.DataFrame(result.mappings().all())

        return df


    

