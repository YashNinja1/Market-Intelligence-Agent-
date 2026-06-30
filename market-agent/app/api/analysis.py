from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.core.database import get_sentiment_summary, get_latest_stocks, get_news_by_symbol
from app.services.fetchers import fetch_all
from app.core.database import insert_all
from app.models.schemas import SentimentSummary, MarketSignal, FetchResponse

router = APIRouter(prefix="/analysis", tags=["Analysis"])


@router.get("/sentiment", response_model=list[SentimentSummary])
async def get_sentiment():
    """Get sentiment breakdown per stock symbol."""
    data = get_sentiment_summary()
    if not data:
        raise HTTPException(status_code=404, detail="No sentiment data found.")
    return data


@router.get("/signals", response_model=list[MarketSignal])
async def get_signals():
    """
    Combined price + sentiment signal per stock.
    ALIGNED = price and sentiment agree.
    DIVERGING = price and sentiment contradict (interesting signal).
    """
    stocks = get_latest_stocks()
    sentiment = get_sentiment_summary()

    if not stocks or not sentiment:
        raise HTTPException(status_code=404, detail="Not enough data for signals.")

    sentiment_map = {s["symbol"]: s for s in sentiment}
    signals = []

    for stock in stocks:
        symbol = stock["symbol"]
        sent = sentiment_map.get(symbol)
        if not sent:
            continue

        price_dir = "UP" if float(stock["change"]) > 0 else "DOWN"
        avg = float(sent["avg_sentiment"])
        sent_dir = "POSITIVE" if avg > 0 else "NEGATIVE"
        aligned = (
            (price_dir == "UP" and sent_dir == "POSITIVE") or
            (price_dir == "DOWN" and sent_dir == "NEGATIVE")
        )

        signals.append({
            "symbol": symbol,
            "price": float(stock["price"]),
            "price_direction": price_dir,
            "sentiment_direction": sent_dir,
            "signal": "ALIGNED" if aligned else "DIVERGING",
            "avg_sentiment": avg
        })

    return signals


@router.post("/fetch", response_model=FetchResponse)
async def trigger_fetch(background_tasks: BackgroundTasks):
    """
    Trigger a fresh data fetch in the background.
    Returns immediately — fetch runs behind the scenes.
    """
    def run_fetch():
        data = fetch_all(symbols=["AAPL", "TSLA", "GOOGL"])
        insert_all(data)

    background_tasks.add_task(run_fetch)

    return {
        "status": "started",
        "stocks_fetched": 0,
        "articles_fetched": 0,
        "message": "Fetch started in background. Check /stocks in 10 seconds."
    }