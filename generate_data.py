import re
from bs4 import BeautifulSoup
import requests
import pprint


def find_number_of_films_by_genre(username=None):
    numbers = {}
    genres = ['action','adventure', 'animation', 'comedy', 'crime', 'documentary', 'drama', 'family',
        'fantasy', 'history', 'horror', 'music', 'mystery', 'romance', 'science-fiction', 'thriller', 'tv-movie', 'war', 'western']
    username = 'vaflacko'


    for genre in genres:
        # Use beautiful soup to go to page
        url = 'https://letterboxd.com/'+ username + '/films/genre/' + genre
        page = requests.get(url)
        soup = BeautifulSoup(page.content,features="html.parser")
        element = soup.find("p", {"class" : "ui-block-heading"}).text

        # Use regular expression to extract number of watched movies
        match = re.search(r'(?<=watched\s)\d+', element)
        if match:
            number = int(match.group())
            print(number)
            numbers[genre] = number
        else:
            print("No match found")
    pprint.pprint(numbers)
    return numbers

def generateLink(URL, x):
    return str(URL) + str(x)

def find_watchlist(username=None):
    username = 'vaflacko'
    x = 1
    watchlist = []
    movieresults = []
    url = 'https://letterboxd.com/' + username + '/watchlist/page/'

    while(True):
    
    # generate link and parse with soup
        link = generateLink(url, x)
        page = requests.get(link)
        soup = BeautifulSoup(page.content,features="html.parser")

        # find movies element
        currmovieresults = soup.find_all("img", {"class" : "image"})
        movieresults += currmovieresults

        # if there is next page button continue loop
        next_button = soup.find("a", {"class":"next"})
        if not next_button:
            break

        x += 1
    
    for element in movieresults:
        watchlist.append(element['alt'])
    print(watchlist)
    return watchlist

def find_watched_list(username=None):
    username = 'vaflacko'
    x = 1
    watched_list = []
    movieresults = []
    url = 'https://letterboxd.com/' + username + '/films/page/'

    while(True):
    
    # generate link and parse with soup
        link = generateLink(url, x)
        page = requests.get(link)
        # with open('output.html', 'a', encoding='utf-8') as file:
        #     file.write(page.text)
        #     file.close()
        soup = BeautifulSoup(page.content,features="html.parser")

        # find movies element
        currmovieresults = soup.find_all("img", {"class" : "image"})
        movieresults += currmovieresults

        # if there is next page button continue loop
        next_button = soup.find("a", {"class":"next"})
        if not next_button:
            break

        x += 1
    
    for element in movieresults:
        watched_list.append(element['alt'])
    print(watched_list)
    print(len(watched_list))
    return watched_list

if __name__=="__main__":
    find_watched_list()