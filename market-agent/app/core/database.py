import os
import logging
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

# Engine is the connection to PostgreSQL
engine = create_engine(DATABASE_URL)


def get_connection():
    """Returns an active database connection."""
    return engine.connect()


def test_connection():
    """Verify database is reachable."""
    try:
        with get_connection() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database connection successful")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False


def insert_stock(stock: dict) -> None:
    query = text("""
        INSERT INTO stocks (symbol, company_name, price, change, change_pct, volume, fetched_at)
        VALUES (:symbol, :company_name, :price, :change, :change_pct, :volume, NOW())
    """)
    with get_connection() as conn:
        conn.execute(query, {
            "symbol": stock["symbol"],
            "company_name": stock.get("company_name", stock["symbol"]),
            "price": stock["price"],
            "change": stock["change"],
            "change_pct": stock["change_percent"],
            "volume": stock["volume"]
        })
        conn.commit()


def insert_news(article: dict) -> None:
    """Insert a single news article."""
    query = text("""
        INSERT INTO news (symbol, title, source, url, summary, sentiment, sentiment_score, published_at)
        VALUES (:symbol, :title, :source, :url, :summary, :sentiment, :sentiment_score, :published_at)
    """)
    with get_connection() as conn:
        conn.execute(query, article)
        conn.commit()


def insert_all(data: dict) -> None:
    """Insert all stocks and news from fetch_all() output."""
    for stock in data["stocks"]:
        insert_stock(stock)

    for article in data["news"]:
        insert_news(article)

    logger.info(f"Inserted {len(data['stocks'])} stocks and {len(data['news'])} articles")

def get_latest_stocks() -> list[dict]:
    query = text("""
        SELECT DISTINCT ON (symbol)
            symbol, company_name, price, change, change_pct, volume, fetched_at
        FROM stocks
        ORDER BY symbol, fetched_at DESC
    """)
    with get_connection() as conn:
        result = conn.execute(query)
        return [dict(row._mapping) for row in result]


def get_news_by_symbol(symbol: str) -> list[dict]:
    """Get all news for a specific stock symbol."""
    query = text("""
        SELECT title, source, sentiment, sentiment_score, published_at
        FROM news
        WHERE symbol = :symbol
        ORDER BY fetched_at DESC
        LIMIT 10
    """)
    with get_connection() as conn:
        result = conn.execute(query, {"symbol": symbol})
        return [dict(row._mapping) for row in result]


def get_sentiment_summary() -> list[dict]:
    """Average sentiment score per symbol — feeds the agent layer."""
    query = text("""
        SELECT
            symbol,
            COUNT(*) as article_count,
            ROUND(AVG(sentiment_score)::numeric, 4) as avg_sentiment,
            SUM(CASE WHEN sentiment = 'Bullish' THEN 1 ELSE 0 END) as bullish,
            SUM(CASE WHEN sentiment = 'Bearish' THEN 1 ELSE 0 END) as bearish
        FROM news
        GROUP BY symbol
        ORDER BY avg_sentiment DESC
    """)
    with get_connection() as conn:
        result = conn.execute(query)
        return [dict(row._mapping) for row in result]

def get_stock_history(symbol: str) -> list[dict]:
    """Get all historical prices for a symbol."""
    query = text("""
        SELECT symbol, price, change, change_pct, volume, fetched_at
        FROM stocks
        WHERE symbol = :symbol
        ORDER BY fetched_at DESC
        LIMIT 50
    """)
    with get_connection() as conn:
        result = conn.execute(query, {"symbol": symbol})
        return [dict(row._mapping) for row in result]
    
def get_all_news() -> list[dict]:
    """Get all recent news articles."""
    query = text("""
        SELECT symbol, title, source, url, summary,
               sentiment, sentiment_score, published_at
        FROM news
        ORDER BY fetched_at DESC
        LIMIT 50
    """)
    with get_connection() as conn:
        result = conn.execute(query)
        return [dict(row._mapping) for row in result]

def remove_stock(symbol: str) -> bool:
    """Remove all data for a symbol from both tables."""
    try:
        with get_connection() as conn:
            conn.execute(text("DELETE FROM news WHERE symbol = :symbol"), {"symbol": symbol})
            conn.execute(text("DELETE FROM stocks WHERE symbol = :symbol"), {"symbol": symbol})
            conn.commit()
            logger.info(f"Removed {symbol} from database")
            return True
    except Exception as e:
        logger.error(f"Failed to remove {symbol}: {e}")
        return False


def get_tracked_symbols() -> list[str]:
    """Get list of all currently tracked symbols."""
    query = text("""
        SELECT DISTINCT symbol FROM stocks ORDER BY symbol
    """)
    with get_connection() as conn:
        result = conn.execute(query)
        return [row[0] for row in result]
    
