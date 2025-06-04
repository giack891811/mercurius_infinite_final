# learning/document_parser.py

"""
Modulo: document_parser.py
Descrizione: Parsing e analisi semantica di contenuti testuali provenienti da PDF e URL per Mercurius∞.
Estrae testi, titoli e concetti chiave.
"""

import fitz  # PyMuPDF
import requests
from bs4 import BeautifulSoup
from typing import List


class DocumentParser:
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Estrae il testo da un file PDF.
        """
        text = ""
        try:
            doc = fitz.open(pdf_path)
            for page in doc:
                text += page.get_text()
            doc.close()
        except Exception as e:
            text = f"[ERRORE PDF]: {e}"
        return text

    def extract_text_from_url(self, url: str) -> str:
        """
        Estrae contenuti leggibili da una pagina web.
        """
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            paragraphs = soup.find_all("p")
            return "\n".join(p.get_text() for p in paragraphs)
        except Exception as e:
            return f"[ERRORE URL]: {e}"

    def extract_keywords(self, content: str, top_n: int = 10) -> List[str]:
        """
        Estrae parole chiave semplici dal contenuto.
        """
        import re
        from collections import Counter

        words = re.findall(r"\b\w{5,}\b", content.lower())
        common = Counter(words).most_common(top_n)
        return [word for word, _ in common]


def parse_document(source: str) -> dict:
    """High level helper to parse a PDF file or URL."""
    parser = DocumentParser()
    if source.lower().startswith("http"):
        text = parser.extract_text_from_url(source)
    else:
        text = parser.extract_text_from_pdf(source)
    keywords = parser.extract_keywords(text)
    return {"text": text, "keywords": keywords}
