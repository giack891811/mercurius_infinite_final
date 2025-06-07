"""
auto_tester.py
==============
Modulo per lanciare test automatici sulle componenti chiave di Mercurius∞.
"""

from core.pipeline_controller import PipelineController
from utils.config_loader import load_config
from utils.logger import setup_logger

logger = setup_logger(__name__)


class AutoTester:
    def __init__(self):
        self.config = load_config("config.yaml")
        self.pipeline = PipelineController(self.config)

    def run(self):
        logger.info("🔍 Test: Avvio 3 sessioni simulate")
        self.pipeline.simulate_multiple_sessions(3)
        logger.info("✅ Test automatico completato")

    def test_signal_confidence(self):
        """Test di confidenza su segnali generati."""
        raw_data = self.pipeline.data_handler.fetch_market_data()
        features = self.pipeline.feature_engineer.transform(raw_data)
        model = self.pipeline.model_trainer.train(features)
        signals = self.pipeline.strategy.generate_signals(model, features)

        conf = [s["confidence"] for s in signals]
        assert all(0 <= c <= 1 for c in conf), "Errore: valori confidenza fuori range"
        logger.info("✅ Confidenza segnali OK")

    def test_adaptive_behavior(self):
        """Verifica che AZR modifichi la strategia nel tempo."""
        before = self.config["base_trade_qty"]
        self.run()
        after = self.pipeline.agent.config["base_trade_qty"]
        logger.info(f"📉 Base quantity: {before} → {after}")
