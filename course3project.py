"""
This project will take you through the process of mashing up data from two different APIs to make movie recommendations. The TasteDive API lets you provide a movie (or bands, TV shows, etc.) as a query input, and returns a set of related items. The OMDB API lets you provide a movie title as a query input and get back data about the movie, including scores from various review sites (Rotten Tomatoes, IMDB, etc.).

You will put those two together. You will use TasteDive to get related movies for a whole list of titles. You’ll combine the resulting lists of related movies, and sort them according to their Rotten Tomatoes scores (which will require making API calls to the OMDB API.)

To avoid problems with rate limits and site accessibility, we have provided a cache file with results for all the queries you need to make to both OMDB and TasteDive. Just use requests_with_caching.get() rather than requests.get(). If you’re having trouble, you may not be formatting your queries properly, or you may not be asking for data that exists in our cache. We will try to provide as much information as we can to help guide you to form queries for which data exists in the cache.

Your first task will be to fetch data from TasteDive. The documentation for the API is at https://tastedive.com/read/api.
"""
import requests_with_caching
import json

def get_movies_from_tastedive(name):
    d={}
    d['q']=name
    d['limit']='5'
    d['type']='movies'
    res=requests_with_caching.get("https://tastedive.com/api/similar",params=d).json()
    return res
    
"""
Please copy the completed function from above into this active code window. Next, you will need to write a function that extracts just the list of movie titles from a dictionary returned by get_movies_from_tastedive. Call it extract_movie_titles.
"""
def extract_movie_titles(dic):
    l=[i['Name'] for i in dic['Similar']['Results']]
    return l

"""
Please copy the completed functions from the two code windows above into this active code window. Next, you’ll write a function, called get_related_titles. It takes a list of movie titles as input. It gets five related movies for each from TasteDive, extracts the titles for all of them, and combines them all into a single list. Don’t include the same movie twice.
"""

def get_related_titles(lst):
    l2=[]
    for i in lst:
        l1= extract_movie_titles(get_movies_from_tastedive(i))
        l2+=[i for i in l1 if i not in l2]
    return l2

"""
Define a function called get_movie_data. It takes in one parameter which is a string that should represent the title of a movie you want to search. The function should return a dictionary with information about that movie.
"""
def get_movie_data(name):
    d={}
    d['t']=name
    d['r']='json'
    res=requests_with_caching.get("http://www.omdbapi.com/",params=d).json()
    return res

"""
Please copy the completed function from above into this active code window. Now write a function called get_movie_rating. It takes an OMDB dictionary result for one movie and extracts the Rotten Tomatoes rating as an integer. For example, if given the OMDB dictionary for “Black Panther”, it would return 97. If there is no Rotten Tomatoes rating, return 0.
"""
def get_movie_rating(d):
    rating=0
    for i in d['Ratings']:
        if i['Source']=='Rotten Tomatoes':
            rating=int(i['Value'][:-1])
            print(rating)
    return rating

"""
Now, you’ll put it all together. Don’t forget to copy all of the functions that you have previously defined into this code window. Define a function get_sorted_recommendations. It takes a list of movie titles as an input. It returns a sorted list of related movie titles as output, up to five related movies for each input movie title. The movies should be sorted in descending order by their Rotten Tomatoes rating, as returned by the get_movie_rating function. Break ties in reverse alphabetic order, so that ‘Yahşi Batı’ comes before ‘Eyyvah Eyvah’.
"""
def get_sorted_recommendations(lst):
    l=get_related_titles(lst)
    l2=list(sorted(l,key=lambda x:(get_movie_rating(get_movie_data(x)),x),reverse=True ))
    return l2 

    # some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
# get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"])
