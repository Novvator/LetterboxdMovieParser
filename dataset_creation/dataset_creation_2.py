# The Movie Database API's limit is fairly generous: you can make up to 40 requests every 10 seconds per IP, 
# according to the TMDB's API documentation as of September 2021. 
# However, as with any API, be sure to check the current terms and rate limits before proceeding. 

# To fetch 1,000,000 movies, you would need to implement pagination. 
# Each page in the TMDB API typically includes 20 movies, so to fetch 1,000,000 movies, you would need to request 50,000 pages.

# Here's an adjusted version of the script that implements pagination:

import requests
import pandas as pd
import time
import json

from apikeyfile import tmdb_api_key

API_KEY = tmdb_api_key
# API_URL = "https://api.themoviedb.org/3/movie/top_rated"
MOVIE_URL = "https://api.themoviedb.org/3/movie/{}"
KEYWORDS_URL = "https://api.themoviedb.org/3/movie/{}/keywords"
MAX_PAGES = 50000  # Change this to the number of pages you want to fetch

def get_movie(api_key, url, movie_id, append_to_response):
    params = {"api_key": api_key, "append_to_response": append_to_response}
    try:
        response = requests.get(url.format(movie_id), params=params)
    except:
        return False
    if response.status_code == 200:
        return response.json()
        time.sleep(0.2)
    else:
        append_to_file('error_movies.csv', "Status Code: " + str(response.status_code) + ", MovieID: " + str(movie_id))
        time.sleep(0.5)
        return False


def get_movie_ids_from_json(json_file):
    with open(json_file, "r", encoding="utf-8-sig") as f:
        data = f.read()
    movies = [json.loads(line)["id"] for line in data.strip().split("\n")]
    return movies

def get_keywords(api_key, url, movie_id):
    params = {"api_key": api_key}
    response = requests.get(url.format(movie_id), params=params)
    return [keyword["name"] for keyword in response.json()["keywords"]]

def append_to_file(file_name, data_to_write):
    with open(file_name, 'a') as file:
    # Write data to the file
        file.write(data_to_write + '\n')

def main():
    data = []
    start_movie = 188701
    movies = get_movie_ids_from_json("movie_ids_05_15_2023.json")
    for idx, curr_movie_id in enumerate(movies[start_movie-1:], start=start_movie):
        # get_movie_start = time.time()
        movie_data = get_movie(API_KEY, MOVIE_URL, curr_movie_id, append_to_response='keywords')
        if movie_data:
            title = movie_data["title"]
            description = movie_data["overview"]
            popularity = movie_data["popularity"]
            vote_average = movie_data["vote_average"]
            try:
                keywords = [keyword["name"] for keyword in movie_data["keywords"]["keywords"]]
            except:
                keywords = ["", ""]
        # print("Time for get movies: ", time.time() - get_movie_start)
        # get_keywords_start = time.time()
        # keywords = get_keywords(API_KEY, KEYWORDS_URL, movie_data["id"])
            data.append({"Movie Title": title, "Description": description, "Keywords": ", ".join(keywords), "Popularity": popularity, "Vote Average": vote_average})
        # print("Time for get keywords: ", time.time() - get_keywords_start)
            if idx % 100 == 0:
            # append_to_file_start = time.time()
                df = pd.DataFrame(data)
                if idx == 100:
                    df.to_csv("dataset_movies_from_json.csv", index=False, encoding="utf-8")
                    data = []
                else:
                    with open("dataset_movies_from_json.csv", "a", newline="", encoding="utf-8") as f:
                        df.to_csv(f, header=False, index=False)
                    data = []
            # print("Time for append to file: ", time.time() - append_to_file_start )
        time.sleep(0.05)


    # Sleep for a short period to avoid hitting the rate limit
    # time.sleep(0.25)

if __name__ == "__main__":
    main()


# This script now fetches movies page by page and sleeps for 0.25 seconds after fetching each page to avoid hitting the rate limit. 
# It continues fetching until it has fetched the number of pages specified by `MAX_PAGES`.

# However, be aware that fetching 1,000,000 movies will take a considerable amount of time and will result in a very large CSV file. 
# It's also important to note that the top_rated endpoint may not contain as many movies as you wish to fetch. 
# You might need to fetch data from different endpoints (such as popular or upcoming) or filter less strictly to reach your target number of movies.