from modules.auto_trader_ai import AutoTraderAI


def test_run_returns_signals():
    ai = AutoTraderAI()
    market_data = [{'symbol': 'XYZ', 'volatility': 1.2}]
    signals = ai.run(market_data)
    assert isinstance(signals, list)
    assert signals
