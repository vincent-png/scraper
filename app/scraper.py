import re
import time
import requests
from bs4 import BeautifulSoup
from typing import Optional
from urllib.parse import urlparse
from app.config import settings

class WebScraper:
    def __init__(self):
        self.headers = {'User-Agent': settings.USER_AGENT}
        self.timeout = settings.REQUEST_TIMEOUT

    def _clean_text(self, text: str) -> str:
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\[[^\]]*\]', '', text)
        text = re.sub(r'<[^>]*>', '', text)
        return text.strip()

    def _extract_main_content(self, soup: BeautifulSoup) -> str:
        selectors = ['article', 'main', '.article-content', '.post-content', '#main-content']
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text()
        return soup.body.get_text() if soup.body else ""

    def scrape_url(self, url: str, retry: int = 0) -> Optional[str]:
        try:
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                return None
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            for element in soup(['script', 'style', 'nav', 'footer', 'iframe', 'noscript']):
                element.decompose()
            content = self._extract_main_content(soup)
            return self._clean_text(content)
        except Exception:
            if retry < settings.MAX_RETRIES:
                time.sleep(2 ** retry)
                return self.scrape_url(url, retry + 1)
            return None