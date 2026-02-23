from tabulate import tabulate
import matplotlib.pyplot as plt
import platform
import subprocess

class CLIView:
    def show_menu(self, current_turn: int):
        print("\n" + "═"*60)
        print(f" 🤖 AI-AUTONOMOUS TRADER | TURN: {current_turn} ")
        print("═"*60)
        print("1. View Market Board       2. View Portfolio")
        print("3. Buy Stock (Manual)      4. Sell Stock (Manual)")
        print("5. EXECUTE AI TRADE        6. END TURN (Simulate)")
        print("7. VIEW ANALYSIS CHARTS    8. EXIT")
        print("─"*60)

    def display_news(self, headline: str, advice: str, sentiment: str):
        color = "🟢" if "BULLISH" in sentiment else "🔴" if "BEARISH" in sentiment else "⚪"
        print(f"\n{color} NEWS: {headline}")
        print(f"💡 AI SYSTEM RECOMMENDATION: {advice}")

    def display_all_histograms(self, history, performance, allocation):
        """Generates three professional histograms side-by-side."""
        plt.figure(figsize=(18, 6))

        # Histogram 1: Portfolio Growth
        plt.subplot(1, 3, 1)
        plt.bar(range(1, len(history) + 1), history, color='#3498db', edgecolor='black')
        plt.title('Total Portfolio Value ($)')
        plt.xlabel('Turns')

        # Histogram 2: Stock Performance %
        plt.subplot(1, 3, 2)
        symbols = list(performance.keys())
        changes = list(performance.values())
        colors = ['#2ecc71' if x >= 0 else '#e74c3c' for x in changes]
        plt.bar(symbols, changes, color=colors, edgecolor='black')
        plt.axhline(0, color='black', linewidth=1)
        plt.title('Stock Profit/Loss (%)')

        # Histogram 3: Investment in Dollars
        plt.subplot(1, 3, 3)
        assets = list(allocation.keys())
        values = list(allocation.values())
        plt.bar(assets, values, color='#f1c40f', edgecolor='black')
        plt.title('Asset Distribution (USD)')

        plt.tight_layout()
        plt.savefig("market_analysis.png")
        plt.close()
        
        print("\n📊 Charts updated! Opening 'market_analysis.png'...")
        self._open_image("market_analysis.png")

    def _open_image(self, file_name: str):
        try:
            if platform.system() == 'Darwin': # macOS auto-open
                subprocess.call(('open', file_name))
        except: pass

    def get_input(self, p): return input(f"👉 {p}: ").strip()
    def display_message(self, m): print(f"\n📢 {m}")
    def display_portfolio(self, portfolio, val):
        print(f"\n--- 💼 PORTFOLIO VALUE: {val}$ | CASH: {portfolio.cash}$ ---")
        if portfolio.holdings:
            data = [[s, q] for s, q in portfolio.holdings.items()]
            print(tabulate(data, headers=["Symbol", "Shares"], tablefmt="grid"))