from django.urls import path

from .views import BookListView, BookDetailView, BookRecommendationsView

urlpatterns = [
    path("", BookListView.as_view(), name="book-list"),
    path("<int:pk>/", BookDetailView.as_view(), name="book-detail"),
    path("<int:pk>/recommendations/", BookRecommendationsView.as_view(), name="book-recommendations"),
]
