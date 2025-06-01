class ColabLinker:
    def __init__(self):
        self.name = "ColabLinker"

    def send_code(self, module: str):
        return f"[{self.name}] Modulo {module} inviato a Colab"
