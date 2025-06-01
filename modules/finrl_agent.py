# modules/finrl_agent.py

"""
Modulo: finrl_agent.py
Descrizione: Wrapper per l’utilizzo di FinRL all’interno di Mercurius∞. Consente addestramento e deploy di agenti RL per trading.
"""

class FinRLAgent:
    def __init__(self):
        self.model = None

    def train(self, data_path: str, model_type="ppo"):
        print(f"📈 Addestramento agente {model_type} su {data_path}")
        # Qui si collegherà al training FinRL in futuro

    def predict(self, state):
        return "🧠 Predizione (stub): buy/sell/hold"

    def evaluate(self):
        return "📊 Performance dell’agente: +4.2% (simulata)"


# Test
if __name__ == "__main__":
    agent = FinRLAgent()
    agent.train("data/btc.csv")
    print(agent.predict("BTC_state"))
