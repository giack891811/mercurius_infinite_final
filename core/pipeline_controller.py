"""
pipeline_controller.py
=======================
Orchestratore principale delle componenti del sistema Mercurius∞.
Permette di avviare cicli completi di analisi, apprendimento e trading
in modalità batch, streaming o simulata.
"""

from utils.logger import setup_logger
from data.market_data_handler import MarketDataHandler
from data.feature_engineering import FeatureEngineer
from models.model_trainer import ModelTrainer
from strategies.strategy_executor import StrategyExecutor
from agents.adaptive_trader import AdaptiveTrader
from agents.memory_manager import MemoryManager


class PipelineController:
    def __init__(self, config):
        self.logger = setup_logger("PipelineController")
        self.config = config

        self.memory = MemoryManager(config)
        self.data_handler = MarketDataHandler(config)
        self.feature_engineer = FeatureEngineer(config)
        self.model_trainer = ModelTrainer(config)
        self.strategy = StrategyExecutor(config)
        self.agent = AdaptiveTrader(
            config,
            memory_manager=self.memory,
            model_trainer=self.model_trainer,
            strategy_executor=self.strategy,
        )

    def run_batch_session(self):
        """Esegue un'intera sessione di ciclo batch."""
        self.logger.info("🚀 Avvio sessione di pipeline Mercurius∞")

        raw_data = self.data_handler.fetch_market_data()
        features = self.feature_engineer.transform(raw_data)
        model = self.model_trainer.train(features)
        signals = self.strategy.generate_signals(model, features)
        self.agent.execute_trades(signals)

        self.logger.info("✅ Sessione pipeline completata")

    def simulate_multiple_sessions(self, n=3):
        """Esegue n sessioni simulate consecutive."""
        for i in range(n):
            self.logger.info(f"▶️ Esecuzione sessione simulata {i + 1}/{n}")
            self.run_batch_session()
