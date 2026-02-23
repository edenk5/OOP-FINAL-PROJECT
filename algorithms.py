from abc import ABC, abstractmethod
import random

class TradingStrategy(ABC):
    """Abstract Base Class for trading algorithms."""
    
    @abstractmethod
    def execute_trade(self, market_data: dict, cash: float) -> dict:
        """Returns a dict with instructions: {'symbol': str, 'action': 'BUY'/'SELL', 'qty': int}"""
        pass

class RandomBot(TradingStrategy):
    """A bot that buys and sells completely randomly (like a monkey playing darts)."""
    def execute_trade(self, market_data: dict, cash: float) -> dict:
        symbol = random.choice(list(market_data.keys()))
        action = random.choice(["BUY", "SELL", "HOLD"])
        qty = random.randint(1, 5)
        return {"symbol": symbol, "action": action, "qty": qty}

class MomentumBot(TradingStrategy):
    """A bot that buys stocks that are going up and sells those going down."""
    def execute_trade(self, market_data: dict, cash: float) -> dict:
        # Finds the most volatile/moving stock
        best_stock = max(market_data.values(), key=lambda s: s.volatility)
        
        # If we have enough cash, buy it
        if cash > best_stock.price * 2:
            return {"symbol": best_stock.symbol, "action": "BUY", "qty": 2}
        return {"symbol": best_stock.symbol, "action": "HOLD", "qty": 0}