import sqlite3
from utils import audit_logger

class DatabaseManager:
    def __init__(self, db_name="algotrade.sqlite"):
        self.db_name = db_name
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_name) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    turn INTEGER,
                    type TEXT,
                    symbol TEXT,
                    quantity INTEGER,
                    price REAL,
                    total REAL
                )''')

    @audit_logger   # <--- Here is our custom decorator!
    def log_transaction(self, turn: int, tx_type: str, symbol: str, quantity: int, price: float):
        total = quantity * price
        with sqlite3.connect(self.db_name) as conn:
            conn.execute("INSERT INTO transactions (turn, type, symbol, quantity, price, total) VALUES (?, ?, ?, ?, ?, ?)",
                         (turn, tx_type, symbol, quantity, price, total))

    def get_history(self):
        history = []
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.execute("SELECT turn, type, symbol, quantity, price, total FROM transactions ORDER BY id DESC LIMIT 10")
            for row in cursor.fetchall():
                history.append(row)
        return history