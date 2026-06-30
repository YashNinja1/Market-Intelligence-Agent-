import requests
import os
import logging
from dotenv import load_dotenv
from app.models.stock_models import StockData
from app.models.stock_models import NewsArticle

load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

ALPHA_KEY = os.getenv("ALPHA_VANTAGE_KEY")
BASE_URL = "https://www.alphavantage.co/query"


class APIError(Exception):
    pass


def fetch_stock(symbol: str) -> StockData | None:
    """Fetch live stock price for a symbol."""
    try:
        logger.info(f"Fetching stock: {symbol}")
        stock = StockData(symbol)
        stock.fetch()
        logger.info(f"Success: {stock.summary()}")
        return stock
    except requests.exceptions.ConnectionError:
        logger.error(f"No internet connection for {symbol}")
    except requests.exceptions.Timeout:
        logger.error(f"Timeout for {symbol}")
    except ValueError as e:
        logger.error(f"Bad data for {symbol}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error for {symbol}: {e}")
    return None


def fetch_news_sentiment(symbol: str, limit: int = 5) -> list[NewsArticle]:
    """
    Fetch news + sentiment scores from Alpha Vantage.
    Returns NewsArticle objects with sentiment baked in.
    """
    try:
        logger.info(f"Fetching news sentiment for: {symbol}")
        params = {
            "function": "NEWS_SENTIMENT",
            "tickers": symbol,
            "limit": limit,
            "apikey": ALPHA_KEY
        }
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        # Alpha Vantage returns this key for news
        feed = data.get("feed", [])
        if not feed:
            logger.warning(f"No news found for {symbol}")
            return []

        articles = []
        for item in feed:

            # Find sentiment score specific to our ticker
            ticker_sentiment = "Neutral"
            sentiment_score = 0.0
            for ts in item.get("ticker_sentiment", []):
                if ts["ticker"] == symbol:
                    ticker_sentiment = ts["ticker_sentiment_label"]
                    sentiment_score = float(ts["ticker_sentiment_score"])
                    break

            articles.append(NewsArticle(
                title=item["title"],
                source=item["source"],
                url=item["url"],
                published_at=item["time_published"],
                summary=item.get("summary", "")
            ))

            # Attach sentiment directly to the article
            articles[-1].sentiment = ticker_sentiment
            articles[-1].sentiment_score = sentiment_score

        logger.info(f"Fetched {len(articles)} articles for {symbol}")
        return articles

    except Exception as e:
        logger.error(f"News sentiment fetch failed for {symbol}: {e}")
        return []


def fetch_all(symbols: list[str]) -> dict:
    """
    Master fetcher — stocks + news sentiment for each symbol.
    """
    results = {
        "stocks": [],
        "news": []
    }

    for symbol in symbols:
        # Fetch stock price
        stock = fetch_stock(symbol)
        if stock:
            results["stocks"].append(stock.to_dict())

        # Fetch news + sentiment for same symbol
        articles = fetch_news_sentiment(symbol)
        for a in articles:
            results["news"].append({
                "symbol": symbol,
                "title": a.title,
                "source": a.source,
                "url": a.url,
                "published_at": a.published_at,
                "summary": a.summary,
                "sentiment": a.sentiment,
                "sentiment_score": a.sentiment_score
            })

    return results

# Company name → Alpha Vantage symbol mapping
# Alpha Vantage also has a search endpoint — we'll use both

KNOWN_COMPANIES = {
    "apple": "AAPL",
    "tesla": "TSLA",
    "google": "GOOGL",
    "alphabet": "GOOGL",
    "microsoft": "MSFT",
    "amazon": "AMZN",
    "meta": "META",
    "facebook": "META",
    "netflix": "NFLX",
    "nvidia": "NVDA",
    "amd": "AMD",
    "intel": "INTC",
    "samsung": "SSNLF",
    "uber": "UBER",
    "airbnb": "ABNB",
    "spotify": "SPOT",
    "twitter": "X",
    "paypal": "PYPL",
    "adobe": "ADBE",
    "salesforce": "CRM",
}


def resolve_symbol(query: str) -> dict | None:
    """
    Convert a company name or partial name into a stock symbol.
    First checks local map, then hits Alpha Vantage search API.
    Returns dict with symbol and name, or None if not found.
    """
    query_clean = query.strip().lower()

    # 1. Check local map first (instant, no API call)
    for name, symbol in KNOWN_COMPANIES.items():
        if query_clean in name or name in query_clean:
            return {
                "symbol": symbol,
                "name": query.title(),
                "source": "local"
            }

    # 2. If not found locally, search Alpha Vantage
    try:
        logger.info(f"Searching Alpha Vantage for: {query}")
        params = {
            "function": "SYMBOL_SEARCH",
            "keywords": query,
            "apikey": ALPHA_KEY
        }
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()

        matches = response.json().get("bestMatches", [])
        if not matches:
            logger.warning(f"No symbol found for: {query}")
            return None

        # Take the best match
        best = matches[0]
        return {
            "symbol": best["1. symbol"],
            "name": best["2. name"],
            "source": "alpha_vantage"
        }

    except Exception as e:
        logger.error(f"Symbol search failed for '{query}': {e}")
        return None