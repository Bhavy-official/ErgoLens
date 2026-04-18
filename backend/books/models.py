from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=500)
    author = models.CharField(max_length=200, default="Unknown")
    rating = models.FloatField(default=0.0)
    num_reviews = models.IntegerField(default=0)
    description = models.TextField(blank=True, default="")
    book_url = models.URLField(max_length=500, unique=True)
    cover_image_url = models.URLField(max_length=500, blank=True, default="")
    price = models.CharField(max_length=20, blank=True, default="")
    availability = models.CharField(max_length=100, blank=True, default="")
    genre = models.CharField(max_length=100, blank=True, default="")
    ai_summary = models.TextField(blank=True, default="")
    ai_genre = models.CharField(max_length=100, blank=True, default="")
    ai_sentiment = models.CharField(max_length=50, blank=True, default="")
    ai_recommendation_text = models.TextField(blank=True, default="")
    insights_generated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
