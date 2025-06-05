import json
from datetime import datetime
import requests

AZR_API = "http://localhost:11434/validate"

def analyze_and_validate_code(code_snippet, objective="check logic and suggest improvements"):
    request_payload = {
        "prompt": (
            f"Analyze the following code:\n{code_snippet}\nObjective: {objective}"
        ),
        "model": "azr-logic",
        "stream": False,
    }

    try:
        response = requests.post(AZR_API, json=request_payload)
        result = response.json().get("response", "No response from AZR.")
        log_meta_reasoning(code_snippet, result)
        return result
    except Exception as e:
        return f"AZR connection failed: {str(e)}"

def log_meta_reasoning(input_text, output_result):
    log_file = "logs/self_monitoring/meta_reasoning_log.json"
    entry = {
        "timestamp": datetime.now().isoformat(),
        "input": input_text,
        "output": output_result
    }
    try:
        with open(log_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        data = []

    data.append(entry)
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
