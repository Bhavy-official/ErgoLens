#!/bin/bash
set -e

# Entrypoint script for Django backend
# Handles migrations, optional data initialization, and server startup

echo "🚀 Starting Ergosphere Backend..."

cd /app/backend

# ============================================================================
# 1. Run Database Migrations
# ============================================================================
echo "📦 Running migrations..."
python manage.py migrate --noinput

# ============================================================================
# 2. Collect Static Files (optional, for production)
# ============================================================================
if [ "$COLLECT_STATIC" = "true" ]; then
    echo "📁 Collecting static files..."
    python manage.py collectstatic --noinput
fi

# ============================================================================
# 3. Initialize Data (Scrape, Generate Insights, Build Index)
# ============================================================================

# Only run initialization if INITIALIZE_DATA is set to 'true'
if [ "$INITIALIZE_DATA" = "true" ]; then
    echo "🔄 Initializing data..."
    
    # Scrape books
    if [ "$SCRAPE_BOOKS" = "true" ]; then
        echo "🕷️  Scraping books from books.toscrape.com (${MAX_PAGES} pages)..."
        python manage.py scrape_books --max-pages "${MAX_PAGES:-50}"
    fi
    
    # Generate AI insights
    if [ "$GENERATE_INSIGHTS" = "true" ]; then
        echo "💡 Generating AI insights for books..."
        python manage.py generate_insights --all
    fi
    
    # Build ChromaDB index
    if [ "$BUILD_INDEX" = "true" ]; then
        echo "🔍 Building ChromaDB vector index..."
        python manage.py build_index --all
    fi
fi

# ============================================================================
# 4. Create Superuser (optional, for first-time setup)
# ============================================================================
if [ "$CREATE_SUPERUSER" = "true" ]; then
    echo "👤 Creating superuser..."
    python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print("✅ Superuser 'admin' created")
else:
    print("⚠️  Superuser 'admin' already exists")
END
fi

# ============================================================================
# 5. Start Services (Nginx + Gunicorn via supervisord)
# ============================================================================
echo "🌍 Starting Nginx + Gunicorn via supervisord..."
exec supervisord -c /etc/supervisor/conf.d/supervisord.conf
