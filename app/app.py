import streamlit as st
import pickle
import pandas as pd
import numpy as np
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import os
from pathlib import Path

TMDB_API_KEY = os.environ.get("TMDB_API_KEY", "")
TMDB_FALLBACK_POSTER = "https://via.placeholder.com/500x750?text=Poster+Not+Available"
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Loading save modules
@st.cache_resource
def load_model():
    models_dir = PROJECT_ROOT / "models"
    movies = pickle.load((models_dir / "movies.pkl").open("rb"))
    similarity = pickle.load((models_dir / "similarity_matrix.pkl").open("rb"))
    movie_indices = pickle.load((models_dir / "movie_indices.pkl").open("rb"))
    return movies, similarity, movie_indices

movies, similarity, movie_indices = load_model()

session = requests.Session()
retry_strategy = Retry(total=3, backoff_factor=0.5, status_forcelist=[429, 500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)

# define function to fetch movie poster from API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get("poster_path")
        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path
    except requests.RequestException:
        pass
    return TMDB_FALLBACK_POSTER

# recommendation function
def recommend(movie):
    index = movie_indices[movie]
    distances = similarity[index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
     
    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters

# streamlit UI
st.set_page_config(page_title="Movie Recommendation System", page_icon=":clapper:", layout="wide")
st.title("Movie Recommendation System")
st.markdown("This is a simple movie recommendation system that recommends movies based on the movie you select.")

# get movie list from dropdown
movie_list = movies['title'].values

# representing the name and poster of the recommended movies
selected_movie = st.selectbox('Select a movie:', movie_list)
if st.button('Recommend'):
    recommended_movies, recommended_posters = recommend(selected_movie)
    st.subheader("Recommended Movies:")
    cols = st.columns(len(recommended_movies))
    for col, movie, poster in zip(cols, recommended_movies, recommended_posters):
        with col:
            st.image(poster, use_container_width=True)
            st.caption(movie)
