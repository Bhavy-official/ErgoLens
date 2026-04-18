from django.urls import path

from .views import InsightGenerateView

urlpatterns = [
    path("generate/", InsightGenerateView.as_view(), name="insight-generate"),
]
