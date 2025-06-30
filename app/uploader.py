import os
from supabase import create_client, Client
from pathlib import Path
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class SupabaseUploader:
    def __init__(self):
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
        self.bucket = os.environ.get("SUPABASE_BUCKET", "scraped-results")
        
        if not url or not key:
            raise ValueError("Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY in environment variables")
        
        self.client: Client = create_client(url, key)

    def upload_file(self, file_path: Path):
        """Upload file to Supabase Storage"""
        try:
            with open(file_path, "rb") as f:
                file_data = f.read()
                file_name = file_path.name

                res = self.client.storage.from_(self.bucket).upload(
                    path=file_name,
                    file=file_data,
                    file_options={"content-type": "text/csv"}
                )

                logger.info(f"Uploaded {file_name} to Supabase Storage bucket '{self.bucket}'")
                return res
        except Exception as e:
            logger.error(f"Failed to upload to Supabase: {e}")
            raise
