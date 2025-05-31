# evolution/web_scraper.py

"""
Modulo: web_scraper.py
Descrizione: Sistema di acquisizione automatica per l’auto-evoluzione di Mercurius∞.
Scarica, estrae e indicizza contenuti testuali e di codice da pagine web, GitHub e documentazione.
"""

import requests
from bs4 import BeautifulSoup
from typing import List


class WebScraper:
    def __init__(self, user_agent: str = "MercuriusBot/1.0"):
        self.headers = {"User-Agent": user_agent}

    def get_text_from_url(self, url: str) -> str:
        """
        Scarica testo leggibile da una pagina web.
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code != 200:
                return f"[Errore HTTP {response.status_code}]"

            soup = BeautifulSoup(response.text, "html.parser")
            texts = [p.get_text() for p in soup.find_all(["p", "pre", "code", "li"])]
            return "\n".join(texts).strip()

        except Exception as e:
            return f"[Errore scraping]: {e}"

    def extract_code_blocks(self, html_text: str) -> List[str]:
        """
        Estrae blocchi <code> o <pre> come frammenti di codice.
        """
        soup = BeautifulSoup(html_text, "html.parser")
        code_blocks = soup.find_all(["code", "pre"])
        return [block.get_text() for block in code_blocks if block.get_text()]
