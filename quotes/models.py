from django.db import models
import requests

class MovieQuote(models.Model):
    movie_title = models.CharField(max_length=200)
    imdb_id = models.CharField(max_length=20)
    quote_text = models.TextField()
    character = models.CharField(max_length=100, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)  
    submitted_by = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        if not self.imdb_id:
            api_key = "20aec232"
            url = f"http://www.omdbapi.com/?t={self.movie_title}&apikey={api_key}"
            response = requests.get(url)
            data = response.json()
            if data.get("imdbID"):
                self.imdb_id = data["imdbID"]
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.movie_title} - "{self.quote_text[:40]}..."'
