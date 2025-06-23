# main/models.py

from pydantic import BaseModel
from typing import List, Optional

class Article(BaseModel):
    title: str
    body: str
    published_date: Optional[str] = None
    source: Optional[str] = None

class Entity(BaseModel):
    name: str
    confidence: float

class Sentiment(BaseModel):
    entity_name: str
    sentiment: str  # positive, negative, neutral
    score: float

class TickerMapping(BaseModel):
    entity_name: str
    ticker: str
    exchange: Optional[str] = None
