import re
from bs4 import BeautifulSoup
import requests
import pprint


def find_number_of_films_by_genre(username=None):
    if not username:
        username = 'vaflacko'
    numbers = {}
    genres = ['action','adventure', 'animation', 'comedy', 'crime', 'documentary', 'drama', 'family',
        'fantasy', 'history', 'horror', 'music', 'mystery', 'romance', 'science-fiction', 'thriller', 'tv-movie', 'war', 'western']
    

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
    if not username:
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
    if not username:
        username = 'vaflacko'
    x = 1
    # watched_list = []
    # movieresults = []
    movies_with_ratings = {}
    has_rating = True
    url = 'https://letterboxd.com/' + username + '/films/by/entry-rating/page/'
    # url = 'https://letterboxd.com/' + username + '/films/page/'

    while(True):
    
    # generate link and parse with soup
        link = generateLink(url, x)
        page = requests.get(link)
        soup = BeautifulSoup(page.content,features="html.parser")

        # find movies li element
        movies_li_elements = soup.find_all('li', {"class" : "poster-container"})
        for li_element in movies_li_elements:
            movie_name = li_element.find('img')['alt']
            if has_rating:
                try:
                    rating_span = li_element.find('span', class_='rating')
                    rating_class = rating_span['class']  # Get the list of classes
                    rating_value = rating_class[-1].replace('rated-', '')  # Extract the rating value from the last class
                    movies_with_ratings[movie_name] = int(rating_value)
                except:
                    has_rating = False

            else:
                movies_with_ratings[movie_name] = 'No Rating'

        # # find movies element
        # currmovieresults = soup.find_all("img", {"class" : "image"})
        # movieresults += currmovieresults

        # if there is next page button continue loop
        next_button = soup.find("a", {"class":"next"})
        if not next_button:
            break

        x += 1
    
    # for element in movieresults:
    #     watched_list.append(element['alt'])
    print(movies_with_ratings)
    print(len(movies_with_ratings))
    return movies_with_ratings

if __name__=="__main__":
    list1 = find_watched_list('schaffrillas')