from interface.genesis_bridge import GenesisBridge

class VoiceActivation:
    def __init__(self):
        self.bridge = GenesisBridge()

    def process_input(self, speech: str) -> str:
        if self.bridge.activate_from_voice(speech):
            self.bridge.trigger_activation("voce")
            return "GENESIS attivato!"
        return "Comando vocale ignorato."
