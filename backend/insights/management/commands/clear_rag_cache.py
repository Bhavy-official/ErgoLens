from django.core.cache import cache
from django.core.management.base import BaseCommand

from insights.models import InsightCache


class Command(BaseCommand):
    help = "Clear the RAG answer cache (Django cache + InsightCache DB table)"

    def handle(self, *args, **options):
        deleted, _ = InsightCache.objects.all().delete()
        cache.clear()
        self.stdout.write(
            self.style.SUCCESS(
                f"Cleared {deleted} cached answer(s) from the database and flushed the Django cache."
            )
        )
