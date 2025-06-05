# evolution/logic_injector.py

"""
Modulo: logic_injector.py
Descrizione: Inietta dinamicamente nuove funzioni o logiche all'interno di moduli Python di Mercurius∞.
Include verifica della sintassi, esecuzione in sandbox e tracciamento tramite log sinaptico.
"""

import importlib
import types
import traceback

from memory.synaptic_log import SynapticLog
from core.sandbox_executor import SandboxExecutor


class LogicInjector:
    def __init__(self):
        self.logger = SynapticLog()
        self.sandbox = SandboxExecutor()

    def inject_logic(self, module_name: str, function_code: str, function_name: str) -> bool:
        """
        Inietta una funzione in un modulo esistente, con controlli di sicurezza.

        Args:
            module_name (str): Nome del modulo Python (es. "core.executor")
            function_code (str): Codice Python della funzione (come stringa)
            function_name (str): Nome della funzione da iniettare
        Returns:
            bool: True se l'iniezione è riuscita, False altrimenti
        """
        try:
            # Step 1: Verifica statica
            if not self.verify_syntax(function_code):
                self.logger.log_event("LogicInjector", "SyntaxError", "❌ Codice con sintassi errata.")
                return False

            # Step 2: Esecuzione sandboxata preventiva
            sandbox_result = self.sandbox.run_sandboxed(function_code)
            if not sandbox_result.get("success", False):
                self.logger.log_event("LogicInjector", "SandboxFail", sandbox_result.get("output", "Nessun output"))
                return False

            # Step 3: Iniezione del codice
            compiled_func = compile(function_code, "<injected_function>", "exec")
            module = importlib.import_module(module_name)

            exec_env = {}
            exec(compiled_func, exec_env)

            if function_name not in exec_env:
                raise NameError(f"La funzione '{function_name}' non è stata trovata nel codice fornito.")

            new_func = exec_env[function_name]

            if not isinstance(new_func, types.FunctionType):
                raise TypeError(f"L'oggetto '{function_name}' non è una funzione valida.")

            setattr(module, function_name, new_func)
            self.logger.log_event("LogicInjector", "InjectionSuccess", f"✅ Funzione {function_name} iniettata nel modulo {module_name}")
            return True

        except Exception:
            self.logger.log_event("LogicInjector", "InjectionFailed", traceback.format_exc())
            return False

    def verify_syntax(self, code: str) -> bool:
        """
        Verifica se il codice fornito ha una sintassi valida.

        Args:
            code (str): Codice da verificare.
        Returns:
            bool: True se valido, False in caso di SyntaxError.
        """
        try:
            compile(code, "<syntax_check>", "exec")
            return True
        except SyntaxError as e:
            self.logger.log_event("LogicInjector", "SyntaxError", str(e))
            return False

    def test_injection(self, module_name: str, function_name: str, test_args: tuple = ()) -> str:
        """
        Testa una funzione precedentemente iniettata eseguendola.

        Args:
            module_name (str): Nome del modulo target
            function_name (str): Nome della funzione da testare
            test_args (tuple): Argomenti di test da passare alla funzione

        Returns:
            str: Output del test o errore catturato.
        """
        try:
            module = importlib.import_module(module_name)
            func = getattr(module, function_name)
            result = func(*test_args)
            return f"✅ Output della funzione: {result}"
        except Exception:
            return f"❌ Errore durante il test:\n{traceback.format_exc()}"
