from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers

from books.models import Book
from .generator import InsightGenerator


@extend_schema(
    request=inline_serializer(
        name="InsightGenerateRequest",
        fields={"book_id": serializers.IntegerField()},
    ),
    responses={200: inline_serializer(
        name="InsightGenerateResponse",
        fields={
            "status": serializers.CharField(),
            "book_id": serializers.IntegerField(),
        },
    )},
)
class InsightGenerateView(APIView):
    def post(self, request):
        book_id = request.data.get("book_id")
        if not book_id:
            return Response(
                {"error": "book_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response(
                {"error": f"Book with id={book_id} not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        generator = InsightGenerator()
        try:
            generator.generate_all(book)
        except Exception as exc:
            return Response(
                {"error": str(exc)},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        return Response({
            "status": "completed",
            "book_id": book.id,
        })
