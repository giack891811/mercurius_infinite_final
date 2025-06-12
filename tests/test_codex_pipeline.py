from core.pipeline_controller import PipelineController


def test_pipeline_methods():
    cfg = {"symbols": ["AAA"], "base_trade_qty": 10}
    pc = PipelineController(cfg)
    signals = pc.fetch_signals()
    valid = pc.validate_strategy(signals)
    pc.execute_trades(valid)
    assert isinstance(signals, list)
