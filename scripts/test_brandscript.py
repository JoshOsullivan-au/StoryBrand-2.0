# /// script
# requires-python = ">=3.12"
# dependencies = ["pytest>=8"]
# ///
"""Tests for brandscript.py. Run: uv run --python 3.12 --with pytest pytest scripts/"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import pytest

sys.path.insert(0, str(Path(__file__).parent))

import brandscript as bs  # noqa: E402


def complete_script() -> dict[str, Any]:
    """Return a BrandScript that passes every hard rule."""
    data = bs.blank_script("Tide Books", "brand", "Tide Books")
    data["character"] = {"customer": "Sole-trader tradies", "want": "Books that are always BAS-ready"}
    data["problem"] = {
        "villain": "The shoebox of receipts",
        "external": "Receipts and invoices are never reconciled",
        "internal": "They feel behind and dread the BAS deadline",
        "philosophical": "A good tradie should not lose weekends to paperwork",
    }
    data["guide"] = {
        "empathy": "We know the dread of a BAS letter on a Friday.",
        # Empathy leads with "we know", which the narrative rewrites to "we understand".
        "authority": [{"type": "statistic", "text": "1,200 tradies kept BAS-ready since 2019"}],
    }
    data["plan"]["process"] = {
        "title": "The Clean Books Plan",
        "steps": ["Book a call", "Snap receipts", "Lodge on time"],
    }
    data["cta"] = {"direct": "Book a call", "transitional": "Download the BAS-ready checklist"}
    data["failure"] = [
        {"type": "practical", "text": "ATO penalties"},
        {"type": "emotional", "text": "dread every time the phone rings"},
        {"type": "opportunity", "text": "missed deductions"},
    ]
    data["success"] = [
        {"type": "practical", "text": "BAS lodged early"},
        {"type": "practical", "text": "every deduction claimed"},
        {"type": "feeling", "text": "calm at tax time"},
    ]
    data["identity"] = {"from": "Behind and anxious", "to": "On top of the numbers"}
    data["controlling_idea"] = "Your weekends should be yours, not your receipts'"
    return data


def errors(data: dict[str, Any]) -> set[str]:
    """Return the rule ids of every hard failure."""
    return {finding.rule for finding in bs.check(data) if finding.level == "error"}


def warnings(data: dict[str, Any]) -> set[str]:
    """Return the rule ids of every advisory finding."""
    return {finding.rule for finding in bs.check(data) if finding.level == "warn"}


def test_complete_script_has_no_errors() -> None:
    assert errors(complete_script()) == set()


def test_blank_script_fails_every_section() -> None:
    sections = {finding.section for finding in bs.check(bs.blank_script("X", "brand", "X")) if finding.level == "error"}
    assert sections == {
        "character",
        "problem",
        "guide",
        "plan",
        "cta",
        "failure",
        "success",
        "identity",
        "controlling-idea",
    }


def test_missing_controlling_idea_is_hard() -> None:
    data = complete_script()
    data["controlling_idea"] = ""
    assert "controlling-idea" in errors(data)


def test_long_controlling_idea_warns() -> None:
    data = complete_script()
    data["controlling_idea"] = " ".join(["word"] * 25)
    assert "controlling-idea-length" in warnings(data)


@pytest.mark.parametrize("marker", ["[NEEDS SOURCE]", "[INPUT NEEDED]"])
def test_unverified_marker_is_hard(marker: str) -> None:
    data = complete_script()
    data["guide"]["authority"][0]["text"] += f" {marker}"
    found = [finding for finding in bs.check(data) if finding.rule == "unverified"]
    assert len(found) == 1
    assert found[0].level == "error"
    assert found[0].section == "guide"
    assert "guide.authority.0.text" in found[0].message


def test_schema_one_file_migrates(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path))
    old = complete_script()
    del old["controlling_idea"]
    old["schema"] = 1
    bs.save(bs.store_path("old"), old)
    loaded = bs.load(bs.store_path("old"))
    assert loaded["schema"] == 2
    assert loaded["controlling_idea"] == ""


def test_two_desires_warn() -> None:
    data = complete_script()
    data["character"]["want"] = "Save time and save money"
    assert "single-desire" in warnings(data)


@pytest.mark.parametrize(("count", "rule"), [(2, "process-steps"), (7, "process-steps")])
def test_plan_step_bounds_are_hard(count: int, rule: str) -> None:
    data = complete_script()
    data["plan"]["process"]["steps"] = [f"Step {index}" for index in range(count)]
    assert rule in errors(data)


def test_five_steps_only_warn() -> None:
    data = complete_script()
    data["plan"]["process"]["steps"] = [f"Step {index}" for index in range(5)]
    assert "process-steps" not in errors(data)
    assert "process-steps-soft" in warnings(data)


def test_complete_script_has_no_warnings() -> None:
    assert warnings(complete_script()) == set()


def test_failure_needs_three_items() -> None:
    data = complete_script()
    data["failure"] = data["failure"][:2]
    assert "failure-count" in errors(data)


def test_missing_failure_and_success_kinds_warn() -> None:
    data = complete_script()
    data["failure"] = [{"type": "practical", "text": f"Cost {index}"} for index in range(3)]
    data["success"] = [{"type": "feeling", "text": f"Calm {index}"} for index in range(3)]
    assert {"failure-emotional", "failure-opportunity", "success-practical"} <= warnings(data)


@pytest.mark.parametrize("section", ["plan", "plan.process", "plan.agreement", "character", "problem", "guide", "cta"])
def test_set_rejects_section_paths(section: str) -> None:
    data = bs.blank_script("X", "brand", "X")
    with pytest.raises(SystemExit, match="is a section"):
        bs.set_field(data, section, "oops", append=False)
    assert errors(data)  # check still runs and does not crash


def test_more_failure_than_success_warns() -> None:
    data = complete_script()
    data["failure"].append({"type": "practical", "text": "audit risk"})
    assert "salt-ratio" in warnings(data)


def test_typed_set_rejects_wrong_kind() -> None:
    data = bs.blank_script("X", "brand", "X")
    bs.set_field(data, "failure", "opportunity: missed deductions", append=True)
    assert data["failure"] == [{"type": "opportunity", "text": "missed deductions"}]
    with pytest.raises(SystemExit):
        bs.set_field(data, "success", "emotional: calm", append=True)


def test_narrative_fills_every_slot() -> None:
    narrative = bs.render_narrative(complete_script())
    assert "[empty]" not in narrative
    assert "Our customer, Sole-trader tradies, wants Books that are always BAS-ready." in narrative
    assert "We understand the dread of a BAS letter on a Friday and have demonstrated" in narrative
    assert "Our plan is simple: Book a call, Snap receipts, then Lodge on time." in narrative
    assert "moving from Behind and anxious to On top of the numbers." in narrative


def test_template_has_every_worksheet_line() -> None:
    worksheet = bs.render(complete_script(), "template")
    for line in (
        "* Our customer is:",
        "* Internal problem, how it makes them feel:",
        "* Agreements or commitments that reduce their concerns:",
        "* Emotional consequences: dread every time the phone rings",
        "* Opportunities they could miss: missed deductions",
        "* How they feel: calm at tax time",
        "* Who they become: From Behind and anxious to On top of the numbers",
        "* Controlling idea: Your weekends should be yours, not your receipts'",
        "## Combined narrative",
    ):
        assert line in worksheet


def test_philosophical_without_ought_warns() -> None:
    data = complete_script()
    data["problem"]["philosophical"] = "Paperwork is boring"
    assert "philosophical-ought" in warnings(data)


def test_missing_direct_cta_is_hard() -> None:
    data = complete_script()
    data["cta"]["direct"] = ""
    assert "direct" in errors(data)


def test_set_field_and_append_authority() -> None:
    data = bs.blank_script("X", "brand", "X")
    bs.set_field(data, "guide.authority", "award: Xero Partner of the Year 2025", append=True)
    bs.set_field(data, "guide.authority", "logo: Bunnings", append=True)
    assert [entry["type"] for entry in data["guide"]["authority"]] == ["award", "logo"]


def test_set_rejects_unknown_field_and_bad_authority() -> None:
    data = bs.blank_script("X", "brand", "X")
    with pytest.raises(SystemExit):
        bs.set_field(data, "problem.secret", "value", append=False)
    with pytest.raises(SystemExit):
        bs.set_field(data, "guide.authority", "rumour: everyone loves us", append=True)


def test_cli_round_trip(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path))
    assert bs.main(["init", "--brand", "Tide Books"]) == 0
    slug = capsys.readouterr().out.strip()
    assert slug == "tide-books-brand"
    assert bs.main(["check", "--slug", slug]) == 1
    bs.save(bs.store_path(slug), complete_script())
    assert bs.main(["check", "--slug", slug]) == 0
    assert bs.main(["show", "--slug", slug]) == 0
    assert "## 7. And ends in success" in capsys.readouterr().out
