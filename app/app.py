import streamlit as st
import pickle
import pandas as pd
import numpy as np
import requests

# Loading save modules
@st.cache_resource
def load_model():
    movies = pickle.load(open('../models/movies.pkl', 'rb'))
    similarity = pickle.load(open('../models/similarity_matrix.pkl', 'rb'))
    movie_indices = pickle.load(open('../models/movie_indices.pkl', 'rb'))
    return movies, similarity, movie_indices

movies, similarity, movie_indices = load_model()

# recommendation function
def recommend(movie):
    index = movie_indices[movie]
    distances = similarity[index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)
    
    return recommended_movies

# streamlit UI
st.set_page_config(page_title="Movie Recommendation System", page_icon=":clapper:", layout="wide")
st.title("Movie Recommendation System")
st.markdown("This is a simple movie recommendation system that recommends movies based on the movie you select.")

# get movie list from dropdown
movie_list = movies['title'].values

# Input
selected_movie = st.selectbox('Select a movie:', movie_list)
if st.button('Recommend'):
    recommended_movies = recommend(selected_movie)
    st.subheader("Recommended Movies:")
    for movie in recommended_movies:
        st.write(movie)


# movies poster url