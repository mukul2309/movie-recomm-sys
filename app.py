import streamlit as st  # Importing Streamlit library
import pickle  # Importing pickle for reading pickled data
import pandas as pd  # Importing pandas for data manipulation
import requests  # Importing requests for making HTTP requests

# Function to fetch poster for a given movie ID


def fetch_poster(movie_id):
    try:
        if movie_id is None:
            raise ValueError("Movie ID is None")

        # Constructing URL for fetching movie details
        url = 'https://api.themoviedb.org/3/movie/{}?api_key=f32854651b05c6bdb2d20473a1ac108e&language=en-US'.format(
            movie_id)
        print("Fetching poster from URL:", url)
        # Making HTTP GET request to fetch movie details
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        data = response.json()  # Parsing response JSON
        # Extracting poster path from response
        poster_path = data.get('poster_path')
        if poster_path:
            # Constructing full poster URL
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            print("Poster path not found in response data.")
            return ""  # Return empty string if poster path is not found
    except requests.exceptions.RequestException as e:
        print("Error fetching poster:", e)
        return ""
    except ValueError as ve:
        print("Error:", ve)
        return ""

# Function to recommend movies based on similarity to the selected movie


def recommend(movie):
    # Getting index of selected movie
    movie_index = movies[movies['title'] == movie].index[0]
    # Getting similarity scores for the selected movie
    distances = similarity[movie_index]
    # Sort the distances in descending order
    movies_list = sorted(list(enumerate(distances)),
                         reverse=True, key=lambda x: x[1])
    print("All movies with similarity scores:")
    for i, (index, score) in enumerate(movies_list):
        # Printing movie titles and their similarity scores
        print(f"{movies.iloc[index].title}: {score}")
    recommend_movies = []
    recommend_movies_posters = []
    count = 0
    for i, (index, score) in enumerate(movies_list):
        movie_id = movies.iloc[index].movie_id
        recommend_movies.append(movies.iloc[index].title)
        # Fetching poster for recommended movie
        recommend_movies_posters.append(fetch_poster(movie_id))
        count += 1
        if count == 5:
            break  # Stop once we have 5 recommendations
    # Pad the recommendations with empty strings if fewer than 5 movies are recommended
    while len(recommend_movies) < 5:
        recommend_movies.append("")
        recommend_movies_posters.append("")
    return recommend_movies, recommend_movies_posters


# Loading movie data and similarity scores
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Streamlit app title
st.title('MOVIE RECOMMENDATION SYSTEM')

# Dropdown to select a movie
selected_movie_name = st.selectbox("SEARCH", movies['title'].values)

# Button to trigger recommendation
if st.button('Recommend'):
    # Getting recommendations for the selected movie
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if posters[0]:  # Check if the poster URL is not empty
            st.text(names[0])  # Displaying movie title
            st.image(posters[0])  # Displaying movie poster
    with col2:
        if posters[1]:  # Check if the poster URL is not empty
            st.text(names[1])  # Displaying movie title
            st.image(posters[1])  # Displaying movie poster
    with col3:
        if posters[2]:  # Check if the poster URL is not empty
            st.text(names[2])  # Displaying movie title
            st.image(posters[2])  # Displaying movie poster
    with col4:
        if posters[3]:  # Check if the poster URL is not empty
            st.text(names[3])  # Displaying movie title
            st.image(posters[3])  # Displaying movie poster
    with col5:
        if posters[4]:  # Check if the poster URL is not empty
            st.text(names[4])  # Displaying movie title
            st.image(posters[4])  # Displaying movie poster
