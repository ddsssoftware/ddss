# Tasks

## 1. Domain model owns its schema

- [x] 1.1 Delete `field_order` and the class-level schema attributes from `editor/models/records.py` and give each of the four record classes its own explicit `to_dict` and `from_dict`, written out field by field; verify `editor/tests/test_records.py` asserts every class round-trips its fields, that a JSON object with shuffled keys loads to an equal record, and that unset fields are omitted.
- [x] 1.2 Move `FieldSpec`/`EntitySpec`/`spec_for` into `editor/models/fields.py` and reduce `editor/models/__init__.py` to a re-export barrel; verify `from editor.models import Condition, ENTITY_SPECS, spec_for` still resolves and a test asserts `spec_for` rejects an unknown entity type.
- [x] 1.3 Document in `editor/README.md` that a record class shows its own fields and that key order is not a contract; verify the section names the two methods each record class implements and maps to the tests added by 1.1.

## 2. Persistence and identifiers

- [x] 2.1 Implement `CollectionRepository` in `editor/models/repository.py` (`directory`, `path`, `record_type`, `load`, `load_all`, `save`) delegating file access to the record classes, and deleting nothing yet; verify `editor/tests/test_repository.py` covers a successful load, a non-array file, malformed JSON, a non-object item, a missing file and an unknown entity type.
- [x] 2.2 Implement `IdentifierFactory` in `editor/models/identifiers.py` with `new()`, `is_valid()` and `resolve(existing)`; verify `editor/tests/test_identifiers.py` asserts 32 lowercase hexadecimal characters, no repeats, an unchanged identifier on edit, and a minted one for a new record.
- [x] 2.3 Replace the byte-format test with an order-agnostic one asserting the written file is a valid JSON array whose objects carry exactly the data-model fields with unset fields omitted; verify it also asserts that the same object with shuffled keys loads to an equal record, that unrelated records survive a write, and that a failure part-way through leaves the previous file intact, against a copy of `public/data`.

## 3. Rules as objects

- [x] 3.1 Implement `Validator` in `editor/models/rules.py` with one explicit method per rule — `name_must_be_unique`, `name_and_aka_must_be_title_cased`, `aka_must_not_clash_with_a_name`, `condition_must_have_a_symptom`, `symptom_must_have_a_test`, `references_must_resolve`, `fields_must_fit`, `condition_priority_must_be_a_whole_number`, `identifier_must_be_unused` — and a `validate` that branches on the record class with `isinstance` and calls them in order, keeping every `rule_id` and message verbatim; verify `editor/tests/test_rules.py` covers each method including the editing-excludes-itself cases, alias scope and citations being exempt from name rules.
- [x] 3.2 Verify the single `validate` pass covers identifier uniqueness: add a test asserting one `validate` call reports a duplicate identifier and accepts an unused one.
- [x] 3.3 Implement `Validator.find_references` and `Validator.check_deletion` with the `delete-referenced` message; verify tests assert a referenced record is refused with every referencing record listed, an unreferenced record is allowed, and the client-only collections never block a deletion.
- [x] 3.4 Update the rule table and rule-to-test map in `editor/README.md` to the validator methods and the new test module; verify every rule id in the table is produced by a test asserted in 3.1–3.3.

## 4. The model facade

- [x] 4.1 Implement `EditorModel` in `editor/models/editor_model.py` with the named accessors `conditions`, `symptoms`, `tests`, `citations` and `all_records`, plus `reload`, `label_for`, `spec_for`, `save` and `delete`; verify `editor/tests/test_editor_model.py` asserts `save` persists only when the rule list is empty, returns violations otherwise, mints versus keeps the identifier, and `delete` honours the deletion check.
- [x] 4.2 Verify a blocked save leaves the collection file unchanged and a successful save reaches the file, by comparing contents before and after each call in a test.

## 5. Controllers

- [x] 5.1 Implement `HomeController` exposing the entity menu (`menu`) — no interfaces and no navigation calls; verify `editor/tests/test_controllers.py` asserts the menu lists all four entity types with their labels.
- [x] 5.2 Implement `EntityListController` (`items`, `detail_controller`, `delete`, `refresh`); verify tests assert a search term narrows `items`, `detail_controller` returns a controller bound to the given record, a refused delete returns the violation and leaves the store unchanged, and a successful delete removes the record.
- [x] 5.3 Implement `EntityDetailController` (`initial_values`, `save`); verify tests assert a valid new record is stored with a new identifier and an empty violation list, an edit keeps the identifier, and invalid values return violations and write nothing.
- [x] 5.4 Assert the boundary in `editor/tests/test_layering.py` that no `editor.controllers.*` module imports `textual`; verify the test fails when a temporary import is added and passes when it is removed.

## 6. Views and wiring

- [x] 6.1 Rename `editor/screens/` to `editor/views/` and reduce each screen to presentation (`show_records`, `show_status`, `values`, `show_violations`) that calls one controller method per event, renders the return value, and owns its navigation (`push_screen` with a callback, `dismiss`); verify the ported `editor/tests/test_views.py` drives each view with the Textual pilot and asserts what it renders.
- [x] 6.2 Make `EditorApp` the composition root and router only (build the repository and model, push the home view or, for `--entity-type`, that type's list view, and keep the CSS); verify a pilot test walks home → list → detail → save → back and asserts the list reloads with the new record.
- [x] 6.3 Extend `editor/tests/test_layering.py` to assert no `editor.views.*` module imports `rules` or `repository`, and no `editor.models.*` module imports `textual`; verify the test passes on the finished tree.
- [x] 6.4 Update the architecture section of `editor/README.md` and the editor section of the root `README.md` to describe the three layers, and verify the documented commands (`python editor.py`, `.venv/bin/python -m editor`, `.venv/bin/sseditor`) run as written.

## 7. Remove the superseded modules

- [x] 7.1 Delete `editor/store.py`, `editor/rules.py`, `editor/identifiers.py`, `editor/migration.py`, `editor/tests/test_migration.py` and the empty `editor/screens/`; verify a search finds no import of or reference to any of them and the whole suite passes.
- [x] 7.2 Add the new subpackages to `[tool.setuptools.packages.find]` in `pyproject.toml` if discovery misses them; verify a reinstall succeeds and `sseditor` still starts.

## 8. Integration verification

- [x] 8.1 Run the full suite from a clean environment and verify zero failures and line-and-branch coverage of at least 95%, then regenerate `coverage/html` with `editor/run_unit_test.sh`.
- [x] 8.2 Walk every `sseditor-entity-management` scenario in a terminal against the real `public/data` and verify each behaves as before the rewrite, including one blocked write and one refused deletion.
- [x] 8.3 Verify nothing outside `editor/` changed because of the rewrite: install and package nothing new, confirm `public/data` and `public/app.js` are unmodified (unmodified mtimes), and confirm `editor.py` changed only its import path -- from the removed `editor.store` to `editor.models.records` -- with no change to its flags or behaviour.

## Workflow follow-up

- Archive the change after the project's review requirements are satisfied.
- Verify the archived result and confirm the `scaffold-sseditor` change is archived alongside it.
- Keep the deferred DDClient repair (dropping the deleted client-only collections from `public/app.js`) as separate work.
