from dataclasses import dataclass

@dataclass
class Stock:
    """Model representing a single stock in the market."""
    symbol: str
    name: str
    price: float
    volatility: float

    def update_price(self, percentage_change: float):
        """Encapsulation: Price is updated only through this method."""
        self.price = round(self.price * (1 + percentage_change), 2)
        if self.price < 1.0:
            self.price = 1.0 # Minimum price

    def __repr__(self):
        """Dunder method for developer representation."""
        return f"Stock({self.symbol}, {self.price}$)"

    def __str__(self):
        """Dunder method for user-friendly string."""
        return f"{self.symbol} ({self.name}) - {self.price}$"