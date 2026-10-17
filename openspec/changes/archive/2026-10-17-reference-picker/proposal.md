# Proposal

## Why

The Condition and Symptom detail screens edit their required relationships as comma-separated lists of identifiers typed into a plain text box. After migration, those identifiers are opaque 32-character hex strings, so attaching a symptom or test means leaving the editor, finding the identifier elsewhere, and pasting it without a typo. The administrator cannot see which records are attached, cannot fix an unresolvable identifier, and cannot jump to the related record. The same hidden identifiers also make the list screens' search feel arbitrary, because searching by a synonym the data already stores finds nothing.

## What Changes

- The `reference_list` fields (`Condition.symptoms` and `Symptom.tests`) render as an attach table instead of a text input. Each row shows the attached record's name and identifier, with a **Go to** button and a **Remove** button; an **Add** button above or below the table opens a picker.
- The picker offers only target records already held in the data store (no inline creation) and supports attaching several at once. Its search matches each record's name and every entry of its alternative-name list, case-insensitively.
- Picker entries display the record's name on a name match and `Name (Aka)` on an alternative-name match. The attach table always displays the plain name.
- **Go to** opens the referenced record's own detail screen; returning to the form re-resolves the displayed names so a rename performed there is visible.
- The list screens' search also matches alternative names, while list rows continue to display names only.
- Stored references whose identifier resolves to no record are shown as unknown, remain removable, and cannot be navigated to; the existing rules that refuse the write are unchanged.
- No change to the stored JSON shape: reference fields remain flat lists of identifiers and alternative names are never copied onto a reference.
- No change to validation: a Condition still needs at least one Symptom, a Symptom at least one Test, and unresolvable references are still rejected on save.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `sseditor-entity-management`: the "Add and edit entity records" requirement now covers editing reference-list fields by attaching and detaching stored records through a picker; the "List and search records by entity type" requirement now covers search matching alternative names.

## Impact

- `editor/views/detail.py` — renders the reference table and pushes the picker and the go-to detail screen; `values()` can return a list of identifiers for a reference field.
- `editor/controllers/entity_detail.py` — resolves attached records and builds searchable picker options from the field's target entity type.
- `editor/controllers/entity_list.py` — search matches alternative names.
- A shared matching helper consumed by both controllers, so name/alternative-name matching has one definition.
- A new picker screen, including preservation of selections while the search term changes.
- `editor/tests/test_views.py` and `editor/tests/test_controllers.py` gain table-aware form helpers and alternative-name search cases; `editor/tests/test_fields.py` already enforces that every reference field names a real target.
- No dependency, data-format, or migration changes.
