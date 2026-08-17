"""tool-selection-probe — detect tool-selection scaling limits.

2026 finding: tool-selection accuracy phase-transitions beyond ~60 tools,
driven by semantic confusability (a cosine-similarity threshold ~0.55 marks
routing collapse). This library fingerprints tool descriptions, finds
confusable pairs, and predicts selection accuracy from tool count.

Usage:
    from tool_selection_probe import probe, load_tools

    report = probe(load_tools("tools.json"))
    print(report.scale_risk, report.scale_accuracy)
    for pair in report.risky_pairs:
        print(pair.tool_a, pair.tool_b, pair.similarity)
"""

from .types import ToolProfile, ConfusionPair, ProbeReport
from .profile import tokens, load_tools, surface_text
from .detect import description_similarity, find_confusions, scale_accuracy, scale_risk, probe

__version__ = "0.1.0"

__all__ = [
    "ToolProfile",
    "ConfusionPair",
    "ProbeReport",
    "tokens",
    "load_tools",
    "surface_text",
    "description_similarity",
    "find_confusions",
    "scale_accuracy",
    "scale_risk",
    "probe",
]
