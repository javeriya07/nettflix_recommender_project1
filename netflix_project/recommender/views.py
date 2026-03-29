import pickle
import requests
from django.shortcuts import render
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

movies = pickle.load(open(os.path.join(BASE_DIR, "movies.pkl"), "rb"))
similarity = pickle.load(open(os.path.join(BASE_DIR, "similarity.pkl"), "rb"))

API_KEY = "9ffcd01966843f479edbf0e152e73054"


def fetch_poster(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"

    data = requests.get(url)
    data = data.json()

    poster_path = data.get("poster_path")

    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        return ""


def recommend(movie):

    if movie is None:
        return [], []

    movie = str(movie).strip()

    if movie == "":
        return [], []

    match = movies[movies["title"].str.contains(movie, case=False, na=False)]

    if match.empty:
        return ["Movie not found"], [""]

    index = match.index[0]

    distances = similarity[index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:7]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list:

        movie_id = movies.iloc[i[0]]["movie_id"]

        recommended_movies.append(movies.iloc[i[0]]["title"])

        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters


def home(request):

    movie_list = movies["title"].values

    recommended_movies = []
    recommended_posters = []

    if request.method == "POST":

        movie = request.POST.get("movie","")

        recommended_movies, recommended_posters = recommend(movie)

    movie_data = list(zip(recommended_movies, recommended_posters))

    return render(request, "home.html", {
        "movies": movie_list,
        "movie_data": movie_data
    })