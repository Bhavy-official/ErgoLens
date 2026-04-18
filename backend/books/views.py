from rest_framework import generics, filters
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import Book
from .serializers import BookListSerializer, BookDetailSerializer
from rag.embeddings import embed_text
from rag.vector_store import query as vector_query


@extend_schema(
    parameters=[
        OpenApiParameter(name="genre", description="Filter by genre", type=str),
        OpenApiParameter(name="rating_min", description="Minimum rating", type=float),
        OpenApiParameter(name="search", description="Search by title", type=str),
    ]
)
class BookListView(generics.ListAPIView):
    serializer_class = BookListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["title"]

    def get_queryset(self):
        qs = Book.objects.all()
        genre = self.request.query_params.get("genre")
        rating_min = self.request.query_params.get("rating_min")

        if genre:
            qs = qs.filter(genre__iexact=genre)
        if rating_min:
            try:
                qs = qs.filter(rating__gte=float(rating_min))
            except ValueError:
                pass
        return qs


class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer


@extend_schema(
    description="Get top-5 similar books based on vector similarity",
    responses=BookListSerializer(many=True),
)
class BookRecommendationsView(generics.GenericAPIView):
    serializer_class = BookListSerializer

    def get(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            from rest_framework.response import Response
            return Response({"error": "Book not found"}, status=404)

        text = f"{book.title} {book.description} {book.ai_summary}"
        embedding = embed_text(text)
        chunks, metadatas, distances = vector_query(embedding, top_k=6)

        # Exclude the book itself
        similar_ids = []
        for meta in metadatas:
            bid = meta.get("book_id")
            if bid and bid != book.id and bid not in similar_ids:
                similar_ids.append(bid)
            if len(similar_ids) >= 5:
                break

        similar_books = Book.objects.filter(id__in=similar_ids)
        serializer = BookListSerializer(similar_books, many=True)
        
        from rest_framework.response import Response
        return Response(serializer.data)
