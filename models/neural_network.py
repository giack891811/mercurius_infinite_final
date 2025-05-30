"""
neural_network.py
=================
Definizione di un modello neurale semplice per classificazione dei segnali.
"""

class NeuralNetwork:
    def __init__(self, input_dim):
        self.input_dim = input_dim
        self.weights = [0.5 for _ in range(input_dim)]
        self.bias = 0.1

    def forward(self, inputs):
        """Applica la rete ai dati di input (mock semplificato)."""
        output = sum(x * w for x, w in zip(inputs, self.weights)) + self.bias
        return [self._sigmoid(output)]

    def _sigmoid(self, x):
        """Funzione di attivazione sigmoid."""
        try:
            return 1 / (1 + pow(2.718, -x))
        except OverflowError:
            return 0.0 if x < 0 else 1.0

    def train(self, data):
        """Mock training: registra i dati per debugging."""
        print("Training data ricevuti:", data)

    def update_weights(self, new_weights):
        """Aggiorna i pesi della rete."""
        if len(new_weights) == self.input_dim:
            self.weights = new_weights

    def summary(self):
        """Restituisce un riassunto del modello."""
        return {
            "weights": self.weights,
            "bias": self.bias,
            "input_dim": self.input_dim
        }
