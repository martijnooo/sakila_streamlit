# 🎬 Movie Recommender App

A Streamlit web app that recommends movies based on a text query. Uses semantic search with **SentenceTransformers** embeddings and a precomputed movie database. Includes an **EDA page** and a **Recommender page** with interactive match visualizations.

---

## 🧩 Features

- **Movie Recommendations**  
  Users can input a description or query about a movie, and the app returns the top-N recommendations ranked by semantic similarity.  

- **Match Visualization**  
  Each recommendation displays a dynamic match indicator, including a **donut chart** representing similarity score.  

- **Movie Details**  
  Shows description, category, language, length, and release year for each movie.  

- **EDA (Exploratory Data Analysis)**  
  Explore the movie dataset with interactive charts and insights.  

- **Caching**  
  Models, embeddings, and data are cached for faster loading.  

---

## ⚡ Tech Stack

- **Frontend & UI**: [Streamlit](https://streamlit.io/)  
- **ML / Embeddings**: [SentenceTransformers](https://www.sbert.net/) (`all-MiniLM-L6-v2`)  
- **Similarity**: Cosine similarity  
- **Database**: Supabase SQLAlchemy for movie info  
- **Charts**: [Plotly](https://plotly.com/python/) 
- **Python Version**: 3.11+  

