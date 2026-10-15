# Design

## Context

See `proposal.md` — Why. The `editor/` directory is empty, so everything below is new code. Three constraints from the current repository shape the approach:

- The written data lives in `public/data` and is **shared** with DDClient, which reads four of those files (`conditions`, `symptoms`, `tests`, `citations`) and validates their internal references. The editor must keep those files loadable by DDClient.
- The four client-only collections (`condition-entries.json`, `symptom-entries.json`, `test-entries.json`, `cases.json`) are not owned by the editor and are being deleted by the user; the editor must not depend on their presence.
- The existing `.venv` (Python 3.13.5) has **no `pip`** and no packages, and there is no `pyproject.toml` yet.

The repository already uses `openspec/` with the `spec-driven` schema; this change follows the same shape as the archived `scaffold-ddclient` change.

## Goals / Non-Goals

**Goals:**

- A single validation/integrity layer that owns every rule, so no screen can write an invalid record.
- Direct, dependency-light persistence to the four owned JSON files.
- A migration that produces a store satisfying the same rules the editor enforces.

**Non-Goals:**

- Any change to `public/app.js` or DDClient's behaviour. The breakage caused by deleting the client-only collections is knowingly deferred.
- Schema or lifecycle for the client-only collections; the editor never touches them.
- Concurrent-write protection, locking, backups, undo, or authentication.
- Localisation of title-casing beyond English.

## Decisions

### Structure the editor as a small package with a hard boundary between UI and rules

```
editor/
  __main__.py        entry point (python -m editor)
  app.py             Textual App, screen routing, keyboard bindings
  screens/           list screen + detail screen, one pair per entity type
  models/            record dataclasses per entity type (Condition, Symptom, Test, Citation)
  store.py           read/parse/write the four owned collection files
  rules.py           all validation and integrity rules (pure, no UI)
  identifiers.py     uuid4().hex generation + global uniqueness check
  migration.py       the one-off data migration
  tests/             pytest suite
```

UI code never validates; it submits a candidate record to `rules.py` and renders the returned violations. This keeps the rules testable without a terminal and gives the screens a single failure contract.

### Persist by rewriting the whole collection file

Each accepted write re-serializes the entire collection array to its file in `public/data`. Per the agreed decision there is no locking or concurrency handling. The alternative — in-place patching or a small database — was rejected because the client requires these exact files, and a database would add a second source of truth.

`store.py` validates on read as well as write: a file that is not a JSON array, or that contains a record missing a required field, is reported as an error rather than silently repaired.

### Identifiers: `uuid.uuid4().hex`

New records receive `uuid.uuid4().hex` — 32 lowercase hex characters, satisfying the existing 128-bit identifier requirement without a dependency. Identifiers are immutable after creation, so editing a name never invalidates the references pointing at the record.

Alternatives considered: slug-from-name (readable, but collides and would have to change when names change, breaking references) and a sequential counter (requires a global registry, and leaks row count).

Global uniqueness is checked across the four editable types. Because DDClient only enforces uniqueness _within_ each collection, the editor's check is deliberately stricter than the client's.

### Title-casing with the `titlecase` library; PyICU rejected

`rules.py` uses the `titlecase` package, which implements the American-English style rule the requirement describes (capitalize every word except minor words such as articles, conjunctions, and short prepositions, first and last word always capitalized) and is pure Python. Non-title-cased input is reported as a blocking violation — the editor never silently rewrites a name, per the agreed behaviour.

PyICU was evaluated and rejected: ICU's title casing capitalizes every word boundary and has no notion of minor words, so it would produce `Shortness Of Breath` where the agreed rule requires `Shortness of Breath`. It also requires the ICU C library and cannot be installed into a wheel-less venv without system packages. `str.title()` was rejected because it mangles apostrophes (`Don't` → `Don'T`). The trade-off accepted is that `titlecase` is English-oriented; the library exposes a per-word callback, which is the hook to use if acronym handling needs to be tuned later.

### Reference graph is limited to the four owned types

Only these references exist, and only these are validated and used for the delete guard:

```
   Condition --symptoms--> Symptom --tests--> Test
       |                      |                |
       +------citation-------> Citation <------+
```

Delete refusal reports the referencing records by scanning those three relations. References from the client-only collections are not read, so deleting a record those files still mention is permitted by design.

### Migration as a one-off invocation

The migration is run once, by hand, as a short `python -c` / module invocation rather than committed tooling. It performs, in one pass over the four owned collections:

1. Read all four collections.
2. Build an old-identifier → new-`uuid4().hex` map spanning all four, so cross-type references can be rewritten in the same pass.
3. Rewrite every record's `id` and every reference field (`Condition.symptoms`, `Symptom.tests`, and the `citation` field on Condition/Symptom/Test).
4. Title-case every `name` and every entry of `aka`, and backfill `aka: []` where absent.
5. Write each collection back.

A one-liner was chosen over committed tooling by explicit decision. The risk is recorded below, and the mitigation is to run the editor's own validation layer over the result immediately afterwards, which re-checks the same rules the migration is supposed to satisfy.

### Packaging

`pyproject.toml` declares Textual and `titlecase` as runtime dependencies and `pytest` as a development dependency, with `editor` as the package. Because the existing `.venv` has no `pip`, setup bootstraps it first (`python -m venv --upgrade-deps .venv`, or recreate) before installing. `.gitignore` gains `.venv/`, `__pycache__/`, `*.py[cod]`, `.pytest_cache/`, and `*.egg-info/`; it is currently empty.

## Risks / Trade-offs

- [Risk] Re-identifying existing records invalidates every identifier still referenced by the client-only collections and by DDClient's loader. → Accepted and deferred by decision: those files are being deleted, and the `app.js` clash is handled separately. Mitigation: the migration touches only the four owned files, and the follow-up DDClient repair stays a distinct piece of work rather than a silent edit here.
- [Risk] A hand-run one-off migration is unreviewable and untested, and it rewrites identifiers, so a partial failure can leave the store half-migrated. → Mitigation: run it against a copy of `public/data` first, keep it as a single atomic-in-memory pass that writes only after all four collections are transformed, and validate the result with the editor's own rule layer before discarding the copy.
- [Risk] `titlecase` is American-English and heuristic; acronyms such as `MRI` may be handled unexpectedly. → Mitigation: title-casing violations block saving rather than auto-correcting, so a bad conversion surfaces to the administrator instead of being written silently; the per-word callback is the tuning hook.
- [Risk] Blocking saves on non-title-cased input is stricter than hand-editing and may frustrate bulk corrections. → Accepted: it is the requested behaviour, and the migration performs the bulk correction once.
- [Risk] Rewriting whole files on every write loses data if the process dies mid-write. → Accepted with the no-concurrency decision; the mitigation available cheaply is writing to a temporary file and renaming, which the store can adopt without changing the rules or the client contract.
- [Risk] Validation stricter than DDClient's could reject data the client would accept, and the client could later accept data the editor would have rejected. → Mitigation: the editor's rules are the stricter superset, and both are covered by the test suite for the shared collections.

## Migration Plan

1. Add `pyproject.toml`, `.gitignore` entries, and bootstrap the virtual environment with the dependencies.
2. Implement the data store, rules, and identifier generation with their unit tests.
3. Build the Textual screens on top of the rules.
4. Copy `public/data` aside, run the migration against the working files, validate the result with the rules layer, then compare with the copy to confirm only the four owned files changed.
5. Delete the four client-only collection files.
6. Rollback: restore the four owned collection files from the copy taken in step 4; no other state is persisted.

## Open Questions

- Which exact minor-word set the spec's "short prepositions" covers is delegated to the `titlecase` library's default list; if the administrator disputes a specific word, the list can be customized without changing the capability's contract.
