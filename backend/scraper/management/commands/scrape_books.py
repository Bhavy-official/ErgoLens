import logging

from django.conf import settings
from django.core.management.base import BaseCommand

from scraper.scraper import BookScraper

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Scrape books from books.toscrape.com"

    def add_arguments(self, parser):
        parser.add_argument(
            "--max-pages",
            type=int,
            default=None,
            help="Number of catalogue pages to scrape (default: MAX_PAGES env var)",
        )

    def handle(self, *args, **options):
        max_pages = options["max_pages"] or settings.MAX_PAGES
        self.stdout.write(f"Starting scraper with max_pages={max_pages}")

        scraper = BookScraper()
        result = scraper.run(max_pages=max_pages)

        self.stdout.write(
            self.style.SUCCESS(
                f"Scraping complete. Created: {result['created']}, Skipped: {result['skipped']}"
            )
        )
