import argparse
import sys
from modules.Neo.trainer_orchestrator import bootstrap_agents

def create_agent(nome):
    print(f"🧬 Creo nuovo agente: {nome}")
    # Qui va la chiamata reale per generare un agente AI specifico
    bootstrap_agents(agent_name=nome)

def elenco_task():
    print("📜 Task disponibili:")
    print(" - crea_agente --nome <NomeAgente>")
    print(" - avvia_bootstrap")
    print(" - help")

def main():
    parser = argparse.ArgumentParser(description="Mercurius∞ TaskManager CLI – Modalità Jarvis+ Ultra")
    parser.add_argument("--task", type=str, required=True, help="Task da eseguire (es: crea_agente, avvia_bootstrap, help)")
    parser.add_argument("--nome", type=str, help="Nome agente, modulo o oggetto")
    args = parser.parse_args()

    if args.task == "crea_agente" and args.nome:
        create_agent(args.nome)
    elif args.task == "avvia_bootstrap":
        print("🟢 Avvio sequenza di bootstrap completa!")
        bootstrap_agents()
    elif args.task == "help":
        elenco_task()
    else:
        print("❌ Comando non riconosciuto. Usa '--task help' per la lista.")

if __name__ == "__main__":
    main()
