# Design

## Context

See `proposal.md` for motivation and the delta spec for required behavior.

Current constraints that shape the approach:

- `editor/models/fields.py` already declares `reference_list` for `Condition.symptoms` and `Symptom.tests`, each with a `target` entity type. Both target types carry a `name` and an `aka` list, so one implementation serves both.
- `EntityDetailView` builds every field from the spec and reads values as text. `EntityDetailController` converts text to record values per record class.
- Records are matched by identifier, not object identity: `EditorModel` reloads collections from disk, so the record a caller holds is usually not the record the model holds.
- The installed Textual is 8.2.8. `DataTable` cells accept renderables only (no widget cells), `SelectionList` has no built-in filter, and the project has no modal-screen pattern yet.
- Lists are plain `ListView`s; search currently compares the term with `EditorModel.label_for` only.
- Loaded data may already contain unresolvable references; the validator only rejects them at save time.

## Goals / Non-Goals

**Goals:**

- One reference table component used by both `reference_list` fields.
- One definition of "matches" shared by the picker and the list screens.
- Attach, remove, and go-to as real, keyboard-focusable buttons.
- Multi-select picker whose pending choices survive filter changes.
- Keep the model, repository, and validator untouched.

**Non-Goals:**

- Inline creation of target records.
- Changing single `reference` fields (a Condition's citation) or turning them into a picker.
- Reordering attached references or de-duplicating stored data.
- Annotating list rows with alternative names.
- Searching by identifier.

## Decisions

### 1. Custom row list, not `DataTable`

Each reference row is a `Horizontal` containing the name, the identifier, a **Go to** button, and a **Remove** button, all inside a `VerticalScroll`.

`DataTable` cannot host widgets in cells in Textual 8.2.8, and the alternative — a table with a selected-row action bar — was rejected because it contradicts the requested per-row buttons and adds a selection mode the administrator must learn.

The row widget carries the identifier (`ReferenceRow.identifier`). Buttons have no per-row widget ids: widget ids must be unique per screen, and repeated `remove`/`goto` ids would collide. `on_button_pressed` resolves the identifier from `event.button.parent`.

### 2. A shared matcher in the controller layer

A new module `editor/controllers/matching.py` provides pure functions:

- `matches(record, term)` — case-insensitive substring over the label and the alternative-name entries.
- `annotated_label(record, term)` — the label alone on a name match, `Name (Aka)` on an alternative-name match, `None` when nothing matches.

It imports only models, never `textual`, so `test_layering` stays satisfied. `EntityListController.items` uses `matches`; `EntityDetailController` builds picker options with `annotated_label`.

Alternatives considered:

- Add matching to `EditorModel` next to `label_for` — rejected because matching is not model state, and it would put a search algorithm on the object whose job is loading and saving.
- Let each controller implement matching — rejected: two definitions of "search by alternative name" will drift and only one will get fixed.
- Let `SelectionList` filter itself — it has no filter API, and its matching would live in the view, violating the view/controller split.

Precedence is fixed: a name match wins and is never annotated; otherwise the **first matching alias in list order** is shown. Joining every matched alias makes prompts unbounded in width for no additional information.

Alias access is defensive: a missing, `None`, or non-list `aka` behaves as an empty list, because loaded data may predate the migration guarantee.

### 3. `values()` returns lists for reference fields

`EntityDetailView.values()` returns `dict[str, str | list[str]]`; reference fields contribute the identifiers currently in the table. `EntityDetailController._list_value` accepts either a list or the existing comma-separated text.

The alternative — joining identifiers with `", "` in the view — was rejected: the join is lossless for hex identifiers, but it makes the form's authoritative state a string again, so every future reference field would round-trip through text for no reason and the tests would assert a format rather than a meaning.

`initial_values()` keeps its shape; the view ignores the text for reference fields and asks the controller for their attached references instead.

### 4. Controller surface for references

`EntityDetailController` gains:

- `attached_references(field_name)` — the records referenced by the stored record, in stored order, with `None` for an identifier that no longer resolves.
- `available_references(field_name, term)` — target records not already attached, paired with their display label.
- `lookup_reference(field_name, identifier)` — the current record or `None`, used to refresh a row after returning from **Go to**.

The target entity type comes from `FieldSpec.target`, so the controller has no per-field branching and adding a reference field later needs no new code.

### 5. Picker screen with explicit pending state

`ReferencePickerView(Screen[list[str] | None])` composes a search `Input` and a `SelectionList`. It keeps `chosen: set[str]` as its own state:

- Rebuilding options on `Input.Changed` re-selects every id in `chosen` that is currently offered.
- Ids that fall out of the filter stay in `chosen`.
- Confirming dismisses with `chosen`; cancelling dismisses with `None`.

Dismissing with `None` rather than an empty list keeps "cancelled" distinguishable from "confirmed with nothing selected", so the form is only mutated on a real confirmation.

The picker only offers records; creating a target record remains a task for that entity type's list screen. When the referenced collection is empty or fully attached, the picker says so and where to create one, instead of presenting an empty list.

### 6. Go-to reuses the existing detail screen

**Go to** pushes `EntityDetailView` with an `EntityDetailController` for the target entity type and the referenced record. On dismiss, the condition/symptom form re-resolves the row labels through `lookup_reference`, so a rename performed in the nested screen appears on return. The form's widget state is untouched while the nested screen is on top.

Nested saving reloads the model; the open form is unaffected because its save path matches the edited record by identifier.

### 7. Dangling references stay editable, not fatal

An attached identifier that resolves to nothing renders as `<unknown> (<identifier>)` with **Go to** disabled and **Remove** enabled. Saving is still refused by `reference-unknown`, so the row is the only way out — matching the existing rule that nothing is silently repaired.

## Risks / Trade-offs

- **Selection state lost on filter change** → `chosen` lives in the picker, not in the `SelectionList`; a test types a filter after ticking a record and asserts the record is still attached on confirmation.
- **Duplicate button ids** → rows carry the identifier and buttons have no per-row id; a test asserts two rows with distinct references both remove correctly.
- **Unsaved form state vs nested save** → the nested screen is pushed, never substituted; the form is only dismissed by its own Save or Cancel.
- **Focus traversal with many rows** → buttons are ordinary focusable widgets; a view test tabs to a row button rather than relying on mouse clicks. Row count in real data is small, so no virtualisation.
- **Wide identifiers in narrow terminals** → names and identifiers use separate labels with fixed identifier width; the table scrolls vertically, identifiers are never abbreviated in the stored value.
- **Alias data that is a string rather than a list** → the matcher normalises before iterating; a controller test covers missing, `None`, and scalar aliases.
- **Shared matcher changes list-search results** → intended and specified: list search now finds records by alias while rows keep displaying names; existing name-search tests remain valid.

## Migration Plan

No data migration. The stored JSON shape, identifiers, and validator are unchanged. Existing unresolvable references become visible, removable rows on the detail screen; nothing is rewritten automatically.

## Open Questions

None.
