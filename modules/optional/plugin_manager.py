"""
Modulo: plugin_manager.py
Responsabilità: Rileva e gestisce moduli opzionali/plugin caricabili runtime.
Autore: Mercurius∞ AI Engineer
"""

import importlib

OPTIONAL_PLUGINS = [
    "modules.optional.huggingface_tools",
    "modules.optional.n8n_connector",
    "modules.optional.elevenlabs_tts",
    "modules.optional.vosk_stt"
]

class PluginManager:
    def __init__(self):
        self.plugins = {}
        self._load_plugins()

    def _load_plugins(self):
        for plugin_path in OPTIONAL_PLUGINS:
            try:
                module = importlib.import_module(plugin_path)
                # Usa la prima classe trovata nel modulo (convenzionale)
                cls = [obj for name, obj in vars(module).items() if isinstance(obj, type) and name != "PluginManager"][0]
                self.plugins[plugin_path] = cls()
            except Exception as e:
                self.plugins[plugin_path] = f"[❌ Non caricato]: {e}"

    def is_plugin_available(self, plugin_name):
        plugin = self.plugins.get(plugin_name)
        return hasattr(plugin, "is_available") and plugin.is_available()

    def run_plugin_task(self, plugin_name, *args, **kwargs):
        plugin = self.plugins.get(plugin_name)
        if hasattr(plugin, "run_task"):
            return plugin.run_task(*args, **kwargs)
        return "[❌ Metodo run_task non disponibile]"

    def list_plugins(self):
        return {k: "[OK]" if hasattr(v, "is_available") and v.is_available() else v for k, v in self.plugins.items()}
