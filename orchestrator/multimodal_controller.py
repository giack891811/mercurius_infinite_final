"""
Modulo: multimodal_controller.py
Responsabilità: Gestione integrata di input multimodali e pianificazione strategica
Autore: Mercurius∞ Engineer Mode
"""

from modules.speech import SpeechToText, TextToSpeech
from modules.nlp import CommandInterpreter
from modules.gesture import GestureRecognizer
from modules.planner import ActionPlanner
from modules.goal_manager import GoalManager
from orchestrator.autonomy_controller import AutonomyController
from typing import Optional


class MultimodalController:
    """
    Orchestratore intelligente per input vocali, gesti e pianificazione autonoma.
    """

    def __init__(self):
        self.speech_in = SpeechToText()
        self.speech_out = TextToSpeech()
        self.interpreter = CommandInterpreter()
        self.gesture = GestureRecognizer()
        self.planner = ActionPlanner()
        self.goal_mgr = GoalManager()
        self.autonomy = AutonomyController()

    def listen_and_interpret(self, simulate_input: Optional[str] = None) -> dict:
        """
        Ascolta input vocale (o usa simulazione) e lo converte in comando.
        """
        if simulate_input:
            text = simulate_input
        else:
            text = self.speech_in.listen()

        self.speech_out.speak(f"Hai detto: {text}")
        return self.interpreter.interpret(text)

    def receive_gesture(self, gesture_name: Optional[str] = None) -> dict:
        """
        Interpreta gesto manuale (o simulato) in azione.
        """
        if gesture_name:
            return self.gesture.interpret_gesture(gesture_name)
        else:
            return self.gesture.recognize(None)

    def plan_and_act(self, command: dict):
        """
        Registra obiettivo, pianifica e attiva il ciclo cognitivo.
        """
        action = command["action"]
        context = command.get("context", {})

        self.goal_mgr.add_goal(action, priority=1, context=context)
        goal = self.goal_mgr.get_next_goal()

        if goal:
            plan = self.planner.generate_plan(goal.name, goal.context)
            self.speech_out.speak(self.planner.describe_plan(plan))

            for step in plan:
                output = f"Eseguo: {step['action']}"
                print(output)
                self.autonomy.process_experience(step["action"], "eseguito", True, step.get("params", {}))
            self.goal_mgr.complete_goal(goal.name)
        else:
            self.speech_out.speak("Nessun obiettivo disponibile.")

    def run_full_cycle(self, input_text: Optional[str] = None, gesture: Optional[str] = None):
        """
        Esegue un ciclo completo multimodale.
        """
        if input_text:
            cmd = self.listen_and_interpret(simulate_input=input_text)
        elif gesture:
            cmd = self.receive_gesture(gesture)
        else:
            self.speech_out.speak("Nessun input fornito.")
            return

        if cmd["action"] != "ignora":
            self.plan_and_act(cmd)
        else:
            self.speech_out.speak("Non ho capito cosa fare.")
