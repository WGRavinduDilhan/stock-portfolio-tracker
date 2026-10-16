import json
import os
from peewee import SqliteDatabase, Model, CharField, FloatField, IntegerField

# ── SQLite setup (peewee ORM) ────────────────────────────────────────────────
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "portfolio.db")
db = SqliteDatabase(DB_PATH)


class HoldingModel(Model):
    """SQLite table that maps one row per ticker."""
    ticker    = CharField(primary_key=True)
    shares    = FloatField()
    buy_price = FloatField()

    class Meta:
        database = db
        table_name = "holdings"


# Create table if it doesn't exist yet
db.connect(reuse_if_open=True)
db.create_tables([HoldingModel], safe=True)
db.close()


# ── Portfolio class ──────────────────────────────────────────────────────────
class Portfolio:
    def __init__(self):
        self.holdings: dict = {}  # { ticker: {shares, buy_price} }

    # ── CRUD ─────────────────────────────────────────────────────────────────
    def add_stock(self, ticker: str, shares: float, buy_price: float) -> None:
        """Add or update (average cost) a stock in the portfolio."""
        if ticker in self.holdings:
            old_shares    = self.holdings[ticker]["shares"]
            old_price     = self.holdings[ticker]["buy_price"]
            total_shares  = old_shares + shares
            avg_price     = (old_shares * old_price + shares * buy_price) / total_shares
            self.holdings[ticker] = {"shares": total_shares, "buy_price": avg_price}
        else:
            self.holdings[ticker] = {"shares": shares, "buy_price": buy_price}

        self.save_to_db()  # Auto-persist after every change

    def remove_stock(self, ticker: str) -> None:
        """Remove a stock from the portfolio."""
        self.holdings.pop(ticker, None)
        # Delete from SQLite too
        try:
            db.connect(reuse_if_open=True)
            HoldingModel.delete().where(HoldingModel.ticker == ticker).execute()
            db.close()
        except Exception as e:
            print(f"DB remove error for {ticker}: {e}")

    def get_holdings(self) -> dict:
        """Return current holdings dict."""
        return self.holdings

    # ── Persistence: JSON ────────────────────────────────────────────────────
    JSON_PATH = os.path.join(os.path.dirname(__file__), "..", "portfolio.json")

    def save_to_json(self, path: str = None) -> None:
        """Write holdings to portfolio.json."""
        path = path or self.JSON_PATH
        try:
            with open(path, "w") as f:
                json.dump(self.holdings, f, indent=2)
        except Exception as e:
            print(f"JSON save error: {e}")

    def load_from_json(self, path: str = None) -> None:
        """Load holdings from portfolio.json (used as fallback)."""
        path = path or self.JSON_PATH
        try:
            if os.path.exists(path):
                with open(path) as f:
                    self.holdings = json.load(f)
        except Exception as e:
            print(f"JSON load error: {e}")

    # ── Persistence: SQLite via Peewee ───────────────────────────────────────
    def save_to_db(self) -> None:
        """
        Upsert all current holdings into SQLite.
        Uses get_or_create + save — works reliably across all peewee versions.
        Falls back to JSON persistence on any DB error.
        """
        try:
            db.connect(reuse_if_open=True)
            with db.atomic():
                for ticker, data in self.holdings.items():
                    obj, created = HoldingModel.get_or_create(
                        ticker=ticker,
                        defaults={
                            "shares":    data["shares"],
                            "buy_price": data["buy_price"],
                        },
                    )
                    if not created:
                        obj.shares    = data["shares"]
                        obj.buy_price = data["buy_price"]
                        obj.save()
            db.close()
            # Keep JSON in sync as a human-readable backup
            self.save_to_json()
        except Exception as e:
            print(f"DB save error: {e}")
            self.save_to_json()  # Fallback to JSON

    def load_from_db(self) -> None:
        """Load holdings from SQLite on startup."""
        try:
            db.connect(reuse_if_open=True)
            rows = HoldingModel.select()
            for row in rows:
                self.holdings[row.ticker] = {
                    "shares":    row.shares,
                    "buy_price": row.buy_price,
                }
            db.close()
        except Exception as e:
            print(f"DB load error: {e}. Falling back to JSON.")
            self.load_from_json()
