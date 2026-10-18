"""Tests for the validator: one section per rule method.

Scenario names are carried over from the previous rule-by-rule suite, so the
rule-to-test map in ``editor/README.md`` stays traceable.
"""

from __future__ import annotations

import pytest

from editor.models.records import Citation, Condition, Record, Symptom, Test
from editor.models.rules import (
    NAME_MAX_LENGTH,
    Validator,
    Violation,
    is_title_cased,
)

VALID_BIBTEX = "@misc{reference, title={Reference}}"


class FakeModel:
    """The queries the validator needs, built from four plain lists.

    ``EditorModel`` implements exactly these accessors, so using a stand-in here
    keeps this file about the rules and nothing else.
    """

    def __init__(
        self,
        conditions: list[Record] | None = None,
        symptoms: list[Record] | None = None,
        tests: list[Record] | None = None,
        citations: list[Record] | None = None,
    ) -> None:
        self._conditions = list(conditions or [])
        self._symptoms = list(symptoms or [])
        self._tests = list(tests or [])
        self._citations = list(citations or [])

    def conditions(self) -> list[Record]:
        return list(self._conditions)

    def symptoms(self) -> list[Record]:
        return list(self._symptoms)

    def tests(self) -> list[Record]:
        return list(self._tests)

    def citations(self) -> list[Record]:
        return list(self._citations)

    def all_records(self) -> list[Record]:
        return self._conditions + self._symptoms + self._tests + self._citations


@pytest.fixture
def validator() -> Validator:
    return Validator()


def _empty() -> FakeModel:
    return FakeModel()


def _rule_names(violations: list[Violation]) -> set[str]:
    return {violation.rule for violation in violations}


# --- name_must_be_unique ---------------------------------------------------


def test_duplicate_name_in_the_same_type_is_rejected(validator: Validator) -> None:
    model = FakeModel(conditions=[Condition(id="a", name="Common Cold")])
    candidate = Condition(id="b", name="Common Cold")

    violations = validator.validate(candidate, None, model)

    assert "name-unique" in _rule_names(violations)


def test_duplicate_name_among_tests_is_rejected(validator: Validator) -> None:
    model = FakeModel(tests=[Test(id="a", name="Chest Examination")])
    candidate = Test(id="b", name="Chest Examination")

    violations = validator.validate(candidate, None, model)

    assert "name-unique" in _rule_names(violations)


def test_the_same_name_in_another_type_is_allowed(validator: Validator) -> None:
    model = FakeModel(conditions=[Condition(id="a", name="Common Cold")])
    candidate = Symptom(id="b", name="Common Cold")

    violations = validator.validate(candidate, None, model)

    assert "name-unique" not in _rule_names(violations)


def test_editing_a_record_does_not_clash_with_itself(validator: Validator) -> None:
    stored = Condition(id="a", name="Common Cold")
    model = FakeModel(conditions=[stored])

    violations = validator.validate(stored, stored, model)

    assert "name-unique" not in _rule_names(violations)


def test_a_different_records_name_is_still_rejected_while_editing(
    validator: Validator,
) -> None:
    stored = Condition(id="a", name="Common Cold")
    other = Condition(id="b", name="Influenza")
    model = FakeModel(conditions=[stored, other])
    candidate = Condition(id="a", name="Influenza")

    violations = validator.validate(candidate, stored, model)

    assert "name-unique" in _rule_names(violations)


def test_a_nameless_record_is_not_checked_for_uniqueness(validator: Validator) -> None:
    model = FakeModel(conditions=[Condition(id="a", name="Common Cold")])

    assert validator.name_must_be_unique(Condition(id="b"), None, model) == []
    assert (
        validator.name_must_be_unique(Condition(id="b", name="   "), None, model)
        == []
    )
    assert validator.name_must_be_unique(Condition(id="b", name=5), None, model) == []


# --- name_and_aka_must_be_title_cased --------------------------------------


def test_non_title_cased_name_is_rejected(validator: Validator) -> None:
    candidate = Condition(id="a", name="Common cold")

    violations = validator.validate(candidate, None, _empty())

    assert "name-title-case" in _rule_names(violations)
    assert "Common Cold" in violations[0].message


def test_non_title_cased_alternative_name_is_rejected(validator: Validator) -> None:
    candidate = Condition(id="a", name="Common Cold", aka=["Head cold"])

    violations = validator.validate(candidate, None, _empty())

    assert "aka-title-case" in _rule_names(violations)
    assert violations[0].field == "aka[0]"


def test_corrected_values_are_accepted(validator: Validator) -> None:
    candidate = Condition(id="a", name="Shortness of Breath", aka=["Breathlessness"])

    violations = validator.validate(candidate, None, _empty())

    assert not {"name-title-case", "aka-title-case"} & _rule_names(violations)


def test_title_casing_rule_is_idempotent_on_valid_values() -> None:
    for value in ["Shortness of Breath", "Runny Nose", "X-Ray of the Chest"]:
        assert is_title_cased(value)


def test_citations_are_not_subject_to_name_rules(validator: Validator) -> None:
    candidate = Citation(id="a", bibtex=VALID_BIBTEX)

    violations = validator.validate(candidate, None, _empty())

    assert not {
        "name-unique",
        "name-title-case",
        "aka-title-case",
        "aka-name-clash",
    } & _rule_names(violations)


# --- aka_must_not_clash_with_a_name ----------------------------------------


def test_alias_equal_to_the_records_own_name_is_rejected(validator: Validator) -> None:
    candidate = Condition(id="a", name="Common Cold", aka=["Common Cold"])

    violations = validator.validate(candidate, None, _empty())

    assert "aka-name-clash" in _rule_names(violations)
    assert violations[0].field == "aka[0]"


def test_alias_equal_to_another_records_name_is_rejected(
    validator: Validator,
) -> None:
    model = FakeModel(symptoms=[Symptom(id="b", name="Cough")])
    candidate = Symptom(id="a", name="Fever", aka=["Cough"])

    violations = validator.validate(candidate, None, model)

    assert "aka-name-clash" in _rule_names(violations)


def test_alias_equal_to_a_name_of_another_type_is_allowed(
    validator: Validator,
) -> None:
    model = FakeModel(conditions=[Condition(id="b", name="Cough")])
    candidate = Symptom(id="a", name="Fever", aka=["Cough"])

    violations = validator.validate(candidate, None, model)

    assert "aka-name-clash" not in _rule_names(violations)


def test_alias_matching_another_records_alias_is_allowed(
    validator: Validator,
) -> None:
    other = Symptom(id="b", name="Cough", aka=["Tussis"])
    stored = Symptom(id="c", name="Fever", aka=["Tussis"])
    model = FakeModel(symptoms=[other, stored])

    violations = validator.validate(stored, stored, model)

    assert "aka-name-clash" not in _rule_names(violations)


def test_alias_clash_with_another_name_still_applies_while_editing(
    validator: Validator,
) -> None:
    stored = Symptom(id="a", name="Fever", aka=[])
    other = Symptom(id="b", name="Cough", aka=[])
    model = FakeModel(symptoms=[stored, other])
    candidate = Symptom(id="a", name="Fever", aka=["Cough"])

    violations = validator.validate(candidate, stored, model)

    assert "aka-name-clash" in _rule_names(violations)


def test_a_blank_or_non_text_alias_is_ignored(validator: Validator) -> None:
    candidate = Symptom(id="a", name="Fever", aka=["  ", 5])

    assert validator.aka_must_not_clash_with_a_name(candidate, None, _empty()) == []


# --- required relationships ------------------------------------------------


def test_condition_without_a_symptom_is_rejected(validator: Validator) -> None:
    candidate = Condition(id="a", name="Common Cold", symptoms=[])

    violations = validator.validate(candidate, None, _empty())

    assert "reference-required" in _rule_names(violations)


def test_symptom_without_a_test_is_rejected(validator: Validator) -> None:
    candidate = Symptom(id="a", name="Fever", tests=[])

    violations = validator.validate(candidate, None, _empty())

    assert "reference-required" in _rule_names(violations)


# --- references_must_resolve -----------------------------------------------


def test_unresolvable_symptom_reference_is_rejected(validator: Validator) -> None:
    model = FakeModel(citations=[Citation(id="cite")])
    candidate = Condition(
        id="a", name="Common Cold", symptoms=["missing"], citation="cite"
    )

    violations = validator.validate(candidate, None, model)

    assert "reference-unknown" in _rule_names(violations)


def test_unresolvable_citation_reference_is_rejected(validator: Validator) -> None:
    candidate = Symptom(id="a", name="Fever", tests=["t1"], citation="nope")

    violations = validator.validate(candidate, None, _empty())

    assert "reference-unknown" in _rule_names(violations)


def test_resolvable_references_are_accepted(validator: Validator) -> None:
    model = FakeModel(
        symptoms=[Symptom(id="s1", name="Cough")],
        tests=[Test(id="t1", name="Chest Examination")],
        citations=[Citation(id="cite")],
    )
    candidate = Condition(
        id="a",
        name="Common Cold",
        symptoms=["s1"],
        citation="cite",
        priority=3,
    )

    assert validator.validate(candidate, None, model) == []


def test_a_reference_of_the_wrong_type_is_rejected(validator: Validator) -> None:
    candidate = Condition(id="a", name="Common Cold", symptoms=5)

    violations = validator.validate(candidate, None, _empty())

    assert "reference-invalid" in _rule_names(violations)


def test_a_blank_reference_is_rejected(validator: Validator) -> None:
    candidate = Condition(id="a", name="Common Cold", symptoms=["  "])

    violations = validator.validate(candidate, None, _empty())

    assert "reference-invalid" in _rule_names(violations)


def test_a_non_text_reference_is_rejected(validator: Validator) -> None:
    candidate = Condition(id="a", name="Common Cold", symptoms=[42])

    violations = validator.validate(candidate, None, _empty())

    assert "reference-invalid" in _rule_names(violations)


def test_a_single_identifier_is_accepted_as_a_reference(
    validator: Validator,
) -> None:
    model = FakeModel(citations=[Citation(id="cite")])
    candidate = Test(id="a", name="Chest Examination", citation="cite")

    assert validator.validate(candidate, None, model) == []


# --- fields_must_fit -------------------------------------------------------


def test_over_long_name_is_rejected(validator: Validator) -> None:
    candidate = Condition(id="a", name="A" + "a" * 256)

    violations = validator.validate(candidate, None, _empty())

    assert "field-too-long" in _rule_names(violations)


def test_name_at_the_limit_is_accepted(validator: Validator) -> None:
    model = FakeModel(symptoms=[Symptom(id="s1", name="Cough")])
    candidate = Condition(
        id="a",
        name="A" + "a" * 255,
        symptoms=["s1"],
        priority=1,
    )

    assert len(candidate.name) == NAME_MAX_LENGTH
    assert validator.validate(candidate, None, model) == []


def test_over_long_description_is_rejected(validator: Validator) -> None:
    candidate = Test(id="a", name="Fever", desc="x" * 1025)

    violations = validator.validate(candidate, None, _empty())

    assert "field-too-long" in _rule_names(violations)


def test_over_long_citation_field_is_rejected(validator: Validator) -> None:
    candidate = Citation(id="a", bibtex="x" * 2049, ieee="short")

    violations = validator.validate(candidate, None, _empty())

    assert "field-too-long" in _rule_names(violations)


def test_citation_fields_at_the_limit_are_accepted(validator: Validator) -> None:
    candidate = Citation(id="a", bibtex="x" * 2048, ieee="y" * 2048)

    assert validator.fields_must_fit(candidate) == []


def test_over_long_citation_ieee_is_rejected(validator: Validator) -> None:
    candidate = Citation(id="a", bibtex="x" * 2048, ieee="y" * 2049)

    assert "field-too-long" in _rule_names(validator.fields_must_fit(candidate))


def test_a_record_class_without_length_limits_is_not_checked(
    validator: Validator,
) -> None:
    assert validator.fields_must_fit(Record()) == []


# --- bibtex_must_be_valid --------------------------------------------------


def test_valid_bibtex_is_accepted(validator: Validator) -> None:
    candidate = Citation(id="a", bibtex=VALID_BIBTEX)

    assert validator.bibtex_must_be_valid(candidate) == []


@pytest.mark.parametrize(
    "value",
    [
        "",
        "hello world",
        "@misc{a, title={A}}\n@misc{b, title={B}}",
        "@misc{a, title={A}}\n@misc{a, title={B}}",
        "@misc{a, title={A}",
        "@misc{empty}",
    ],
)
def test_invalid_bibtex_is_rejected(validator: Validator, value: str) -> None:
    candidate = Citation(id="a", bibtex=value)

    violations = validator.validate(candidate, None, _empty())

    assert [violation.rule for violation in violations] == ["bibtex-invalid"]
    assert violations[0].field == "bibtex"


def test_non_text_bibtex_is_rejected(validator: Validator) -> None:
    candidate = Citation(id="a", bibtex=5)

    violations = validator.validate(candidate, None, _empty())

    assert "bibtex-invalid" in _rule_names(violations)


# --- condition_priority_must_be_a_whole_number -----------------------------


def test_condition_priority_must_be_a_whole_number(validator: Validator) -> None:
    candidate = Condition(id="a", name="Fever", priority="high")

    violations = validator.validate(candidate, None, _empty())

    assert "field-invalid" in _rule_names(violations)


def test_condition_priority_may_be_zero(validator: Validator) -> None:
    model = FakeModel(symptoms=[Symptom(id="s1", name="Cough")])
    candidate = Condition(id="a", name="Fever", priority=0, symptoms=["s1"])

    assert validator.validate(candidate, None, model) == []


def test_a_boolean_is_not_accepted_as_priority(validator: Validator) -> None:
    candidate = Condition(id="a", name="Fever", priority=True)

    violations = validator.validate(candidate, None, _empty())

    assert "field-invalid" in _rule_names(violations)


def test_a_record_without_a_priority_is_not_checked_for_one(
    validator: Validator,
) -> None:
    assert validator.condition_priority_must_be_a_whole_number(Citation(id="a")) == []


# --- identifier_must_be_unused ---------------------------------------------


def test_a_duplicate_identifier_is_reported(validator: Validator) -> None:
    model = FakeModel(
        citations=[Citation(id="b" * 32, bibtex=VALID_BIBTEX, ieee="i")]
    )
    candidate = Citation(id="b" * 32, bibtex=VALID_BIBTEX, ieee="i")

    violations = validator.validate(candidate, None, model)

    assert [violation.rule for violation in violations] == ["identifier-duplicate"]


def test_a_duplicate_identifier_in_another_type_is_reported(
    validator: Validator,
) -> None:
    model = FakeModel(symptoms=[Symptom(id="b" * 32, name="Cough")])
    candidate = Citation(id="b" * 32, bibtex=VALID_BIBTEX, ieee="i")

    violations = validator.validate(candidate, None, model)

    assert [violation.rule for violation in violations] == ["identifier-duplicate"]


def test_an_unused_identifier_is_accepted(validator: Validator) -> None:
    model = FakeModel(
        citations=[Citation(id="b" * 32, bibtex=VALID_BIBTEX, ieee="i")]
    )
    candidate = Citation(id="c" * 32, bibtex=VALID_BIBTEX, ieee="i")

    assert validator.validate(candidate, None, model) == []


def test_editing_a_record_does_not_collide_with_its_own_identifier(
    validator: Validator,
) -> None:
    stored = Citation(id="b" * 32, bibtex="b", ieee="i")
    model = FakeModel(citations=[stored])

    assert validator.identifier_must_be_unused(stored, stored, model) == []


# --- find_references and check_deletion ------------------------------------


def test_referencing_records_are_reported(validator: Validator) -> None:
    model = FakeModel(
        symptoms=[Symptom(id="s1", name="Cough")],
        conditions=[Condition(id="c1", name="Common Cold", symptoms=["s1"])],
    )

    references = validator.find_references("symptoms", "s1", model)

    assert [(r.entity_type, r.field, r.label) for r in references] == [
        ("conditions", "symptoms", "Common Cold")
    ]


def test_a_referenced_record_cannot_be_deleted(validator: Validator) -> None:
    model = FakeModel(
        symptoms=[Symptom(id="s1", name="Cough")],
        conditions=[Condition(id="c1", name="Common Cold", symptoms=["s1"])],
    )

    violations = validator.check_deletion("symptoms", "s1", model)

    assert [violation.rule for violation in violations] == ["delete-referenced"]
    assert "Common Cold" in violations[0].message


def test_an_unreferenced_record_can_be_deleted(validator: Validator) -> None:
    model = FakeModel(symptoms=[Symptom(id="s1", name="Cough")])

    assert validator.check_deletion("symptoms", "s1", model) == []


def test_a_referenced_citation_cannot_be_deleted(validator: Validator) -> None:
    model = FakeModel(
        citations=[Citation(id="cite", bibtex="b", ieee="i")],
        tests=[Test(id="t1", name="Chest Examination", citation="cite")],
    )

    violations = validator.check_deletion("citations", "cite", model)

    assert violations
    assert violations[0].rule == "delete-referenced"


def test_every_referencing_record_is_listed(validator: Validator) -> None:
    model = FakeModel(
        citations=[Citation(id="cite", bibtex="b", ieee="i")],
        conditions=[
            Condition(id="c1", name="Common Cold", symptoms=["s1"], citation="cite"),
            Condition(id="c2", name="Influenza", symptoms=["s1"], citation="cite"),
        ],
    )

    references = validator.find_references("citations", "cite", model)

    assert len(references) == 2


def test_a_test_can_block_a_citation_deletion(validator: Validator) -> None:
    model = FakeModel(
        symptoms=[Symptom(id="s1", name="Cough", tests=["t1"], citation="cite")],
        citations=[Citation(id="cite", bibtex="b", ieee="i")],
    )

    references = validator.find_references("citations", "cite", model)

    assert [(r.entity_type, r.field) for r in references] == [("symptoms", "citation")]


def test_a_symptom_can_block_a_test_deletion(validator: Validator) -> None:
    model = FakeModel(
        tests=[Test(id="t1", name="Chest Examination")],
        symptoms=[Symptom(id="s1", name="Cough", tests=["t1"])],
    )

    references = validator.find_references("tests", "t1", model)

    assert [(r.entity_type, r.field) for r in references] == [("symptoms", "tests")]


def test_client_only_collections_never_block_a_deletion(validator: Validator) -> None:
    """The guard knows only the four owned collections, so nothing else blocks."""
    model = FakeModel(symptoms=[Symptom(id="s1", name="Cough")])

    assert validator.check_deletion("symptoms", "s1", model) == []


def test_references_only_match_the_entity_type_they_point_at(
    validator: Validator,
) -> None:
    model = FakeModel(
        tests=[Test(id="shared", name="Chest Examination")],
        symptoms=[Symptom(id="s1", name="Cough", tests=["shared"])],
    )

    assert validator.find_references("symptoms", "shared", model) == []
    assert len(validator.find_references("tests", "shared", model)) == 1


def test_a_referencing_record_without_a_name_is_labelled_by_its_identifier(
    validator: Validator,
) -> None:
    model = FakeModel(
        citations=[Citation(id="cite", bibtex="b", ieee="i")],
        symptoms=[Symptom(id="s1", citation="cite")],
    )

    references = validator.find_references("citations", "cite", model)

    assert [reference.label for reference in references] == ["s1"]


def test_a_referencing_record_with_neither_name_nor_identifier_is_unknown(
    validator: Validator,
) -> None:
    model = FakeModel(
        citations=[Citation(id="cite", bibtex="b", ieee="i")],
        symptoms=[Symptom(id=7, citation="cite")],
    )

    references = validator.find_references("citations", "cite", model)

    assert [reference.label for reference in references] == ["<unknown>"]
