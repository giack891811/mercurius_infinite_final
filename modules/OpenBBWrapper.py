"""Wrapper simulato per alcune funzioni di OpenBB."""

class OpenBBWrapper:
    def fetch_financials(self, symbol: str) -> dict:
        """Restituisce dati finanziari simulati per un simbolo."""
        return {
            "symbol": symbol,
            "revenue": 1000000,
            "debt": 500000,
        }
