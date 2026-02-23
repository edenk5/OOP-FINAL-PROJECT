from exceptions import InsufficientFundsError, InsufficientSharesError

class Portfolio:
    def __init__(self, owner_name: str, cash: float = 10000.0):
        self.owner_name = owner_name
        self._cash = cash  # Encapsulation
        self.holdings = {} # Dictionary: {symbol: quantity}

    @property
    def cash(self) -> float:
        return round(self._cash, 2)

    def add_position(self, symbol: str, quantity: int, price: float):
        cost = quantity * price
        if cost > self._cash:
            raise InsufficientFundsError(cost, self._cash)
        
        self._cash -= cost
        self.holdings[symbol] = self.holdings.get(symbol, 0) + quantity

    def remove_position(self, symbol: str, quantity: int, price: float):
        if self.holdings.get(symbol, 0) < quantity:
            raise InsufficientSharesError("Transaction Failed: Not enough shares to sell!")
        
        revenue = quantity * price
        self._cash += revenue
        self.holdings[symbol] -= quantity
        
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]

    def __add__(self, amount: float):
        """Operator Overloading (Dunder __add__): portfolio + 1000 adds cash."""
        self._cash += amount
        return self

    def __len__(self):
        """Dunder __len__: Returns the total number of physical shares owned."""
        return sum(self.holdings.values())

    def __getitem__(self, symbol: str):
        """Dunder __getitem__: Allows accessing stock quantities like a dictionary (e.g., portfolio['AAPL'])."""
        if symbol not in self.holdings:
            raise KeyError(f"You do not own any shares of {symbol}.")
        return self.holdings[symbol]