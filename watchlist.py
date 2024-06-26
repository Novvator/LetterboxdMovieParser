import pickle
import requests
import random
from bs4 import BeautifulSoup
import os

def setupLink(username_input, genre_input):
    genres = [
        'action', 'adventure', 'animation', 'comedy', 'crime', 'documentary', 
        'drama', 'family', 'fantasy', 'history', 'horror', 'music', 'mystery', 
        'romance', 'science-fiction', 'thriller', 'tv-movie', 'war', 'western'
    ]

    username = username_input.lower()
    genre = genre_input.lower()

    if genre == 'random':
        genre = random.choice(genres)
        print('Genre is:', genre)

    genre_link = ('genre/' + genre + '/').replace(" ", "-").lower() if genre != 'all' else ''
    URL = f"https://letterboxd.com/{username}/watchlist/{genre_link}page/"
    
    return URL, genre

def generateLink(URL, x):
    return f"{URL}{x}"
    
def getMovies(username, genre, URL=None):
    cache_dict = {}

    if not URL:
        URL, genre = setupLink(username, genre)

    foundlistincache, movies, cache_dict = readPickleCache(username, genre, cache_dict)
    if foundlistincache and movies:
        return movies

    movies, movielinkpartsresults = [], []
    x = 1

    while True:
        link = generateLink(URL, x)
        page = requests.get(link)
        soup = BeautifulSoup(page.content, features="html.parser")

        currmovieresults = soup.find_all("img", {"class": "image"})
        currdivresults = soup.find_all("div", {"class": "film-poster"})

        movies.extend(currmovieresults)
        movielinkpartsresults.extend(currdivresults)

        next_button = soup.find("a", {"class": "next"})
        if not next_button:
            break

        x += 1

    movie_dict = {movie['alt']: linkpart['data-film-slug'] for movie, linkpart in zip(movies, movielinkpartsresults)}

    if movie_dict:
        print("Movies retrieved successfully.")
    else:
        print(f"You have no {genre.title()} movies in your watchlist.")

    createPickleCache(username, genre, movie_dict, cache_dict)
    return movie_dict

def findMovieLink(movie):
    movie = movie.translate(str.maketrans('', '', '.:,()+')).replace(" ", "-").lower()
    return f'https://letterboxd.com/film/{movie}'

def readPickleCache(username, genre, cache_dict):
    try:
        with open("cachedmovies.pkl", 'rb') as file:
            cache_dict = pickle.load(file)
    except FileNotFoundError:
        print('cache_dict not found')
        
    key = f"{username}_{genre}"
    movies = cache_dict.get(key, {})
    foundlist = bool(movies)
    print(cache_dict.keys())
    return foundlist, movies, cache_dict

def createPickleCache(username, genre, movies, cache_dict):
    key = f"{username}_{genre}"
    cache_dict[key] = movies
    with open("cachedmovies.pkl", 'wb') as file:
        pickle.dump(cache_dict, file)
