import os
import json
from pathlib import Path

AGENTS_BASE_DIR = Path("generated_agents")

def list_agents():
    return [d.name for d in AGENTS_BASE_DIR.iterdir() if d.is_dir()]

def load_manifest(agent_name):
    path = AGENTS_BASE_DIR / agent_name / "manifest.json"
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def define_hierarchy(agent_list):
    hierarchy = {
        "core_controller": agent_list[0],
        "delegates": agent_list[1:]
    }
    with open("memory/agent_hierarchy.json", "w", encoding="utf-8") as f:
        json.dump(hierarchy, f, indent=2)
    return hierarchy

def send_internal_message(sender, recipient, message):
    comms_dir = Path("memory/internal_comms")
    comms_dir.mkdir(parents=True, exist_ok=True)
    msg_path = comms_dir / f"{sender}_to_{recipient}.json"
    with open(msg_path, "w", encoding="utf-8") as f:
        json.dump({"from": sender, "to": recipient, "message": message}, f, indent=2)
    return str(msg_path)