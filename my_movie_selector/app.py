from flask import Flask, render_template, request
from movie import Movie, currentMovie
from watchlist import getMovies, delete_cached_movies
from toplists import setupTopLinks
from tmdb import tmbd_poster_from_link
import random

app = Flask(__name__)

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
    username = request.form['username']
    genre = request.form['genre']
    movies = getMovies(username, genre)
    movie_list = list(movies)
    default_lists = [getMovies('default', f'def{i}') for i in range(4)]
    # Implement your score calculation logic here
    scores = {}
    # Example scores calculation:
    # scores = calculate_score(movie_list, *default_lists)
    max_score = max(scores.values())
    films_with_max_score = [film for film, score in scores.items() if score == max_score]
    chosen_movie = random.choice(films_with_max_score)
    currentMovie.title = chosen_movie
    currentMovie.setupLinks(movies[currentMovie.title])
    return update_movie_display(currentMovie.title, currentMovie.tmdblink)

@app.route('/download_top_lists')
def download_top_lists():
    setupTopLinks()
    return "Top lists downloaded successfully!"

@app.route('/delete_cached_movies')
def delete_cached_movies_route():
    delete_cached_movies()
    return "Cached movies deleted successfully!"

def update_movie_display(title, tmdblink):
    tmbd_poster_from_link(tmdblink)
    return render_template('index.html', title=title, tmdblink=tmdblink)

if __name__ == '__main__':
    app.run(debug=True)
