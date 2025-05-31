import os

with open("file_albero_locale.txt", "w", encoding="utf-8") as f:
    for root, dirs, files in os.walk("."):
        level = root.replace(os.getcwd(), '').count(os.sep)
        indent = '  ' * level
        f.write(f"{indent}{os.path.basename(root)}/\n")
        subindent = '  ' * (level + 1)
        for file in files:
            f.write(f"{subindent}{file}\n")
