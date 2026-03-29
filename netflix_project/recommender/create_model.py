import pandas as pd
import ast
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load datasets
movies = pd.read_csv("tmdb_5000_movies.csv")
credits = pd.read_csv("tmdb_5000_credits.csv")

# Merge datasets
movies = movies.merge(credits, on="title")

# Select important columns
movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]

movies.dropna(inplace=True)

def convert(text):
    L = []
    for i in ast.literal_eval(text):
        L.append(i['name'])
    return L


movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)
movies['cast'] = movies['cast'].apply(convert)


def fetch_director(text):
    L = []
    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            L.append(i['name'])
    return L


movies['crew'] = movies['crew'].apply(fetch_director)

movies['overview'] = movies['overview'].apply(lambda x: x.split())

movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

new = movies[['movie_id','title','tags']]

new['tags'] = new['tags'].apply(lambda x: " ".join(x))
new['tags'] = new['tags'].apply(lambda x: x.lower())

cv = CountVectorizer(max_features=5000, stop_words='english')

vectors = cv.fit_transform(new['tags']).toarray()

similarity = cosine_similarity(vectors)

pickle.dump(new, open('movies.pkl', 'wb'))
pickle.dump(similarity, open('similarity.pkl', 'wb'))

print("Model created successfully")