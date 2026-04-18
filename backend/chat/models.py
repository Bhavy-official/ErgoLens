from django.db import models


class ChatMessage(models.Model):
    session_id = models.CharField(max_length=64, db_index=True)
    question = models.TextField()
    answer = models.TextField()
    sources = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"[{self.session_id[:8]}] {self.question[:50]}"
