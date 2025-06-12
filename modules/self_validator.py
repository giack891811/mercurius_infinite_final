"""Verifica semplice di coerenza dei moduli."""

import importlib


def validate_module(module_name: str) -> bool:
    try:
        mod = importlib.import_module(module_name)
    except Exception:
        return False
    required = ["__doc__"]
    return all(hasattr(mod, attr) for attr in required)
