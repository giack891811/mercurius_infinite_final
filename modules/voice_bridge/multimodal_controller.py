\"\"\"Multimodal Controller – gestisce input vocali / video ed eventi.  
Versione placeholder ma importabile.
\"\"\"

from utils.logger import setup_logger

logger = setup_logger(__name__)

class MultimodalController:
    \"\"\"Gestisce routing tra voice bridge, eye agent e LLM.\"\"\"

    def __init__(self):
        self.active = False

    def start(self):
        self.active = True
        logger.info("MultimodalController avviato")

    def stop(self):
        self.active = False
        logger.info("MultimodalController fermato")

    def handle_event(self, event: dict):
        \"\"\"Route di un evento (stub).\"\"\"
        logger.debug("Evento ricevuto: %s", event)
        # TODO: integrazione con eye_agent / speech_agent
        return {"handled": True, "event": event}