import os

def check_files():
    # Controlla tutti i file split
    split_files = [f'project_tree_part{i}.txt' for i in range(1, 58)]
    print("\n--- Audit Mercurius∞ project_tree SPLIT ---\n")
    missing = []
    for f in split_files:
        if not os.path.isfile(f):
            missing.append(f)
    if missing:
        print("❌ Mancano i seguenti file split:")
        for f in missing:
            print(" -", f)
    else:
        print("✅ Tutti i file split sono presenti!")

    # Esempio check extra (personalizza qui)
    print("\nEsempio: controlla se esiste README.md e requirements.txt")
    for fname in ['README.md', 'requirements.txt']:
        print(f"- {fname}: {'OK' if os.path.isfile(fname) else 'MANCANTE'}")

if __name__ == "__main__":
    check_files()
