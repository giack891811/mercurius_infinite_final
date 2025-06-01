import os

def print_tree(startpath, file=None):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * level
        line = f"{indent}📁 {os.path.basename(root)}"
        print(line) if file is None else print(line, file=file)
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            fline = f"{subindent}- {f}"
            print(fline) if file is None else print(fline, file=file)

if __name__ == "__main__":
    with open("mercurius_tree.txt", "w", encoding="utf-8") as out_file:
        print("📂 Mercurius∞ Project Structure", file=out_file)
        print("=" * 40, file=out_file)
        print_tree(".", file=out_file)
