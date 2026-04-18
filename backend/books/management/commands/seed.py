from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from books.models import Book

class Command(BaseCommand):
    help = 'Seeds the database with an admin user and some mock books.'

    def handle(self, *args, **kwargs):
        # Create superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin')
            self.stdout.write(self.style.SUCCESS('Admin user created (admin / admin).'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists.'))

        # Seed specific mock book data to satisfy initial dashboard views
        books_data = [
            {
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "rating": 4.5,
                "num_reviews": 1200,
                "description": "A novel set in the Jazz Age that tells the tragic story of Jay Gatsby.",
                "book_url": "https://example.com/gatsby",
                "cover_image_url": "https://via.placeholder.com/150",
                "price": "£10.99",
                "availability": "In stock",
                "genre": "Fiction",
                "ai_summary": "A classic story of wealth, love, and the American Dream.",
                "ai_genre": "Classic Fiction",
                "ai_sentiment": "Negative - Tragic downfall of the protagonist.",
                "ai_recommendation_text": "If you like historical dramas about the 1920s, you will love this.",
                "insights_generated": True
            },
            {
                "title": "Dune",
                "author": "Frank Herbert",
                "rating": 4.8,
                "num_reviews": 3400,
                "description": "A sci-fi epic concerning the desert planet Arrakis and the spice melange.",
                "book_url": "https://example.com/dune",
                "cover_image_url": "https://via.placeholder.com/150",
                "price": "£14.99",
                "availability": "In stock",
                "genre": "Science Fiction",
                "ai_summary": "Intergalactic politics and ecology battle on a harsh desert planet.",
                "ai_genre": "Science Fiction",
                "ai_sentiment": "Neutral - Epic and objective storytelling.",
                "ai_recommendation_text": "If you like grand space operas with deep lore, Dune is essential.",
                "insights_generated": True
            }
        ]

        # Bulk create or get
        count = 0
        for b_data in books_data:
            obj, created = Book.objects.get_or_create(book_url=b_data["book_url"], defaults=b_data)
            if created:
                count += 1
        
        if count > 0:
            self.stdout.write(self.style.SUCCESS(f'Successfully seeded {count} books.'))
        else:
            self.stdout.write(self.style.WARNING('Books already seeded.'))
