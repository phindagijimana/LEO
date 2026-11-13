"""Setting names are LEO_*. Older MEDAI_LEO_*, MEDAI_*, and VECTA_* values still work."""
from __future__ import annotations

import os


def _keys(name: str) -> list[str]:
    if name.startswith("MEDAI_LEO_"):
        name = "LEO_" + name[len("MEDAI_LEO_"):]
    elif name.startswith("MEDAI_"):
        name = "LEO_" + name[len("MEDAI_"):]
    elif name.startswith("VECTA_"):
        name = "LEO_" + name[len("VECTA_"):]
    rest = name[4:] if name.startswith("LEO_") else name
    canon = name if name.startswith("LEO_") else "LEO_" + rest
    return [canon, f"MEDAI_LEO_{rest}", f"MEDAI_{rest}", f"VECTA_{rest}"]


def getenv(name: str, default=None):
    """Read LEO_<name>. Fall back to MEDAI_LEO_<name>, MEDAI_<name>, then VECTA_<name>."""
    for key in _keys(name):
        if key in os.environ:
            return os.environ[key]
    return default


def setdefault(name: str, value: str) -> str:
    current = getenv(name)
    if current is None:
        os.environ[_keys(name)[0]] = value
        return value
    return current
