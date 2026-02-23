import yfinance as yf
import random
from tabulate import tabulate
from stock import Stock
from portfolio import Portfolio
from database import DatabaseManager
from view import CLIView
from ai_service import AIFinancialAnalyst

class MainController:
    def __init__(self):
        self.turn = 1
        self.db = DatabaseManager()
        self.view = CLIView()
        self.ai = AIFinancialAnalyst()
        self.portfolio = Portfolio(owner_name="Eden") # Eden
        self.symbols = ["AAPL", "TSLA", "GOOGL", "NVDA", "MSFT"]
        self.market = {}
        self.initial_prices = {}
        self.last_ai_advice = ""
        
        # Initial sync and first AI call
        self._sync_market()
        self._fetch_initial_ai_advice()
        self.portfolio_history = [self._get_portfolio_value()]

    def _sync_market(self):
        print("\n🌐 Connecting to real-time market data...")
        for sym in self.symbols:
            try:
                price = yf.Ticker(sym).fast_info.last_price
                self.market[sym] = Stock(sym, sym, round(price, 2), 0.12)
                if sym not in self.initial_prices: self.initial_prices[sym] = price
            except:
                self.market[sym] = Stock(sym, sym, 150.0, 0.12)
                self.initial_prices[sym] = 150.0

    def _fetch_initial_ai_advice(self):
        data = self.ai.generate_market_news()
        self.last_ai_advice = data['advice']
        self.view.display_news(data['headline'], data['advice'], data['sentiment'])

    def _execute_ai_trade(self):
        """Autonomous execution of AI recommendation using 50% of cash."""
        if not self.last_ai_advice: return

        parts = self.last_ai_advice.split()
        if len(parts) < 2: return
        
        action, sym = parts[0], parts[1]
        if sym not in self.market: return

        if "BUY" in action:
            # Aggressive: Spend 50% of cash
            qty = int((self.portfolio.cash * 0.5) // self.market[sym].price)
            if qty > 0: self._execute_transaction("BUY", sym, qty)
            else: self.view.display_message("AI: Not enough cash to execute this BUY.")
        elif "SELL" in action:
            # Sell 100% of holdings for that symbol
            qty = self.portfolio.holdings.get(sym, 0)
            if qty > 0: self._execute_transaction("SELL", sym, qty)
            else: self.view.display_message(f"AI: You don't own {sym} to sell it.")

    def _advance_turn(self):
        self.turn += 1
        data = self.ai.generate_market_news()
        self.last_ai_advice = data['advice']
        self.view.display_news(data['headline'], data['advice'], data['sentiment'])
        
        bias = 0.08 if "BULLISH" in data['sentiment'] else -0.08 if "BEARISH" in data['sentiment'] else 0.0
        for stock in self.market.values():
            stock.update_price(random.uniform(-stock.volatility, stock.volatility) + bias)
        
        self.portfolio_history.append(self._get_portfolio_value())
        self.view.display_message(f"--- TURN {self.turn} STARTED ---")

    def _show_history_and_graph(self):
        perf = {s: ((st.price - self.initial_prices[s])/self.initial_prices[s])*100 for s, st in self.market.items()}
        alloc = {"Cash": round(self.portfolio.cash, 2)}
        for s, q in self.portfolio.holdings.items():
            if q > 0: alloc[s] = round(q * self.market[s].price, 2)
        self.view.display_all_histograms(self.portfolio_history, perf, alloc)

    def _execute_transaction(self, t_type, sym, qty):
        try:
            if t_type == "BUY": self.portfolio.add_position(sym, qty, self.market[sym].price)
            else: self.portfolio.remove_position(sym, qty, self.market[sym].price)
            self.db.log_transaction(self.turn, t_type, sym, qty, self.market[sym].price)
            self.view.display_message(f"TRADE SUCCESS: {t_type} {qty}x {sym}")
        except Exception as e: self.view.display_message(f"ERROR: {str(e)}")

    def run(self):
        while True:
            self.view.show_menu(self.turn)
            c = self.view.get_input("Select Action (1-8)")
            if c == "1": self._show_market()
            elif c == "2": self.view.display_portfolio(self.portfolio, self._get_portfolio_value())
            elif c == "3": self._manual_trade("BUY")
            elif c == "4": self._manual_trade("SELL")
            elif c == "5": self._execute_ai_trade()
            elif c == "6": self._advance_turn()
            elif c == "7": self._show_history_and_graph()
            elif c == "8": break

    def _get_portfolio_value(self):
        total = self.portfolio.cash
        for s, q in self.portfolio.holdings.items(): total += q * self.market[s].price
        return round(total, 2)

    def _show_market(self):
        data = [[s.symbol, f"{s.price:.2f}$", f"{s.volatility*100:.0f}%"] for s in self.market.values()]
        print(tabulate(data, headers=["Symbol", "Price", "Volatility"], tablefmt="fancy_grid"))

    def _manual_trade(self, t):
        self._show_market()
        s = self.view.get_input("Symbol").upper()
        q = self.view.get_input("Qty")
        if s in self.market and q.isdigit(): self._execute_transaction(t, s, int(q))