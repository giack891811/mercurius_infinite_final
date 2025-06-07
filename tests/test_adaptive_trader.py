from agents.adaptive_trader import AdaptiveTrader
from agents.memory_manager import MemoryManager
from models.model_trainer import ModelTrainer


class DummyStrategy:
    def execute(self, trade):
        return {'status': 'ok'}


def test_execute_trades(tmp_path):
    config = {'base_trade_qty': 10, 'min_confidence': 0.0, 'experience_file': str(tmp_path/'exp.json')}
    memory = MemoryManager(config)
    trainer = ModelTrainer(config)
    strategy = DummyStrategy()
    trader = AdaptiveTrader(config, memory, trainer, strategy)

    signals = [
        {'symbol': 'AAA', 'action': 'BUY', 'volatility': 1, 'confidence': 1.0, 'timestamp': 'now'}
    ]
    trader.execute_trades(signals)
    history = trader.get_trade_history()
    assert len(history) == 1
    assert history[0]['symbol'] == 'AAA'
