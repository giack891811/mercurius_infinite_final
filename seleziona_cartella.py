from tkinter import Tk, filedialog

root = Tk()
root.withdraw()  # Nasconde la finestra principale
folder_path = filedialog.askdirectory(title="Seleziona una cartella")

print("📁 Cartella selezionata:", folder_path)
