import sys
import pathlib
import types

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Stub external dependencies
_dummy_openai = types.SimpleNamespace(
    ChatCompletion=types.SimpleNamespace(create=lambda **_: {"choices": [{"message": {"content": "ok"}}]})
)
_dummy = types.SimpleNamespace()
for name, mod in {
    "openai": _dummy_openai,
    "torch": _dummy,
    "speech_recognition": _dummy,
    "fitz": _dummy,
    "yaml": _dummy,
    "psutil": _dummy,
    "requests": _dummy,
}.items():
    if name not in sys.modules:
        sys.modules[name] = mod
