# Letterboxd Movie Parser

## Overview

Letterboxd Movie Parser is a Python application that allows users to select a random movie from their Letterboxd watchlist based on specified genres. It uses the Tkinter library for the graphical user interface (GUI) and various other libraries to fetch and display movie data.

## Features

- Select a random movie from a user's Letterboxd watchlist.
- Filter movies by genre.
- Display movie posters using TMDB links.
- Cache movie data to improve performance.
- Delete cached movie data.
- Display movies based on scores calculated from multiple predefined lists.

## Requirements

- Python 3.7+
- Required Python packages:
  - `requests`
  - `beautifulsoup4`
  - `Pillow`
  - `wget`
  - `tkinter` (part of the standard library)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/letterboxd-movie-selector.git
    cd letterboxd-movie-selector
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the application:
    ```sh
    python gui.py
    ```

2. In the GUI:
   - Enter your Letterboxd username.
   - Enter a genre (or "random" for a random genre, or "all" for all genres).
   - Click "Movie time!" to select a random movie.
   - Click "Movie Time Scores!" to select a movie based on scores from predefined lists.
   - Click "Download Top Lists" to download predefined top lists.
   - Click "Delete Cached Movies" to delete cached watchlist data.