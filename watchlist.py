from operator import ge
from urllib.error import HTTPError
import requests
import random
from bs4 import BeautifulSoup
import wget
import shutil
import urllib.request
from PIL import ImageTk, Image




def getMovies(username, genre):
    i = 1
    x = 1

    y=0

    movies = []
    movieids = []
    genres = ['action','adventure', 'animation', 'comedy', 'crime', 'documentary', 'drama', 'family',
    'fantasy', 'history', 'horror', 'music', 'mystery', 'romance', 'science-fiction', 'thriller', 'tv-movie', 'war', 'western']

    #get username
    username = username.lower()

    #get genre
    inp = genre.lower()

    #if genre = random
    if(inp == 'random'):
        inp = genres[random.randrange(19)]
        print('Genre is: ' + inp)

    #create genre link
    genre = ('genre/' + inp + '/').replace(" ","-").lower()

    #if genre = all
    if(inp == 'all'):
        genre = ''

    #use beautifulSoup to get movies from link
    while(i!=0):
        i = 0
        URL = "https://letterboxd.com/" + username + "/watchlist/" + genre + "page/" + str(x)
        page = requests.get(URL)

        soup = BeautifulSoup(page.content,features="html.parser")

        
        movieresults = soup.find_all("img", {"class" : "image"})
        idresults = soup.find_all("div", {"class" : "film-poster"})

        for movie in movieresults:
            try:
                movies.append(movie['alt'])
            except KeyError:
                pass
            i=i+1

        for movie in idresults:
            movieids.append(movie['data-film-id'])
        x += 1

    if(len(movies) != 0):
        print(movies)
    else:
        print("You have no " + inp.title() +  " movies in your watchlist.")

    return movies, movieids



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

def findImage(movie):
    link = findMovieLink(movie)
    page = requests.get(link)

    soup = BeautifulSoup(page.content,features="html.parser")

    imagelink = soup.find("img", {"itemprop" : "image"})
    return imagelink['src']


#download image to display
def downloadImage(imagelink):
    r = requests.get(imagelink, stream=True)
    if r.status_code == 200:
        with open("img.png", 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
        return 'img.png'
    else:
        print('Error: Could not get image')
        return 0
    





