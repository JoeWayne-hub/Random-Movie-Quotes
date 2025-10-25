from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('movies/', views.movie_list, name='movie_list'),
    path('movies/<str:imdb_id>/', views.movie_detail, name='movie_detail'),
    path('search/', views.search_movie, name='search_movie'),
    path('search_quote/', views.search_quote, name='search_quote'),
    path('suggest/<str:imdb_id>/', views.suggest_quote, name='suggest_quote'),

]

