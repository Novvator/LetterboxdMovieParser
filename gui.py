import random
import tkinter as tk
import watchlist
from PIL import ImageTk, Image
import os


username = 'andrewgunner'
genre = 'random'

ran = 2
movies = []
movieids = []
title = ''



def do():
  print('okay')

def getMovies():
  movies = watchlist.getMovies(username.get(), genre.get())
  chooseMovie(movies)


def chooseMovie(movies):
  ran = random.randint(0,len(movies)-1)
  print('chosen movie is: ' + movies[ran])
  titlelabel['text'] = movies[ran]
  # if images work:
  # watchlist.downloadImage(watchlist.findImage(movies[ran]))
  # replaceImage()

  return ran

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
button.place(relwidth=0.2, relheight=0.03, relx=0.4, rely=0.95)

#imglabel
# try:
#   img = Image.open('img.png')
#   img = ImageTk.PhotoImage(img)
# imgLabel = tk.Label(canvas, image = img, anchor= 'center')
imgLabel = tk.Label(canvas, anchor= 'center')
imgLabel.place(relwidth=0.7, relheight=0.6, relx=0.15, rely=0.15)
# except FileNotFoundError:
#   print('Image file not found')
#   imgLabel = tk.Label(canvas, text = "" ,anchor= 'center')
#   imgLabel.place(relwidth=0.7, relheight=0.6, relx=0.15, rely=0.15)



root.bind("<Return>", replaceImage)
root.mainloop()

# with images working
# try:
#   os.remove("img.png")
# except FileNotFoundError:
#   print('img.png file does not exist')