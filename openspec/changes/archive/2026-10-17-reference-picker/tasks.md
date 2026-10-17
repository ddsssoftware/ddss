# Tasks

## 1. Shared name and alternative-name matching

- [x] 1.1 Add `editor/controllers/matching.py` with `matches(record, term)` and `annotated_label(record, term)`: case-insensitive substring over the spec label and each `aka` entry, name match unannotated, first matching alias shown as `Name (Aka)`, malformed or missing `aka` treated as empty. Verify with a new `editor/tests/test_matching.py` covering name match, alias match, both, no match, empty term, and non-list aliases.
- [x] 1.2 Switch `EntityListController.items` to the shared `matches` and keep `label_for` as the displayed text. Verify in `editor/tests/test_controllers.py` that a term matching only an alias returns the record, and that the returned record still labels as its name.

## 2. Reference data on the detail controller

- [x] 2.1 Add `attached_references(field_name)`, `available_references(field_name, term)`, and `lookup_reference(field_name, identifier)` to `EntityDetailController`, resolving the target entity type from `FieldSpec.target`. Verify in `editor/tests/test_controllers.py`: stored order preserved, unresolvable identifier yields `None`, already attached records are excluded from the available list, and labels follow the annotation rule.
- [x] 2.2 Let the controller accept a list of identifiers for a reference field (`Mapping[str, Any]` / `_list_value`), so a form value can be a list as well as comma-separated text. Verify with controller tests that both input forms build the same `Condition.symptoms` and `Symptom.tests` values, and that an empty list still trips `reference-required`.
- [x] 2.3 Widen `EntityDetailView.values()` typing to `dict[str, str | list[str]]` without changing text-field behavior. Verify in `editor/tests/test_controllers.py` that saving a condition from list values persists the identifiers in order.

## 3. Reference table in the detail view

- [x] 3.1 Add a reference row widget (name label, identifier label, `Go to`, `Remove`) carrying its identifier, and render one per attached reference inside the detail form instead of the text `Input`. Verify in `editor/tests/test_views.py` that an edited condition shows one row per attached symptom with name and identifier, and that a new condition shows an empty table.
- [x] 3.2 Handle `Remove` by deleting the row from the form state without touching the model; ensure two rows with different identifiers remove independently. Verify with a view test that the removed identifier is absent from `values()` and from the stored record after Save.
- [x] 3.3 Handle `Go to` by pushing the target record's `EntityDetailView`, and re-resolve the row label on return so a rename is visible and the form's other edits survive. Verify with a view test that edits the referenced symptom's name, returns, and sees the new name with the condition form's unsaved values intact.
- [x] 3.4 Render unresolvable stored references as unknown with `Go to` disabled and `Remove` enabled. Verify with a view test that saving still reports `reference-unknown`, and that removing the row lets the same form save.

## 4. Record picker

- [x] 4.1 Add `ReferencePickerView` with a search `Input`, a `SelectionList`, `chosen` state preserved across filter changes, confirm returning the chosen identifiers and cancel returning `None`; show an explanatory message when nothing is available to attach. Verify in `editor/tests/test_views.py` that a term matching an alias offers `Name (Aka)`, a name match offers the plain name, and a filter typed after ticking keeps the ticked record attached on confirmation.
- [x] 4.2 Wire the table's `Add` action to the picker and append the returned identifiers as rows at the end. Verify with a view test that attaching two records in one confirmation produces two rows and stores both identifiers.
- [x] 4.3 Apply the same table and picker to `Symptom.tests` through the existing `FieldSpec.target`, with no per-field branching. Verify with a view test that editing a symptom attaches a test and that the saved `tests` list holds the chosen identifier.

## 5. Documentation

- [x] 5.1 Update `editor/README.md` to describe reference-table editing, the picker's name/alternative-name search, list search matching alternative names while rows display names, and the unknown-reference display. Verify the described flows match the implemented screens.

## 6. Integration verification

- [x] 6.1 Make the view test helpers table-aware (replace the `symptoms`/`tests` text fills) and run `.venv/bin/python -m pytest -q`; all tests must pass with total coverage at or above the 95% gate.
- [x] 6.2 Run `openspec validate "reference-picker" --strict` and confirm no validation errors.
- [x] 6.3 Launch `python3 editor.py` and manually verify: attach two symptoms to a condition, remove one, open a symptom with **Go to** and return, search a list screen by an alias, and save.

## Workflow follow-up

- Archive the change after review and verification are complete.
