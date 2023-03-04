import requests
from apikeyfile import apikey
# Search for the movie using the Movie Database API
movie_response = requests.get('https://api.themoviedb.org/3/search/movie',
                              params={'api_key': apikey,
                                      'query': 'the matrix'})

# Check if the request was successful
if movie_response.status_code == requests.codes.ok:
    # Parse the JSON response
    movie_data = movie_response.json()

    # Extract the title and release year of the first result
    title = movie_data['results'][0]['title']
    year = movie_data['results'][0]['release_date'].split('-')[0]

    # Search for the title on Netflix using the uNoGS API
    netflix_response = requests.get('https://unogsng.p.rapidapi.com/search',
                                    headers={'X-RapidAPI-Host': 'unogsng.p.rapidapi.com',
                                             'X-RapidAPI-Key': '0f465b3f0amshdaaca5272006633p12f55ajsn607ba5920a7b'},
                                    params={'query': 'The Matrix'})

    # Check if the request was successful
    if netflix_response.status_code == requests.codes.ok:
        # Parse the JSON response
        netflix_data = netflix_response.json()

        # Check if the title is available on Netflix
        if netflix_data['total'] > 0:
            # Print the countries where the title is available
            for result in netflix_data['results']:
                print(result)
        else:
            print(f'{title} is not currently available on Netflix in any country.')
    else:
        # Handle the error
        print('Error:', netflix_response.status_code)
else:
    # Handle the error
    print('Error:', movie_response.status_code)

if __name__=="__main__":
    pass
