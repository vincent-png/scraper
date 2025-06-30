import os
from pathlib import Path

class Settings:
    BASE_DIR = Path(__file__).resolve().parent.parent
    SHEET_NAME = os.getenv("SHEET_NAME", "Web Scraper Links")
    WORKSHEET_NAME = os.getenv("WORKSHEET_NAME", "Sheet1")
    URL_COLUMN = os.getenv("URL_COLUMN", "URL")
    START_ROW = int(os.getenv("START_ROW", "2"))

    USER_AGENT = "Mozilla/5.0"
    REQUEST_TIMEOUT = 10
    MAX_RETRIES = 3

    SUMMARY_MODEL = "facebook/bart-large-cnn"
    QA_MODEL = "deepset/roberta-base-squad2"
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    SUMMARY_MAX_LENGTH = 150
    SUMMARY_MIN_LENGTH = 30

    OUTPUT_DIR = BASE_DIR / "data" / "output"

settings = Settings()
