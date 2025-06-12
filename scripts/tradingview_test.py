"""Esegue una prova rapida del modulo TradingView."""

from trading.trading_core import TradingViewInterface


def main() -> None:
    tv = TradingViewInterface()
    tv.connect()
    tv.execute_order("BTCUSD", "buy", 1)
    print(tv.get_status())


if __name__ == "__main__":
    main()
