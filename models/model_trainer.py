"""
model_trainer.py
================
Training del modello neurale e interfaccia per predizioni.
"""

from models.neural_network import NeuralNetwork
from utils.logger import setup_logger

logger = setup_logger(__name__)

class ModelTrainer:
    def __init__(self, config):
        self.config = config
        self.model = NeuralNetwork(input_dim=3)

    def train(self, features):
        """Addestra il modello con le feature fornite."""
        training_data = []
        for f in features:
            inputs = [
                f["price_volatility_ratio"],
                f["momentum"],
                f["volatility"]
            ]
            training_data.append(inputs)
        self.model.train(training_data)
        logger.info(f"Modello addestrato su {len(training_data)} campioni")
        return self.model

    def predict(self, feature_row):
        """Predice l'output per una riga di feature."""
        inputs = [
            feature_row["price_volatility_ratio"],
            feature_row["momentum"],
            feature_row["volatility"]
        ]
        pred = self.model.forward(inputs)
        logger.debug(f"Predizione: {pred}")
        return pred

    def retrain_on_error(self, features, performance_feedback):
        """Esegue un retraining se la performance scende sotto la soglia."""
        threshold = self.config.get("retrain_threshold", 0.65)
        if performance_feedback["accuracy"] < threshold:
            logger.warning("Retraining attivato: accuracy bassa")
            self.train(features)
