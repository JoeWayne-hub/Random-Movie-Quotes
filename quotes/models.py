from django.db import models

# Movie table — holds info about each movie
class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    release_year = models.IntegerField(null=True, blank=True)
    poster_url = models.URLField(blank=True)

    def __str__(self):
        return self.title

# Quote table — stores quotes linked to a movie
class Quote(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="quotes")
    text = models.TextField()
    character = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'"{self.text[:50]}..." - {self.character}'
