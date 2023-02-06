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
    genre_link = ('genre/' + genre + '/').replace(" ","-").lower()\

    URL = "https://letterboxd.com/" + username + "/watchlist/" + genre_link + "page/"

    return URL

def generateLink(URL, x):
    return str(URL) + str(x)
    

def getMovies(username, genre, URL=None):
    start1 = time.time()
    
    i = 1
    x = 1

    foundlistincache = False
    movies = []
    movieids = []

    #check if list is cached
    foundlistincache, movies = readCSVCache(username, genre)
    if foundlistincache:
        if(len(movies) != 0):
            return movies
        
    #setup link
    if not URL:
        URL = setupLink(username, genre)

    #use beautifulSoup to get movies from link
    start2 = time.time()
    while(i!=0):
        i = 0
        
        link = generateLink(URL, x)

        start3 = time.time()
        page = requests.get(link)
        end3 = time.time()
        soup = BeautifulSoup(page.content,features="html.parser")
        movieresults = soup.find_all("img", {"class" : "image"})
        # print(movieresults)

        # find movies div
        # idresults = soup.find_all("div", {"class" : "film-poster"})

        #create movie titles list
        for movie in movieresults:
        # try:
            movies.append(movie['alt'])
        # except KeyError:
            # pass
            i=i+1

        # movie div attributes
        # for movie in idresults:
        #     movieids.append(movie['data-film-id'])
        x += 1

    end2 = time.time()
    if(len(movies) != 0):
        print(movies)
    else:
        print("You have no " + genre.title() +  " movies in your watchlist.")

    createcsvcache(username, genre, movies)
    end1 = time.time()
    print("whole runtime: ")
    print(end1 - start1)
    print("loop runtime: ")
    print(end2 - start2)
    print("get url runtime: ")
    print(end3 - start3)
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
            if genrestring == row[0] and userfound == True:
                # cachegenre = row.replace('g3nP3: ','')
                genrefound = True
                # print("cachegenre found")
                continue
            if userstring == row[0]:
                # cacheusername = row.replace('us3rn4m3: ','')
                # print("cacheusername found")
                userfound = True
                continue

    return foundlist, movies


def createcsvcache(username, genre, movies):
    with open("D:\\Users\\SenpaiOrigin\\Documents\\LetterboxdMovieParser\\cachedmovies.csv", 'a', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["us3rn4m3: " + username])
        writer.writerow(["g3nP3: " + genre])
        writer.writerow(movies)

