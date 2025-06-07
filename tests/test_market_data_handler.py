import types
from data.market_data_handler import MarketDataHandler


def test_fetch_normalize_filter():
    handler = MarketDataHandler({'symbols': ['AAA', 'BBB']})
    data = handler.fetch_market_data()
    assert len(data) == 2
    for d in data:
        assert 'symbol' in d and 'price' in d and 'volatility' in d and 'volume' in d

    norm = handler.normalize_data(data)
    for d in norm:
        assert 0 <= d['price_norm'] <= 1
        assert 0 <= d['volatility_norm'] <= 1

    filt = handler.filter_by_volume(norm, min_volume=0)
    assert filt == norm
