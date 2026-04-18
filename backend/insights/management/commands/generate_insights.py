import logging
import time

from django.core.management.base import BaseCommand

from books.models import Book
from insights.generator import InsightGenerator

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Generate AI insights for books using Groq"

    def add_arguments(self, parser):
        parser.add_argument(
            "--book-id",
            type=int,
            default=None,
            help="Generate insights for a specific book by ID",
        )
        parser.add_argument(
            "--all",
            action="store_true",
            help="Generate insights for all books without insights",
        )

    def handle(self, *args, **options):
        generator = InsightGenerator()

        if options["book_id"]:
            try:
                book = Book.objects.get(id=options["book_id"])
            except Book.DoesNotExist:
                self.stderr.write(self.style.ERROR(f"Book with id={options['book_id']} not found"))
                return
            generator.generate_all(book)
            self.stdout.write(self.style.SUCCESS(f"Insights generated for: {book.title}"))

        elif options["all"]:
            books = Book.objects.filter(insights_generated=False)
            total = books.count()
            self.stdout.write(f"Generating insights for {total} books...")

            for i, book in enumerate(books, 1):
                self.stdout.write(f"  [{i}/{total}] {book.title}")
                try:
                    generator.generate_all(book)
                except Exception as e:
                    self.stderr.write(self.style.ERROR(f"    Error: {e}"))
                time.sleep(1)

            self.stdout.write(self.style.SUCCESS(f"Done. Processed {total} books."))
        else:
            self.stderr.write("Provide --book-id N or --all")
