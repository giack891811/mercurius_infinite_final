"""Basic project conflict analyzer."""
from __future__ import annotations

import pkgutil
from collections import defaultdict


def scan_conflicts() -> None:
    packages = defaultdict(list)
    for module in pkgutil.iter_modules():
        root = module.name.split('.')[0].lower()
        packages[root].append(module.name)
    conflicts = {k: v for k, v in packages.items() if len(v) > 1}
    if not conflicts:
        print("No obvious module name conflicts found.")
        return
    print("Potential conflicts detected:")
    for base, mods in conflicts.items():
        joined = ', '.join(mods)
        print(f" - {base}: {joined}")


if __name__ == "__main__":
    scan_conflicts()
