# 📐 tool-selection-probe

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![CI](https://github.com/wwb-bill/tool-selection-probe/actions/workflows/ci.yml/badge.svg)](https://github.com/wwb-bill/tool-selection-probe/actions/workflows/ci.yml)
[![No Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen)](#)

**Detect tool-selection scaling limits.** 2026 finding: tool-selection accuracy **phase-transitions beyond ~60 tools**, driven by semantic confusability (a ~0.55 similarity threshold marks routing collapse). This library fingerprints tool descriptions, finds confusable pairs, and predicts selection accuracy from tool count.

> Zero dependencies. Pure Python stdlib.

## Quick Start

```bash
pip install tool-selection-probe
```

## Usage

```python
from tool_selection_probe import probe, load_tools

report = probe(load_tools("tools.json"))
print(report.scale_risk, report.scale_accuracy)   # "high" 0.05
for pair in report.risky_pairs:                   # similarity >= 0.55
    print(pair.tool_a, pair.tool_b, pair.similarity)
```

## CLI

```bash
tool-selection-probe probe tools.json --json    # CI exit 1 on risky pairs or high scale risk
tool-selection-probe pair 'Search documents' 'Search documents and files'
tool-selection-probe scale 100
```

### tools.json

```json
{"tools": [{"name": "search", "description": "Search documents and files",
            "capabilities": ["find", "retrieve"]}]}
```

## What it detects

| Signal | Meaning |
|--------|---------|
| `risky_pairs` | descriptions with ≥0.55 similarity — routing collapse risk |
| `scale_accuracy` | predicted selection accuracy (logistic drop centered at 60 tools) |
| `scale_risk` | low ≤30 · medium ≤60 · high >60 |

## License

MIT © [wwb-bill](https://github.com/wwb-bill)
