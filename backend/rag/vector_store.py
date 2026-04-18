import chromadb
from django.conf import settings

from .chunker import chunk_text
from .embeddings import embed_texts

COLLECTION_NAME = "book_chunks"

_client = None


def get_chroma_client():
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)
    return _client


def get_collection():
    client = get_chroma_client()
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


def add_book(book):
    genre_label = " ".join(
        filter(None, [book.genre, book.ai_genre])
    )
    text = ""
    if genre_label:
        text += genre_label + ". "
    if book.description:
        text += book.description + " "
    if book.ai_summary:
        text += book.ai_summary

    text = text.strip()
    if not text:
        return 0

    chunks = chunk_text(text)
    if not chunks:
        return 0

    collection = get_collection()
    ids = [f"book_{book.id}_chunk_{i}" for i in range(len(chunks))]
    metadatas = [
        {
            "book_id": book.id,
            "book_title": book.title,
            "chunk_index": i,
            "genre": book.genre or "",
            "ai_genre": book.ai_genre or "",
        }
        for i in range(len(chunks))
    ]
    embeddings = embed_texts(chunks)

    collection.upsert(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
    )
    return len(chunks)


DISTANCE_THRESHOLD = 0.65


def query(question_embedding, top_k=5):
    collection = get_collection()
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )
    chunks = results["documents"][0] if results["documents"] else []
    metadatas = results["metadatas"][0] if results["metadatas"] else []
    distances = results["distances"][0] if results["distances"] else []
    return chunks, metadatas, distances
