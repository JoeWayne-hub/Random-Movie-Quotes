from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the Movie Quotes App!")

def movie_list(request):
    return HttpResponse("Here’s a list of all movies and their famous quotes.")

def movie_detail(request, movie_id):
    return HttpResponse(f"This is movie number {movie_id}.")

