# config/startup.py
from sentence_transformers import SentenceTransformer
import logging

logger = logging.getLogger(__name__)

logger.info("Preloading SentenceTransformer model...")
SENTENCE_TRANSFORMER = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
logger.info("SentenceTransformer loaded successfully.")