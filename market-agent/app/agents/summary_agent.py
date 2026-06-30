from app.agents.base_agent import BaseAgent


SYSTEM_PROMPT = """
You are a senior financial analyst writing a daily market intelligence report.

Given analysis results from multiple specialist agents, write a clear, concise
market brief that a portfolio manager would actually want to read.

Rules:
- Use professional but readable language
- Lead with the most important insight
- Keep it under 150 words
- End with one line: "Recommendation: ..."
- Plain text only, no markdown, no bullet points
"""


class SummaryAgent(BaseAgent):

    def __init__(self):
        super().__init__(
            name="SummaryAgent",
            system_prompt=SYSTEM_PROMPT
        )

    def summarize(self, all_results: list[dict]) -> str:
        report_data = "\n\n".join([
            f"""SYMBOL: {r['symbol']}
Price: ${r['stock']['price']} | Trend: {r['trend']['trend']} ({r['trend']['momentum']} momentum)
Sentiment: {r['sentiment']['overall_sentiment']} (confidence: {r['sentiment']['confidence']})
Key Signal: {r['sentiment']['key_signal']}
Risk Level: {r['risk']['risk_level']}
Recommendation: {r['risk']['recommendation']}""".strip()
            for r in all_results
        ])

        prompt = f"""
Write a market intelligence brief based on the following agent analysis.
Plain text only, no markdown:

{report_data}

Write the brief now:
"""
        return self.run(prompt)