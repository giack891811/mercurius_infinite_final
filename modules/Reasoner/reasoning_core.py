from datetime import datetime

def analyze_thought(trigger, context=None):
    timestamp = datetime.now().isoformat()
    decision = f"Analisi attivata da '{trigger}'. Contesto: {context or 'nessuno'}."
    log_entry = {"time": timestamp, "trigger": trigger, "decision": decision}
    save_episode(log_entry)
    return decision

def save_episode(entry):
    with open("modules/Reasoner/episodic_memory.log", "a", encoding="utf-8") as log_file:
        log_file.write(str(entry) + "\n")