from pydantic import BaseModel

class ScraperInput(BaseModel):
    url: str
    category: str = "general"
