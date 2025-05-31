# evolution/logic_injector.py

"""
Modulo: logic_injector.py
Descrizione: Inietta dinamicamente nuove funzioni o logiche all'interno di moduli Python di Mercurius∞.
Traccia ogni modifica tramite log sinaptico e verifica la sintassi prima dell'iniezione.
"""

import importlib
import types
import traceback
from memory.synaptic_log import SynapticLog


class LogicInjector:
    def __init__(self):
        self.logger = SynapticLog()

    def inject_logic(self, module_name: str, function_code: str, function_name: str) -> bool:
        """
        Inietta una funzione in un modulo esistente, se possibile.

        Args:
            module_name (str): Nome del modulo Python (es. "core.executor")
            function_code (str): Codice Python della funzione (come stringa)
            function_name (str): Nome della funzione da iniettare
        Returns:
            bool: True se l'iniezione è riuscita, False in caso contrario
        """
        try:
            compiled_func = compile(function_code, "<injected_function>", "exec")
            module = importlib.import_module(module_name)

            exec_env = {}
            exec(compiled_func, exec_env)

            if function_name not in exec_env:
                raise NameError(f"La funzione '{function_name}' non è stata definita nel codice fornito.")

            new_func = exec_env[function_name]

            if not isinstance(new_func, types.FunctionType):
                raise TypeError(f"L'oggetto '{function_name}' non è una funzione valida.")

            setattr(module, function_name, new_func)
            self.logger.log_event("LogicInjector", "InjectionSuccess", f"{function_name} in {module_name}")
            return True

        except Exception as e:
            self.logger.log_event("LogicInjector", "InjectionFailed", traceback.format_exc())
            return False

    def verify_syntax(self, code: str) -> bool:
        """
        Verifica se il codice fornito ha una sintassi valida.

        Returns:
            bool: True se il codice è sintatticamente valido.
        """
        try:
            compile(code, "<syntax_check>", "exec")
            return True
        except SyntaxError as e:
            self.logger.log_event("LogicInjector", "SyntaxError", str(e))
            return False

    def test_injection(self, module_name: str, function_name: str, test_args: tuple = ()) -> str:
        """
        Esegue un test sulla funzione iniettata per verificarne il comportamento.

        Returns:
            str: Output del test o errore catturato.
        """
        try:
            module = importlib.import_module(module_name)
            func = getattr(module, function_name)
            result = func(*test_args)
            return f"✅ Output: {result}"
        except Exception as e:
            return f"❌ Errore durante il test: {traceback.format_exc()}"
