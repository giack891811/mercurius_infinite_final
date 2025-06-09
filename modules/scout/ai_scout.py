"""ai_scout.py
==============
Modulo AIScout per Mercurius∞.

Responsabilità: Ricercare nuovi strumenti o dataset AI su varie fonti online
(GitHub, HuggingFace, arXiv, PapersWithCode, siti ufficiali) senza installare
nulla. Produce report utili alla crescita del sistema.
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from typing import List, Dict

import requests

from utils.logger import setup_logger

# Logger dedicato con file sotto logs/ai_scout/
logger = setup_logger("AIScout", logfile="logs/ai_scout/ai_scout.log")


class AIScout:
    """Modulo di scouting AI."""

    def __init__(self) -> None:
        os.makedirs("logs/ai_scout", exist_ok=True)
        logger.info("AIScout initialized")

    # -------------------------- Ricerca -----------------------------------
    def search_new_ai_tools(self, query: str = "artificial intelligence") -> List[Dict[str, str]]:
        """Cerca progetti AI interessanti in varie piattaforme.

        Restituisce una lista di dizionari con informazioni base sul progetto.
        La funzione non installa alcun pacchetto.
        """
        results: List[Dict[str, str]] = []

        # GitHub search
        try:
            gh_resp = requests.get(
                "https://api.github.com/search/repositories",
                params={"q": query, "sort": "stars", "per_page": 5},
                timeout=10,
            )
            gh_resp.raise_for_status()
            for item in gh_resp.json().get("items", []):
                results.append(
                    {
                        "name": item.get("full_name"),
                        "url": item.get("html_url"),
                        "license": item.get("license", {}).get("name", "N/A"),
                        "compatibility": item.get("language", ""),
                        "source": "GitHub",
                    }
                )
        except Exception as exc:  # pragma: no cover - dipendenze rete
            logger.error(f"GitHub search failed: {exc}")

        # HuggingFace models
        try:
            hf_resp = requests.get(
                "https://huggingface.co/api/models",
                params={"search": query, "limit": 5},
                timeout=10,
            )
            hf_resp.raise_for_status()
            for model in hf_resp.json():
                results.append(
                    {
                        "name": model.get("modelId"),
                        "url": f"https://huggingface.co/{model.get('modelId')}",
                        "license": model.get("license", "N/A"),
                        "compatibility": "Transformers",
                        "source": "HuggingFace",
                    }
                )
        except Exception as exc:  # pragma: no cover - dipendenze rete
            logger.error(f"HuggingFace search failed: {exc}")

        # arXiv recent papers
        try:
            import xml.etree.ElementTree as ET

            arxiv_resp = requests.get(
                "http://export.arxiv.org/api/query",
                params={"search_query": query, "start": 0, "max_results": 5},
                timeout=10,
            )
            arxiv_resp.raise_for_status()
            root = ET.fromstring(arxiv_resp.text)
            for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
                title = entry.find("{http://www.w3.org/2005/Atom}title").text
                url = entry.find("{http://www.w3.org/2005/Atom}id").text
                results.append(
                    {
                        "name": title.strip(),
                        "url": url.strip(),
                        "license": "arXiv",
                        "compatibility": "Paper",
                        "source": "arXiv",
                    }
                )
        except Exception as exc:  # pragma: no cover - dipendenze rete
            logger.error(f"arXiv search failed: {exc}")

        # PapersWithCode search
        try:
            pwc_resp = requests.get(
                "https://paperswithcode.com/api/v0/search/",
                params={"q": query, "limit": 5},
                timeout=10,
            )
            pwc_resp.raise_for_status()
            for paper in pwc_resp.json().get("results", []):
                results.append(
                    {
                        "name": paper.get("title"),
                        "url": paper.get("url_abs"),
                        "license": paper.get("open_access_pdf", "N/A"),
                        "compatibility": "Paper",
                        "source": "PapersWithCode",
                    }
                )
        except Exception as exc:  # pragma: no cover - dipendenze rete
            logger.error(f"PapersWithCode search failed: {exc}")

        logger.info(f"Found {len(results)} entries for '{query}'")
        return results

    # ---------------------------- Report ----------------------------------
    def generate_report(
        self, entries: List[Dict[str, str]] | None = None, as_json: bool = False
    ) -> str:
        """Genera un report in formato Markdown o JSON.

        ``entries`` può essere ``None`` per effettuare una ricerca immediata.
        Ritorna il percorso del file generato.
        """
        if entries is None:
            entries = self.search_new_ai_tools()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        ext = "json" if as_json else "md"
        filename = f"logs/ai_scout/report_{timestamp}.{ext}"

        if as_json:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(entries, f, indent=2, ensure_ascii=False)
        else:
            with open(filename, "w", encoding="utf-8") as f:
                f.write("# AIScout Report\n\n")
                for item in entries:
                    f.write(f"## {item.get('name')}\n")
                    f.write(f"- Link: {item.get('url')}\n")
                    f.write(f"- Licenza: {item.get('license')}\n")
                    f.write(f"- Compatibilità: {item.get('compatibility')}\n")
                    f.write(f"- Fonte: {item.get('source')}\n\n")

        logger.info(f"Report generated: {filename}")
        return filename


if __name__ == "__main__":  # pragma: no cover - manual run
    scout = AIScout()
    data = scout.search_new_ai_tools()
    scout.generate_report(data)
