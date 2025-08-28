import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
import pandas as pd

# Load .env file
load_dotenv()

def sql_connection():
    # Break the connection info into components
    url = URL.create(
    drivername="mysql+mysqlconnector",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    database=os.getenv("DB_NAME")
)

    engine = create_engine(url)

    return engine

def daily_rentals_by_store(engine, year=2005):
    with engine.connect() as conn:
        result = conn.execute(text(f"""select c.city, s.store_id, r.rental_id, r.rental_date from rental r
                                    JOIN inventory i
                                    ON i.inventory_id = r.inventory_id
                                    JOIN store s
                                    ON s.store_id = i.store_id
                                    JOIN address a
                                    ON s.address_id = a.address_id
                                    JOIN city c
                                    ON a.city_id = c.city_id
                                    where year(r.rental_date) = {year}"""))
        df = pd.DataFrame(result)
        df["rental_date"] = df["rental_date"].dt.date
        return df.groupby(["city", "rental_date"]).agg({"rental_id":"count"})
    

def revenue_by_store(engine):
    with engine.connect() as conn:
        result = conn.execute(text(f"""select c.city, p.amount, r.rental_date from payment p
                                    JOIN rental r 
                                    ON r.rental_id = p.rental_id
                                    JOIN inventory i 
                                    ON i.inventory_id = r.inventory_id
                                    JOIN store s
                                    ON i.store_id = s.store_id
                                    JOIN address a
                                    ON s.address_id = a.address_id
                                    JOIN city c
                                    ON a.city_id = c.city_id;"""))
        df = pd.DataFrame(result)
        return df


def top_n_rented_movies_by_store(engine, n=5, year=2005):
    with engine.connect() as conn:
        result = conn.execute(text(f"""select f.title, r.rental_id, r.rental_date, c.city from rental r 
                                    JOIN inventory i 
                                    ON i.inventory_id = r.inventory_id
                                    JOIN film f
                                    on i.film_id = f.film_id
                                    JOIN store s
                                    ON i.store_id = s.store_id
                                    JOIN address a
                                    ON s.address_id = a.address_id
                                    JOIN city c
                                    ON a.city_id = c.city_id
                                    where year(r.rental_date) = {year}"""))
        df = pd.DataFrame(result)

        return df
    
def get_movies(engine):
        with engine.connect() as conn:
            result = conn.execute(text(f"""select f.title, f.description from film f"""))
            df = pd.DataFrame(result)

        return df

    

