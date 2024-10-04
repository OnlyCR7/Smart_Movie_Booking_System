from flask import Flask, render_template
import numpy as np
import pandas as pd
import difflib
from flask import Flask, render_template, request, jsonify
import requests
import gdown
import pickle
import io

app = Flask(__name__)

# Google Drive links for the uploaded files
vec_url = 'https://drive.google.com/uc?id=1Vt-8TCKZ1_eew-3HfWKJZgtUcNLHNdb5'
sim_url = 'https://drive.google.com/uc?id=1wfLNeUyFfsag0za4UJ-QHpvJ15iYNs1O'

# Function to download and load a pickle file
def load_pickle_with_gdown(url):
    # Download the file to a temporary location
    temp_file = gdown.download(url, quiet=True)
    
    # Load the pickle object from the file
    with open(temp_file, 'rb') as f:
        return pickle.load(f)

# Load the vectorizer and similarity matrix
vectorizer = load_pickle_with_gdown(vec_url)

similarity = load_pickle_with_gdown(sim_url)



# Google Drive file ID from your link
file_id = '1TCeFRLCGtOzIA0EKVW6rODBfNQ0Zw_i0'
url = f'https://drive.google.com/uc?id={file_id}'

dataset = pd.read_csv(url)  # Update with your actual path
all_movies = dataset['title'].tolist()

def get_recommendations(favorite_movie):
    # Handle NaN values by replacing them with empty strings
    dataset['genres'] = dataset['genres'].fillna('')
    dataset['keywords'] = dataset['keywords'].fillna('')
    dataset['tagline'] = dataset['tagline'].fillna('')
    dataset['cast'] = dataset['cast'].fillna('')
    dataset['director'] = dataset['director'].fillna('')

    # Combine features
    combined_features = dataset['genres'] + ' ' + dataset['keywords'] + ' ' + dataset['tagline'] + ' ' + dataset['cast'] + ' ' + dataset['director']
    
    # Ensure all combined features are strings
    combined_features = combined_features.astype(str)

    # Vectorize the combined features
    feature_vectors = vectorizer.transform(combined_features)
    
    # Find close matches
    movie_name = favorite_movie
    find_close_match = difflib.get_close_matches(movie_name, all_movies)
    
    if not find_close_match:
        return ["No match found"]
    
    close_match = find_close_match[0]
    movie_index = dataset[dataset.title == close_match]['index'].values[0]
    
    # Calculate similarity scores
    similarity_score = list(enumerate(similarity[movie_index]))
    sorted_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)
    
    # Get top 10 movie recommendations
    recommended_movies = []
    for i, movie in enumerate(sorted_movies):
        if i >= 10:  # Limit to top 10 recommendations
            break
        index = movie[0]
        title_of_movie = dataset[dataset.index == index]['title'].values[0]
        recommended_movies.append(f"{i+1}. {title_of_movie}")
    
    return recommended_movies


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/food')
def food():
    return render_template('food.html')

@app.route('/movies')
def movies():
    return render_template('movies.html')

@app.route('/booking')
def booking():
    return render_template('booking.html')

@app.route('/recommend_movie', methods=['GET', 'POST'])
def recommend_movie():
    if request.method == 'POST':
        favorite_movie = request.form.get('favorite_movie')
        recommended_movies = get_recommendations(favorite_movie)
        return jsonify(recommended_movies=recommended_movies)
    return render_template('recommend_movie.html')
 # Make sure this file exists in templates

@app.route('/login')
def login():
    return render_template('login.html')  # Make sure this file exists in templates

if __name__ == '__main__':
    app.run(debug=True)
