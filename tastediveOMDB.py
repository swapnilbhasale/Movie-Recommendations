import requests
import json

'''The Tastedive api provides recommendations for movies, music, TV shows etc.
   The follwing function takes a argument *name*, uses the requests module to construct the URL and fetch data from the API.
   The use the API with any erros we need to request a free API key, allowing the application th access the API
   Given a movie input, the API return a list of similar movies, upto value *limit*
'''
def get_movies_from_tastedive(name):
    baseurl = "https://tastedive.com/api/similar"
    params_dict = {}
    params_dict['q']=name
    params_dict['limit']='5'
    params_dict['k']='325880-mashup-N8P5UYAZ'
    tastedive_res = requests.get(baseurl, params= params_dict)
    print(tastedive_res.url)
    data= tastedive_res.json()
    return data

'''The OMDB API take *name* of movie as input and return data for the movie. The data includes Cast, PLot, Ratings etc.
   As above, to access this API we need to register to get a API key.
'''
def get_movie_data(name): #this function returns information about the movie
    baseurl = "http://www.omdbapi.com/"
    params_dict = {}
    params_dict['apikey'] = 'bdaa750c'
    params_dict['t'] = name
    params_dict['r'] = 'json'
    params_dict['type'] = 'movie'
    omdb_res = requests.get(baseurl, params = params_dict)
    print(omdb_res.url)
    data = omdb_res.json()
    return data

'''This fuction takes input from value returned by the OMDB API, to return the rating value from
   Rotten Tomatoes (if available) for a given movie'''
def get_movie_rating(data_dict):
    list_of_rating = data_dict['Ratings']
    for src in data_dict['Ratings']:
        if src['Source'] == 'Rotten Tomatoes':
            return int(src['Value'].rstrip('%'))
    return 0

'''This fuction extracts a list (here length = 5) of movies returned by the Tastedive API
'''
def extract_movie_titles(data):
    extracted_movies = []
    for item in data['Similar']['Results']: #each item is a dictionary with keys 'Name' and 'Type'
        if item['Type'] == 'movie':
            extracted_movies.append(item['Name'])
    return extracted_movies

def get_related_titles(movie_titles_list):
    related_titles = []
    for movie in movie_titles_list:
        data = get_movies_from_tastedive(movie)
        extracted_movies = extract_movie_titles(data)
        for m in extracted_movies:
            if m not in related_titles:
                related_titles.append(m)
    return related_titles

'''This function recommends high rated similar movies to users
'''
def get_sorted_recommendations(movies_list):
    related_titles = get_related_titles(movies_list)
    movie_rating_list = []
    recommendations = []
    for movie in related_titles:
        movie_data_dict = get_movie_data(movie)
        rating = get_movie_rating(movie_data_dict)
        movie_rating_list.append((rating, movie))
    movie_rating_list = sorted(movie_rating_list, reverse=True)
    for item in movie_rating_list:
        recommendations.append(item[1])
    return recommendations
    
    
recommendations = get_sorted_recommendations(['rush hour'])
print(recommendations)



