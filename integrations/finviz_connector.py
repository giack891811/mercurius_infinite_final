"""
finviz_connector.py
===================
Scraping dei fondamentali e notizie da Finviz per Mercurius∞.
"""

import requests
from bs4 import BeautifulSoup


class FinvizConnector:
    def __init__(self):
        self.base = "https://finviz.com/quote.ashx?t="

    def fetch(self, symbol):
        url = self.base + symbol
        headers = {"User-Agent": "Mozilla/5.0"}
        soup = BeautifulSoup(requests.get(url, headers=headers).text, "html.parser")
        data = {}
        for row in soup.select("table.snapshot-table2 tr"):
            cells = row.find_all("td")
            for i in range(0, len(cells), 2):
                if i+1 < len(cells):
                    key = cells[i].text.strip()
                    val = cells[i+1].text.strip()
                    data[key] = val
        return data
