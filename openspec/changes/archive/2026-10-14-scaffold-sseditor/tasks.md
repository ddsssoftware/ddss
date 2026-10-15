# Tasks

## 1. Project setup and packaging

- [x] 1.1 Add `pyproject.toml` declaring the `editor` package with Textual and `titlecase` as runtime dependencies and `pytest` as a development dependency, and verify installation into the project virtual environment succeeds.
- [x] 1.2 Bootstrap the existing virtual environment (it has no `pip`) and add `.venv/`, `__pycache__/`, `*.py[cod]`, `.pytest_cache/`, and `*.egg-info/` to the empty `.gitignore`, then verify `pytest` runs and that the virtual environment is no longer reported by `git status`.
- [x] 1.3 Create the `editor` package skeleton (`__main__.py`, `app.py`, `models/`, `screens/`, `store.py`, `rules.py`, `identifiers.py`, `migration.py`, `tests/`) and verify a smoke test imports the package and the test runner collects it.
- [x] 1.4 Fix `openspec/project-sseditor.md`: renumber the duplicated `REQ-002-001` and the mis-prefixed `REQ-0002-003`, and add Citation to the CRUD entity list. Verify every requirement identifier in the file is unique and the list names all four editable entity types.

## 2. Data store and identifiers

- [x] 2.1 Implement the collection path map for the four owned collections and JSON reading that rejects a non-array file, and verify unit tests cover a successful load and the malformed-file error; also assert the client-only collections are absent from the map.
- [x] 2.2 Implement identifier generation with `uuid.uuid4().hex` plus the global uniqueness check across all four editable types, and verify unit tests assert 32 lowercase hexadecimal characters, an unchanged identifier after an edit, and rejection of a duplicate.
- [x] 2.3 Implement whole-file write-back that preserves unrelated records, and verify a unit test asserts unrelated records survive a write and the written file parses as an array.

## 3. Validation and integrity rules

- [x] 3.1 Implement name uniqueness within an entity type and the title-casing rule for names and alternative names as blocking violations, and verify unit tests cover a duplicate name, a non-title-cased name, a non-title-cased alternative name, and acceptance of a corrected value.
- [x] 3.2 Implement the alternative-name-versus-name clash rule scoped to the same entity type, and verify unit tests cover a clash with the record's own name and with another record's name of the same type.
- [x] 3.3 Implement reference validation and the required-relationship and length rules, and verify unit tests cover an unresolvable reference, a Condition with no symptom, a Symptom with no test, and an over-long name or description.
- [x] 3.4 Implement the delete guard over the limited reference graph plus the referencing-records report, and verify unit tests cover refusal of a referenced record with its referencing records listed, and deletion of an unreferenced record.
- [x] 3.5 Document the rules and their blocking-versus-informational behaviour in `editor/README.md`, and verify every rule named there maps to a unit test in this group.

## 4. Terminal user interface

- [x] 4.1 Build the list screen for each editable entity type with a search control, and verify screen tests assert every stored record of that type is listed and that a search term narrows the list.
- [x] 4.2 Build the detail screen for each entity type supporting add, edit, and cancel, and verify screen tests assert a new record is stored and listed, an edit keeps the record's identifier, and cancelling leaves the store unchanged.
- [x] 4.3 Surface rule violations in the detail screen so a blocked write keeps the screen open and displays the warning, and verify a screen test asserts non-title-cased input blocks saving and leaves the collection file unchanged.
- [x] 4.4 Add the delete action with its refusal report, and verify a screen test asserts a referenced record is not deleted and the referencing records are shown.
- [x] 4.5 Document how to install and launch SSEditor in `README.md`, and verify the documented commands run as written.

## 5. Data migration and cleanup

- [x] 5.1 Implement the one-off migration pass that maps old identifiers to new ones across all four owned collections, rewrites identifiers and their references, title-cases names and alternative names, and backfills empty alternative-name lists. Verify by running it against a copy of `public/data` and confirming the result satisfies the rules layer.
- [x] 5.2 Run the migration against `public/data` and verify the result: every identifier is 32 lowercase hexadecimal characters, every name and alternative name is title cased, every reference resolves, and a diff against the pre-migration copy shows only the four owned files changed.
- [x] 5.3 Delete the four client-only collection files and verify SSEditor still lists, edits, and deletes records, and that those files are neither read nor written.

## 6. Integration verification

- [x] 6.1 Run the complete `pytest` suite from a clean environment and verify it passes.
- [x] 6.2 Walk the spec scenarios end to end in a terminal session against the migrated data and verify each one behaves as specified.
- [x] 6.3 Confirm `git diff` shows no change to `public/app.js`, and record the deferred DDClient clash and the deleted client-only collections as follow-up work.

## Workflow follow-up

- Archive the change after the project's review requirements are satisfied.
- Verify the archived result and the migrated `public/data` collections after archiving.
