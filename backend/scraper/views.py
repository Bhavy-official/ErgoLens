import threading

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers

from .scraper import BookScraper


@extend_schema(
    request=inline_serializer(
        name="ScrapeRequest",
        fields={"max_pages": serializers.IntegerField(default=50)},
    ),
    responses={200: inline_serializer(
        name="ScrapeResponse",
        fields={
            "status": serializers.CharField(),
            "message": serializers.CharField(),
        },
    )},
)
class ScrapeView(APIView):
    def post(self, request):
        max_pages = request.data.get("max_pages", 50)
        if not isinstance(max_pages, int) or max_pages < 1:
            return Response(
                {"error": "max_pages must be a positive integer"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        def run_scraper():
            scraper = BookScraper()
            scraper.run(max_pages=max_pages)

        thread = threading.Thread(target=run_scraper, daemon=True)
        thread.start()

        return Response({
            "status": "started",
            "message": f"Scraping {max_pages} pages in background",
        })
