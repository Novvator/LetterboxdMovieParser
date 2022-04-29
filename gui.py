import random
import tkinter as tk
import watchlist
from PIL import ImageTk, Image
import os

#get movies and links
movies, movieids, imagelinks = watchlist.getMovies()

def chooseMovie():
  print ('length of movies = ', len(movies))
  print ('length of moviesids = ', len(movieids))
  print ('length of imagelinks = ', len(imagelinks))
  ran = random.randint(0,len(movies)-1)
  print ('random int = ', ran)
  return ran

ran = chooseMovie()

watchlist.downloadImage(ran,imagelinks)

print("chosen movie is: ", movies[ran])
print(imagelinks[ran])



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

#open file and export movies to a listt
    

root = tk.Tk()
center_window(700, 700)

root.title('Movie Selector')

canvas = tk.Canvas(root, height=700, width=700, bg="#809FFF")
canvas.pack()


    
label = tk.Label(canvas, text = "Press the button to select a random movie from the list", bg='white')
label.place(relwidth=0.57, relheight=0.03, relx=0.215, rely=0.035)

try:
  img = Image.open('img.png')
  img = ImageTk.PhotoImage(img)
  imgLabel = tk.Label(canvas, image = img, anchor= 'center')
  imgLabel.place(relwidth=0.7, relheight=0.7, relx=0.15, rely=0.1)
except FileNotFoundError:
  print('Image file not found')
  imgLabel = tk.Label(canvas, text = "Photo not found" ,anchor= 'center')
  imgLabel.place(relwidth=0.7, relheight=0.7, relx=0.15, rely=0.1)


label1 = tk.Label(canvas, text = "", bg="#809FFF")
label1.place(relwidth=0.7, relheight=0.03, relx=0.15, rely=0.815)

button = tk.Button(canvas, bg='gray', fg='red', text="Movie time!", command= chooseMovie)
button.place(relwidth=0.2, relheight=0.05, relx=0.4, rely=0.86)



root.mainloop()

os.remove("img.png")