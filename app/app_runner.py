import os
import logging
import pandas as pd
from pathlib import Path
from typing import List, Dict
from datetime import datetime
from tqdm import tqdm

# Optional: only needed if running locally with .env
from dotenv import load_dotenv
load_dotenv()

from app.google_sheets import GoogleSheetsClient
from app.scraper import WebScraper
from app.processor import ContentProcessor
from app.progress_tracker import ProgressTracker
from app.config import settings

logger = logging.getLogger(__name__)

class WebScraperApp:
    def __init__(self):
        self.sheets_client = GoogleSheetsClient()
        self.scraper = WebScraper()
        self.processor = ContentProcessor()
        self.progress = ProgressTracker(self.sheets_client)
        self.pending_updates = {}
        settings.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    def _commit_updates(self):
        if not self.pending_updates:
            return
        self.sheets_client.batch_update_rows(self.pending_updates)
        self.pending_updates = {}

    def upload_to_supabase(self, file_path: Path):
        try:
            from supabase import create_client
            url = os.environ['SUPABASE_URL']
            key = os.environ['SUPABASE_SERVICE_ROLE_KEY']
            supabase = create_client(url, key)

            with open(file_path, 'rb') as f:
                supabase.storage.from_('scraped-results').upload(
                    path=file_path.name,
                    file=f,
                    file_options={"content-type": "text/csv"}
                )
            logger.info(f"Uploaded {file_path.name} to Supabase storage bucket")
        except Exception as e:
            logger.error(f"Supabase upload failed: {e}")

    def run(self):
        logger.info("Starting web scraping process")
        records = self.sheets_client.get_sheet_data()
        self.progress.stats['total'] = len(records)
        results = []

        for i, record in enumerate(tqdm(records, desc="Processing URLs")):
            url = record.get(settings.URL_COLUMN, "")
            if not url or not isinstance(url, str) or not url.startswith('http'):
                continue

            result = {'original_row': i + settings.START_ROW, 'url': url, **record}
            try:
                text = self.scraper.scrape_url(url)
                if not text:
                    result['status'] = 'failed'
                    results.append(result)
                    continue

                processed = self.processor.process_content(text)
                if not processed:
                    result['status'] = 'failed'
                    results.append(result)
                    continue

                result.update({
                    'status': 'success',
                    'summary': processed.get('summary'),
                    'word_count': processed.get('word_count')
                })
                results.append(result)

            except Exception as e:
                result['status'] = 'error'
                result['error'] = str(e)
                results.append(result)

            self.progress.update_stats(result)

        df = pd.DataFrame(results)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = settings.OUTPUT_DIR / f"scraped_results_{timestamp}.csv"
        df.to_csv(output_file, index=False)
        logger.info(f"Saved results to {output_file}")

        self._commit_updates()
        self.progress.update_progress_cell()

        self.upload_to_supabase(output_file)

        return output_file
