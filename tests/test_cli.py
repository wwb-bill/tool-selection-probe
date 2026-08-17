"""Tests for CLI."""

import json
import os

import pytest

from tool_selection_probe.cli import main


def _write_tools(tmp_path, tools):
    p = tmp_path / "tools.json"
    p.write_text(json.dumps({"tools": tools}), encoding="utf-8")
    return p


class TestCLI:
    def test_probe_clean(self, tmp_path, capsys):
        os.chdir(tmp_path)
        p = _write_tools(tmp_path, [
            {"name": "search", "description": "Search documents"},
            {"name": "bake", "description": "Bake sourdough bread"},
        ])
        with pytest.raises(SystemExit) as exc:
            main(["probe", str(p)])
        assert exc.value.code == 0
        assert "scale risk low" in capsys.readouterr().out

    def test_probe_risky(self, tmp_path, capsys):
        os.chdir(tmp_path)
        p = _write_tools(tmp_path, [
            {"name": "s1", "description": "Search documents and files"},
            {"name": "s2", "description": "Search documents and files"},
        ])
        with pytest.raises(SystemExit) as exc:
            main(["probe", str(p), "--json"])
        assert exc.value.code == 1
        d = json.loads(capsys.readouterr().out)
        assert d["risky_pairs"] == 1

    def test_pair(self, capsys):
        with pytest.raises(SystemExit) as exc:
            main(["pair", "Search documents", "Search documents"])
        assert exc.value.code == 1  # similarity >= 0.55
        assert "similarity" in capsys.readouterr().out

    def test_pair_clean(self, capsys):
        with pytest.raises(SystemExit) as exc:
            main(["pair", "Search documents", "Bake bread"])
        assert exc.value.code == 0

    def test_scale(self, capsys):
        with pytest.raises(SystemExit):
            main(["scale", "100"])
        assert "predicted accuracy" in capsys.readouterr().out
