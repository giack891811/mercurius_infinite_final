def run_codex_from_md(path: str) -> str:
    import os
    import markdown
    import re

    if not os.path.exists(path):
        return f"File non trovato: {path}"

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = re.findall(r"```python(.*?)```", content, re.DOTALL)
    if not blocks:
        return "Nessun blocco Python trovato"

    for block in blocks:
        exec(block.strip(), globals())

    return f"SELF_MISSION eseguita da {path}"
