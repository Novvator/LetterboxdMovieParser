from operator import ge
import pickle
from urllib.error import HTTPError
import requests
import random
from bs4 import BeautifulSoup
import wget
import shutil
import urllib.request
from PIL import ImageTk, Image
import csv
import time

def setupLink(username_input, genre_input):
    genres = ['action','adventure', 'animation', 'comedy', 'crime', 'documentary', 'drama', 'family',
    'fantasy', 'history', 'horror', 'music', 'mystery', 'romance', 'science-fiction', 'thriller', 'tv-movie', 'war', 'western']

    #get username
    username = username_input.lower()

    #get genre
    genre = genre_input.lower()

    #if genre = random
    if(genre == 'random'):
        genre = genres[random.randrange(19)]
        print('Genre is: ' + genre)

    #if genre = all
    if(genre == 'all'):
        genre = ''

    #create genre link
    genre_link = ('genre/' + genre + '/').replace(" ","-").lower()

    URL = "https://letterboxd.com/" + username + "/watchlist/" + genre_link + "page/"

    return URL, genre

def generateLink(URL, x):
    return str(URL) + str(x)
    

def getMovies(username, genre, URL=None):

    foundlistincache = False
    movies = {}
    cache_dict = {}
    x = 1

    #setup link
    if not URL:
        URL, genre = setupLink(username, genre)

    #check if list is cached
    foundlistincache, movies, cache_dict = readPickleCache(username, genre, cache_dict)
    if foundlistincache:
        if(len(movies) != 0):
            return movies
        
    #use beautifulSoup to get movies from link
    movieresults = []
    movielinkpartsresults = []
    while(True):

        # generate link and parse with soup
        link = generateLink(URL, x)
        page = requests.get(link)
        soup = BeautifulSoup(page.content,features="html.parser")

        # find movies element
        currmovieresults = soup.find_all("img", {"class" : "image"})
        movieresults += currmovieresults

        # find movies link poster element
        currdivresults = soup.find_all("div", {"class" : "film-poster"})
        movielinkpartsresults += currdivresults

        # if there is next page button continue loop
        next_button = soup.find("a", {"class":"next"})
        if not next_button:
            break

        x += 1

    # put linkparts into movies dict
    for enum, movie in enumerate(movieresults):
        movies[movie['alt']] = movielinkpartsresults[enum]['data-film-slug']
        
    if(len(movies) != 0):
        # print(movies)
        pass
    else:
        print("You have no " + genre.title() +  " movies in your watchlist.")

    createPickleCache(username, genre, movies, cache_dict)
    return movies


def findMovieLink(movie):
    movie = movie.replace(".","")
    movie = movie.replace(":","")
    movie = movie.replace(",","")
    movie = movie.replace("+","")
    movie = movie.replace("(","")
    movie = movie.replace(")","")
    movie = movie.replace(" ", "-")
    link = 'https://letterboxd.com/film/' + movie
    link = link.lower()
    return link

#doesnt work, it used to return the poster, now returns an empty one

# def findImage(movie):
#     link = findMovieLink(movie)
#     page = requests.get(link)

#     soup = BeautifulSoup(page.content,features="html.parser")

#     imagelink = soup.find("img", {"alt" : movie})
#     return imagelink['src']

# old download image to display

# def downloadImage(imagelink):
#     r = requests.get(imagelink, stream=True)
#     if r.status_code == 200:
#         with open("img.png", 'wb') as f:
#             r.raw.decode_content = True
#             shutil.copyfileobj(r.raw, f)
#         return 'img.png'
#     else:
#         print('Error: Could not get image')
#         return 0

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