# evolution/auto_updater.py

"""
Modulo: auto_updater.py
Descrizione: Sistema di auto-evoluzione per Mercurius∞.
Analizza contenuti scaricati, genera codice, verifica in sandbox e salva come nuovo modulo.
"""

import os
from core.sandbox_executor import SandboxExecutor
from evolution.web_scraper import WebScraper
from memory.synaptic_log import SynapticLog
import re
import datetime


class AutoUpdater:
    def __init__(self):
        self.scraper = WebScraper()
        self.sandbox = SandboxExecutor()
        self.logger = SynapticLog()

    def evolve_from_url(self, url: str, save_dir: str = "modules/generated/") -> str:
        """
        Scarica un contenuto e tenta di generare codice eseguibile da esso.
        """
        os.makedirs(save_dir, exist_ok=True)
        raw_html = self.scraper.get_text_from_url(url)
        code_blocks = self.scraper.extract_code_blocks(raw_html)

        generated_files = []
        for i, code in enumerate(code_blocks):
            if not self.sandbox.static_analysis(code):
                continue

            result = self.sandbox.run_sandboxed(code)
            if result["success"]:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                file_name = f"{save_dir}/evo_snippet_{i}_{timestamp}.py"
                with open(file_name, "w") as f:
                    f.write(code)
                self.logger.log_event("AutoUpdater", "Generated", file_name)
                generated_files.append(file_name)

        return f"✅ {len(generated_files)} snippet salvati da {url}"
