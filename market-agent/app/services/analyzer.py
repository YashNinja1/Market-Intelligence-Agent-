import pandas as pd
import json


def analyze(filepath: str):
    with open(filepath) as f:
        data = json.load(f)

    # Stock analysis
    stocks_df = pd.DataFrame(data["stocks"])
    stocks_df["price"] = pd.to_numeric(stocks_df["price"])
    stocks_df["change"] = pd.to_numeric(stocks_df["change"])

    print("\n===== STOCK PRICES =====")
    print(stocks_df[["symbol", "price", "change", "change_percent"]])

    # Sentiment analysis
    news_df = pd.DataFrame(data["news"])

    print("\n===== SENTIMENT BREAKDOWN =====")
    sentiment_counts = news_df.groupby(["symbol", "sentiment"]).size().unstack(fill_value=0)
    print(sentiment_counts)

    print("\n===== AVERAGE SENTIMENT SCORE PER STOCK =====")
    avg_sentiment = news_df.groupby("symbol")["sentiment_score"].mean().sort_values(ascending=False)
    print(avg_sentiment)

    print("\n===== COMBINED SIGNAL =====")
    for _, stock in stocks_df.iterrows():
        symbol = stock["symbol"]
        stock_news = news_df[news_df["symbol"] == symbol]

        if stock_news.empty:
            print(
                f"{symbol}: Price {'UP' if stock['change'] > 0 else 'DOWN'} "
                f"| Sentiment NULL | Signal: NULL"
            )
            continue

        avg = stock_news["sentiment_score"].mean()
        price_dir = "UP" if stock["change"] > 0 else "DOWN"
        sent_dir = "POSITIVE" if avg > 0 else "NEGATIVE"
        alignment = "ALIGNED" if (
            (price_dir == "UP" and sent_dir == "POSITIVE") or
            (price_dir == "DOWN" and sent_dir == "NEGATIVE")
        ) else "DIVERGING"
        print(f"{symbol}: Price {price_dir} | Sentiment {sent_dir} | Signal: {alignment}")


if __name__ == "__main__":
    analyze("full_data.json")