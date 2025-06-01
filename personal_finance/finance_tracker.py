# personal_finance/finance_tracker.py
"""
Modulo: finance_tracker.py
Descrizione: Traccia spese personali da CSV/JSON e genera report mensile.
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

DATA_FILE = Path("personal_finance/expenses.csv")
DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

class FinanceTracker:
    def __init__(self):
        if DATA_FILE.exists():
            self.df = pd.read_csv(DATA_FILE)
        else:
            self.df = pd.DataFrame(columns=["date", "category", "amount", "note"])

    def add_expense(self, amount: float, category: str, note: str = ""):
        new = {"date": datetime.utcnow().date(), "category": category, "amount": amount, "note": note}
        self.df = self.df.append(new, ignore_index=True)
        self.df.to_csv(DATA_FILE, index=False)

    def monthly_summary(self, month: str | None = None):
        month = month or datetime.utcnow().strftime("%Y-%m")
        df_month = self.df[self.df["date"].astype(str).str.startswith(month)]
        return df_month.groupby("category")["amount"].sum().to_dict()
