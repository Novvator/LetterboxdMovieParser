from bs4 import BeautifulSoup
import requests


class Movie:
    def __init__(self, title, link):
        self.title = title
        self.link = link
        self.tmdblink = link
    
    def setupLinks(self, link):
    # def get_tmdb_link(chosen_movie_link):
        self.link = link
        url = 'http://letterboxd.com' + '/film/' + self.link
        page = requests.get(url)
        soup = BeautifulSoup(page.content,features="html.parser")
        tmdb_element = soup.find("a", {"data-track-action": "TMDb"})
        self.tmdblink = tmdb_element['href']

currentMovie = Movie("", "")