from app.agents.base_agent import BaseAgent
from app.agents.sentiment_agent import parse_json_safe


SYSTEM_PROMPT = """
You are a stock market trend analyst.

Given a stock's current price data and recent history, you must:
1. Identify the price trend: UPTREND, DOWNTREND, or SIDEWAYS
2. Assess momentum strength: STRONG, MODERATE, WEAK
3. Suggest a short-term outlook for the next 24 hours

Respond ONLY in valid JSON. No markdown, no extra text:
{
  "symbol": "TSLA",
  "trend": "UPTREND",
  "momentum": "MODERATE",
  "price_change_pct": "+2.3%",
  "volume_signal": "Above average volume confirms trend",
  "outlook": "Likely to continue upward if volume holds",
  "confidence": 0.74
}
"""


class TrendAgent(BaseAgent):

    def __init__(self):
        super().__init__(
            name="TrendAgent",
            system_prompt=SYSTEM_PROMPT
        )

    def analyze(self, stock: dict, history: list[dict] = None) -> dict:
        fallback = {
            "symbol": stock["symbol"],
            "trend": "SIDEWAYS",
            "momentum": "WEAK",
            "price_change_pct": stock.get("change_pct", "0%"),
            "volume_signal": "Unable to assess",
            "outlook": "Insufficient data",
            "confidence": 0.0
        }

        history_text = ""
        if history:
            history_text = "\nRecent price history:\n" + "\n".join([
                f"  {h['fetched_at']}: ${h['price']}"
                for h in history[:10]
            ])

        prompt = f"""
Analyze price trend for: {stock['symbol']}

Current data:
- Price: ${stock['price']}
- Change today: {stock['change']} ({stock['change_pct']})
- Volume: {stock['volume']}
{history_text}

Return only a JSON object. No extra text.
"""
        response = self.run(prompt)
        return parse_json_safe(response, fallback)