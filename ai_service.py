from google import genai

class AIFinancialAnalyst:
    def __init__(self):
        """Initializes the AI with the latest Gemini 2.0 model."""
        self.api_key = "AIzaSyAe2u-M20eHCIVwkb0hYLLNot5SyceuD2U"
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = "gemini-2.0-flash" 

    def generate_market_news(self) -> dict:
        """Forces the AI to provide decisive trading signals (BUY/SELL)."""
        prompt = (
            "You are an aggressive Wall Street trader. "
            "1. Generate a dramatic 1-sentence financial news headline. "
            "2. You MUST provide a clear 'BUY <symbol>' or 'SELL <symbol>' advice. "
            "Symbols available: AAPL, TSLA, GOOGL, NVDA, MSFT. "
            "Do not suggest 'HOLD'. Be decisive and loud. "
            "Format: Headline | Advice | Sentiment (BULLISH/BEARISH)"
        )
        try:
            print(f"🧠 AI is hunting for the next big move...")
            response = self.client.models.generate_content(model=self.model_name, contents=prompt)
            text = response.text
            parts = text.split('|')
            
            return {
                "headline": parts[0].strip() if len(parts) > 0 else "Market volatility at peak.",
                "advice": parts[1].strip().upper() if len(parts) > 1 else "BUY NVDA",
                "sentiment": parts[2].strip().upper() if len(parts) > 2 else "BULLISH"
            }
        except Exception:
            # High-priority fallback to ensure the game never stops
            return {"headline": "Massive market shift detected.", "advice": "BUY TSLA", "sentiment": "BULLISH"}