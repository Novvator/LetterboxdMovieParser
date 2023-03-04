import requests
import re

# Set up the API endpoint and parameters
def tmbd_poster_from_link(tmdb_url):
    tmdb_url = 'https://www.themoviedb.org/movie/659/'
    api_key = '70a0207fb286f95fb40238e3910d0f0e'
    pattern = r'/movie/(\d+)/?$'  # Regex pattern to extract the movie ID
    movie_id = re.search(pattern, tmdb_url).group(1)
    url = f'https://api.themoviedb.org/3/movie/{movie_id}'
    params = {'api_key': api_key}

    # Send the API request and parse the response
    response = requests.get(url, params=params)
    if response.status_code == requests.codes.ok:
        data = response.json()

        # Extract the poster path and build the full URL
        poster_path = data['poster_path']
        base_url = 'https://image.tmdb.org/t/p/'
        poster_size = 'w185'  # Example size, you can use other sizes as well
        # base_url = data['images']['base_url']
        # poster_sizes = data['images']['poster_sizes']
        # wanted_size = poster_sizes[2]
        poster_url = f'{base_url}{poster_size}{poster_path}'

        # Download the image and save it to a file0
        response = requests.get(poster_url)
        if response.status_code == requests.codes.ok:
            with open('movie_poster.jpg', 'wb') as f:
                f.write(response.content)
    else:
        print('Error:', response.status_code)

if __name__=="__main__":
    tmbd_poster_from_link('')
