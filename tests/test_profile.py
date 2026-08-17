"""Tests for tool profiles."""

import json
from pathlib import Path

from tool_selection_probe import ToolProfile, load_tools, tokens, surface_text


class TestTokens:
    def test_extracts_significant(self):
        t = tokens("Search documents and files quickly")
        assert "search" in t
        assert "documents" in t
        assert "and" not in t  # stop word

    def test_empty(self):
        assert tokens("") == set()


class TestLoadTools:
    def test_list_format(self, tmp_path: Path):
        p = tmp_path / "tools.json"
        p.write_text(json.dumps([
            {"name": "search", "description": "Search docs", "capabilities": ["find"]},
        ]), encoding="utf-8")
        tools = load_tools(p)
        assert tools[0].name == "search"
        assert tools[0].capabilities == ["find"]

    def test_object_format(self, tmp_path: Path):
        p = tmp_path / "tools.json"
        p.write_text(json.dumps({"tools": [{"name": "a", "description": "d"}]}), encoding="utf-8")
        assert load_tools(p)[0].name == "a"

    def test_missing_fields_default(self, tmp_path: Path):
        p = tmp_path / "tools.json"
        p.write_text(json.dumps([{"name": "a"}]), encoding="utf-8")
        tools = load_tools(p)
        assert tools[0].description == ""
        assert tools[0].capabilities == []


class TestSurfaceText:
    def test_combines(self):
        t = ToolProfile(name="x", description="Search documents", capabilities=["find", "retrieve"])
        surface = surface_text(t)
        assert "Search documents" in surface
        assert "find" in surface
