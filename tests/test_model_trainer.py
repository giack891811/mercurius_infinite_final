from models.model_trainer import ModelTrainer


def test_train_predict():
    trainer = ModelTrainer({})
    features = [
        {'price_volatility_ratio': 1.0, 'momentum': 2, 'volatility': 1},
        {'price_volatility_ratio': 0.5, 'momentum': 1, 'volatility': 0.5},
    ]
    trainer.train(features)
    out = trainer.predict(features[0])
    assert isinstance(out, list) and len(out) == 1
    assert 0 <= out[0] <= 1
