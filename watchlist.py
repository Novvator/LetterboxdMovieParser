from operator import ge
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


def getMovies(username, genre):
    start1 = time.time()
    

    i = 1
    x = 1

    y=0

    foundlistincache = False
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

    foundlistincache, movies = readCSVCache(username, genre)
    if foundlistincache:
        if(len(movies) != 0):
            # print(movies)
            pass
        else:
            print("You have no " + inp.title() +  " movies in your watchlist.")
        return movies

    #use beautifulSoup to get movies from link
    start2 = time.time()
    while(i!=0):
        i = 0
        URL = "https://letterboxd.com/" + username + "/watchlist/" + genre + "page/" + str(x)
        page = requests.get(URL)

        soup = BeautifulSoup(page.content,features="html.parser")

        
        movieresults = soup.find_all("img", {"class" : "image"})
        # find movies div
        # idresults = soup.find_all("div", {"class" : "film-poster"})
        # print(movieresults)
        for movie in movieresults:
            try:
                movies.append(movie['alt'])
            except KeyError:
                pass
            i=i+1

        # movie div attributes
        # for movie in idresults:
        #     movieids.append(movie['data-film-id'])
        x += 1

    end2 = time.time()
    if(len(movies) != 0):
        print(movies)
    else:
        print("You have no " + inp.title() +  " movies in your watchlist.")

    createcsvcache(username, genre, movies)
    end1 = time.time()
    print("whole runtime: ")
    print(end1 - start1)
    print("loop runtime: ")
    print(end2 - start2)
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

#doesnt work, it returns an empty poster
def findImage(movie):
    link = findMovieLink(movie)
    page = requests.get(link)

    soup = BeautifulSoup(page.content,features="html.parser")

    imagelink = soup.find("img", {"alt" : movie})
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
    

def readCSVCache(username, genre):
    movies = []
    userfound = False
    genrefound = False
    foundlist = False
    with open("D:\\Users\\SenpaiOrigin\\Documents\\LetterboxdMovieParser\\cachedmovies.csv", 'r') as file:
        reader = csv.reader(file)
        userstring = "us3rn4m3: " + username
        genrestring = "g3nP3: " + genre
        for row in reader:
            if genrefound and userfound:
                movies = row
                foundlist = True
                print("list found")
                break
            if genrestring in row and userfound == True:
                # cachegenre = row.replace('g3nP3: ','')
                genrefound = True
                # print("cachegenre found")
                continue
            if userstring in row:
                # cacheusername = row.replace('us3rn4m3: ','')
                # print("cacheusername found")
                userfound = True
                continue

    return foundlist, movies


def createcsvcache(username, genre, movies):
    print(username,genre)
    with open("D:\\Users\\SenpaiOrigin\\Documents\\LetterboxdMovieParser\\cachedmovies.csv", 'a', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["us3rn4m3: " + username])
        writer.writerow(["g3nP3: " + genre])
        writer.writerow(movies)

