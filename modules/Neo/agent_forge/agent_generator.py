import os
import json
from datetime import datetime

AGENT_FOLDER = "generated_agents"

def generate_agent(name, mission, modules_needed=None):
    if modules_needed is None:
        modules_needed = []

    agent_path = os.path.join(AGENT_FOLDER, name)
    os.makedirs(agent_path, exist_ok=True)

    # README
    with open(os.path.join(agent_path, "README.md"), "w", encoding="utf-8") as f:
        f.write(f"# 🤖 Agent: {name}\n\n## Mission\n{mission}\n")

    # Mission
    with open(os.path.join(agent_path, "mission.md"), "w", encoding="utf-8") as f:
        f.write(mission)

    # Init
    with open(os.path.join(agent_path, "__init__.py"), "w", encoding="utf-8") as f:
        f.write(f"# Init for agent {name}")

    # Config
    config = {
        "name": name,
        "mission": mission,
        "created": datetime.now().isoformat(),
        "modules": modules_needed
    }
    with open(os.path.join(agent_path, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

    return f"Agent '{name}' generated in {agent_path}"