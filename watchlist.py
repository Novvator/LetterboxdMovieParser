from operator import ge
from urllib.error import HTTPError
import requests
import random
from bs4 import BeautifulSoup
import wget
import shutil
import urllib.request
from PIL import ImageTk, Image




def getMovies():
    i = 1
    x = 1

    y=0

    movies = []
    movieids = []
    genres = ['action','adventure', 'animation', 'comedy', 'crime', 'documentary', 'drama', 'family',
    'fantasy', 'history', 'horror', 'music', 'mystery', 'romance', 'science-fiction', 'thriller', 'tv-movie', 'war', 'western']

    #get username
    username = (input('Type your username: ')).lower()

    #get genre
    inp = input('Choose genre or random or all: ')

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
                #print(movie['data-film-name'])
                movies.append(movie['alt'])
            except KeyError:
                #print(movie['data-film-slug'])
                #movies.append(movie['data-film-slug'][6:][:-1].replace("-"," ").title())
                pass
            i=i+1

        for movie in idresults:
            movieids.append(movie['data-film-id'])
        x += 1

    if(len(movies) != 0):
        print(movies)
    else:
        print("You have no " + inp.title() +  " movies in your watchlist.")

    imagelinks = findImageLinks(movies,movieids)
    return movies, movieids, imagelinks


#find movie poster image links
def findImageLinks(movies, movieids):
    imagelinks = []
    for x in range(len(movies)):
        link = 'https://a.ltrbxd.com/resized/film-poster/'
        for number in movieids[x]:
            link += str(number) + '/'
        link += str(movieids[x])+'-'+movies[x].replace(" ","-").lower()+'-0-460-0-690-crop.jpg'
        imagelinks.append(link)
    return imagelinks


#allimages = {}
#for x in imagelinks:
#    try:
#       allimages["img_" + str(x))] = wget.download(x)
#    except HTTPError:
#        print('not valid link in' + str(x))

#print(*imagelinks, sep = '\n')

#download image to display
def downloadImage(x, imagelinks):
    r = requests.get(imagelinks[x], stream=True)
    if r.status_code == 200:
        with open("img.png", 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
        return 'img.png'
    else:
        print('Error: Could not get image')
        return 0
    





