def main():
    print("🔁 Avvio completo Mercurius∞")
    print("🧠 Modalità Jarvis+ attiva: Visione, Voce, Dashboard, AI Cognitiva")
    from ai_launcher import ensure_ai_online
    ensure_ai_online()

    # Avviare sequenze di bootstrap dei moduli AI
    from modules.Neo.trainer_orchestrator import bootstrap_agents
    bootstrap_agents()

if __name__ == "__main__":
    main()