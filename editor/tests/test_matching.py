"""Tests for matching by name and alternative name."""

from __future__ import annotations

from editor.controllers.matching import aliases_of, annotated_label, matches
from editor.models.records import Condition, Symptom

CONDITION = Condition(
    id="c1",
    name="Common Cold",
    aka=["Cold", "Upper Respiratory Infection"],
)


def test_a_name_matches() -> None:
    assert matches(CONDITION, "common") is True
    assert matches(CONDITION, "cold") is True


def test_an_alternative_name_matches() -> None:
    assert matches(CONDITION, "upper respiratory") is True


def test_matching_ignores_case_and_surrounding_space() -> None:
    assert matches(CONDITION, "  COMMON  ") is True
    assert matches(CONDITION, "  rhinovirus  ") is False


def test_no_match_is_reported() -> None:
    assert matches(CONDITION, "fever") is False
    assert annotated_label(CONDITION, "fever") is None


def test_an_empty_term_matches_everything() -> None:
    assert matches(CONDITION, "") is True
    assert matches(CONDITION, "   ") is True
    assert annotated_label(CONDITION, "") == "Common Cold"


def test_a_name_match_is_not_annotated() -> None:
    assert annotated_label(CONDITION, "cold") == "Common Cold"


def test_an_alternative_name_match_is_annotated() -> None:
    assert (
        annotated_label(CONDITION, "upper respiratory")
        == "Common Cold (Upper Respiratory Infection)"
    )


def test_the_first_matching_alternative_name_is_shown() -> None:
    record = Condition(
        id="c1",
        name="Common Cold",
        aka=["Upper Respiratory Infection", "Upper Airway Infection"],
    )

    assert annotated_label(record, "upper") == (
        "Common Cold (Upper Respiratory Infection)"
    )


def test_a_name_without_alternative_names_still_matches() -> None:
    symptom = Symptom(id="s1", name="Cough")

    assert matches(symptom, "cough") is True
    assert matches(symptom, "tussis") is False
    assert aliases_of(symptom) == []


def test_a_non_list_alternative_name_is_tolerated() -> None:
    record = Condition(id="c1", name="Common Cold", aka="Cold")

    assert aliases_of(record) == []
    assert matches(record, "cold") is True
    assert matches(record, "tussis") is False


def test_non_text_alternative_names_are_ignored() -> None:
    record = Condition(id="c1", name="Common Cold", aka=["Cold", 7, None])

    assert aliases_of(record) == ["Cold"]
    assert annotated_label(record, "cold") == "Common Cold"


def test_a_record_without_a_name_falls_back_to_its_identifier() -> None:
    record = Condition(id="a" * 32)

    assert matches(record, "aaaa") is True
    assert annotated_label(record, "aaaa") == "a" * 32
