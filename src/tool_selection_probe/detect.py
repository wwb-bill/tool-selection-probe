"""Confusion and scale detection — tool-selection limits."""

from __future__ import annotations

import math

from .types import ToolProfile, ConfusionPair, ProbeReport
from .profile import tokens, surface_text


def description_similarity(a: ToolProfile, b: ToolProfile) -> float:
    """Jaccard similarity of significant tokens between tool surfaces."""
    ta = tokens(surface_text(a))
    tb = tokens(surface_text(b))
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def find_confusions(tools: list[ToolProfile],
                    threshold: float = 0.3) -> list[ConfusionPair]:
    """All pairs above the confusion threshold, sorted by similarity desc."""
    pairs: list[ConfusionPair] = []
    for i in range(len(tools)):
        for j in range(i + 1, len(tools)):
            sim = description_similarity(tools[i], tools[j])
            if sim >= threshold:
                pairs.append(ConfusionPair(tool_a=tools[i].name,
                                           tool_b=tools[j].name,
                                           similarity=sim))
    pairs.sort(key=lambda p: -p.similarity)
    return pairs


def scale_accuracy(n_tools: int) -> float:
    """Predicted selection accuracy given tool count.

    2026 finding: a phase transition beyond ~60 tools driven by semantic
    confusability. Model: logistic drop centered at 60.
    """
    if n_tools <= 30:
        return 1.0
    # logistic: 1 / (1 + exp((n - 60) / 12))
    return round(1.0 / (1.0 + math.exp((n_tools - 60) / 12.0)), 3)


def scale_risk(n_tools: int) -> str:
    if n_tools <= 30:
        return "low"
    if n_tools <= 60:
        return "medium"
    return "high"


def probe(tools: list[ToolProfile]) -> ProbeReport:
    """Full probe: confusion pairs + scale risk."""
    pairs = find_confusions(tools)
    max_sim = max((p.similarity for p in pairs), default=0.0)
    report = ProbeReport(
        tool_count=len(tools),
        confusion_pairs=pairs,
        max_similarity=max_sim,
        scale_risk=scale_risk(len(tools)),
        scale_accuracy=scale_accuracy(len(tools)),
    )
    return report
