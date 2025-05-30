# config_schema.py
CONFIG_SCHEMA = {
    "symbols": {"type": "list", "schema": {"type": "string"}},
    "base_trade_qty": {"type": "integer", "min": 1},
    "min_confidence": {"type": "float", "min": 0, "max": 1},
    "retrain_threshold": {"type": "float", "min": 0, "max": 1},
    "azr_profit_floor": {"type": "float", "min": 0}
}
