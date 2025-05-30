"""Assegna pesi adattivi ai moduli in base al loro utilizzo."""

module_weights = {}

def update_weight(module_name, increment=0.1):
    module_weights[module_name] = module_weights.get(module_name, 1.0) + increment
    return module_weights[module_name]