import logging

from django.core.management.base import BaseCommand

from books.models import Book
from rag.vector_store import add_book

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Build ChromaDB index from book data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--all",
            action="store_true",
            help="Index all books (not just those with insights_generated=True)",
        )

    def handle(self, *args, **options):
        if options["all"]:
            books = Book.objects.all()
        else:
            books = Book.objects.filter(insights_generated=True)

        total = books.count()
        self.stdout.write(f"Indexing {total} books...")

        indexed = 0
        total_chunks = 0
        for book in books:
            chunks_added = add_book(book)
            if chunks_added > 0:
                indexed += 1
                total_chunks += chunks_added

        self.stdout.write(
            self.style.SUCCESS(
                f"Indexing complete. Books indexed: {indexed}/{total}, Total chunks: {total_chunks}"
            )
        )
