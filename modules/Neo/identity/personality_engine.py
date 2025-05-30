import json
from pathlib import Path

PROFILE_PATH = Path("memory/dialog_style_profile.json")

DEFAULT_PROFILE = {
    "tone": "educato",
    "registro": "narrativo",
    "alias": ["Mercurius", "Sigma"],
    "stile": "Jarvis+",
    "preferenze": {
        "formale": True,
        "umorismo": "moderato",
        "citazioni": True
    }
}

def get_profile():
    if not PROFILE_PATH.exists():
        save_profile(DEFAULT_PROFILE)
    return json.loads(PROFILE_PATH.read_text(encoding="utf-8"))

def save_profile(profile_data):
    PROFILE_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROFILE_PATH.write_text(json.dumps(profile_data, indent=2), encoding="utf-8")

def update_alias(nickname):
    profile = get_profile()
    if nickname not in profile["alias"]:
        profile["alias"].append(nickname)
        save_profile(profile)