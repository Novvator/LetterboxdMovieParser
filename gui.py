import random
import tkinter as tk
from tmdb import tmbd_poster_from_link
import watchlist
from PIL import ImageTk, Image
import os
from toplists import setupTopLinks
from movie import currentMovie
import threading

class MovieSelectorApp:
    def __init__(self, root):
        self.root = root
        self.buttons = []
        self.setup_ui()
        self.movies = []
        self.movie_ids = []

    def setup_ui(self):
        self.center_window(700, 700)
        self.root.title('Letterboxd Movie Selector')

        self.canvas = tk.Canvas(self.root, height=700, width=700, bg="#809FFF")
        self.canvas.pack()

        self.label = tk.Label(self.canvas, text="Press the button to select a random movie from your list", bg='white')
        self.label.place(relwidth=0.57, relheight=0.03, relx=0.215, rely=0.035)

        self.title_label = tk.Label(self.canvas, text='', bg='white')
        self.title_label.place(relwidth=0.57, relheight=0.03, relx=0.215, rely=0.1)

        self.username = tk.StringVar()
        self.username_entry = tk.Entry(self.canvas, text="Username: ", textvariable=self.username)
        self.username_entry.place(relwidth=0.57, relheight=0.05, relx=0.215, rely=0.83)

        self.genre = tk.StringVar()
        self.genre_entry = tk.Entry(self.canvas, text="Genre: ", textvariable=self.genre)
        self.genre_entry.place(relwidth=0.57, relheight=0.05, relx=0.215, rely=0.88)

        download_button = tk.Button(self.canvas, bg='gray', fg='black', text="Download Top Lists", command=self.threaded_function(setupTopLinks))
        download_button.place(relwidth=0.18, relheight=0.03, relx=0.035, rely=0.95)
        self.buttons.append(download_button)

        delete_button = tk.Button(self.canvas, bg='gray', fg='black', text="Delete Cached Movies", command=self.threaded_function(self.delete_cached_movies))
        delete_button.place(relwidth=0.18, relheight=0.03, relx=0.78, rely=0.95)
        self.buttons.append(delete_button)

        movie_time_button = tk.Button(self.canvas, bg='gray', fg='black', text="Movie time!", command=self.threaded_function(self.get_movies))
        movie_time_button.place(relwidth=0.2, relheight=0.03, relx=0.53, rely=0.95)
        self.buttons.append(movie_time_button)

        movie_time_scores_button = tk.Button(self.canvas, bg='gray', fg='black', text="Movie Time Scores!", command=self.threaded_function(self.get_movies_with_score))
        movie_time_scores_button.place(relwidth=0.2, relheight=0.03, relx=0.27, rely=0.95)
        self.buttons.append(movie_time_scores_button)

        self.setup_image_label()

    def center_window(self, width=700, height=700):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.root.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

    def setup_image_label(self):
        try:
            img = Image.open('img.png')
            img = ImageTk.PhotoImage(img)
            self.img_label = tk.Label(self.canvas, image=img, anchor='center')
        except FileNotFoundError:
            print('Image file not found')
            self.img_label = tk.Label(self.canvas, text='', anchor='center')
        self.img_label.place(relwidth=0.7, relheight=0.6, relx=0.15, rely=0.15)

    def threaded_function(self, func):
        def wrapper():
            self.disable_buttons()
            thread = threading.Thread(target=func)
            thread.start()
            self.root.after(100, self.check_thread, thread)
        return wrapper

    def check_thread(self, thread):
        if thread.is_alive():
            self.root.after(100, self.check_thread, thread)
        else:
            self.enable_buttons()

    def disable_buttons(self):
        for button in self.buttons:
            button.config(state=tk.DISABLED)

    def enable_buttons(self):
        for button in self.buttons:
            button.config(state=tk.NORMAL)

    def get_movies(self):
        movies = watchlist.getMovies(self.username.get(), self.genre.get())
        self.choose_movie(movies)

    def get_movies_with_score(self):
        movies = watchlist.getMovies(self.username.get(), self.genre.get())
        movie_list = list(movies)
        default_lists = [watchlist.getMovies('default', f'def{i}') for i in range(4)]
        scores = self.calculate_score(movie_list, *default_lists)
        self.choose_movie_from_scores(scores, movies)

    def choose_movie(self, movies):
        movie_list = list(movies)
        chosen_movie = random.choice(movie_list)
        currentMovie.title = chosen_movie
        currentMovie.setupLinks(movies[currentMovie.title])
        self.update_movie_display(currentMovie.title, currentMovie.tmdblink)

    def calculate_score(self, watchlist, *default_lists):
        scores = {}
        lists_set = [set(lst) for lst in default_lists]
        for film in set(watchlist):
            score = sum(film in lst for lst in lists_set)
            scores[film] = score
        sorted_scores = dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))
        print(sorted_scores)
        return sorted_scores

    def choose_movie_from_scores(self, scores, movies):
        max_score = max(scores.values())
        films_with_max_score = [film for film, score in scores.items() if score == max_score]
        chosen_movie = random.choice(films_with_max_score)
        currentMovie.title = chosen_movie
        currentMovie.setupLinks(movies[currentMovie.title])
        self.update_movie_display(currentMovie.title, currentMovie.tmdblink)

    def update_movie_display(self, title, tmdblink):
        print('chosen movie is:', title)
        self.title_label['text'] = title
        tmbd_poster_from_link(tmdblink)
        self.replace_image()

    def delete_cached_movies(self):
        pickle_filename = "cachedmovies.pkl"
        if os.path.exists(pickle_filename):
            os.remove(pickle_filename)
            print("Pickle file deleted successfully!")
        else:
            print("Pickle file does not exist.")

    def replace_image(self):
        try:
            img2 = ImageTk.PhotoImage(Image.open("img.png"))
            self.img_label.configure(image=img2)
            self.img_label.image = img2
        except FileNotFoundError:
            print("Image file not found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieSelectorApp(root)
    root.mainloop()

    try:
        os.remove("img.png")
    except FileNotFoundError:
        print('img.png file does not exist')
