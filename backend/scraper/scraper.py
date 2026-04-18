import logging
import os
import time
import platform  # Needed to detect Windows vs Render (Linux)

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from books.models import Book



logging.basicConfig(
    level=logging.INFO,  # Use DEBUG for even more detail
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

BASE_URL = "https://books.toscrape.com"

STAR_MAP = {
    "one": 1.0,
    "two": 2.0,
    "three": 3.0,
    "four": 4.0,
    "five": 5.0,
}

class BookScraper:
    def __init__(self):
        options = Options()
        
        # Headless for scraping (works on Windows & Linux)
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")

        system_platform = platform.system()
        logger.info(f"Detected platform: {system_platform}")

        if system_platform == "Windows":
            logger.info("Using Selenium Manager to automatically handle ChromeDriver")
            # Selenium 4.6+ automatically downloads and manages ChromeDriver
            self.driver = webdriver.Chrome(options=options)
        else:
            logger.info("Using Linux/Render paths for Chrome & ChromeDriver")
            chrome_bin = os.environ.get("CHROME_BIN", "/usr/bin/google-chrome")
            chromedriver_path = os.environ.get("CHROMEDRIVER_PATH", "/usr/bin/chromedriver")

            if not os.path.exists(chrome_bin):
                raise FileNotFoundError(f"Chrome binary not found at {chrome_bin}")
            if not os.path.exists(chromedriver_path):
                raise FileNotFoundError(f"ChromeDriver not found at {chromedriver_path}")

            options.binary_location = chrome_bin
            self.driver = webdriver.Chrome(
                service=Service(executable_path=chromedriver_path),
                options=options
            )

        logger.info("Chrome WebDriver initialized successfully")

    def _get_soup(self, url):
        self.driver.get(url)
        time.sleep(1)
        return BeautifulSoup(self.driver.page_source, "html.parser")

    def _parse_rating(self, article):
        star_tag = article.select_one("p.star-rating")
        if star_tag:
            classes = [c.lower() for c in star_tag.get("class", []) if c.lower() != "star-rating"]
            if classes:
                return STAR_MAP.get(classes[0], 0.0)
        return 0.0

    def scrape_list_page(self, url):
        soup = self._get_soup(url)
        articles = soup.select("article.product_pod")
        books = []
        for article in articles:
            title_tag = article.select_one("h3 a")
            title = title_tag.get("title", "") if title_tag else ""
            relative_url = title_tag.get("href", "") if title_tag else ""
            
            # Normalize URL
            if relative_url.startswith("catalogue/"):
                book_url = f"{BASE_URL}/{relative_url}"
            elif relative_url.startswith("../"):
                book_url = f"{BASE_URL}/catalogue/{relative_url.lstrip('../')}"
            else:
                book_url = f"{BASE_URL}/catalogue/{relative_url}"

            img_tag = article.select_one("img.thumbnail")
            cover_src = img_tag.get("src", "") if img_tag else ""
            if cover_src.startswith("../"):
                cover_image_url = f"{BASE_URL}/{cover_src.lstrip('../')}"
            else:
                cover_image_url = f"{BASE_URL}/{cover_src}"

            price_tag = article.select_one("p.price_color")
            price = price_tag.get_text(strip=True) if price_tag else ""

            avail_tag = article.select_one("p.instock.availability")
            availability = avail_tag.get_text(strip=True) if avail_tag else ""

            rating = self._parse_rating(article)

            books.append({
                "title": title,
                "book_url": book_url,
                "cover_image_url": cover_image_url,
                "price": price,
                "availability": availability,
                "rating": rating,
            })
        return books

    def scrape_detail_page(self, url):
        soup = self._get_soup(url)
        desc_tag = soup.select_one("#product_description ~ p")
        description = desc_tag.get_text(strip=True) if desc_tag else ""

        breadcrumb_links = soup.select("ul.breadcrumb li a")
        genre = ""
        if len(breadcrumb_links) >= 3:
            genre = breadcrumb_links[2].get_text(strip=True)

        num_reviews = 0
        rows = soup.select("table.table-striped tr")
        for row in rows:
            th = row.select_one("th")
            td = row.select_one("td")
            if th and td and "number of reviews" in th.get_text(strip=True).lower():
                try:
                    num_reviews = int(td.get_text(strip=True))
                except ValueError:
                    pass

        return {
            "description": description,
            "genre": genre,
            "num_reviews": num_reviews,
        }

    def run(self, max_pages=50):
        total_created = 0
        total_skipped = 0

        try:
            for page_num in range(1, max_pages + 1):
                if page_num == 1:
                    list_url = f"{BASE_URL}/catalogue/page-1.html"
                else:
                    list_url = f"{BASE_URL}/catalogue/page-{page_num}.html"

                logger.info(f"Scraping list page {page_num}: {list_url}")
                books_data = self.scrape_list_page(list_url)

                for book_data in books_data:
                    # Check if already exists
                    if Book.objects.filter(book_url=book_data["book_url"]).exists():
                        total_skipped += 1
                        logger.debug(f"  Skipped (exists): {book_data['title']}")
                        continue

                    # Scrape detail page
                    detail_data = self.scrape_detail_page(book_data["book_url"])
                    book_data.update(detail_data)

                    # Create book
                    try:
                        Book.objects.create(**book_data)
                        total_created += 1
                        logger.info(f"  Created: {book_data['title']}")
                    except Exception as e:
                        logger.error(f"  Error creating book: {e}")

                logger.info(f"  Page {page_num} done. Created: {total_created}, Skipped: {total_skipped}")
        finally:
            self.driver.quit()

        return {"created": total_created, "skipped": total_skipped}