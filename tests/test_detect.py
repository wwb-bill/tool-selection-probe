"""Tests for confusion and scale detection."""

from tool_selection_probe import (
    ToolProfile, description_similarity, find_confusions, scale_accuracy,
    scale_risk, probe,
)


def _t(name, desc, caps=None):
    return ToolProfile(name=name, description=desc, capabilities=caps or [])


class TestSimilarity:
    def test_identical(self):
        assert description_similarity(_t("a", "Search documents"), _t("b", "Search documents")) == 1.0

    def test_disjoint(self):
        assert description_similarity(_t("a", "Search documents"), _t("b", "Bake sourdough bread")) == 0.0

    def test_partial(self):
        s = description_similarity(_t("a", "Search documents and files"), _t("b", "Search the web"))
        assert 0.0 < s < 1.0

    def test_empty_descriptions(self):
        assert description_similarity(_t("a", ""), _t("b", "")) == 0.0


class TestConfusions:
    def test_finds_pairs(self):
        tools = [_t("s1", "Search documents"), _t("s2", "Search files"), _t("read", "Read a file")]
        pairs = find_confusions(tools, threshold=0.3)
        assert len(pairs) >= 1
        assert all(p.similarity >= 0.3 for p in pairs)

    def test_threshold_filters(self):
        tools = [_t("a", "Search documents"), _t("b", "Bake sourdough bread")]
        assert find_confusions(tools, threshold=0.3) == []

    def test_sorted(self):
        tools = [_t("a", "Search documents and files"), _t("b", "Search documents"), _t("c", "Search")]
        pairs = find_confusions(tools, threshold=0.3)
        sims = [p.similarity for p in pairs]
        assert sims == sorted(sims, reverse=True)


class TestScale:
    def test_small_accurate(self):
        assert scale_accuracy(10) == 1.0
        assert scale_accuracy(30) == 1.0

    def test_phase_transition(self):
        assert scale_accuracy(60) < 1.0
        assert scale_accuracy(100) < scale_accuracy(60)
        assert scale_accuracy(200) < 0.1

    def test_risk_levels(self):
        assert scale_risk(10) == "low"
        assert scale_risk(45) == "medium"
        assert scale_risk(100) == "high"


class TestProbe:
    def test_clean_small(self):
        tools = [_t("a", "Search documents"), _t("b", "Bake bread")]
        report = probe(tools)
        assert report.tool_count == 2
        assert report.scale_risk == "low"
        assert report.scale_accuracy == 1.0

    def test_confusion_detected(self):
        tools = [_t("a", "Search documents and files"), _t("b", "Search documents and files")]
        report = probe(tools)
        assert len(report.risky_pairs) == 1
        assert report.max_similarity == 1.0

    def test_large_scale_risk(self):
        tools = [_t(f"tool_{i}", f"Generic operation number {i}") for i in range(100)]
        report = probe(tools)
        assert report.scale_risk == "high"

    def test_summary_shape(self):
        tools = [_t("a", "Search documents")]
        s = probe(tools).summary()
        assert "tool_count" in s and "scale_risk" in s
