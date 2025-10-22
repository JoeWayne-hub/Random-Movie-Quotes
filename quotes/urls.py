from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  
    path('movies/', views.movie_list, name='movie_list'), 
    path('movies/<str:movie_id>/', views.movie_detail, name='movie_detail'),
    path('search/', views.search_movie, name='search_movie'), 
]
