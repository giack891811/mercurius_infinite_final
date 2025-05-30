"""
console.py
==========
Console interattiva CLI per lanciare operazioni Mercurius∞.
Permette esecuzioni batch, test, AZR e analisi performance.
"""

from core.pipeline_controller import PipelineController
from core.auto_tester import AutoTester
from utils.config_loader import load_config
from modules.experience.experience_memory import ExperienceMemory
from modules.metrics.performance_metrics import PerformanceMetrics

def main():
    config = load_config("config.yaml")
    pipeline = PipelineController(config)
    tester = AutoTester()
    memory = ExperienceMemory(config)

    print("=== Mercurius∞ CLI ===")
    print("1. Esegui una sessione")
    print("2. Simula 3 sessioni")
    print("3. Avvia test automatici")
    print("4. Mostra metriche esperienziali")
    print("5. Esci")

    choice = input("Scelta: ")

    if choice == "1":
        pipeline.run_batch_session()
    elif choice == "2":
        pipeline.simulate_multiple_sessions(3)
    elif choice == "3":
        tester.run()
        tester.test_signal_confidence()
        tester.test_adaptive_behavior()
    elif choice == "4":
        summary = PerformanceMetrics(memory.get_recent_experiences()).summary()
        print("📊 Metriche Esperienziali:")
        for k, v in summary.items():
            print(f"- {k}: {v}")
    else:
        print("Uscita...")

if __name__ == "__main__":
    main()
