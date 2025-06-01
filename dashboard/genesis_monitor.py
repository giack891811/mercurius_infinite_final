"""
Modulo: genesis_monitor.py
Descrizione: Monitor real-time dello stato degli agenti GENESIS.
"""

class GenesisMonitor:
    def __init__(self):
        self.status = "IDLE"
        self.agent_activity = {}

    def update_status(self, new_status: str):
        self.status = new_status

    def log_agent_activity(self, agent_name: str, status: str):
        self.agent_activity[agent_name] = status

    def display(self):
        print("🧠 GENESIS STATUS:")
        print(f"Stato corrente: {self.status}")
        for agent, activity in self.agent_activity.items():
            print(f"• {agent} → {activity}")
