import re
from bs4 import BeautifulSoup
import requests
import pprint

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
