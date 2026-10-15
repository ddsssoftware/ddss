# Proposal

## Why

SSEditor already does its job, but its implementation is structurally uneven. The domain logic is split between module-level function libraries (`store.py`, `rules.py`, `identifiers.py`, `migration.py`) and Textual `Screen` subclasses that simultaneously act as view, controller, validator and persistence layer. As a result a screen cannot be tested without a terminal, the rules cannot be reused outside a screen, and adding an entity type or a rule means editing several unrelated places. Restructuring the package as an object-oriented MVC application gives every concern exactly one owner and makes each unit testable on its own.

## What Changes

- Rewrite the `editor` package as an object-oriented, Model-View-Controller application:
    - `editor/models/` — the domain model (the record classes) and the data-access model (a repository/collection class replacing `store.py`), plus the validator that holds every rule.
    - `editor/views/` — the Textual screens (`screens/` is renamed), reduced to presentation: compose widgets, read input, render what the controller returns, and own screen navigation.
    - `editor/controllers/` — new orchestration layer owning the use cases (list, search, add, edit, delete); each method takes values and returns a result for the view to render.
- Replace the module-level function APIs with collaborating classes: a record hierarchy (kept and extended), a collection/repository object, a single validator class holding every rule, and an identifier factory.
- Drop the record classes' `field_order` altogether: each class reads and writes its own fields by name, and nothing treats key order as significant. Key order, whitespace and formatting are not part of the data contract.
- Prefer plain, explicit code over generic machinery: rules branch on the record class with `isinstance`, records show their own fields, and controllers are called directly and return their results. No rule registry, no dynamic field lookup, no interface protocols.
- **BREAKING (internal only)**: the module-level functions in `store.py`, `rules.py`, `identifiers.py` and `migration.py` are removed; `editor/screens/` becomes `editor/views/`; `editor/models/__init__.py` keeps the field/entity specs but they are moved behind model classes.
- Preserve the externally observable contract so nothing outside the package has to change: the `editor.py` launcher and its `--data-directory` / `--entity-type` flags, the `python -m editor` and `sseditor` entry points, every screen interaction and keyboard binding, every rule's accept/reject decision and message, and the JSON contract of the four owned collections in `public/data` — each file stays a valid JSON array whose objects carry the data-model fields, with unset fields omitted and key order carrying no meaning.
- **Remove the one-off migration entirely**: `editor/migration.py` and `editor/tests/test_migration.py` are deleted and no `Migrator` is reintroduced. The four collections are already in the required format, so the module has no remaining job.
- Rewrite the unit-test suite against the new class APIs, covering the same behaviours, and keep the existing 95% line-and-branch coverage gate.
- Update `editor/README.md` (rule-to-test map and module overview), the root `README.md` (unchanged commands, updated "How it works" pointer), and `pyproject.toml` package discovery if needed.

## Capabilities

### New Capabilities

<!-- None: this is a pure internal refactor. The behaviour described by the
     pending `sseditor-entity-management` capability is preserved unchanged, and
     that capability's spec is owned by the (unarchived) `scaffold-sseditor`
     change, not re-declared here. -->

None.

### Modified Capabilities

<!-- No requirement changes. -->

None.

This change sets `skip_specs: true`: specs describe system behaviour, and this change alters only the internal structure of the implementation. Every existing behavioural requirement — listing and searching, adding and editing, hexadecimal identifiers, identifier and name uniqueness, title casing, alias clashes, reference validation, the delete guard, required relationships and length limits, whole-file persistence, and ignoring unowned collections — is preserved as-is.

## Impact

- **Rewritten code**: the whole `editor/` package — `app.py`, `__main__.py`, `models/`, the renamed `views/`, and the new `controllers/`, plus the rule, identifier and repository classes.
- **Removed code**: `editor/migration.py` and `editor/tests/test_migration.py`.
- **Unchanged interfaces**: `editor.py` launcher and flags; `python -m editor`; the `sseditor` console script; the `public/data/*.json` contract (a valid array of objects carrying the data-model fields, key order insignificant) and the identifier format.
- **Tests**: `editor/tests/` rewritten to the class APIs; the coverage gate in `pyproject.toml` is unchanged.
- **Docs**: `editor/README.md` and the root `README.md` updated; `openspec/` planning artifacts added by this change.
- **Out of scope**: any change to `public/app.js` or DDClient; the already-known DDClient breakage from the deleted client-only collections; new entities, new rules, concurrency, locking, undo, or authentication.
