from flask import Flask, render_template
import pickle
import numpy as np
import pandas as pd
import difflib
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

with open('vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

with open('similarity.pkl', 'rb') as f:
    similarity = pickle.load(f)
    
dataset = pd.read_csv('movies.csv')  # Update with your actual path
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
