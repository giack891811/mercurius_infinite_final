import os
import inspect
import importlib.util

def generate_module_docs(target_folder="modules", output_file="README_MODULES.md"):
    doc_lines = ["# 📚 Documentazione dei Moduli Interni\n"]
    for root, dirs, files in os.walk(target_folder):
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                path = os.path.join(root, file)
                module_name = path.replace("/", ".").replace(".py", "")
                doc_lines.append(f"\n## 📄 Modulo: `{module_name}`\n")
                try:
                    spec = importlib.util.spec_from_file_location(module_name, path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    for name, obj in inspect.getmembers(module):
                        if inspect.isfunction(obj) or inspect.isclass(obj):
                            doc_lines.append(f"### {name}\n```python\n{inspect.getdoc(obj)}\n```\n")
                except Exception as e:
                    doc_lines.append(f"⚠️ Errore nel caricare il modulo: {e}\n")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(doc_lines))