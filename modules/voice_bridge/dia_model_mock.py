"""
Mock per dia.model se il pacchetto non è installabile localmente.
"""

class Dia:
    @staticmethod
    def from_pretrained(model_name: str):
        class DummyModel:
            def generate(self, text):
                import numpy as np
                return np.zeros(44100)
        return DummyModel()
