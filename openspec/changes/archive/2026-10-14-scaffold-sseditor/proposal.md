# Proposal

## Why

SSEditor does not exist yet: `editor/` is empty, so the clinical data that DDClient presents can only be maintained by hand-editing JSON. Nothing enforces the integrity rules the system depends on — identifier uniqueness, valid foreign keys, and protection against deleting referenced records — so a hand edit can silently corrupt the data set or produce dangling references. Establishing the editor now creates a safe write path for the writable clinical entities and brings the existing fixtures into the required format, so the rules can be enforced from the start rather than retrofitted.

## What Changes

- Create the SSEditor application in `editor/` as a terminal app built on the Textual library, with a list/search screen and an add/edit screen for each writable entity type.
- Provide CRUD for four entity types: **Condition**, **Symptom**, **Test**, and **Citation**.
- Mint identifiers with `uuid.uuid4().hex` (32 lowercase hex characters) for new records, satisfying the existing 128-bit identifier requirement.
- Enforce the integrity rules on every write: globally unique identifiers, valid foreign-key references, and refusal to delete an entity that is still referenced, reporting the referencing records.
- Enforce the per-type content rules: unique names, title-cased names and AKA entries, AKA not clashing with any name of the same type, required minimum relationships, and field length limits.
- **BREAKING**: migrate the existing `public/data` rows for the four writable collections to the required format — fresh `uuid4` hex identifiers and title-cased names/AKA — and backfill the missing `aka` arrays. The current slug-style identifiers are replaced, so anything still referencing them breaks.
- Ignore the four collections SSEditor does not own (`condition-entries.json`, `symptom-entries.json`, `test-entries.json`, `cases.json`) entirely: the editor never reads, validates, migrates, or writes them.
- Add project packaging (`pyproject.toml`) declaring the Textual and title-casing dependencies, plus the corresponding `.gitignore` entries.
- Add `pytest` unit tests covering the validation, identifier generation, reference, and migration logic.

## Capabilities

### New Capabilities

- `sseditor-entity-management`: Provides the terminal-based administration workflow for the writable clinical entity types — listing, searching, creating, editing, and deleting records against the shared `public/data` JSON store while enforcing data-integrity and content rules.

### Modified Capabilities

<!-- No existing capability specs change. DDClient's behaviour contract is untouched by this change. -->

## Impact

- New code: the `editor/` package (Textual application, data-access layer, validation/integrity layer, identifier generation, and the one-off migration).
- New manifest: `pyproject.toml`; updated `.gitignore` for the virtual environment and Python caches.
- New dependencies: Textual (UI), `titlecase` (title-casing rule), and `pytest` for tests. PyICU is deliberately not used.
- Modified data: `public/data/conditions.json`, `symptoms.json`, `tests.json`, and `citations.json` are rewritten in place by the migration. The editor writes these same files directly.
- Modified documentation: `openspec/project-sseditor.md` is corrected (duplicate/mis-prefixed requirement identifiers, and Citation added to the CRUD entity list).
- Out of scope: `public/app.js` and the DDClient breakage caused by deleting the ignored collections, plus the schema of the ignored collections. These are knowingly deferred to later work.
