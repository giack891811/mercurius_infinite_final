# orchestrator/real_life_controller.py
"""
Modulo: real_life_controller.py
Descrizione: Router comandi voce per vita reale (agenda, smart-home, finanze, email)
"""

from integrations.agenda.agenda_manager import AgendaManager
from integrations.smart_home.home_assistant_bridge import HomeAssistantBridge
from personal_finance.finance_tracker import FinanceTracker
from communications.email_assistant import EmailAssistant
from modules.ai_kernel.command_interpreter import CommandInterpreter
from modules.voice_bridge.pyttsx3_tts import Pyttsx3TTS

agenda = AgendaManager()
home = HomeAssistantBridge()
fin = FinanceTracker()
mail = EmailAssistant()
tts = Pyttsx3TTS()
interp = CommandInterpreter()

def execute(command: str):
    cmd = interp.interpret(command)
    act = cmd.get("action")
    ctx = cmd.get("context", {})
    if act == "saluta":
        tts.speak("Ciao! Come posso aiutarti?")
    elif act == "apri_app":
        app = ctx.get("app")
        tts.speak(f"Apro {app}")
    elif act == "mostra_dati":
        month = fin.monthly_summary()
        tts.speak(f"Spese del mese: {month}")
    else:
        tts.speak("Comando non riconosciuto.")

if __name__ == "__main__":
    while True:
        txt = input("🗣️> ")
        execute(txt)
