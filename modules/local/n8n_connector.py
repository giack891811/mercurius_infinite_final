class N8nConnector:
    def __init__(self):
        self.name = "n8n"

    def trigger_flow(self, flow_id: str) -> str:
        return f"[{self.name}] Flusso {flow_id} attivato localmente"
