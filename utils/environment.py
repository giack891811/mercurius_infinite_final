"""
Modulo: environment.py
Responsabilità: Caricare e gestire le variabili di ambiente per Mercurius∞
Autore: Mercurius∞ Engineer Mode
"""

import os
from dotenv import load_dotenv

class Environment:
    """
    Carica il file .env e fornisce accesso centralizzato alle variabili di ambiente.
    """

    def __init__(self, dotenv_path: str = ".env"):
        self.loaded = False
        self.dotenv_path = dotenv_path
        self.load_environment()

    def load_environment(self):
        """
        Carica le variabili da .env nel sistema.
        """
        if os.path.exists(self.dotenv_path):
            load_dotenv(dotenv_path=self.dotenv_path)
            self.loaded = True
        else:
            raise FileNotFoundError(f"File .env non trovato in {self.dotenv_path}")

    def get(self, key: str, default=None):
        """
        Recupera una variabile d'ambiente.
        """
        return os.getenv(key, default)

    def get_openai_config(self) -> dict:
        return {
            "use_openai": self.get("USE_OPENAI") == "1",
            "api_key": self.get("OPENAI_API_KEY"),
            "chat_model": self.get("OPENAI_CHAT_MODEL"),
            "embed_model": self.get("OPENAI_EMBED_MODEL")
        }

    def get_web_monitor_credentials(self) -> dict:
        return {
            "user": self.get("WM_USER"),
            "password": self.get("WM_PASS")
        }

    def get_mcp_config(self) -> dict:
        return {
            "token": self.get("MCP_TOKEN"),
            "introspect_url": self.get("MCP_INTROSPECT_URL")
        }

    def get_mercurius_api_key(self) -> str:
        return self.get("MERCURIUS_API_KEY")

    def get_run_mode(self) -> str:
        """Restituisce la modalità operativa di AION."""
        return self.get("AION_RUN_MODE", "dialogic-autonomous")
