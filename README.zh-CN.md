# 📐 tool-selection-probe

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

**检测工具选择规模限制。** 2026 发现:工具选择准确率在 **~60 个工具** 处发生相位转变,由语义混淆驱动(~0.55 相似度阈值标记路由塌缩)。本库指纹化工具描述、发现混淆对、从工具数预测选择准确率。

> 零依赖。纯 Python 标准库。

```python
from tool_selection_probe import probe, load_tools
report = probe(load_tools("tools.json"))
print(report.scale_risk, report.scale_accuracy)
for pair in report.risky_pairs:
    print(pair.tool_a, pair.tool_b, pair.similarity)
```

```bash
pip install tool-selection-probe
tool-selection-probe probe tools.json --json
tool-selection-probe pair 'Search documents' 'Search documents and files'
tool-selection-probe scale 100
```

MIT © [wwb-bill](https://github.com/wwb-bill)
