import json
import re
from app.agents.base_agent import BaseAgent
import logging

logging.basicConfig(level=logging.INFO)
def parse_json_safe(response: str, fallback: dict) -> dict:
    """
    Robustly parse JSON from Llama responses.
    Llama sometimes adds explanations before/after JSON — this handles all cases.
    """
    # 1. Strip markdown code fences
    clean = re.sub(r"```json|```", "", response).strip()

    # 2. Try direct parse first
    try:
        return json.loads(clean)
    except json.JSONDecodeError:
        pass

    # 3. Extract first JSON object found anywhere in the text
    match = re.search(r"\{.*?\}", clean, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

    # 4. Extract largest JSON block (handles nested objects)
    matches = re.findall(r"\{[^{}]*\}", clean)
    for m in reversed(matches):  # try largest first
        try:
            return json.loads(m)
        except json.JSONDecodeError:
            continue

    # 5. Give up — return fallback
    logging.warning(f"Could not parse JSON from response: {response[:100]}")
    return fallback


# rest of sentiment_agent.py stays exactly the same
SYSTEM_PROMPT = """
You are a financial sentiment analyst specializing in stock market news.

Given a list of news articles with their sentiment scores for a stock, you must:
1. Analyze the overall market mood for that stock
2. Identify the strongest bullish or bearish signals
3. Rate overall sentiment: STRONGLY_BULLISH, BULLISH, NEUTRAL, BEARISH, STRONGLY_BEARISH
4. Explain your reasoning in 2-3 sentences

You MUST respond with ONLY a valid JSON object, nothing else before or after it:
{
  "symbol": "AAPL",
  "overall_sentiment": "BULLISH",
  "confidence": 0.82,
  "key_signal": "Strong earnings beat drives positive momentum",
  "reasoning": "3 out of 4 articles report strong earnings...",
  "bullish_count": 3,
  "bearish_count": 1
}
"""


class SentimentAgent(BaseAgent):

    def __init__(self):
        super().__init__(
            name="SentimentAgent",
            system_prompt=SYSTEM_PROMPT
        )

    def analyze(self, symbol: str, articles: list[dict]) -> dict:
        fallback = {
            "symbol": symbol,
            "overall_sentiment": "NEUTRAL",
            "confidence": 0.0,
            "key_signal": "No news available",
            "reasoning": "Insufficient data to analyze sentiment.",
            "bullish_count": 0,
            "bearish_count": 0
        }

        if not articles:
            return fallback

        articles_text = "\n".join([
            f"- [{a.get('sentiment', 'Unknown')} | score: {a.get('sentiment_score', 0)}] {a['title']}"
            for a in articles[:10]
        ])

        prompt = f"""
Analyze sentiment for stock: {symbol}

News articles:
{articles_text}

Return ONLY a JSON object, no other text.
"""
        response = self.run(prompt)
        return parse_json_safe(response, fallback)