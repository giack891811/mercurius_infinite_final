# Mercurius∞ Installer

Questa cartella contiene i file necessari per generare l'installer di Mercurius∞ per Windows.

## File Principali

- `MercuriusInstaller.sln` – soluzione Visual Studio che include il progetto di deployment `MercuriusInstaller.vdproj`.
- `MercuriusInstaller.vdproj` – progetto Visual Studio Installer Projects.
- `create_installer.ps1` – script PowerShell che compila la soluzione tramite MSBuild.
- `start_all_services.ps1` – avvia i servizi principali (AZR, Ollama, EyeAgent, Josh Bridge, n8n, SleepTimeCompute).
- `build_flow_n8n.json` – workflow n8n che esegue `create_installer.ps1` via webhook.

## Utilizzo Rapido

1. Apri PowerShell e lancia `create_installer.ps1` per compilare l'installer.
2. Avvia `start_all_services.ps1` per eseguire tutti i servizi richiesti.
3. Importa `build_flow_n8n.json` in n8n se desideri automatizzare la build via webhook.

Assicurati di avere installato **Visual Studio** (con estensione *Visual Studio Installer Projects*), `n8n` e gli altri tool richiesti.
