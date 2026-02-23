class TradingError(Exception):
    """Base class for exceptions in this module."""
    pass

class InsufficientFundsError(TradingError):
    """Raised when the portfolio doesn't have enough cash for a transaction."""
    def __init__(self, required: float, available: float):
        self.message = f"Transaction Failed: Need {required}$, but only have {available}$."
        super().__init__(self.message)

class InsufficientSharesError(TradingError):
    """Raised when trying to sell more shares than owned."""
    pass