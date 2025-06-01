class GenesisMonitor:
    def __init__(self):
        self.status = "🟡 Standby"

    def update_status(self, new_status: str):
        self.status = new_status

    def show(self):
        print(f"🌐 Stato attuale della rete GENESIS: {self.status}")
