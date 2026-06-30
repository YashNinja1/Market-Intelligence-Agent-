from app.agents.base_agent import BaseAgent
from app.agents.sentiment_agent import parse_json_safe


SYSTEM_PROMPT = """
You are a financial risk analyst.

Given combined stock price data and news sentiment, identify:
1. Key risk factors (max 3)
2. Risk level: LOW, MEDIUM, HIGH, CRITICAL
3. Whether any immediate action alerts are needed

Respond ONLY in valid JSON. No markdown, no extra text:
{
  "symbol": "TSLA",
  "risk_level": "MEDIUM",
  "risk_factors": [
    "High volatility with 4.2% daily swing",
    "Bearish news sentiment contradicts price rise"
  ],
  "alert": false,
  "alert_message": null,
  "recommendation": "Monitor closely. Diverging signals suggest caution."
}
"""


class RiskAgent(BaseAgent):

    def __init__(self):
        super().__init__(
            name="RiskAgent",
            system_prompt=SYSTEM_PROMPT
        )

    def analyze(self, stock: dict, sentiment_result: dict) -> dict:
        fallback = {
            "symbol": stock["symbol"],
            "risk_level": "MEDIUM",
            "risk_factors": ["Unable to fully assess risk"],
            "alert": False,
            "alert_message": None,
            "recommendation": "Manual review recommended"
        }

        prompt = f"""
Assess risk for: {stock['symbol']}

Price data:
- Current price: ${stock['price']}
- Change: {stock['change']} ({stock['change_pct']})
- Volume: {stock['volume']}

Sentiment analysis:
- Overall sentiment: {sentiment_result.get('overall_sentiment')}
- Confidence: {sentiment_result.get('confidence')}
- Key signal: {sentiment_result.get('key_signal')}
- Bullish articles: {sentiment_result.get('bullish_count')}
- Bearish articles: {sentiment_result.get('bearish_count')}

Return only a JSON object. No extra text.
"""
        response = self.run(prompt)
        return parse_json_safe(response, fallback)