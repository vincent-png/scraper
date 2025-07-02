from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.app_runner import WebScraperApp
from app.uploader import SupabaseUploader
from app.models import ScraperInput  # <-- New input model

from pathlib import Path

app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "online"}

@app.post("/run")
def run_scraper(data: ScraperInput):
    try:
        # Initialize and run scraper with parameters
        scraper = WebScraperApp(url=data.url, category=data.category)
        output: Path = scraper.run()

        # Upload CSV to Supabase
        uploader = SupabaseUploader()
        uploader.upload_file(output)

        return JSONResponse(content={"status": "success", "output": str(output)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "detail": str(e)})
