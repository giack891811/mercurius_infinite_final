# tests/test_modular_end2end.py

"""
Test End-to-End per Mercurius∞
Simula i flussi completi: video -> trascrizione -> generazione codice -> sandbox -> auto-fix -> comando -> log.
Autore: Mercurius∞ AI Engineer
"""

import os
import sys
import pytest

# Importa i moduli core di Mercurius∞
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

pytest.skip("Dipendenze pesanti non disponibili", allow_module_level=True)

from learning.video_learner import VideoLearner
from core.sandbox_executor import SandboxExecutor
from modules.local.localai_adapter import LocalAI
from modules.local.leon_ai_bridge import LeonAI

import datetime

RESULT_LOG = "end2end_test_results.log"

def log_result(test_name, result, details=""):
    timestamp = datetime.datetime.now().isoformat()
    with open(RESULT_LOG, "a", encoding="utf-8") as logf:
        logf.write(f"[{timestamp}] {test_name} — {'SUCCESS' if result else 'FAIL'}\n{details}\n\n")
    print(f"{test_name}: {'✅' if result else '❌'}")

# Test 1: Video locale → Trascrizione
def test_video_to_text():
    print("\n--- Test 1: Video locale → Trascrizione ---")
    video_path = "tests/sample.mp3"  # Puoi sostituire con un file audio/video locale reale
    vl = VideoLearner()
    if not os.path.exists(video_path):
        log_result("test_video_to_text", False, "File video/audio di test non trovato.")
        return False
    transcript = vl.extract_insights_from_video(video_path)
    passed = isinstance(transcript, str) and len(transcript.strip()) > 0 and not transcript.startswith("[❌")
    log_result("test_video_to_text", passed, transcript)
    return passed

# Test 2: Prompt a LocalAI → Risposta testuale
def test_localai_text_generation():
    print("\n--- Test 2: Prompt a LocalAI ---")
    ai = LocalAI()
    prompt = "Scrivi una poesia sull'intelligenza artificiale."
    response = ai.execute_task(prompt)
    passed = isinstance(response, str) and len(response.strip()) > 10
    log_result("test_localai_text_generation", passed, response)
    return passed

# Test 3: Codice errato → Sandbox → Auto-fix
def test_sandbox_autofix():
    print("\n--- Test 3: Codice errato → Sandbox → Auto-fix ---")
    code_with_bug = "for i in range(5)\n    print(i)"  # Manca i due punti!
    sandbox = SandboxExecutor(timeout_seconds=3)
    static_ok = sandbox.static_analysis(code_with_bug)
    # static_analysis dovrebbe fallire, quindi tentiamo subito autofix
    if not static_ok:
        fix = sandbox.autofix_with_llm(code_with_bug, "SyntaxError: expected ':'")
        # Ora testiamo il fix se esiste
        result = sandbox.run_sandboxed(fix)
        passed = result.get("success", False)
        log_result("test_sandbox_autofix", passed, result.get("output", fix))
        return passed
    else:
        log_result("test_sandbox_autofix", False, "Il codice errato è stato accettato erroneamente.")
        return False

# Test 4: Comando locale via LeonAI
def test_leonai_command():
    print("\n--- Test 4: LeonAI comando locale ---")
    leon = LeonAI()
    command = "echo Mercurius è operativo!"
    output = leon.run_command(command)
    passed = "Mercurius" in output
    log_result("test_leonai_command", passed, output)
    return passed

# Test 5: Pipeline completa — Video → Trascrizione → Generazione codice → Sandbox
def test_full_pipeline():
    print("\n--- Test 5: Pipeline completa ---")
    ai = LocalAI()
    sandbox = SandboxExecutor(timeout_seconds=3)
    video_path = "tests/sample.mp3"  # Sostituisci con un tuo file di test

    # Step 1: Trascrizione
    vl = VideoLearner()
    if not os.path.exists(video_path):
        log_result("test_full_pipeline", False, "File video/audio di test non trovato.")
        return False
    transcript = vl.extract_insights_from_video(video_path)

    # Step 2: Generazione codice dalla trascrizione
    prompt = f"Genera un semplice script Python che stampa la frase:\n{transcript.strip().split('.')[0]}"
    code = ai.execute_task(prompt)

    # Step 3: Validazione Sandbox
    result = sandbox.run_sandboxed(code)
    passed = result.get("success", False)
    log_result("test_full_pipeline", passed, result.get("output", code))
    return passed

if __name__ == "__main__":
    print("🧪 Mercurius∞ — Test End-to-End")
    all_passed = True
    tests = [
        test_video_to_text,
        test_localai_text_generation,
        test_sandbox_autofix,
        test_leonai_command,
        test_full_pipeline,
    ]
    for test in tests:
        try:
            all_passed &= test()
        except Exception as e:
            log_result(test.__name__, False, f"Exception: {e}")
            all_passed = False
    print("\n=== RISULTATO FINALE ===")
    print("Tutti i test superati!" if all_passed else "Alcuni test NON superati — vedi log.")
