"""Core types for tool-selection-probe."""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass
class ToolProfile:
    """A tool's selection-relevant surface: name + description."""

    name: str
    description: str = ""
    capabilities: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> ToolProfile:
        known = {f for f in cls.__dataclass_fields__}
        return cls(**{k: v for k, v in d.items() if k in known})


@dataclass
class ConfusionPair:
    """Two tools whose descriptions are semantically confusable."""

    tool_a: str
    tool_b: str
    similarity: float  # 0-1

    def to_dict(self) -> dict[str, Any]:
        return {"tool_a": self.tool_a, "tool_b": self.tool_b,
                "similarity": round(self.similarity, 3)}


@dataclass
class ProbeReport:
    """Aggregate probe report."""

    tool_count: int = 0
    confusion_pairs: list[ConfusionPair] = field(default_factory=list)
    max_similarity: float = 0.0
    scale_risk: str = "low"  # low | medium | high
    scale_accuracy: float = 1.0  # predicted selection accuracy

    @property
    def risky_pairs(self) -> list[ConfusionPair]:
        return [p for p in self.confusion_pairs if p.similarity >= 0.55]

    def summary(self) -> dict[str, Any]:
        return {
            "tool_count": self.tool_count,
            "confusion_pairs": len(self.confusion_pairs),
            "risky_pairs": len(self.risky_pairs),
            "max_similarity": round(self.max_similarity, 3),
            "scale_risk": self.scale_risk,
            "scale_accuracy": round(self.scale_accuracy, 3),
        }
