import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv
import time

load_dotenv()
API_KEY = os.getenv("ALPHA_VANTAGE_KEY")

def fetch_stock_price(symbol: str) -> dict:
    """Fetch latest stock quote for a given symbol e.g. AAPL, TSLA"""
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": API_KEY
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    
    data = response.json()["Global Quote"]
    
    return {
        "symbol": data["01. symbol"],
        "price": float(data["05. price"]),
        "change": data["09. change"],
        "change_percent": data["10. change percent"],
        "volume": data["06. volume"],
        "fetched_at": datetime.now().isoformat()
    }


def fetch_multiple_stocks(symbols: list) -> list:
    """Fetch data for a list of stock symbols"""
    results = []
    for symbol in symbols:
        try:
            stock = fetch_stock_price(symbol)
            results.append(stock)
            print(f"Fetched {symbol}: ${stock['price']}")
            time.sleep(12)
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
            
    return results


def save_to_json(data: list, filename: str) -> None:
    output = {
        "fetched_at": datetime.now().isoformat(),
        "count": len(data),
        "stocks": data
    }
    with open(filename, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nSaved to {filename}")


if __name__ == "__main__":
    symbols = ["AAPL", "TSLA", "GOOGL"]
    stocks = fetch_multiple_stocks(symbols)
    save_to_json(stocks, "stock_data.json")