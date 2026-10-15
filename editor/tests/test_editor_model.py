"""Tests for the model facade: the in-memory store and the only writer."""

from __future__ import annotations

from pathlib import Path

from editor.models.editor_model import EditorModel
from editor.models.records import Citation, Condition, Record, Symptom, Test
from editor.models.repository import CollectionRepository


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


# -- reading ----------------------------------------------------------------


def test_the_model_loads_every_owned_collection(tmp_path: Path) -> None:
    model = _model(
        tmp_path,
        conditions=[Condition(id="c1", name="Common Cold")],
        citations=[Citation(id="cite", bibtex="b", ieee="i")],
    )

    assert [record.id for record in model.conditions()] == ["c1"]
    assert model.symptoms() == []
    assert model.tests() == []
    assert [record.id for record in model.citations()] == ["cite"]
    assert len(model.all_records()) == 2


def test_reload_picks_up_a_change_made_outside_the_model(tmp_path: Path) -> None:
    model = _model(tmp_path)

    CollectionRepository(tmp_path).save(
        "citations", [Citation(id="a" * 32, bibtex="b", ieee="i")]
    )
    assert model.citations() == []

    model.reload()

    assert [record.id for record in model.citations()] == ["a" * 32]


def test_a_load_error_is_reported_and_leaves_the_collections_empty(
    tmp_path: Path,
) -> None:
    repository = CollectionRepository(tmp_path)
    repository.save("symptoms", [])
    repository.save("tests", [])
    repository.save("citations", [])
    (tmp_path / "conditions.json").write_text("not json at all", encoding="utf-8")

    model = EditorModel(repository)

    assert model.load_error is not None
    assert "conditions.json" in model.load_error
    assert model.conditions() == []


def test_the_accessors_hand_out_copies(tmp_path: Path) -> None:
    model = _model(tmp_path, conditions=[Condition(id="c1", name="Common Cold")])

    model.conditions().append(Condition(id="c2", name="Influenza"))

    assert len(model.conditions()) == 1


def test_label_for_returns_the_field_that_names_the_record(tmp_path: Path) -> None:
    model = _model(tmp_path)

    assert model.label_for(Condition(id="a", name="Common Cold")) == "Common Cold"
    assert (
        model.label_for(Citation(id="a", bibtex="Some Source", ieee="i"))
        == "Some Source"
    )


def test_label_for_falls_back_to_the_identifier(tmp_path: Path) -> None:
    model = _model(tmp_path)

    assert model.label_for(Condition(id="a")) == "a"
    assert model.label_for(Condition(id="a", name="   ")) == "a"


def test_spec_for_returns_the_entity_spec(tmp_path: Path) -> None:
    model = _model(tmp_path)

    assert model.spec_for("conditions").label == "Condition"


# -- writing ----------------------------------------------------------------


def test_a_valid_new_record_is_stored_with_a_fresh_identifier(
    tmp_path: Path,
) -> None:
    model = _model(tmp_path)

    violations = model.save(Citation(id=None, bibtex="b", ieee="i"))

    assert violations == []
    stored = model.citations()[0]
    assert model.identifiers.is_valid(stored.id)


def test_an_edit_keeps_the_identifier(tmp_path: Path) -> None:
    stored = Citation(id="a" * 32, bibtex="b", ieee="i")
    model = _model(tmp_path, citations=[stored])
    changed = Citation(id=stored.id, bibtex="b2", ieee="i")

    violations = model.save(changed, existing=stored)

    assert violations == []
    assert [record.id for record in model.citations()] == ["a" * 32]
    assert model.citations()[0].bibtex == "b2"


def test_a_record_is_stored_in_its_own_collection(tmp_path: Path) -> None:
    model = _model(
        tmp_path,
        symptoms=[Symptom(id="s1", name="Cough")],
        tests=[Test(id="t1", name="Chest Examination")],
        citations=[Citation(id="cite", bibtex="b", ieee="i")],
    )

    assert model.save(
        Condition(
            id=None,
            name="Common Cold",
            symptoms=["s1"],
            priority=1,
            citation="cite",
        )
    ) == []
    assert model.save(
        Symptom(id=None, name="Fever", tests=["t1"], citation="cite")
    ) == []
    assert model.save(Test(id=None, name="Blood Count", citation="cite")) == []
    assert model.save(Citation(id=None, bibtex="b2", ieee="i2")) == []

    assert len(model.conditions()) == 1
    assert len(model.symptoms()) == 2
    assert len(model.tests()) == 2
    assert len(model.citations()) == 2


def test_a_blocked_save_returns_violations_and_writes_nothing(
    tmp_path: Path,
) -> None:
    model = _model(tmp_path)
    before = (tmp_path / "conditions.json").read_text(encoding="utf-8")

    violations = model.save(
        Condition(id=None, name="Common cold", symptoms=[], priority=1)
    )

    assert violations
    assert model.conditions() == []
    assert (tmp_path / "conditions.json").read_text(encoding="utf-8") == before


def test_a_successful_save_reaches_the_file(tmp_path: Path) -> None:
    model = _model(tmp_path)

    model.save(Citation(id=None, bibtex="b", ieee="i"))

    assert [record.bibtex for record in CollectionRepository(tmp_path).load("citations")] == [
        "b"
    ]


def test_delete_removes_an_unreferenced_record(tmp_path: Path) -> None:
    stored = Citation(id="a" * 32, bibtex="b", ieee="i")
    model = _model(tmp_path, citations=[stored])

    assert model.delete(stored) == []

    assert model.citations() == []
    assert CollectionRepository(tmp_path).load("citations") == []


def test_delete_refuses_a_referenced_record(tmp_path: Path) -> None:
    symptom = Symptom(id="s1", name="Cough", tests=["t1"])
    test = Test(id="t1", name="Chest Examination")
    model = _model(tmp_path, symptoms=[symptom], tests=[test])

    violations = model.delete(test)

    assert [violation.rule for violation in violations] == ["delete-referenced"]
    assert model.tests() == [test]
