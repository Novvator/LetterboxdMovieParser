import random
import tkinter as tk

from bs4 import BeautifulSoup
import requests
from tmdb import tmbd_poster_from_link
import watchlist
from PIL import ImageTk, Image
import os
from imdb1 import tmdb_poster
from toplists import setupTopLinks

username = 'andrewgunner'
genre = 'random'

ran = 2
movies = []
movieids = []
title = ''

#--------------------------------------------------------
#IT NOW WORKS ONLY THE FIRST TIME - TODO FIX CREATECSVCACHE WITH PICKLE

def do():
  print('okay')

def getMovies():
  movies = watchlist.getMovies(username.get(), genre.get())
  chooseMovie(movies)


def getMoviesWithScore():
  movies = watchlist.getMovies(username.get(), genre.get())
  movieslist = list(movies)
  list1 = watchlist.getMovies('default', 'def0')
  list2 = watchlist.getMovies('default', 'def1')
  list3 = watchlist.getMovies('default', 'def2')
  list4 = watchlist.getMovies('default', 'def3')
  scores = calculate_score(movieslist, list1, list2, list3, list4)
  chooseMovieFromScores(scores, movies)

def chooseMovie(movies):
  movieslist = list(movies)
  ran = random.randint(0,len(movieslist)-1)
  chosen = movieslist[ran]
  print('chosen movie is: ' + chosen)
  titlelabel['text'] = movieslist[ran]
  # if images work:
  # watchlist.downloadImage(watchlist.findImage(movies[ran]))
  tmbd_poster_from_link(get_tmdb_link(movies[chosen]))
  replaceImage()

  return ran


def calculate_score(watchlist, list1, list2, list3, list4):
    scores = {}
    lists_set = [set(list1), set(list2), set(list3), set(list4)]
    for film in set(watchlist):
        score = 0
        for lst in lists_set:
            if film in lst:
                score += 1
        scores[film] = score
    sorted_scores = dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))
    print(sorted_scores)
    return sorted_scores


def chooseMovieFromScores(scores, movies):
    max_score = max(scores.values())
    films_with_max_score = [film for film, score in scores.items() if score == max_score]
    chosen = random.choice(films_with_max_score)
    print('chosen movie is: ' + chosen)
    titlelabel['text'] = chosen
    tmbd_poster_from_link(get_tmdb_link(movies[chosen]))
    replaceImage()
    return 

def get_tmdb_link(chosen_movie_link):
    url = 'http://letterboxd.com' + chosen_movie_link
    page = requests.get(url)
    soup = BeautifulSoup(page.content,features="html.parser")
    tmdb_element = soup.find("a", {"data-track-action": "TMDb"})
    tmdb_link = tmdb_element['href']
    return tmdb_link

def replaceImage():
  img2 = ImageTk.PhotoImage(Image.open("img.png"))
  imgLabel.configure(image = img2)
  imgLabel.image = img2




#User Interface
def changeText(self,textt):
    self.configure(text =textt)
        
def center_window(width=700, height=700):
    # get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))

list1 = []
    
try:
  open("D:\\Users\\SenpaiOrigin\\Documents\\LetterboxdMovieParser\\cachedmovies.csv",'x')
except:
  pass

root = tk.Tk()
center_window(700, 700)


root.title('Letterboxd Movie Selector')

canvas = tk.Canvas(root, height=700, width=700, bg="#809FFF")
canvas.pack()


    
label = tk.Label(canvas, text = "Press the button to select a random movie from your list", bg='white')
label.place(relwidth=0.57, relheight=0.03, relx=0.215, rely=0.035)

titlelabel = tk.Label(canvas, text = title, bg='white')
titlelabel.place(relwidth=0.57, relheight=0.03, relx=0.215, rely=0.1)


username = tk.StringVar()
usernamelabel = tk.Entry(canvas , text = "Username: ", textvariable=username)
usernamelabel.place(relwidth=0.57, relheight=0.05, relx=0.215, rely=0.83)

genre = tk.StringVar()
genrelabel = tk.Entry(canvas , text = "Genre: ", textvariable=genre)
genrelabel.place(relwidth=0.57, relheight=0.05, relx=0.215, rely=0.88)

button = tk.Button(canvas, bg='gray', fg='black', text="Movie time!", command= getMovies)
button.place(relwidth=0.2, relheight=0.03, relx=0.6, rely=0.95)

button = tk.Button(canvas, bg='gray', fg='black', text="Movie Time Scores!", command= getMoviesWithScore)
button.place(relwidth=0.2, relheight=0.03, relx=0.2, rely=0.95)

#imglabel
try:
  img = Image.open('img.png')
  img = ImageTk.PhotoImage(img)
  imgLabel = tk.Label(canvas, image = img, anchor= 'center')
  imgLabel = tk.Label(canvas, anchor= 'center')
  imgLabel.place(relwidth=0.7, relheight=0.6, relx=0.15, rely=0.15)
except FileNotFoundError:
  print('Image file not found')
  imgLabel = tk.Label(canvas, text = "" ,anchor= 'center')
  imgLabel.place(relwidth=0.7, relheight=0.6, relx=0.15, rely=0.15)



root.bind("<Return>", replaceImage)
root.mainloop()

# with images working
try:
  os.remove("img.png")
except FileNotFoundError:
  print('img.png file does not exist')