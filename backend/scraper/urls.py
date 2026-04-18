from django.urls import path

from .views import ScrapeView

urlpatterns = [
    path("", ScrapeView.as_view(), name="scrape"),
]
