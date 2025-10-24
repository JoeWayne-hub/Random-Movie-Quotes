from django import forms
from .models import MovieQuote

class MovieQuoteForm(forms.ModelForm):
    class Meta:
        model = MovieQuote
        fields = ['movie_title', 'quote_text', 'character']
        labels = {
            'movie_title': 'Movie Title',
            'quote_text': 'Add a Quote',
            'character': 'Who said it?',
        }
# New form for public submissions
class QuoteSuggestionForm(forms.ModelForm):
    class Meta:
        model = MovieQuote
        fields = ['quote_text', 'character', 'submitted_by']
        labels = {
            'quote_text': 'Your Suggested Quote',
            'character': 'Who said it?',
            'submitted_by': 'Your Name (optional)',
        }