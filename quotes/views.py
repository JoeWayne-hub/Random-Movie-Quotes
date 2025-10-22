from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie, Quote
import random
import requests


# Home Page - Shows random quotes
def home(request):
    quotes = list(Quote.objects.all())
    random_quote = random.choice(quotes) if quotes else None
    return render(request, 'quotes/home.html', {'random_quote': random_quote})


# Movie List - Shows all movies
def movie_list(request):
    search_query = request.GET.get('search', '')
    movies = []

    if search_query:
        api_key = "20aec232"
        url = f"http://www.omdbapi.com/?s={search_query}&apikey={api_key}"
        response = requests.get(url)
        data = response.json()
        print(data)  

        if data.get("Search"):
            for item in data["Search"]:
                movies.append({
                    "id": item["imdbID"], 
                    "title": item["Title"],
                    "year": item["Year"],
                    "poster": item["Poster"],
                    "type": item["Type"],
                })

    return render(request, 'quotes/movie_list.html', {
        'movies': movies,
        'search_query': search_query
    })


# Movie Detail - Shows quotes for one movie
def movie_detail(request, movie_id):
    api_key = "20aec232"
    url = f"http://www.omdbapi.com/?i={movie_id}&apikey={api_key}"
    response = requests.get(url)
    movie = response.json()
    return render(request, 'quotes/movie_detail.html', {'movie': movie})


# Search Function - Uses OMDB API
def search_movie(request):
    query = request.GET.get('q')  
    results = []

    if query:
        api_key = "20aec232"  
        url = f"http://www.omdbapi.com/?s={query}&apikey=20aec232"
        response = requests.get(url)
        data = response.json()
        print(data)


        if data.get("Search"):
            for item in data["Search"]:
                results.append({
                    "title": item.get("Title"),
                    "year": item.get("Year"),
                    "poster": item.get("Poster"),
                    "type": item.get("Type"),
                })

    return render(request, 'quotes/search.html', {'results': results, 'query': query})