"""Tests for the controller layer.

A controller takes values and returns a result, so these tests call one method and
read the return value: no terminal, and no stand-ins for a view.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from editor.controllers.entity_detail import EntityDetailController
from editor.controllers.entity_list import EntityListController
from editor.controllers.home import HomeController
from editor.models.editor_model import EditorModel
from editor.models.records import Citation, Condition, Record, Symptom, Test
from editor.models.repository import CollectionRepository

ENTITY_TYPES = ("conditions", "symptoms", "tests", "citations")
VALID_BIBTEX = "@misc{another, title={Another Source}}"

#: One valid stored record per entity type.
STORED: dict[str, Record] = {
    "conditions": Condition(
        id="c1",
        name="Common Cold",
        desc="A cold",
        aka=["Cold"],
        symptoms=["s1"],
        priority=1,
        citation="z1",
    ),
    "symptoms": Symptom(
        id="s1", name="Cough", desc="A cough", aka=["Tussis"], tests=["t1"], citation="z1"
    ),
    "tests": Test(
        id="t1", name="Chest Examination", desc="A test", aka=["CXR"], citation="z1"
    ),
    "citations": Citation(id="z1", bibtex="Source", ieee="IEEE"),
}


def _model(
    data_directory: Path,
    conditions: list[Record] | None = None,
    symptoms: list[Record] | None = None,
    tests: list[Record] | None = None,
    citations: list[Record] | None = None,
) -> EditorModel:
    """A model over a directory holding exactly these four collections."""
    repository = CollectionRepository(data_directory)
    repository.save("conditions", conditions or [])
    repository.save("symptoms", symptoms or [])
    repository.save("tests", tests or [])
    repository.save("citations", citations or [])
    return EditorModel(repository)


def _labels(controller: EntityListController) -> list[str]:
    return [controller.label_for(record) for record in controller.items()]


# --- HomeController --------------------------------------------------------


def test_the_menu_lists_all_four_entity_types_with_their_labels(
    tmp_path: Path,
) -> None:
    controller = HomeController(_model(tmp_path))

    assert controller.menu() == [
        ("conditions", "Condition"),
        ("symptoms", "Symptom"),
        ("tests", "Test"),
        ("citations", "Citation"),
    ]


# --- EntityListController --------------------------------------------------


def test_items_lists_every_record_of_the_type(tmp_path: Path) -> None:
    model = _model(
        tmp_path,
        conditions=[
            Condition(id="a", name="Common Cold"),
            Condition(id="b", name="Influenza"),
        ],
    )
    controller = EntityListController(model, "conditions")

    assert _labels(controller) == ["Common Cold", "Influenza"]


def test_a_search_term_narrows_the_items(tmp_path: Path) -> None:
    model = _model(
        tmp_path,
        conditions=[
            Condition(id="a", name="Common Cold"),
            Condition(id="b", name="Influenza"),
        ],
    )
    controller = EntityListController(model, "conditions")

    assert _labels(controller) == ["Common Cold", "Influenza"]
    assert [
        controller.label_for(record) for record in controller.items("cold")
    ] == ["Common Cold"]


def test_searching_ignores_case_and_surrounding_space(tmp_path: Path) -> None:
    model = _model(tmp_path, conditions=[Condition(id="a", name="Common Cold")])
    controller = EntityListController(model, "conditions")

    assert len(controller.items("  COMMON  ")) == 1


def test_a_search_term_matches_an_alternative_name(tmp_path: Path) -> None:
    model = _model(
        tmp_path,
        conditions=[
            Condition(id="a", name="Common Cold", aka=["Rhinitis"]),
            Condition(id="b", name="Influenza"),
        ],
    )
    controller = EntityListController(model, "conditions")

    matched = controller.items("rhin")

    assert [controller.label_for(record) for record in matched] == ["Common Cold"]


@pytest.mark.parametrize("entity_type", ENTITY_TYPES)
def test_every_entity_type_can_be_listed(tmp_path: Path, entity_type: str) -> None:
    model = _model(tmp_path, **{entity_type: [STORED[entity_type]]})
    controller = EntityListController(model, entity_type)

    assert len(controller.records()) == 1
    assert _labels(controller) == [model.label_for(STORED[entity_type])]


def test_the_detail_controller_is_bound_to_the_record_it_is_given(
    tmp_path: Path,
) -> None:
    stored = Condition(id="a", name="Common Cold")
    controller = EntityListController(_model(tmp_path, conditions=[stored]), "conditions")

    assert controller.detail_controller(stored).record is stored
    assert controller.detail_controller(None).is_new is True


def test_a_refused_delete_returns_the_violation_and_keeps_the_record(
    tmp_path: Path,
) -> None:
    test = Test(id="t1", name="Chest Examination")
    model = _model(
        tmp_path,
        tests=[test],
        symptoms=[Symptom(id="s1", name="Cough", tests=["t1"])],
    )
    controller = EntityListController(model, "tests")

    violations = controller.delete(test)

    assert [violation.rule for violation in violations] == ["delete-referenced"]
    assert len(controller.records()) == 1


def test_a_successful_delete_removes_the_record(tmp_path: Path) -> None:
    test = Test(id="t1", name="Chest Examination")
    controller = EntityListController(_model(tmp_path, tests=[test]), "tests")

    assert controller.delete(test) == []
    assert controller.records() == []


def test_refresh_reloads_from_disk(tmp_path: Path) -> None:
    controller = EntityListController(_model(tmp_path), "citations")

    CollectionRepository(tmp_path).save(
        "citations", [Citation(id="z1", bibtex="Source", ieee="IEEE")]
    )
    assert controller.items() == []

    controller.refresh()

    assert len(controller.items()) == 1


def test_a_load_error_is_available_to_the_view(tmp_path: Path) -> None:
    repository = CollectionRepository(tmp_path)
    repository.save("symptoms", [])
    repository.save("tests", [])
    repository.save("citations", [])
    (tmp_path / "conditions.json").write_text("not json at all", encoding="utf-8")

    controller = EntityListController(EditorModel(repository), "conditions")

    error = controller.load_error()

    assert error is not None
    assert "conditions.json" in error


# --- EntityDetailController ------------------------------------------------


@pytest.mark.parametrize("entity_type", ENTITY_TYPES)
def test_a_new_record_starts_with_every_field_empty(
    tmp_path: Path, entity_type: str
) -> None:
    controller = EntityDetailController(_model(tmp_path), entity_type)

    assert controller.is_new is True
    assert set(controller.initial_values()) == set(controller.fields())
    assert set(controller.initial_values().values()) == {""}


@pytest.mark.parametrize("entity_type", ENTITY_TYPES)
def test_a_stored_record_fills_every_form_field(
    tmp_path: Path, entity_type: str
) -> None:
    stored = STORED[entity_type]
    controller = EntityDetailController(
        _model(tmp_path, **{entity_type: [stored]}), entity_type, stored
    )

    values = controller.initial_values()

    assert set(values) == set(controller.fields())
    assert all(value != "" for value in values.values())


def test_the_initial_values_show_the_stored_record(tmp_path: Path) -> None:
    stored = STORED["conditions"]
    controller = EntityDetailController(
        _model(tmp_path, conditions=[stored]), "conditions", stored
    )

    assert controller.initial_values() == {
        "name": "Common Cold",
        "desc": "A cold",
        "aka": "Cold",
        "symptoms": "s1",
        "priority": "1",
        "citation": "z1",
    }


def test_citation_initial_values_show_the_stored_ieee(tmp_path: Path) -> None:
    stored = Citation(
        id="z1",
        bibtex="@misc{reference, title={Reference}}",
        ieee="hand authored",
    )
    controller = EntityDetailController(
        _model(tmp_path, citations=[stored]), "citations", stored
    )

    assert controller.initial_values() == {
        "bibtex": "@misc{reference, title={Reference}}",
        "ieee": "hand authored",
    }


def test_the_form_ieee_value_is_ignored(tmp_path: Path) -> None:
    model = _model(tmp_path)
    controller = EntityDetailController(model, "citations")

    violations = controller.save(
        {"bibtex": VALID_BIBTEX, "ieee": "typed by hand"}
    )

    assert violations == []
    assert model.citations()[0].ieee == '"Another Source".'


def test_a_valid_new_record_is_stored_from_the_form(tmp_path: Path) -> None:
    model = _model(
        tmp_path,
        symptoms=[Symptom(id="s1", name="Cough")],
        citations=[Citation(id="z1", bibtex="Source", ieee="IEEE")],
    )
    controller = EntityDetailController(model, "conditions")

    violations = controller.save(
        {
            "name": "Common Cold",
            "desc": "A cold",
            "aka": "Cold, Rhinitis",
            "symptoms": "s1",
            "priority": "2",
            "citation": "z1",
        }
    )

    assert violations == []
    stored = model.conditions()[0]
    assert stored.name == "Common Cold"
    assert stored.aka == ["Cold", "Rhinitis"]
    assert stored.symptoms == ["s1"]
    assert stored.priority == 2
    assert model.identifiers.is_valid(stored.id)
    assert controller.is_new is False


def test_an_edit_keeps_the_identifier(tmp_path: Path) -> None:
    stored = Condition(
        id="a" * 32,
        name="Common Cold",
        symptoms=["s1"],
        priority=1,
        citation="z1",
    )
    model = _model(
        tmp_path,
        conditions=[stored],
        symptoms=[Symptom(id="s1", name="Cough")],
        citations=[Citation(id="z1", bibtex="Source", ieee="IEEE")],
    )
    controller = EntityDetailController(model, "conditions", stored)

    violations = controller.save(
        {
            "name": "Influenza",
            "desc": "",
            "aka": "",
            "symptoms": "s1",
            "priority": "1",
            "citation": "z1",
        }
    )

    assert violations == []
    assert [record.id for record in model.conditions()] == ["a" * 32]
    assert model.conditions()[0].name == "Influenza"


def test_invalid_values_return_violations_and_write_nothing(tmp_path: Path) -> None:
    model = _model(tmp_path, symptoms=[Symptom(id="s1", name="Cough")])
    controller = EntityDetailController(model, "conditions")

    violations = controller.save(
        {
            "name": "common cold",
            "desc": "",
            "aka": "",
            "symptoms": "s1",
            "priority": "1",
            "citation": "",
        }
    )

    rules_hit = {violation.rule for violation in violations}
    assert "name-title-case" in rules_hit
    assert "reference-invalid" in rules_hit
    assert model.conditions() == []


def test_a_non_numeric_priority_is_rejected_by_the_rules(tmp_path: Path) -> None:
    model = _model(
        tmp_path,
        symptoms=[Symptom(id="s1", name="Cough")],
        citations=[Citation(id="z1", bibtex="Source", ieee="IEEE")],
    )
    controller = EntityDetailController(model, "conditions")

    violations = controller.save(
        {
            "name": "Common Cold",
            "desc": "",
            "aka": "",
            "symptoms": "s1",
            "priority": "high",
            "citation": "z1",
        }
    )

    assert [violation.rule for violation in violations] == ["field-invalid"]
    assert model.conditions() == []


def test_every_entity_type_can_be_saved_from_the_form(tmp_path: Path) -> None:
    model = _model(
        tmp_path,
        symptoms=[Symptom(id="s1", name="Cough")],
        tests=[Test(id="t1", name="Chest Examination")],
        citations=[Citation(id="z1", bibtex="Source", ieee="IEEE")],
    )

    assert EntityDetailController(model, "conditions").save(
        {
            "name": "Common Cold",
            "desc": "",
            "aka": "",
            "symptoms": "s1",
            "priority": "1",
            "citation": "z1",
        }
    ) == []
    assert EntityDetailController(model, "symptoms").save(
        {"name": "Fever", "desc": "", "aka": "", "tests": "t1", "citation": "z1"}
    ) == []
    assert EntityDetailController(model, "tests").save(
        {"name": "Blood Count", "desc": "", "aka": "", "citation": "z1"}
    ) == []
    assert EntityDetailController(model, "citations").save(
        {"bibtex": VALID_BIBTEX, "ieee": "IEEE"}
    ) == []

    assert len(model.all_records()) == 7


# --- references on the detail form -----------------------------------------


def test_attached_references_keep_stored_order_and_report_unknowns(
    tmp_path: Path,
) -> None:
    stored = Condition(
        id="a" * 32,
        name="Common Cold",
        symptoms=["s2", "missing", "s1"],
    )
    model = _model(
        tmp_path,
        conditions=[stored],
        symptoms=[Symptom(id="s1", name="Cough"), Symptom(id="s2", name="Fever")],
    )
    controller = EntityDetailController(model, "conditions", stored)

    attached = controller.attached_references("symptoms")

    assert [reference.identifier for reference in attached] == [
        "s2",
        "missing",
        "s1",
    ]
    assert [
        reference.record.name if reference.record else None
        for reference in attached
    ] == ["Fever", None, "Cough"]


def test_a_new_record_has_no_attached_references(tmp_path: Path) -> None:
    controller = EntityDetailController(
        _model(tmp_path, symptoms=[Symptom(id="s1", name="Cough")]),
        "conditions",
    )

    assert controller.attached_references("symptoms") == []


def test_available_references_leave_out_the_attached_records(
    tmp_path: Path,
) -> None:
    model = _model(
        tmp_path,
        symptoms=[
            Symptom(id="s1", name="Cough"),
            Symptom(id="s2", name="Fever"),
            Symptom(id="s3", name="Sore Throat"),
        ],
    )
    stored = Condition(id="a" * 32, name="Common Cold", symptoms=["s1"])
    controller = EntityDetailController(model, "conditions", stored)

    assert [
        choice.identifier for choice in controller.available_references("symptoms")
    ] == ["s2", "s3"]
    assert [
        choice.identifier
        for choice in controller.available_references("symptoms", attached=["s2"])
    ] == ["s3"]


def test_available_references_annotate_alternative_name_matches(
    tmp_path: Path,
) -> None:
    model = _model(
        tmp_path,
        symptoms=[Symptom(id="s2", name="Fever", aka=["Pyrexia"])],
    )
    controller = EntityDetailController(model, "conditions")

    choices = controller.available_references("symptoms", "pyr")

    assert [(choice.identifier, choice.label) for choice in choices] == [
        ("s2", "Fever (Pyrexia)")
    ]


def test_a_name_match_in_the_picker_is_not_annotated(tmp_path: Path) -> None:
    model = _model(
        tmp_path,
        symptoms=[Symptom(id="s2", name="Fever", aka=["Pyrexia"])],
    )
    controller = EntityDetailController(model, "conditions")

    choices = controller.available_references("symptoms", "fev")

    assert [(choice.identifier, choice.label) for choice in choices] == [
        ("s2", "Fever")
    ]


def test_lookup_reference_returns_the_current_record(tmp_path: Path) -> None:
    model = _model(tmp_path, symptoms=[Symptom(id="s1", name="Cough")])
    stored = Condition(id="a" * 32, name="Common Cold", symptoms=["s1"])
    controller = EntityDetailController(model, "conditions", stored)

    found = controller.lookup_reference("symptoms", "s1")

    assert found is not None
    assert found.name == "Cough"
    assert controller.lookup_reference("symptoms", "missing") is None


def test_a_reference_field_accepts_a_list_of_identifiers(tmp_path: Path) -> None:
    model = _model(
        tmp_path,
        symptoms=[Symptom(id="s1", name="Cough"), Symptom(id="s2", name="Fever")],
        citations=[Citation(id="z1", bibtex="Source", ieee="IEEE")],
    )
    controller = EntityDetailController(model, "conditions")

    violations = controller.save(
        {
            "name": "Common Cold",
            "desc": "",
            "aka": "",
            "symptoms": ["s2", "s1"],
            "priority": "1",
            "citation": "z1",
        }
    )

    assert violations == []
    assert model.conditions()[0].symptoms == ["s2", "s1"]


def test_a_symptom_test_reference_accepts_a_list(tmp_path: Path) -> None:
    model = _model(
        tmp_path,
        tests=[Test(id="t1", name="Chest Examination")],
        citations=[Citation(id="z1", bibtex="Source", ieee="IEEE")],
    )
    controller = EntityDetailController(model, "symptoms")

    violations = controller.save(
        {
            "name": "Cough",
            "desc": "",
            "aka": "",
            "tests": ["t1"],
            "citation": "z1",
        }
    )

    assert violations == []
    assert model.symptoms()[0].tests == ["t1"]


def test_an_empty_reference_list_is_still_required(tmp_path: Path) -> None:
    model = _model(
        tmp_path,
        citations=[Citation(id="z1", bibtex="Source", ieee="IEEE")],
    )
    controller = EntityDetailController(model, "conditions")

    violations = controller.save(
        {
            "name": "Common Cold",
            "desc": "",
            "aka": "",
            "symptoms": [],
            "priority": "1",
            "citation": "z1",
        }
    )

    assert "reference-required" in {violation.rule for violation in violations}
    assert model.conditions() == []
