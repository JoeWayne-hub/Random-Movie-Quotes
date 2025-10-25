from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import MovieQuote
import random
import requests
from .forms import MovieQuoteForm


# Home Page - Shows random quotes
def home(request):
    # Get unique movies that have at least one quote
    movies_with_quotes = MovieQuote.objects.values('movie_title', 'imdb_id').distinct()

    # Prepare movie data list
    movie_data = []
    api_key = "20aec232"

    for movie in movies_with_quotes:
        imdb_id = movie['imdb_id']

        # Fetch movie details from OMDb to get poster
        url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={api_key}"
        response = requests.get(url)
        data = response.json()

        # Get random quote for the movie
        quotes = MovieQuote.objects.filter(movie_title=movie['movie_title'])
        if quotes.exists():
            random_quote = random.choice(list(quotes))
            movie_data.append({
                'movie_title': movie['movie_title'],
                'imdb_id': imdb_id,
                'poster': data.get('Poster', ''),
                'year': data.get('Year', ''),
                'quote_text': random_quote.quote_text,
                'character': random_quote.character,
            })

    return render(request, 'quotes/home.html', {'movie_data': movie_data})



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
# quotes/views.py
from django.shortcuts import render, get_object_or_404
from .models import MovieQuote
from .forms import MovieQuoteForm
import requests

def movie_detail(request, imdb_id):
    # Initialize the form early to avoid UnboundLocalError
    form = MovieQuoteForm()

    # Get all quotes for this movie
    quotes = MovieQuote.objects.filter(imdb_id=imdb_id, approved=True)

    # Fetch movie details from OMDB API
    api_key = "20aec232"
    url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={api_key}"
    response = requests.get(url)
    movie = response.json()

    # If someone submits a quote for this movie
    if request.method == "POST":
        form = MovieQuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.imdb_id = imdb_id
            quote.movie_title = movie.get("Title", "")
            quote.save()
            form = MovieQuoteForm()

    # Render the movie page with quotes and the quote form
    return render(request, "quotes/movie_detail.html", {
        "movie": movie,
        "quotes": quotes,
        "form": form
    })


# Search Function - Uses OMDB API
def search_movie(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        api_key = "20aec232"  # OMDb API key
        url = f"http://www.omdbapi.com/?s={query}&apikey={api_key}"
        response = requests.get(url)
        data = response.json()

        if data.get("Search"):
            for item in data["Search"]:
                results.append({
                    "imdb_id": item["imdbID"],
                    "title": item["Title"],
                    "year": item["Year"],
                    "poster": item["Poster"],
                })

    return render(request, 'quotes/search.html', {'results': results, 'query': query})


# Search for quotes by movie title
def search_quote(request):
    query = request.GET.get('q', '')
    movies_with_quotes = []

    if query:
        # Get all matching quotes
        quotes = MovieQuote.objects.filter(movie_title__icontains=query, approved=True)

        # Group quotes by movie (using IMDb ID)
        grouped = {}
        for quote in quotes:
            if quote.imdb_id not in grouped:
                grouped[quote.imdb_id] = {
                    'title': quote.movie_title,
                    'imdb_id': quote.imdb_id,
                    'quotes': []
                }
            grouped[quote.imdb_id]['quotes'].append(quote)

        # Fetch movie posters via OMDB
        api_key = "20aec232"
        for imdb_id, data in grouped.items():
            url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={api_key}"
            response = requests.get(url)
            movie_data = response.json()
            data['poster'] = movie_data.get('Poster', '')
            data['year'] = movie_data.get('Year', '')
            movies_with_quotes.append(data)

    return render(request, 'quotes/search_quote.html', {'movies_with_quotes': movies_with_quotes, 'query': query})

def suggest_quote(request, imdb_id):
    api_key = "20aec232"
    url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={api_key}"
    response = requests.get(url)
    movie = response.json()

    if request.method == 'POST':
        form = QuoteSuggestionForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.movie_title = movie['Title']
            quote.imdb_id = imdb_id
            quote.approved = False  # stays hidden until admin approves
            quote.save()
            return render(request, 'quotes/success.html', {'movie': movie})

    else:
        form = QuoteSuggestionForm()

    return render(request, 'quotes/suggest_quote.html', {
        'movie': movie,
        'form': form
    })
