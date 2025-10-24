from django.contrib import admin
from .models import MovieQuote

@admin.register(MovieQuote)
class MovieQuoteAdmin(admin.ModelAdmin):
    list_display = ('movie_title', 'character', 'quote_text', 'imdb_id', 'added_at')
    search_fields = ('movie_title', 'quote_text', 'character')
    list_filter = ('added_at',)
