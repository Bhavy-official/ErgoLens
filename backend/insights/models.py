from django.db import models


class InsightCache(models.Model):
    cache_key = models.CharField(max_length=64, unique=True, db_index=True)
    question = models.TextField()
    answer = models.TextField()
    sources = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Cache: {self.cache_key[:16]}..."
