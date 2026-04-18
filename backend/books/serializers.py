from rest_framework import serializers

from .models import Book


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "rating",
            "genre",
            "ai_genre",
            "price",
            "cover_image_url",
            "insights_generated",
        ]


class BookDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"
