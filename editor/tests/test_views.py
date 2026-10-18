"""View tests: listing, searching, editing, blocked writes, and deletions.

Every case drives the real Textual views with the pilot and asserts what the
view shows or what reached the store on disk.
"""

from __future__ import annotations

import asyncio
from pathlib import Path

import pytest
from textual.widgets import (
    Button,
    Input,
    ListView,
    OptionList,
    SelectionList,
    Static,
    TextArea,
)

from editor.app import EditorApp
from editor.models.records import (
    Citation,
    Condition,
    Record,
    RecordError,
    Symptom,
    Test,
)
from editor.models.repository import CollectionRepository
from editor.views.detail import EntityDetailView
from editor.views.home import HomeView
from editor.views.list import EntityListView
from editor.views.picker import ReferencePickerView

CITATION_ID = "d" * 32
TEST_ID = "c" * 32
SYMPTOM_ID = "b" * 32
CONDITION_ID = "a" * 32
SECOND_CONDITION_ID = "e" * 32
SECOND_SYMPTOM_ID = "f" * 32
THIRD_SYMPTOM_ID = "9" * 32
SECOND_TEST_ID = "8" * 32


def _seed(data_directory: Path) -> None:
    """Write a small, fully valid store."""
    repository = CollectionRepository(data_directory)
    repository.save(
        "citations",
        [
            Citation(
                id=CITATION_ID,
                bibtex="@misc{ref, title={Reference}}",
                ieee="Reference.",
            )
        ],
    )
    repository.save(
        "tests",
        [
            Test(
                id=TEST_ID,
                name="Chest Examination",
                desc="Examination of the chest.",
                aka=[],
                citation=CITATION_ID,
            )
        ],
    )
    repository.save(
        "symptoms",
        [
            Symptom(
                id=SYMPTOM_ID,
                name="Cough",
                desc="A forceful expulsion of air.",
                aka=["Tussis"],
                tests=[TEST_ID],
                citation=CITATION_ID,
            )
        ],
    )
    repository.save(
        "conditions",
        [
            Condition(
                id=CONDITION_ID,
                name="Common Cold",
                desc="A mild upper respiratory infection.",
                aka=[],
                symptoms=[SYMPTOM_ID],
                priority=1,
                citation=CITATION_ID,
            ),
            Condition(
                id=SECOND_CONDITION_ID,
                name="Influenza",
                desc="An acute viral respiratory illness.",
                aka=[],
                symptoms=[SYMPTOM_ID],
                priority=3,
                citation=CITATION_ID,
            ),
        ],
    )


def _stored(data_directory: Path, entity_type: str) -> list[Record]:
    """Return what is on disk for one collection."""
    return CollectionRepository(data_directory).load(entity_type)


def _add_records(data_directory: Path, entity_type: str, *records: Record) -> None:
    """Append records to one collection and write it back."""
    repository = CollectionRepository(data_directory)
    repository.save(entity_type, [*repository.load(entity_type), *records])


def _status(view: EntityListView) -> str:
    """Return the status line the view is showing."""
    return str(view.query_one("#status", Static).content)


def _violations(view: EntityDetailView) -> str:
    """Return what the view is showing as the reason a write was refused."""
    return str(view.query_one("#violations", Static).content)


def _picker_status(view: ReferencePickerView) -> str:
    """Return the message the picker shows under its search box."""
    return str(view.query_one("#picker-status", Static).content)


def _select(view: EntityListView, index: int) -> None:
    view.query_one("#records", ListView).index = index


def _fill(detail: EntityDetailView, **values: str) -> None:
    """Fill the form, attaching references instead of typing identifier lists."""
    for field_name, value in values.items():
        field_spec = next(
            field for field in detail.controller.spec.fields if field.name == field_name
        )
        if field_spec.kind == "reference_list":
            identifiers = [part.strip() for part in value.split(",") if part.strip()]
            detail.attach_references(field_name, identifiers)
            continue
        widget_id = f"#field-{field_name}"
        if field_spec.kind == "long_text":
            detail.query_one(widget_id, TextArea).text = value
        else:
            detail.query_one(widget_id, Input).value = value


# --- listing and search ----------------------------------------------------


def test_listing_shows_every_record_of_the_type(tmp_path: Path) -> None:
    async def scenario() -> None:
        _seed(tmp_path)
        app = EditorApp(tmp_path, initial_entity_type="conditions")

        async with app.run_test() as pilot:
            await pilot.pause()
            view = app.screen
            assert isinstance(view, EntityListView)

            assert view.visible_labels() == ["Common Cold", "Influenza"]

    asyncio.run(scenario())


def test_search_narrows_the_list(tmp_path: Path) -> None:
    async def scenario() -> None:
        _seed(tmp_path)
        app = EditorApp(tmp_path, initial_entity_type="conditions")

        async with app.run_test() as pilot:
            await pilot.pause()
            view = app.screen
            assert isinstance(view, EntityListView)

            view.query_one("#search", Input).value = "influ"
            await pilot.pause()

            assert view.visible_labels() == ["Influenza"]

    asyncio.run(scenario())


def test_labels_fall_back_to_the_identifier(tmp_path: Path) -> None:
    async def scenario() -> None:
        _seed(tmp_path)
        CollectionRepository(tmp_path).save(
            "conditions", [Condition(id=CONDITION_ID)]
        )
        app = EditorApp(tmp_path, initial_entity_type="conditions")

        async with app.run_test() as pilot:
            await pilot.pause()
            view = app.screen
            assert isinstance(view, EntityListView)

            assert view.visible_labels() == [CONDITION_ID]

    asyncio.run(scenario())


def test_actions_without_a_selection_report_it(tmp_path: Path) -> None:
    async def scenario() -> None:
        CollectionRepository(tmp_path).save("conditions", [])
        app = EditorApp(tmp_path, initial_entity_type="conditions")

        async with app.run_test() as pilot:
            await pilot.pause()
            view = app.screen
            assert isinstance(view, EntityListView)

            view.action_edit()
            await pilot.pause()
            assert _status(view) == "Select a record to edit."

            view.action_delete()
            await pilot.pause()
            assert _status(view) == "Select a record to delete."

    asyncio.run(scenario())


def test_a_load_error_is_shown_when_the_view_mounts(tmp_path: Path) -> None:
    async def scenario() -> None:
        (tmp_path / "conditions.json").write_text("not json", encoding="utf-8")
        app = EditorApp(tmp_path, initial_entity_type="conditions")

        async with app.run_test() as pilot:
            await pilot.pause()
            view = app.screen
            assert isinstance(view, EntityListView)

            assert "conditions.json" in _status(view)

    asyncio.run(scenario())


def test_a_failed_reload_after_saving_is_reported(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    async def scenario() -> None:
        _seed(tmp_path)
        app = EditorApp(tmp_path, initial_entity_type="conditions")

        async with app.run_test() as pilot:
            await pilot.pause()
            view = app.screen
            assert isinstance(view, EntityListView)

            def explode(self: CollectionRepository) -> dict[str, list[Record]]:
                raise RecordError("Could not read conditions.json.")

            monkeypatch.setattr(CollectionRepository, "load_all", explode)

            view.after_detail(True)
            await pilot.pause()

            assert "conditions.json" in _status(view)

    asyncio.run(scenario())


# --- reference tables ------------------------------------------------------


def test_editing_shows_attached_references_as_rows(tmp_path: Path) -> None:
    async def scenario() -> None:
        _seed(tmp_path)
        app = EditorApp(tmp_path, initial_entity_type="conditions")

        async with app.run_test() as pilot:
            await pilot.pause()
            view = app.screen
            assert isinstance(view, EntityListView)

            _select(view, 0)
            await pilot.pause()
            view.action_edit()
            await pilot.pause()

            detail = app.screen
            assert isinstance(detail, EntityDetailView)

            rows = detail.reference_rows("symptoms")
            assert [row.identifier for row in rows] == [SYMPTOM_ID]
            assert rows[0].label == "Cough"
            assert detail.reference_identifiers("symptoms") == [SYMPTOM_ID]

    asyncio.run(scenario())


def test_a_new_record_starts_with_an_empty_reference_table(
    tmp_path: Path,
) -> None:
    async def scenario() -> None:
        _seed(tmp_path)
        app = EditorApp(tmp_path, initial_entity_type="conditions")

        async with app.run_test() as pilot:
            await pilot.pause()
            view = app.screen
            assert isinstance(view, EntityListView)

            view.action_add()
            await pilot.pause()

            detail = app.screen
            assert isinstance(detail, EntityDetailView)

            assert detail.reference_rows("symptoms") == []
            assert detail.query_one("#add-symptoms") is not None

    asyncio.run(scenario())


def test_removing_a_reference_updates_the_form_and_the_store(
    tmp_path: Path,
) -> None:
    async def scenario() -> None:
        _seed(tmp_path)
        repository = CollectionRepository(tmp_path)
        repository.save(
            "symptoms",
            [
                Symptom(
                    id=SYMPTOM_ID,
                    name="Cough",
                    tests=[TEST_ID],
                    citation=CITATION_ID,
                ),
                Symptom(
                    id=SECOND_SYMPTOM_ID,
                    name="Fever",
                    tests=[TEST_ID],
                    citation=CITATION_ID,
                ),
            ],
        )
        repository.save(
            "conditions",
            [
                Condition(
                    id=CONDITION_ID,
                    name="Common Cold",
                    symptoms=[SYMPTOM_ID, SECOND_SYMPTOM_ID],
                    priority=1,
                    citation=CITATION_ID,
                )
            ],
        )
        app = EditorApp(tmp_path, initial_entity_type="conditions")

        async with app.run_test() as pilot:
            await pilot.pause()
            view = app.screen
            assert isinstance(view, EntityListView)

            _select(view, 0)
            await pilot.pause()
            view.action_edit()
            await pilot.pause()

            detail = app.screen
            assert isinstance(detail, EntityDetailView)
            assert detail.reference_identifiers("symptoms") == [
                SYMPTOM_ID,
                SECOND_SYMPTOM_ID,
            ]

            first_row = detail.reference_rows("symptoms")[0]
            detail.on_button_pressed(
                Button.Pressed(first_row.query_one(".reference-remove", Button))
            )
            await pilot.pause()

            assert detail.reference_identifiers("symptoms") == [SECOND_SYMPTOM_ID]
            assert detail.values()["symptoms"] == [SECOND_SYMPTOM_ID]

            detail.action_save()
            await pilot.pause()

            stored = _stored(tmp_path, "conditions")[0]
            assert stored.symptoms == [SECOND_SYMPTOM_ID]

    asyncio.run(scenario())


def test_opening_a_reference_returns_to_the_form_with_its_edits(
    tmp_path: Path,
) -> None:
    async def scenario() -> None:
        _seed(tmp_path)
        app = EditorApp(tmp_path, initial_entity_type="conditions")

        async with app.run_test() as pilot:
            await pilot.pause()
            view = app.screen
            assert isinstance(view, EntityListView)

            _select(view, 0)
            await pilot.pause()
            view.action_edit()
            await pilot.pause()

            detail = app.screen
            assert isinstance(detail, EntityDetailView)
            _fill(detail, name="Cold In Progress")

            row = detail.reference_rows("symptoms")[0]
            detail.on_button_pressed(
                Button.Pressed(row.query_one(".reference-goto", Button))
            )
            await pilot.pause()

            referenced = app.screen
            assert isinstance(referenced, EntityDetailView)
            assert referenced.controller.spec.entity_type == "symptoms"

            _fill(referenced, name="Coughing")
            referenced.action_save()
            await pilot.pause()

            assert app.screen is detail
            assert detail.values()["name"] == "Cold In Progress"
            assert detail.reference_rows("symptoms")[0].label == "Coughing"
            assert _stored(tmp_path, "conditions")[0].name == "Common Cold"

    asyncio.run(scenario())


def test_an_unresolvable_reference_is_shown_and_can_be_removed(
    tmp_path: Path,
) -> None:
    async def scenario() -> None:
        _seed(tmp_path)
        CollectionRepository(tmp_path).save(
            "conditions",
            [
                Condition(
                    id=CONDITION_ID,
                    name="Common Cold",
                    symptoms=["missing", SYMPTOM_ID],
                    priority=1,
                    citation=CITATION_ID,
                )
            ],
        )
        app = EditorApp(tmp_path, initial_entity_type="conditions")

        async with app.run_test() as pilot:
            await pilot.pause()
            view = app.screen
            assert isinstance(view, EntityListView)

            _select(view, 0)
            await pilot.pause()
            view.action_edit()
            await pilot.pause()

            detail = app.screen
            assert isinstance(detail, EntityDetailView)
            unknown, known = detail.reference_rows("symptoms")

            assert unknown.label == "Unknown"
            assert unknown.query_one(".reference-goto", Button).disabled is True
            assert known.query_one(".reference-goto", Button).disabled is False

            detail.action_save()
            await pilot.pause()

            assert app.screen is detail
            assert "does not exist" in _violations(detail)

            detail.on_button_pressed(
                Button.Pressed(unknown.query_one(".reference-remove", Button))
            )
            await pilot.pause()
            detail.action_save()
            await pilot.pause()

            assert app.screen is view
            assert _stored(tmp_path, "conditions")[0].symptoms == [SYMPTOM_ID]

    asyncio.run(scenario())


def test_the_picker_searches_names_and_alternative_names(
    tmp_path: Path,
) -> None:
    async def scenario() -> None:
        _seed(tmp_path)
        _add_records(
            tmp_path,
            "symptoms",
            Symptom(
                id=SECOND_SYMPTOM_ID,
                name="Fever",
                aka=["Pyrexia"],
                tests=[TEST_ID],
                citation=CITATION_ID,
            ),
            Symptom(
                id=THIRD_SYMPTOM_ID,
                name="Sore Throat",
                tests=[TEST_ID],
                citation=CITATION_ID,
            ),
        )
        app = EditorApp(tmp_path, initial_entity_type="conditions")

        async with app.run_test() as pilot:
            await pilot.pause()
            view = app.screen
            assert isinstance(view, EntityListView)

            _select(view, 0)
            await pilot.pause()
            view.action_edit()
            await pilot.pause()

            detail = app.screen
            assert isinstance(detail, EntityDetailView)

            detail.open_reference_picker("symptoms")
            await pilot.pause()

            picker = app.screen
            assert isinstance(picker, ReferencePickerView)
            options = picker.query_one("#picker-options", SelectionList)
            assert options.option_count == 2
            assert [
                str(options.get_option_at_index(index).prompt)
                for index in range(options.option_count)
            ] == ["Fever", "Sore Throat"]

            options.select(SECOND_SYMPTOM_ID)
            await pilot.pause()

            picker.query_one("#picker-search", Input).value = "pyr"
            await pilot.pause()

            assert options.option_count == 1
            assert str(options.get_option_at_index(0).prompt) == "Fever (Pyrexia)"

            picker.query_one("#picker-search", Input).value = "sore"
            await pilot.pause()

            assert options.option_count == 1
            assert SECOND_SYMPTOM_ID in picker.chosen

            picker.action_attach()
            await pilot.pause()

            assert app.screen is detail
            assert detail.reference_identifiers("symptoms") == [
                SYMPTOM_ID,
                SECOND_SYMPTOM_ID,
            ]

            detail.action_save()
            await pilot.pause()

            assert _stored(tmp_path, "conditions")[0].symptoms == [
                SYMPTOM_ID,
                SECOND_SYMPTOM_ID,
            ]

    asyncio.run(scenario())


def test_attaching_several_records_at_once(tmp_path: Path) -> None:
    async def scenario() -> None:
        _seed(tmp_path)
        _add_records(
            tmp_path,
            "symptoms",
            Symptom(
                id=SECOND_SYMPTOM_ID,
                name="Fever",
                tests=[TEST_ID],
                citation=CITATION_ID,
            ),
            Symptom(
                id=THIRD_SYMPTOM_ID,
                name="Sore Throat",
                tests=[TEST_ID],
                citation=CITATION_ID,
            ),
        )
        app = EditorApp(tmp_path, initial_entity_type="conditions")

        async with app.run_test() as pilot:
            await pilot.pause()
            view = app.screen
            assert isinstance(view, EntityListView)

            _select(view, 0)
            await pilot.pause()
            view.action_edit()
            await pilot.pause()

            detail = app.screen
            assert isinstance(detail, EntityDetailView)

            detail.open_reference_picker("symptoms")
            await pilot.pause()

            picker = app.screen
            assert isinstance(picker, ReferencePickerView)
            options = picker.query_one("#picker-options", SelectionList)
            options.select(SECOND_SYMPTOM_ID)
            options.select(THIRD_SYMPTOM_ID)
            await pilot.pause()

            picker.action_attach()
            await pilot.pause()

            assert detail.reference_identifiers("symptoms") == [
                SYMPTOM_ID,
                SECOND_SYMPTOM_ID,
                THIRD_SYMPTOM_ID,
            ]

            detail.action_save()
            await pilot.pause()

            assert _stored(tmp_path, "conditions")[0].symptoms == [
                SYMPTOM_ID,
                SECOND_SYMPTOM_ID,
                THIRD_SYMPTOM_ID,
            ]

    asyncio.run(scenario())


def test_the_same_table_edits_a_symptoms_tests(tmp_path: Path) -> None:
    async def scenario() -> None:
        _seed(tmp_path)
        _add_records(
            tmp_path,
            "tests",
            Test(id=SECOND_TEST_ID, name="Blood Count", citation=CITATION_ID),
        )
        app = EditorApp(tmp_path, initial_entity_type="symptoms")

        async with app.run_test() as pilot:
            await pilot.pause()
            view = app.screen
            assert isinstance(view, EntityListView)

            _select(view, 0)
            await pilot.pause()
            view.action_edit()
            await pilot.pause()

            detail = app.screen
            assert isinstance(detail, EntityDetailView)
            assert detail.reference_identifiers("tests") == [TEST_ID]

            detail.open_reference_picker("tests")
            await pilot.pause()

            picker = app.screen
            assert isinstance(picker, ReferencePickerView)
            options = picker.query_one("#picker-options", SelectionList)
            assert options.option_count == 1
            options.select(SECOND_TEST_ID)
            await pilot.pause()

            picker.action_attach()
            await pilot.pause()

            assert detail.reference_identifiers("tests") == [
                TEST_ID,
                SECOND_TEST_ID,
            ]

            detail.action_save()
            await pilot.pause()

            assert _stored(tmp_path, "symptoms")[0].tests == [
                TEST_ID,
                SECOND_TEST_ID,
            ]

    asyncio.run(scenario())


def test_the_picker_reports_when_there_is_nothing_to_attach(
    tmp_path: Path,
) -> None:
    async def scenario() -> None:
        _seed(tmp_path)
        app = EditorApp(tmp_path, initial_entity_type="conditions")

        async with app.run_test() as pilot:
            await pilot.pause()
            view = app.screen
            assert isinstance(view, EntityListView)

            _select(view, 0)
            await pilot.pause()
            view.action_edit()
            await pilot.pause()

            detail = app.screen
            assert isinstance(detail, EntityDetailView)
            detail.open_reference_picker("symptoms")
            await pilot.pause()

            picker = app.screen
            assert isinstance(picker, ReferencePickerView)
            assert _picker_status(picker) == "No records available to attach."

            picker.on_button_pressed(
                Button.Pressed(picker.query_one("#cancel", Button))
            )
            await pilot.pause()

            assert app.screen is detail
            assert detail.reference_identifiers("symptoms") == [SYMPTOM_ID]

    asyncio.run(scenario())


# --- adding and editing ----------------------------------------------------


def test_adding_a_record_stores_and_lists_it(tmp_path: Path) -> None:
    async def scenario() -> None:
        _seed(tmp_path)
        app = EditorApp(tmp_path, initial_entity_type="conditions")

        async with app.run_test() as pilot:
            await pilot.pause()
            view = app.screen
            assert isinstance(view, EntityListView)

            view.action_add()
            await pilot.pause()

            detail = app.screen
            assert isinstance(detail, EntityDetailView)
            _fill(
                detail,
                name="Pneumonia",
                desc="An infection of the lung tissue.",
                aka="",
                symptoms=SYMPTOM_ID,
                priority="5",
                citation=CITATION_ID,
            )
            detail.action_save()
            await pilot.pause()

            assert [record.name for record in _stored(tmp_path, "conditions")] == [
                "Common Cold",
                "Influenza",
                "Pneumonia",
            ]
            assert view.visible_labels() == [
                "Common Cold",
                "Influenza",
                "Pneumonia",
            ]
            assert _status(view) == "Saved."

    asyncio.run(scenario())


def test_editing_keeps_the_identifier(tmp_path: Path) -> None:
    async def scenario() -> None:
        _seed(tmp_path)
        app = EditorApp(tmp_path, initial_entity_type="conditions")

        async with app.run_test() as pilot:
            await pilot.pause()
            view = app.screen
            assert isinstance(view, EntityListView)

            _select(view, 0)
            await pilot.pause()
            view.action_edit()
            await pilot.pause()

            detail = app.screen
            assert isinstance(detail, EntityDetailView)
            _fill(detail, name="Common Cold Virus")
            detail.action_save()
            await pilot.pause()

            renamed = [
                record
                for record in _stored(tmp_path, "conditions")
                if record.name == "Common Cold Virus"
            ]
            assert len(renamed) == 1
            assert renamed[0].id == CONDITION_ID

    asyncio.run(scenario())


def test_abandoned_edits_are_discarded(tmp_path: Path) -> None:
    async def scenario() -> None:
        _seed(tmp_path)
        app = EditorApp(tmp_path, initial_entity_type="conditions")
        before = (tmp_path / "conditions.json").read_text(encoding="utf-8")

        async with app.run_test() as pilot:
            await pilot.pause()
            view = app.screen
            assert isinstance(view, EntityListView)

            _select(view, 0)
            await pilot.pause()
            view.action_edit()
            await pilot.pause()

            detail = app.screen
            assert isinstance(detail, EntityDetailView)
            _fill(detail, name="Something Else")
            detail.action_cancel()
            await pilot.pause()

            assert app.screen is view
            assert (tmp_path / "conditions.json").read_text(
                encoding="utf-8"
            ) == before

    asyncio.run(scenario())


def test_a_blocked_write_keeps_the_view_open_and_shows_the_warning(
    tmp_path: Path,
) -> None:
    async def scenario() -> None:
        _seed(tmp_path)
        app = EditorApp(tmp_path, initial_entity_type="conditions")
        before = (tmp_path / "conditions.json").read_text(encoding="utf-8")

        async with app.run_test() as pilot:
            await pilot.pause()
            view = app.screen
            assert isinstance(view, EntityListView)

            view.action_add()
            await pilot.pause()

            detail = app.screen
            assert isinstance(detail, EntityDetailView)
            _fill(
                detail,
                name="pneumonia",
                desc="An infection of the lung tissue.",
                aka="",
                symptoms=SYMPTOM_ID,
                priority="5",
                citation=CITATION_ID,
            )
            detail.action_save()
            await pilot.pause()

            assert app.screen is detail
            assert "not title cased" in _violations(detail)
            assert (tmp_path / "conditions.json").read_text(
                encoding="utf-8"
            ) == before

    asyncio.run(scenario())


def test_a_null_field_starts_empty(tmp_path: Path) -> None:
    async def scenario() -> None:
        _seed(tmp_path)
        CollectionRepository(tmp_path).save(
            "conditions", [Condition(id=CONDITION_ID, name="Common Cold")]
        )
        app = EditorApp(tmp_path, initial_entity_type="conditions")

        async with app.run_test() as pilot:
            await pilot.pause()
            view = app.screen
            assert isinstance(view, EntityListView)

            _select(view, 0)
            await pilot.pause()
            view.action_edit()
            await pilot.pause()

            detail = app.screen
            assert isinstance(detail, EntityDetailView)

            assert detail.values() == {
                "name": "Common Cold",
                "desc": "",
                "aka": "",
                "symptoms": [],
                "priority": "",
                "citation": "",
            }

    asyncio.run(scenario())


def test_description_supports_multiline_text(tmp_path: Path) -> None:
    async def scenario() -> None:
        _seed(tmp_path)
        app = EditorApp(tmp_path, initial_entity_type="conditions")

        async with app.run_test() as pilot:
            await pilot.pause()
            view = app.screen
            assert isinstance(view, EntityListView)

            view.action_add()
            await pilot.pause()

            detail = app.screen
            assert isinstance(detail, EntityDetailView)
            _fill(
                detail,
                name="Pneumonia",
                desc="An infection\nof the lung tissue.",
                aka="",
                symptoms=SYMPTOM_ID,
                priority="5",
                citation=CITATION_ID,
            )
            detail.action_save()
            await pilot.pause()

            added = [
                record
                for record in _stored(tmp_path, "conditions")
                if record.name == "Pneumonia"
            ]
            assert added[0].desc == "An infection\nof the lung tissue."

    asyncio.run(scenario())


def test_the_ieee_field_is_read_only(tmp_path: Path) -> None:
    async def scenario() -> None:
        _seed(tmp_path)
        app = EditorApp(tmp_path, initial_entity_type="citations")

        async with app.run_test() as pilot:
            await pilot.pause()
            view = app.screen
            assert isinstance(view, EntityListView)

            _select(view, 0)
            await pilot.pause()
            view.action_edit()
            await pilot.pause()

            detail = app.screen
            assert isinstance(detail, EntityDetailView)
            assert detail.query_one("#field-ieee", TextArea).read_only is True
            assert detail.query_one("#field-bibtex", TextArea).read_only is False

    asyncio.run(scenario())


def test_a_multiline_citation_round_trips_through_the_view(
    tmp_path: Path,
) -> None:
    bibtex = (
        "@article{multi,\n"
        "  author = {Müller, Jürgen},\n"
        "  title = {A multiline\n"
        "    title},\n"
        "  journal = {Journal of Testing},\n"
        "  year = {2020}\n"
        "}"
    )

    async def scenario() -> None:
        _seed(tmp_path)
        app = EditorApp(tmp_path, initial_entity_type="citations")

        async with app.run_test() as pilot:
            await pilot.pause()
            view = app.screen
            assert isinstance(view, EntityListView)

            view.action_add()
            await pilot.pause()

            detail = app.screen
            assert isinstance(detail, EntityDetailView)
            detail.query_one("#field-bibtex", TextArea).text = bibtex
            detail.action_save()
            await pilot.pause()

            assert app.screen is view
            stored = [
                record
                for record in _stored(tmp_path, "citations")
                if record.bibtex == bibtex
            ]
            assert len(stored) == 1
            assert stored[0].bibtex == bibtex
            assert "\n" not in stored[0].ieee
            assert stored[0].ieee.isascii()
            assert "Muller" in stored[0].ieee
            assert bibtex in view.visible_labels()

    asyncio.run(scenario())


def test_a_non_numeric_priority_is_rejected_by_the_rules(tmp_path: Path) -> None:
    async def scenario() -> None:
        _seed(tmp_path)
        app = EditorApp(tmp_path, initial_entity_type="conditions")

        async with app.run_test() as pilot:
            await pilot.pause()
            view = app.screen
            assert isinstance(view, EntityListView)

            view.action_add()
            await pilot.pause()

            detail = app.screen
            assert isinstance(detail, EntityDetailView)
            _fill(
                detail,
                name="Pneumonia",
                desc="",
                aka="",
                symptoms=SYMPTOM_ID,
                priority="high",
                citation=CITATION_ID,
            )
            detail.action_save()
            await pilot.pause()

            assert app.screen is detail
            assert "whole number" in _violations(detail)

    asyncio.run(scenario())


# --- buttons ---------------------------------------------------------------


def test_the_list_buttons_open_add_edit_and_delete(tmp_path: Path) -> None:
    async def scenario() -> None:
        _seed(tmp_path)
        app = EditorApp(tmp_path, initial_entity_type="conditions")

        async with app.run_test() as pilot:
            await pilot.pause()
            view = app.screen
            assert isinstance(view, EntityListView)

            await pilot.click("#add")
            await pilot.pause()
            assert isinstance(app.screen, EntityDetailView)
            await pilot.click("#cancel")
            await pilot.pause()

            _select(view, 0)
            await pilot.pause()
            await pilot.click("#edit")
            await pilot.pause()
            assert isinstance(app.screen, EntityDetailView)
            await pilot.click("#cancel")
            await pilot.pause()

            _select(view, 1)
            await pilot.pause()
            await pilot.click("#delete")
            await pilot.pause()

            assert [record.name for record in _stored(tmp_path, "conditions")] == [
                "Common Cold"
            ]

    asyncio.run(scenario())


def test_the_detail_buttons_save_and_cancel(tmp_path: Path) -> None:
    async def scenario() -> None:
        _seed(tmp_path)
        app = EditorApp(tmp_path, initial_entity_type="conditions")

        async with app.run_test() as pilot:
            await pilot.pause()
            view = app.screen
            assert isinstance(view, EntityListView)

            view.action_add()
            await pilot.pause()
            detail = app.screen
            assert isinstance(detail, EntityDetailView)
            _fill(
                detail,
                name="Pneumonia",
                desc="",
                aka="",
                symptoms=SYMPTOM_ID,
                priority="5",
                citation=CITATION_ID,
            )
            await pilot.click("#save")
            await pilot.pause()

            assert app.screen is view
            assert [record.name for record in _stored(tmp_path, "conditions")] == [
                "Common Cold",
                "Influenza",
                "Pneumonia",
            ]

    asyncio.run(scenario())


# --- deleting --------------------------------------------------------------


def test_deleting_a_referenced_record_is_refused_and_reported(
    tmp_path: Path,
) -> None:
    async def scenario() -> None:
        _seed(tmp_path)
        app = EditorApp(tmp_path, initial_entity_type="symptoms")

        async with app.run_test() as pilot:
            await pilot.pause()
            view = app.screen
            assert isinstance(view, EntityListView)

            _select(view, 0)
            await pilot.pause()
            view.action_delete()
            await pilot.pause()

            assert "Common Cold" in _status(view)
            assert [record.id for record in _stored(tmp_path, "symptoms")] == [
                SYMPTOM_ID
            ]

    asyncio.run(scenario())


def test_deleting_an_unreferenced_record_removes_it(tmp_path: Path) -> None:
    async def scenario() -> None:
        _seed(tmp_path)
        app = EditorApp(tmp_path, initial_entity_type="conditions")

        async with app.run_test() as pilot:
            await pilot.pause()
            view = app.screen
            assert isinstance(view, EntityListView)

            _select(view, 1)
            await pilot.pause()
            view.action_delete()
            await pilot.pause()

            assert [record.id for record in _stored(tmp_path, "conditions")] == [
                CONDITION_ID
            ]
            assert view.visible_labels() == ["Common Cold"]
            assert _status(view) == f"Deleted {SECOND_CONDITION_ID}."

    asyncio.run(scenario())


# --- the home view and the whole walk --------------------------------------


def test_the_home_view_lists_every_entity_type(tmp_path: Path) -> None:
    async def scenario() -> None:
        app = EditorApp(tmp_path)

        async with app.run_test() as pilot:
            await pilot.pause()
            view = app.screen
            assert isinstance(view, HomeView)

            options = view.query_one("#entity-types", OptionList)
            assert [option.id for option in options.options] == [
                "conditions",
                "symptoms",
                "tests",
                "citations",
            ]

    asyncio.run(scenario())


def test_choosing_an_entity_type_opens_its_list_view(tmp_path: Path) -> None:
    async def scenario() -> None:
        _seed(tmp_path)
        app = EditorApp(tmp_path)

        async with app.run_test() as pilot:
            await pilot.pause()
            view = app.screen
            assert isinstance(view, HomeView)

            options = view.query_one("#entity-types", OptionList)
            options.highlighted = 0
            options.action_select()
            await pilot.pause()

            assert isinstance(app.screen, EntityListView)
            assert app.screen.visible_labels() == ["Common Cold", "Influenza"]

    asyncio.run(scenario())


def test_closing_the_list_view_returns_to_the_home_view(tmp_path: Path) -> None:
    async def scenario() -> None:
        app = EditorApp(tmp_path)

        async with app.run_test() as pilot:
            await pilot.pause()
            home = app.screen
            home.query_one("#entity-types", OptionList).action_select()
            await pilot.pause()

            app.screen.action_close()
            await pilot.pause()

            assert app.screen is home

    asyncio.run(scenario())


def test_the_whole_walk_from_home_to_a_stored_record(tmp_path: Path) -> None:
    async def scenario() -> None:
        _seed(tmp_path)
        app = EditorApp(tmp_path)

        async with app.run_test() as pilot:
            await pilot.pause()
            home = app.screen
            assert isinstance(home, HomeView)

            home.query_one("#entity-types", OptionList).action_select()
            await pilot.pause()
            view = app.screen
            assert isinstance(view, EntityListView)

            view.action_add()
            await pilot.pause()
            detail = app.screen
            assert isinstance(detail, EntityDetailView)
            _fill(
                detail,
                name="Pneumonia",
                desc="An infection of the lung tissue.",
                aka="",
                symptoms=SYMPTOM_ID,
                priority="5",
                citation=CITATION_ID,
            )
            detail.action_save()
            await pilot.pause()

            assert app.screen is view
            assert view.visible_labels() == [
                "Common Cold",
                "Influenza",
                "Pneumonia",
            ]
            assert [record.name for record in _stored(tmp_path, "conditions")] == [
                "Common Cold",
                "Influenza",
                "Pneumonia",
            ]

    asyncio.run(scenario())
