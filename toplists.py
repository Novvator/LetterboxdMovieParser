from watchlist import getMovies

def setupTopLinks():

    toplinks = ["https://letterboxd.com/dave/list/official-top-250-narrative-feature-films/page/",
                "https://letterboxd.com/andredenervaux/list/youre-not-the-same-person-once-the-film-has/page/",
                "https://letterboxd.com/ellefnning/list/for-when-you-want-to-feel-something/page/",
                "https://letterboxd.com/peterstanley/list/1001-movies-you-must-see-before-you-die/page/"]

    for enum, link in enumerate(toplinks):
        getMovies("default", "def" + str(enum), link)

if __name__=="__main__":
    setupTopLinks()
