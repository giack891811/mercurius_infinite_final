import argparse
import sys
from modules.Neo.trainer_orchestrator import bootstrap_agents
from modules.LocalAI.local_ai import LocalAI
from modules.LeonAI.leon_ai import LeonAI

class TaskManagerCLI:
    def __init__(self):
        self.localai = LocalAI()
        self.leonai = LeonAI()
        print("🕹️ TaskManager CLI interattivo pronto! Scrivi 'ai: ...' per LLM offline, 'pc: ...' per comandi PC, 'exit' per uscire.")

    def run(self):
        while True:
            try:
                cmd = input("Task> ").strip()
                if not cmd:
                    continue
                if cmd.lower() == "exit":
                    print("Bye Jarvis!")
                    break
                if cmd.startswith("ai:"):
                    prompt = cmd[3:].strip()
                    response = self.localai.rispondi(prompt)
                    print(f"\n🤖 LocalAI: {response}\n")
                elif cmd.startswith("pc:"):
                    sys_cmd = cmd[3:].strip()
                    try:
                        out = self.leonai.esegui_comando(sys_cmd)
                        print(f"\n🦾 LeonAI Output:\n{out}\n")
                    except PermissionError as e:
                        print(f"[SECURITY]: {e}")
                else:
                    print("❓ Comando non riconosciuto. Usa 'ai:' o 'pc:' davanti.")
            except KeyboardInterrupt:
                print("\nInterrotto. Exit.")
                break

def create_agent(nome):
    print(f"🧬 Creo nuovo agente: {nome}")
    # Se bootstrap_agents non supporta argomenti, chiamalo senza parametri.
    bootstrap_agents()



def elenco_task():
    print("📜 Task disponibili:")
    print(" - crea_agente --nome <NomeAgente>")
    print(" - avvia_bootstrap")
    print(" - interactive (modalità CLI interattiva)")
    print(" - help")

def main():
    parser = argparse.ArgumentParser(description="Mercurius∞ TaskManager CLI – Modalità Jarvis+ Ultra")
    parser.add_argument("--task", type=str, help="Task da eseguire (es: crea_agente, avvia_bootstrap, interactive, help)")
    parser.add_argument("--nome", type=str, help="Nome agente, modulo o oggetto")
    args = parser.parse_args()

    if not args.task or args.task == "interactive":
        TaskManagerCLI().run()
    elif args.task == "crea_agente" and args.nome:
        create_agent(args.nome)
    elif args.task == "avvia_bootstrap":
        print("🟢 Avvio sequenza di bootstrap completa!")
        bootstrap_agents()
    elif args.task == "help":
        elenco_task()
    else:
        print("❌ Comando non riconosciuto. Usa '--task help' per la lista.")

