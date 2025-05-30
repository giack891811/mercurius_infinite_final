"""
tradingview_feed.py
===================
Feed di dati simulato compatibile con layout TradingView. Simula ticker in tempo reale.
"""

import random
import time
from threading import Thread

class TradingViewFeed:
    def __init__(self, symbols, callback=None, interval=1.0):
        self.symbols = symbols
        self.interval = interval
        self.callback = callback
        self.running = False

    def _generate_tick(self, symbol):
        price = round(random.uniform(100, 500), 2)
        volume = random.randint(1000, 10000)
        return {
            "symbol": symbol,
            "price": price,
            "volume": volume,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

    def _run_feed(self):
        while self.running:
            for symbol in self.symbols:
                tick = self._generate_tick(symbol)
                if self.callback:
                    self.callback(tick)
            time.sleep(self.interval)

    def start(self):
        self.running = True
        Thread(target=self._run_feed, daemon=True).start()

    def stop(self):
        self.running = False
