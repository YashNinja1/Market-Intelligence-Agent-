from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class StockResponse(BaseModel):
    symbol: str
    price: float
    change: float
    change_pct: str
    volume: int
    fetched_at: datetime

    class Config:
        from_attributes = True


from pydantic import BaseModel
from typing import Optional

class NewsResponse(BaseModel):
    title: str
    source: str

    url: Optional[str] = None
    summary: Optional[str] = None

    sentiment: Optional[str] = None
    sentiment_score: Optional[float] = None

    published_at: str

    class Config:
        from_attributes = True

class SentimentSummary(BaseModel):
    symbol: str
    article_count: int
    avg_sentiment: float
    bullish: int
    bearish: int


class MarketSignal(BaseModel):
    symbol: str
    price: float
    price_direction: str      # UP or DOWN
    sentiment_direction: str  # POSITIVE or NEGATIVE
    signal: str               # ALIGNED or DIVERGING
    avg_sentiment: float


class FetchResponse(BaseModel):
    status: str
    stocks_fetched: int
    articles_fetched: int
    message: str