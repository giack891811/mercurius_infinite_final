"""
main.py
========
Punto di ingresso principale per l'esecuzione del sistema Mercurius∞.

Funzionalità:
- Caricamento configurazioni e logging
- Inizializzazione pipeline: dati, features, modello
- Esecuzione strategia di trading adattiva
- Simulazione esperienza cognitiva (AI Evolutiva)
"""

import logging
from utils.logger import setup_logger
from utils.config_loader import load_config
from data.market_data_handler import MarketDataHandler
from data.feature_engineering import FeatureEngineer
from models.model_trainer import ModelTrainer
from strategies.strategy_executor import StrategyExecutor
from agents.adaptive_trader import AdaptiveTrader
from agents.memory_manager import MemoryManager

# 🔁 Controllore per l'autonomia cognitiva
from orchestrator.autonomy_controller import AutonomyController


def initialize_system():
    """Inizializza il sistema con tutte le componenti core."""
    config = load_config("config.yaml")
    logger = setup_logger(name="MercuriusMain")

    logger.info("📦 Caricamento configurazione completato.")
    logger.debug(f"Configurazione caricata: {config}")

    memory = MemoryManager(config)
    data_handler = MarketDataHandler(config)
    feature_engineer = FeatureEngineer(config)
    model_trainer = ModelTrainer(config)
    strategy = StrategyExecutor(config)
    agent = AdaptiveTrader(config, memory, model_trainer, strategy)

    logger.info("🔧 Sistema inizializzato correttamente.")
    return {
        "config": config,
        "logger": logger,
        "memory": memory,
        "data_handler": data_handler,
        "feature_engineer": feature_engineer,
        "model_trainer": model_trainer,
        "strategy": strategy,
        "agent": agent
    }


def run_pipeline(components: dict):
    """Esegue il ciclo completo di analisi, apprendimento e trading."""
    logger = components["logger"]
    data_handler = components["data_handler"]
    feature_engineer = components["feature_engineer"]
    model_trainer = components["model_trainer"]
    strategy = components["strategy"]
    agent = components["agent"]

    logger.info("🚀 Avvio pipeline operativa Mercurius∞...")

    raw_data = data_handler.fetch_market_data()
    logger.info(f"📊 Dati di mercato ricevuti: {len(raw_data)} records")

    features = feature_engineer.transform(raw_data)
    logger.info("🧠 Feature engineering completato.")

    model = model_trainer.train(features)
    logger.info("🤖 Modello addestrato con successo.")

    signals = strategy.generate_signals(model, features)
    logger.info(f"📈 Segnali generati: {len(signals)}")

    agent.execute_trades(signals)
    logger.info("✅ Trade eseguiti con successo.")


def simulate_experience():
    """Simula esperienze per il controller cognitivo autonomo."""
    print("\n🧠 Avvio simulazione esperienze cognitive...\n")
    auto = AutonomyController()

    experiences = [
        {"action": "Avvia scansione", "outcome": "Area rilevata", "success": True, "context": {}},
        {"action": "Connessione API", "outcome": "Errore 500", "success": False, "context": {"error": "Internal Server Error"}},
        {"action": "Naviga percorso", "outcome": "Riuscito", "success": True, "context": {"speed": "3.2m/s"}},
    ]

    for exp in experiences:
        output = auto.process_experience(
            action=exp["action"],
            outcome=exp["outcome"],
            success=exp["success"],
            context=exp["context"]
        )
        print("\n🧪 Esperienza:")
        print(f" - Riflesso: {output['reflection']}")
        print(f" - Apprendimento: {output['learning']}")

    print("\n📊 Riepilogo Cognitivo:")
    print(auto.summarize_autonomy())

    print("\n📘 Insight Globali:")
    print(auto.report_insights())


if __name__ == "__main__":
    components = initialize_system()
    run_pipeline(components)
    simulate_experience()
