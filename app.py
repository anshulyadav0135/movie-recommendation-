import pickle
import streamlit as st
import requests


# Fetch movie poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return full_path


# Recommendation function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters


# Load data
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movie_list = movies['title'].values

# Streamlit UI
st.set_page_config(page_title="🎥 Movie Explorer", page_icon="🌟", layout="wide")

# Custom CSS for new design
st.markdown("""
    <style>
    /* Background and global styling */
    body {
        background-color: #FCF3CF;
        color: #2C3E50;
        font-family: 'Arial', sans-serif;
    }
    .css-1d391kg {
        background-color: #FCF3CF;
    }

    /* Header styling */
    .stHeader {
        font-size: 2.8em;
        font-weight: bold;
        color: #34495E;
        text-align: center;
        margin-bottom: 20px;
    }

    /* Custom button and selectbox styling */
    .stSelectbox, .stButton>button {
        background-color: #85C1E9 !important;
        color: white !important;
        border-radius: 5px;
        padding: 8px 20px;
        font-weight: bold;
        border: none;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #3498DB !important;
    }

    /* Card style for movie recommendations */
    .movie-card {
        background-color: #FFFFFF;
        border-radius: 15px;
        box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.2);
        padding: 20px;
        margin: 10px;
        text-align: center;
        transition: transform 0.2s ease;
    }
    .movie-card:hover {
        transform: translateY(-10px);
        box-shadow: 0px 12px 20px rgba(0, 0, 0, 0.25);
    }
    .movie-title {
        font-size: 1.2em;
        font-weight: bold;
        color: #34495E;
        margin-top: 10px;
    }
    .movie-poster {
        border-radius: 10px;
        width: 100%;
        height: auto;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown("<h1 class='stHeader'>🌟 Movie Explorer</h1>", unsafe_allow_html=True)
st.write("### Discover movies you'll love based on your favorites!")

# Movie selection
selected_movie = st.selectbox("Select a movie to get recommendations:", movie_list)

# Display recommendations
if st.button("Find Recommendations"):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    st.write("---")
    st.write("## 🎬 Recommended Movies")

    # Display movies in a card-style layout
    cols = st.columns(5, gap="medium")
    for i, col in enumerate(cols):
        with col:
            st.markdown(f"""
                <div class="movie-card">
                    <img src="{recommended_movie_posters[i]}" class="movie-poster" alt="{recommended_movie_names[i]} Poster">
                    <div class="movie-title">{recommended_movie_names[i]}</div>
                </div>
                """, unsafe_allow_html=True)
