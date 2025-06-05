import pickle
import streamlit as st
import requests

st.header("Movies Recommendation System using Machine Learning")

# Load movie data and similarity matrix
movies = pickle.load(open('artifact/movie_list.pkl', 'rb'))
similarity = pickle.load(open('artifact/similary.pkl', 'rb'))

# Movie selection dropdown
movies_list = movies['title'].values
selected_movie = st.selectbox(
    'Type or select a movie to get recommendations:', movies_list
)

# Function to fetch poster image from TMDb API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    response = requests.get(url)
    data = response.json()
    poster_path = data.get('poster_path')
    if poster_path:
        return "http://image.tmdb.org/t/p/w500" + poster_path
    else:
        return ""

# Function to get top 5 recommended movies and posters
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies_names = []
    recommended_movies_posters = []

    for i in distances[1:6]:  # top 5 recommendations (excluding the first one, which is the same movie)
        movie_id = movies.iloc[i[0]]['movie_id']
        recommended_movies_names.append(movies.iloc[i[0]]['title'])
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies_names, recommended_movies_posters

# Button click event
if st.button('Show Recommendation'):
    names, posters = recommend(selected_movie)

    # Display recommendations in columns
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
