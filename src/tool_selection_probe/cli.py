"""CLI for tool-selection-probe."""

from __future__ import annotations

import json
import sys

from .profile import load_tools
from .detect import probe, find_confusions, description_similarity, scale_accuracy


def _utf8_stdout() -> None:
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def main(argv: list[str] | None = None) -> None:
    args = list(argv) if argv is not None else sys.argv[1:]
    if not args or args[0] in ("--help", "-h"):
        print("tool-selection-probe — detect tool-selection scaling limits")
        print("\nUsage:")
        print("  tool-selection-probe probe <tools.json> [--json]")
        print("  tool-selection-probe pair '<desc A>' '<desc B>'")
        print("  tool-selection-probe scale <N>")
        sys.exit(0)

    if args[0] == "probe" and len(args) >= 2:
        tools = load_tools(args[1])
        report = probe(tools)
        if "--json" in args:
            print(json.dumps(report.summary(), indent=2, ensure_ascii=False))
        else:
            risk_icon = {"low": "✅", "medium": "🟡", "high": "🔴"}[report.scale_risk]
            print(f"  {risk_icon} {report.tool_count} tools — scale risk {report.scale_risk} "
                  f"(predicted accuracy {report.scale_accuracy:.0%})")
            for p in report.risky_pairs:
                print(f"      ⚠️ risky pair: {p.tool_a} ~ {p.tool_b} ({p.similarity:.0%})")
        sys.exit(1 if report.risky_pairs or report.scale_risk == "high" else 0)

    if args[0] == "pair" and len(args) >= 3:
        from .types import ToolProfile
        sim = description_similarity(ToolProfile(name="a", description=args[1]),
                                     ToolProfile(name="b", description=args[2]))
        print(f"similarity: {sim:.1%}")
        sys.exit(1 if sim >= 0.55 else 0)

    if args[0] == "scale" and len(args) >= 2:
        n = int(args[1])
        print(f"predicted accuracy at {n} tools: {scale_accuracy(n):.0%}")
        sys.exit(0)

    print(f"Unknown: {args[0]}", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    _utf8_stdout()
    main()
