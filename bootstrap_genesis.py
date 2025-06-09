import os
import yaml
from ai_launcher import ensure_ai_online
from core.orchestrator import Orchestrator

CONFIG_FILE = "config/config.yaml"


def load_config(path: str = CONFIG_FILE) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def check_agents(cfg: dict) -> None:
    agents = cfg.get("agents", {}).get("enabled", [])
    print(f"🔎 Agenti abilitati: {', '.join(agents) if agents else 'nessuno'}")


def main() -> None:
    print("🚀 Bootstrap GENESIS mode")
    cfg = load_config()
    check_agents(cfg)

    print("🔧 Verifica e avvio servizi locali...")
    ensure_ai_online()

    orchestrator = Orchestrator()
    orchestrator.activate_genesis()
    print("✅ Boot completato. Sistema in esecuzione.")


if __name__ == "__main__":
    main()
