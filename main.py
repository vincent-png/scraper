from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.app_runner import WebScraperApp
from app.uploader import SupabaseUploader  # <-- Removed extra space

from pathlib import Path

app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "online"}

@app.post("/run")
def run_scraper():
    try:
        # Run scraper
        scraper = WebScraperApp()
        output: Path = scraper.run()

        # Upload to Supabase
        uploader = SupabaseUploader()
        uploader.upload_file(output)

        return JSONResponse(content={"status": "success", "output": str(output)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "detail": str(e)})
