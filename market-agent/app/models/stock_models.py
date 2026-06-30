from datetime import datetime
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("ALPHA_VANTAGE_KEY")


class StockData:
    """Represents a single stock's market data."""

    def __init__(self, symbol: str):
        self.symbol = symbol.upper()
        self.price = None
        self.change = None
        self.change_percent = None
        self.volume = None
        self.fetched_at = None

    def fetch(self):
        """Fetch latest data from Alpha Vantage and populate fields."""
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": self.symbol,
            "apikey": API_KEY
        }
        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json().get("Global Quote", {})
        if not data:
            raise ValueError(f"No data returned for {self.symbol}")

        self.price = float(data["05. price"])
        self.change = float(data["09. change"])
        self.change_percent = data["10. change percent"].strip("%")
        self.volume = int(data["06. volume"])
        self.fetched_at = datetime.now().isoformat()
        return self

    def is_gaining(self) -> bool:
        """Returns True if stock price went up today."""
        return self.change > 0

    def summary(self) -> str:
        """Human-readable one-line summary."""
        direction = "UP" if self.is_gaining() else "DOWN"
        return (
            f"{self.symbol}: ${self.price:.2f} "
            f"({direction} {self.change_percent}%) "
            f"| Volume: {self.volume:,}"
        )

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON saving."""
        return {
            "symbol": self.symbol,
            "price": self.price,
            "change": self.change,
            "change_percent": self.change_percent,
            "volume": self.volume,
            "fetched_at": self.fetched_at
        }

# Add this to the bottom of models.py

class NewsArticle:
    """Represents a single news article."""

    def __init__(self, title: str, source: str, url: str, published_at: str, summary: str = ""):
        self.title = title
        self.source = source
        self.url = url
        self.published_at = published_at
        self.summary = summary

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "source": self.source,
            "url": self.url,
            "published_at": self.published_at,
            "summary": self.summary
        }

    def __repr__(self):
        return f"<NewsArticle: {self.title[:50]}...>"

class Portfolio:
    """Manages a collection of stocks."""

    def __init__(self, name: str):
        self.name = name
        self.stocks: list[StockData] = []

    def add(self, symbol: str):
        """Add and fetch a stock."""
        try:
            stock = StockData(symbol)
            stock.fetch()
            self.stocks.append(stock)
            print(stock.summary())
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
        return self
    def highest_price(self):
        """Return the stock with the highest current price."""
        if not self.stocks:
            return None

        return max(self.stocks, key=lambda stock: stock.price)
    def total_volume(self):
        """Return the total trading volume for all stocks in the portfolio."""
        total = 0
        for stock in self.stocks:
            total += stock.volume

        return total

    def gainers(self) -> list[StockData]:
        """Return only stocks that went up today."""
        return [s for s in self.stocks if s.is_gaining()]

    def losers(self) -> list[StockData]:
        """Return only stocks that went down today."""
        return [s for s in self.stocks if not s.is_gaining()]

    def report(self):
        """Print a full portfolio report."""
        print(f"\n{'='*40}")
        print(f"Portfolio: {self.name}")
        print(f"{'='*40}")
        print(f"Total stocks tracked: {len(self.stocks)}")
        
        print(f"Highest Price: {self.highest_price().symbol} (${self.highest_price().price:.2f})")

        print(f"Total Volume: {self.total_volume():,}")

        print(f"Gaining: {len(self.gainers())} | Losing: {len(self.losers())}")
        print(f"\nTop gainers:")
        for s in self.gainers():
            print(f"  {s.summary()}")
        print(f"\nUnderperformers:")
        for s in self.losers():
            print(f"  {s.summary()}")

    def to_dict(self) -> dict:
        return {
            "portfolio": self.name,
            "stocks": [s.to_dict() for s in self.stocks]
        }