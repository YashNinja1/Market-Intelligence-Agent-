import logging
from app.agents.sentiment_agent import SentimentAgent
from app.agents.trend_agent import TrendAgent
from app.agents.risk_agent import RiskAgent
from app.agents.summary_agent import SummaryAgent
from app.core.database import (
    get_latest_stocks,
    get_news_by_symbol,
    get_stock_history
)

logger = logging.getLogger(__name__)


class MarketOrchestrator:
    """
    Runs all agents in sequence for each stock symbol.
    Aggregates results into a final intelligence report.
    """

    def __init__(self):
        self.sentiment_agent = SentimentAgent()
        self.trend_agent = TrendAgent()
        self.risk_agent = RiskAgent()
        self.summary_agent = SummaryAgent()
        logger.info("MarketOrchestrator initialized with 4 agents")

    def analyze_symbol(self, stock: dict) -> dict:
        """Run all agents for a single stock symbol."""
        symbol = stock["symbol"]
        logger.info(f"Analyzing {symbol}...")

        # 1. Get news from DB
        articles = get_news_by_symbol(symbol)

        # 2. Get price history from DB
        history = get_stock_history(symbol)

        # 3. Run agents in sequence
        sentiment_result = self.sentiment_agent.analyze(symbol, articles)
        logger.info(f"{symbol} sentiment: {sentiment_result['overall_sentiment']}")

        trend_result = self.trend_agent.analyze(stock, history)
        logger.info(f"{symbol} trend: {trend_result['trend']}")

        risk_result = self.risk_agent.analyze(stock, sentiment_result)
        logger.info(f"{symbol} risk: {risk_result['risk_level']}")

        return {
            "symbol": symbol,
            "stock": stock,
            "sentiment": sentiment_result,
            "trend": trend_result,
            "risk": risk_result
        }

    def run(self) -> dict:
        """
        Full pipeline:
        1. Load all stocks from DB
        2. Run all agents per stock
        3. Generate summary report
        """
        stocks = get_latest_stocks()
        if not stocks:
            return {"error": "No stock data found. Run a fetch first."}

        logger.info(f"Running orchestrator on {len(stocks)} stocks...")

        # Analyze each stock
        all_results = []
        for stock in stocks:
            result = self.analyze_symbol(stock)
            all_results.append(result)

        # Generate final summary report
        logger.info("Generating final market intelligence report...")
        report = self.summary_agent.summarize(all_results)

        return {
            "analysis": all_results,
            "report": report,
            "stocks_analyzed": len(all_results)
        }