from transformers import pipeline
from sentence_transformers import SentenceTransformer
from app.config import settings

class ContentProcessor:
    def __init__(self):
        self.summarizer = pipeline("summarization", model=settings.SUMMARY_MODEL)
        self.embedder = SentenceTransformer(settings.EMBEDDING_MODEL)

    def process_content(self, text: str):
        if not text or len(text.split()) < 50:
            return None
        summary = self.summarizer(text, max_length=settings.SUMMARY_MAX_LENGTH,
                                  min_length=settings.SUMMARY_MIN_LENGTH, do_sample=False)
        embedding = self.embedder.encode(text).tolist()
        return {
            'summary': summary[0]['summary_text'],
            'embedding': embedding,
            'word_count': len(text.split()),
            'char_count': len(text)
        }