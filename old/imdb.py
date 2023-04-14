import requests
import urllib
import os



CONFIG_PATTERN = 'http://api.themoviedb.org/3/configuration?api_key={key}'
IMG_PATTERN = 'http://api.themoviedb.org/3/movie/{imdbid}/images?api_key={key}' 
KEY = '70a0207fb286f95fb40238e3910d0f0e'
            
def _get_json(url):
    r = requests.get(url)
    return r.json()
    
# def _download_images(urls, path='.'):
#     """download all images in list 'urls' to 'path' """

#     for nr, url in enumerate(urls):
#         r = requests.get(url)
#         filetype = r.headers['content-type'].split('/')[-1]
#         filename = 'poster_{0}.{1}'.format(nr+1,filetype)
#         filepath = os.path.join(path, filename)
#         with open(filepath,'wb') as w:
#             w.write(r.content)

    
def _download_image(url, path='.'):
    """download image of url to 'path' """

    r = requests.get(url)
    filetype = r.headers['content-type'].split('/')[-1]
    filename = '0.' + filetype
    filepath = os.path.join(path, filename)
    with open(filepath,'wb') as w:
        w.write(r.content)

def get_poster_url(imdbid):
    #size
    """ return image urls of posters for IMDB id
        returns all poster images from 'themoviedb.org'. Uses the
        maximum available size. 
        Args:
            imdbid (str): IMDB id of the movie
        Returns:
            list: list of urls to the images
    """
    config = _get_json(CONFIG_PATTERN.format(key=KEY))
    base_url = config['images']['base_url']
    sizes = config['images']['poster_sizes']

    """
        'sizes' should be sorted in ascending order, so
            max_size = sizes[-1]
        should get the largest size as well.        
    """
    def size_str_to_int(x):
        return float("inf") if x == 'original' else int(x[1:])
    max_size = max(sizes, key=size_str_to_int)

    poster = _get_json(IMG_PATTERN.format(key=KEY,imdbid=imdbid))['posters'][0]
    # poster_urls = []
    # for poster in posters:
    rel_path = poster['file_path']
    poster_url = "{0}{1}{2}".format(base_url, max_size, rel_path)


    return poster_url

def imdb_id_from_title(title):
    """ return IMDB id for search string

        Args::
            title (str): the movie title search string

        Returns: 
            str. IMDB id, e.g., 'tt0095016' 
            None. If no match was found

    """
    pattern = 'http://www.imdb.com/xml/find?json=1&nr=1&tt=on&q={movie_title}'
    url = pattern.format(movie_title=urllib.parse.urlparse(title))
    r = requests.get(url)
    res = r.json()
    # sections in descending order or preference
    for section in ['popular','exact','substring']:
        key = 'title_' + section 
        if key in res:
            return res[key][0]['id']

def tmdb_posters(title, count=None, outpath='.'):
    imdbid = 'tt0095016'
    url = get_poster_url(imdbid)
    _download_image(url, outpath)

if __name__=="__main__":
    # tmdb_posters('tt0095016')
    tmdb_posters(imdb_id_from_title('Red'))