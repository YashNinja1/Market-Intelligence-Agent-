from fastapi import APIRouter, HTTPException
from app.core.database import get_news_by_symbol, get_all_news
from app.models.schemas import NewsResponse

router = APIRouter(prefix="/news", tags=["News"])


@router.get("/", response_model=list[NewsResponse])
async def get_all_news_endpoint():
    """Get all recent news articles."""
    news = get_all_news()
    if not news:
        raise HTTPException(status_code=404, detail="No news found. Run a fetch first.")
    return news


@router.get("/{symbol}", response_model=list[NewsResponse])
async def get_news_for_symbol(symbol: str):
    """Get news articles for a specific stock."""
    news = get_news_by_symbol(symbol.upper())
    if not news:
        raise HTTPException(status_code=404, detail=f"No news found for {symbol.upper()}")
    return news