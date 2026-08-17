"""Tool profiles — load and fingerprint tool surfaces."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterable

from .types import ToolProfile

_STOP = frozenset("the a an and or but for with from into onto over under about "
                  "this that these those is are was were be been have has had will "
                  "would can could should may might must your their what which when".split())


def tokens(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]{3,}", text.lower()) if w not in _STOP}


def load_tools(path: str | Path) -> list[ToolProfile]:
    """Load tool profiles from JSON (list or {"tools": [...]})."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    items = data.get("tools", []) if isinstance(data, dict) else data
    tools = []
    for d in items:
        tools.append(ToolProfile(
            name=d.get("name", ""),
            description=d.get("description", ""),
            capabilities=d.get("capabilities", []),
        ))
    return tools


def surface_text(profile: ToolProfile) -> str:
    """Combined selection surface: description + capabilities."""
    parts = [profile.description]
    parts.extend(profile.capabilities)
    return " ".join(parts)
