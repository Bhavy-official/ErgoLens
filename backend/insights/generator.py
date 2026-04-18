import logging

from .llm_provider import chat

logger = logging.getLogger(__name__)


class InsightGenerator:
    def generate_summary(self, book):
        if book.ai_summary:
            return book.ai_summary

        prompt = (
            f"Write a concise 3-sentence summary of this book.\n\n"
            f"Title: {book.title}\n"
            f"Genre: {book.genre}\n"
            f"Description: {book.description}\n"
        )
        messages = [
            {"role": "system", "content": "You are a book summarizer. Write concise, informative summaries."},
            {"role": "user", "content": prompt}
        ]
        result = chat(messages=messages, max_tokens=256)
        book.ai_summary = result
        book.save(update_fields=["ai_summary"])
        logger.info(f"Generated summary for: {book.title}")
        return result

    def classify_genre(self, book):
        if book.ai_genre:
            return book.ai_genre

        prompt = (
            f"Classify this book into exactly ONE genre label. "
            f"Choose from: Fiction, Mystery, Romance, Science Fiction, Fantasy, Thriller, "
            f"Historical Fiction, Non-Fiction, Biography, Self-Help, Philosophy, Poetry, "
            f"Horror, Adventure, Young Adult, Children, Humor, Travel, Music, Art, Default.\n\n"
            f"Title: {book.title}\n"
            f"Scraped Genre: {book.genre}\n"
            f"Description: {book.description}\n\n"
            f"Respond with ONLY the genre label, nothing else."
        )
        messages = [
            {"role": "system", "content": "You are a book genre classifier. Respond with only the genre label."},
            {"role": "user", "content": prompt}
        ]
        result = chat(messages=messages, max_tokens=20)
        book.ai_genre = result
        book.save(update_fields=["ai_genre"])
        logger.info(f"Classified genre for: {book.title} -> {result}")
        return result

    def analyze_sentiment(self, book):
        if book.ai_sentiment:
            return book.ai_sentiment

        prompt = (
            f"Analyze the overall sentiment/tone of this book's description.\n\n"
            f"Title: {book.title}\n"
            f"Description: {book.description}\n\n"
            f"Respond with one of: Positive, Neutral, or Negative — "
            f"followed by a single sentence justification."
        )
        messages = [
            {"role": "system", "content": "You are a sentiment analyzer for book descriptions."},
            {"role": "user", "content": prompt}
        ]
        result = chat(messages=messages, max_tokens=100)
        book.ai_sentiment = result
        book.save(update_fields=["ai_sentiment"])
        logger.info(f"Analyzed sentiment for: {book.title}")
        return result

    def generate_recommendation(self, book):
        if book.ai_recommendation_text:
            return book.ai_recommendation_text

        prompt = (
            f"Write a recommendation in the format: "
            f"'If you like {book.title}, you'll also enjoy books that [reason]...'\n\n"
            f"Title: {book.title}\n"
            f"Genre: {book.genre}\n"
            f"Description: {book.description}\n"
        )
        messages = [
            {"role": "system", "content": "You are a book recommender. Write engaging, specific recommendations."},
            {"role": "user", "content": prompt}
        ]
        result = chat(messages=messages, max_tokens=200)
        book.ai_recommendation_text = result
        book.save(update_fields=["ai_recommendation_text"])
        logger.info(f"Generated recommendation for: {book.title}")
        return result

    def generate_all(self, book):
        self.generate_summary(book)
        self.classify_genre(book)
        self.analyze_sentiment(book)
        self.generate_recommendation(book)
        book.insights_generated = True
        book.save(update_fields=["insights_generated"])
        logger.info(f"All insights generated for: {book.title}")
