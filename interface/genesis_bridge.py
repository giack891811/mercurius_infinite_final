class GenesisBridge:
    def __init__(self):
        self.hotword = "Hey Mercurius, attiva GENESIS"

    def activate_from_voice(self, phrase: str) -> bool:
        return phrase.strip().lower() == self.hotword.lower()

    def activate_from_command(self, cmd: str) -> bool:
        return cmd.strip().lower() == "#genesis_mode"

    def trigger_activation(self, method: str = "auto"):
        print("🚀 Attivazione GENESIS in corso via:", method)
        return True
