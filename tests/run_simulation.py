"""
Simulazione: Avvio sistema Mercurius∞ in modalità autonoma.
Scopo: Verifica operatività integrata dei moduli principali.
"""

from modules.start_fullmode.initializer import SystemInitializer

def run_simulation():
    print("🔁 Simulazione in corso...")

    # Inizializzazione e avvio
    system = SystemInitializer()
    system.initialize_environment()
    system.start_components()

    # Interazione simulata
    audio_input = system.audio.listen()
    system.agent.perceive(audio_input)
    decision = system.agent.reason()
    system.agent.act(decision)
    system.audio.speak(f"Ho elaborato: {decision}")

    # Arresto video per sicurezza
    system.vision.stop()
    print("✅ Simulazione completata.")

if __name__ == "__main__":
    run_simulation()
