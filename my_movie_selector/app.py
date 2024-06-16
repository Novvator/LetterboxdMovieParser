from flask import Flask, render_template, request
from movie import Movie, currentMovie
from watchlist import getMovies, delete_cached_movies, choose_movie_with_top_score
from toplists import setupTopLinks
from tmdb import tmbd_poster_from_link
import random

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_random_movie', methods=['POST'])
def get_random_movie():
    username = request.form['username']
    genre = request.form['genre']
    movies = getMovies(username, genre)
    chosen_movie = random.choice(list(movies))
    currentMovie.title = chosen_movie
    currentMovie.setupLinks(movies[currentMovie.title])
    return update_movie_display(currentMovie.title, currentMovie.tmdblink)

@app.route('/get_movies_with_score', methods=['POST'])
def get_movies_with_score():
    # Retrieve movies from the watchlist based on user input
    username = request.form['username']
    genre = request.form['genre']
    movies = getMovies(username, genre)
    max_score_movies = choose_movie_with_top_score(list(movies))
    
    # Randomly select a movie with the maximum score
    chosen_movie = random.choice(max_score_movies)
    # Update currentMovie object with chosen movie details
    currentMovie.title = chosen_movie
    print(movies)
    currentMovie.setupLinks(movies[currentMovie.title])
    
    # Update the movie display in the UI
    return update_movie_display(currentMovie.title, currentMovie.tmdblink)

@app.route('/download_top_lists')
def download_top_lists():
    setupTopLinks()
    return render_template('index.html', mmessage="Top lists downloaded successfully!")

@app.route('/delete_cached_movies')
def delete_cached_movies_route():
    delete_cached_movies()
    return render_template('index.html', mmessage="Cached movies deleted successfully!")

def update_movie_display(title, tmdblink):
    tmbd_poster_from_link(tmdblink)
    return render_template('index.html', title=title, tmdblink=tmdblink)
    
if __name__ == '__main__':
    app.run(debug=True)
