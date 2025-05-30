import json
from datetime import datetime

USER_STYLE_PROFILE = "memory/dialog_style_profile.json"

def save_dialog_entry(text, style="neutro", tone="gentile", alias="utente"):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "alias": alias,
        "text": text,
        "style": style,
        "tone": tone
    }
    try:
        with open(USER_STYLE_PROFILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append(entry)

    with open(USER_STYLE_PROFILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_user_profile_summary():
    try:
        with open(USER_STYLE_PROFILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            recent = data[-1] if data else {}
            return recent
    except:
        return {"style": "neutro", "tone": "gentile", "alias": "utente"}