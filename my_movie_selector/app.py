from flask import Flask, render_template, request
from movie import Movie, currentMovie
from watchlist import getMovies
from toplists import setupTopLinks
from tmdb import tmbd_poster_from_link
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_movies', methods=['POST'])
def get_movies():
    username = request.form['username']
    genre = request.form['genre']
    movies = getMovies(username, genre)
    chosen_movie = random.choice(list(movies))
    currentMovie.title = chosen_movie
    currentMovie.setupLinks(movies[currentMovie.title])
    return render_template('index.html', title=currentMovie.title, tmdblink=currentMovie.tmdblink)

if __name__ == '__main__':
    app.run(debug=True)
