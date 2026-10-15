"""Tests for the plain record classes' own behaviour.

Each class shows its own fields, so these tests pin the fields each class writes
and reads. The file read/write paths are covered by ``test_repository.py``.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from editor.models import records
from editor.models.records import (
    ENTITY_TYPES,
    Citation,
    Condition,
    Record,
    RecordError,
    Symptom,
    Test,
)

#: The fields each record class carries, exactly as the data model defines them.
FIELDS_PER_CLASS: dict[type[Record], set[str]] = {
    Condition: {"id", "name", "desc", "symptoms", "priority", "citation", "aka"},
    Symptom: {"id", "name", "desc", "tests", "citation", "aka"},
    Test: {"id", "name", "desc", "citation", "aka"},
    Citation: {"id", "bibtex", "ieee"},
}

#: class, entity type, collection file name, human label.
IDENTITY_PER_CLASS = [
    (Condition, "conditions", "conditions.json", "Condition"),
    (Symptom, "symptoms", "symptoms.json", "Symptom"),
    (Test, "tests", "tests.json", "Test"),
    (Citation, "citations", "citations.json", "Citation"),
]


def test_records_of_the_same_type_and_values_are_equal() -> None:
    assert Condition(id="a", name="A") == Condition(id="a", name="A")


def test_records_of_different_types_are_not_equal() -> None:
    assert Condition(id="a") != Citation(id="a")


def test_a_record_never_equals_a_non_record() -> None:
    assert (Condition(id="a") == "not a record") is False
    assert (Condition(id="a") != "not a record") is True


def test_a_condition_is_a_record() -> None:
    assert isinstance(Condition(id="a"), Record)


@pytest.mark.parametrize(
    ("record_class", "field_names"), list(FIELDS_PER_CLASS.items())
)
def test_each_class_writes_the_fields_its_entity_type_defines(
    record_class: type[Record], field_names: set[str]
) -> None:
    record = record_class(**{name: f"value-{name}" for name in field_names})

    assert set(record.to_dict()) == field_names
    assert record_class.from_dict(record.to_dict()) == record


@pytest.mark.parametrize(
    ("record_class", "entity_type", "filename", "label"), IDENTITY_PER_CLASS
)
def test_each_class_declares_its_identity(
    record_class: type[Record], entity_type: str, filename: str, label: str
) -> None:
    assert record_class.ENTITY_TYPE == entity_type
    assert record_class.FILENAME == filename
    assert record_class.LABEL == label


def test_to_dict_omits_unset_fields() -> None:
    assert Condition(id="a", name="A", aka=[]).to_dict() == {
        "id": "a",
        "name": "A",
        "aka": [],
    }


def test_from_dict_fills_missing_fields_with_none() -> None:
    record = Symptom.from_dict({"id": "a"})

    assert record.id == "a"
    assert record.name is None
    assert record.tests is None


def test_the_key_order_of_a_stored_object_does_not_matter() -> None:
    expected = Condition(id="a", name="A", desc="D", aka=["B"])

    assert (
        Condition.from_dict({"aka": ["B"], "desc": "D", "name": "A", "id": "a"})
        == expected
    )


def test_repr_names_the_set_fields() -> None:
    text = repr(Test(id="a", name="Chest Examination"))

    assert text.startswith("Test(")
    assert "name='Chest Examination'" in text
    assert "ieee" not in text


def test_path_names_the_collection_file(tmp_path: Path) -> None:
    assert Test.path(tmp_path) == tmp_path / "tests.json"


def test_unknown_entity_type_is_rejected_by_the_registry() -> None:
    with pytest.raises(RecordError, match="Unknown entity type"):
        records.record_type("cases")


def test_the_registry_covers_exactly_the_editable_types() -> None:
    assert set(ENTITY_TYPES) == {
        "conditions",
        "symptoms",
        "tests",
        "citations",
    }
