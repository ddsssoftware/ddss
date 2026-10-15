# Design

## Context

See `proposal.md` — Why. The starting point is the working SSEditor described by the `scaffold-sseditor` change:

- `editor/models/records.py` already defines a real `Record` class hierarchy (`Condition`, `Symptom`, `Test`, `Citation`), so the domain model is a good foundation to build on.
- `editor/store.py`, `editor/rules.py`, `editor/identifiers.py` and `editor/migration.py` are module-level function libraries holding parallel `dict`s keyed by entity type (`REFERENCE_FIELDS`, `REQUIRED_REFERENCES`, `FIELD_MAX_LENGTHS`, `INTEGER_FIELDS`, `LABELS`), so the same entity-type knowledge is restated in five tables.
- `editor/screens/{home,list,detail}.py` are Textual `Screen` subclasses that compose widgets, read input, decide validity, call `store`, and push each other. Validity is decided in the screen (`EntityDetailScreen.action_save` calls `rules.validate_record` _and then_ `rules.check_identifier_uniqueness` — two calls a caller can get wrong).
- `editor/models/__init__.py` holds the presentation descriptors (`FieldSpec`, `EntitySpec`) alongside re-exports, so the "models" package already mixes the domain, the UI schema and a barrel file.

Two hard constraints survive the rewrite because they are outside the package:

- **Behaviour is contractual.** The `sseditor-entity-management` capability (currently a pending delta in the unarchived `scaffold-sseditor` change) fixes every rule decision, every message, the identifier format, the list/search/add/edit/delete flow, and whole-file persistence. The rewrite preserves all of it; this change therefore sets `skip_specs: true` (see `proposal.md` — Capabilities).
- **The four JSON files are shared** with DDClient. The contract is that each file is a valid JSON array whose objects carry the data-model fields, with unset fields omitted. Key order and whitespace carry no meaning, so the writer is free to emit keys in any order and no consumer may depend on one.

## Goals / Non-Goals

**Goals:**

- One owner per concern: domain model, persistence, rules, and orchestration each in a single place.
- Controllers and rules usable and testable without a terminal; views testable without business logic.
- Plain, explicit code throughout: no rule registry, no dynamic field lookup, no interface protocols, no indirection the reader has to resolve in their head.
- Eliminate the parallel entity-type `dict`s in `rules.py` by writing each rule against the record class it applies to.
- Make "validate then persist" a single call that callers cannot split incorrectly.

**Non-Goals:**

- No reflective or generic machinery: nothing discovers rules, fields, or handlers at run time.
- No new entity types, rules, screens, or key bindings; no change to any accept/reject decision or message.
- No change to the JSON contract in `public/data` or to the identifier format.
- No change to the interface of `editor.py`, to the `python -m editor` / `sseditor` entry points, or to their flags. `editor.py` does move one import, because deleting `editor.store` removes the module it read `ENTITY_TYPES` and `DEFAULT_DATA_DIRECTORY` from; both names and the launcher's behaviour are unchanged.
- No dependency, concurrency, locking, undo, or authentication work.
- No `public/app.js` or DDClient change; the deferred DDClient breakage stays deferred.

## Decisions

### 1. A three-layer package: `models/`, `views/`, `controllers/`

```
editor/
  __init__.py            package docstring (unchanged)
  __main__.py            entry point (unchanged behaviour)
  app.py                 EditorApp: composition root + router
  models/
    __init__.py          barrel: re-export the public model names
    records.py           Record hierarchy (kept; each class writes its own fields)
    fields.py            FieldSpec / EntitySpec presentation descriptors
    repository.py        CollectionRepository (replaces store.py)
    identifiers.py       IdentifierFactory (replaces identifiers.py functions)
    rules.py             Validator, Violation, Reference (replaces rules.py)
    editor_model.py      EditorModel: the MVC "Model" facade
  controllers/
    __init__.py          barrel
    home.py              HomeController
    entity_list.py       EntityListController
    entity_detail.py     EntityDetailController
  views/
    __init__.py          barrel
    home.py              HomeView      (was screens/home.py)
    list.py              EntityListView, RecordItem (was screens/list.py)
    detail.py            EntityDetailView (was screens/detail.py)
  tests/                 rewritten suite (test_views.py replaces test_screens.py)
```

`models/` holds both the domain model and the persistence/model layer, matching the existing directory and avoiding a fourth top-level package for a small app. `screens/` is renamed `views/` so the directory name states its role.

Alternatives considered: keeping `screens/` and adding `controllers/` (rejected — two names, one role, and the reader has to learn which is which); a single `models.py`/`views.py`/`controllers.py` trio of modules (rejected — the rules alone are ~400 lines and the entity count is expected to grow).

### 2. Controllers decide, views render and navigate — no interfaces

A controller is a plain object whose methods take values and return results. It never calls back into a view, and it never imports Textual:

```python
class EntityListController:
    def __init__(self, model: EditorModel, entity_type: str) -> None: ...
    def items(self, term: str = "") -> list[Record]: ...
    def detail_controller(self, record: Record | None) -> EntityDetailController: ...
    def delete(self, record: Record) -> list[Violation]: ...   # empty means deleted
    def refresh(self) -> None: ...

class EntityDetailController:
    def __init__(self, model: EditorModel, entity_type: str, record: Record | None = None) -> None: ...
    def initial_values(self) -> dict[str, str]: ...
    def save(self, values: Mapping[str, str]) -> list[Violation]: ...   # empty means stored
```

- A view calls one controller method from an event handler and renders the return value: `violations = self.controller.save(self.values())`, then either `self.dismiss(True)` or `self.show_violations(violations)`.
- The view owns screen navigation, because pushing and popping screens is a Textual concern with a Textual mechanism: the list view calls `push_screen(detail_view, callback=self.after_detail)` and the detail view calls `dismiss(...)`. No `Navigator` interface and no callback plumbing of our own.
- `EditorApp` is the composition root and router: it builds the model and pushes the first screen. It implements no interface.

This is a forced decision, not a preference. Textual's `Screen` and `App` are built on `textual.message_pump._MessagePumpMeta`, which conflicts with `ABCMeta`: `class X(SomeABC, Screen)` raises `TypeError: metaclass conflict`. So an `ABC` or `Protocol` interface cannot be mixed into a view or into `EditorApp` — a declared interface would be a fiction that neither base could satisfy. Stating the contract in the controller's method signatures, and pinning it with tests, is both honest and checkable.

Alternatives considered: `typing.Protocol` interfaces for the view and the navigator (rejected — implicit, unenforced, and unnecessary once controllers return results instead of calling back); `ABC` interfaces (rejected — cannot be mixed into a Textual screen or app, see above); views calling the model directly (this is the current coupling, rejected); a message-passing/observer bus (rejected — the app has three screens and an explicit call graph is easier to follow).

### 3. One `Validator` class holds every rule

No rule base class, no context object, no registry. `Validator` has one method per rule, and `validate` reads as the complete rule list for a record:

```python
class Validator:
    def validate(self, record: Record, existing: Record | None,
                 model: EditorModel) -> list[Violation]:
        violations: list[Violation] = []
        if isinstance(record, (Condition, Symptom, Test)):
            violations += self.name_must_be_unique(record, existing, model)
            violations += self.name_and_aka_must_be_title_cased(record)
            violations += self.aka_must_not_clash_with_a_name(record, existing, model)
        if isinstance(record, Condition):
            violations += self.condition_must_have_a_symptom(record)
        if isinstance(record, Symptom):
            violations += self.symptom_must_have_a_test(record)
        violations += self.references_must_resolve(record, model)
        violations += self.fields_must_fit(record)
        violations += self.condition_priority_must_be_a_whole_number(record)
        violations += self.identifier_must_be_unused(record, existing, model)
        return violations

    def find_references(self, entity_type: str, identifier: str, model: EditorModel) -> list[Reference]: ...
    def check_deletion(self, entity_type: str, identifier: str, model: EditorModel) -> list[Violation]: ...
```

Each method keeps the `rule_id` and the message text it produces today, verbatim:

| Method                                      | Rule ids produced                        |
| ------------------------------------------- | ---------------------------------------- |
| `name_must_be_unique`                       | `name-unique`                            |
| `name_and_aka_must_be_title_cased`          | `name-title-case`, `aka-title-case`      |
| `aka_must_not_clash_with_a_name`            | `aka-name-clash`                         |
| `condition_must_have_a_symptom`             | `reference-required`                     |
| `symptom_must_have_a_test`                  | `reference-required`                     |
| `references_must_resolve`                   | `reference-invalid`, `reference-unknown` |
| `fields_must_fit`                           | `field-too-long`                         |
| `condition_priority_must_be_a_whole_number` | `field-invalid`                          |
| `identifier_must_be_unused`                 | `identifier-duplicate`                   |
| `check_deletion`                            | `delete-referenced`                      |

`validate` shows the whole rule set in about fifteen readable lines, so a reader never has to work out which rule applies to which entity type. The delete check lives on the same class because it is just another rule, even though it takes an identifier rather than a candidate record.

Alternatives considered: a `Rule` ABC with one class per rule plus a `Rulebook` registry (rejected — a plugin framework for ten fixed rules; you cannot see which rules apply without tracing the registry); free functions in a `rules` module (rejected — the rules would be stateless functions rather than object behaviour, and the record rules and the delete check would have no common home).

### 4. Records show their own fields; rules branch on the record class

Each record class writes its own fields out. There is no `field_order`, no `fields` inventory and no class-level schema table: `to_dict` returns a literal dict named field by field, and `from_dict` reads the same fields back by name.

```python
class Condition(Record):
    def to_dict(self) -> dict[str, Any]:
        data = {
            "id": self.id,
            "name": self.name,
            "desc": self.desc,
            "symptoms": self.symptoms,
            "priority": self.priority,
            "citation": self.citation,
            "aka": self.aka,
        }
        return {key: value for key, value in data.items() if value is not None}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "Condition":
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            desc=data.get("desc"),
            symptoms=data.get("symptoms"),
            priority=data.get("priority"),
            citation=data.get("citation"),
            aka=data.get("aka"),
        )
```

A reader sees exactly which fields a Condition carries. Nothing loops and nothing is looked up by name. Key order is visibly irrelevant because no code depends on it: the dict literal is not an ordering contract, the writer emits whatever order the mapping yields, and a file with a different key order loads to an equal record.

The rules likewise branch on the record class rather than on an entity-type string: `isinstance(record, Condition)` is checked by the type checker, greppable, and impossible to mistype into a silent no-op. The limits and reference field names the rules need are named module constants used where they are checked (`NAME_MAX_LENGTH = 256`, `TEXT_MAX_LENGTH = 1024`), not attributes consulted through `type(record)`.

Entity-type strings survive in exactly one place — the mapping the outside world needs (the CLI `--entity-type` value, the file name, the view label) — so there is one table to read instead of five. `Record` keeps only what is genuinely shared: `load`, `save`, `__eq__` and `__repr__`.

Alternatives considered: a `fields`/`field_order` inventory driving a generic `to_dict`/`from_dict` (rejected — the class stops showing its own shape, and the generic code exists only to save four short methods); schema facts as class attributes consulted by the rules (rejected — indirection the reader must resolve, and the very thing being removed); the parallel `dict`s in `rules.py` (rejected — a field or a limit has to be changed in two coordinated places).

### 5. `EditorModel` is the only writer, and validation is atomic

```python
class EditorModel:
    def __init__(self, repository: CollectionRepository,
                 validator: Validator | None = None,
                 identifiers: IdentifierFactory | None = None) -> None: ...
    def reload(self) -> None: ...
    def conditions(self) -> list[Condition]: ...
    def symptoms(self) -> list[Symptom]: ...
    def tests(self) -> list[Test]: ...
    def citations(self) -> list[Citation]: ...
    def all_records(self) -> list[Record]: ...      # every type, for identifier uniqueness
    def label_for(self, record: Record) -> str: ...
    def spec_for(self, entity_type: str) -> EntitySpec: ...
    def save(self, record: Record, existing: Record | None = None) -> list[Violation]: ...
    def delete(self, record: Record) -> list[Violation]: ...
```

Named accessors replace the `Mapping[str, Sequence[Record]]` that today is threaded through every rule: a rule that needs symptoms asks for `model.symptoms()` and reads it concretely. `all_records()` exists for the one rule that genuinely spans every type, identifier uniqueness.

`save` mints or keeps the identifier, runs the whole `Validator` (including identifier uniqueness) and persists only when the violation list is empty; it returns the empty list on success. `delete` runs `check_deletion` and removes the record only when it passes. Both return violations rather than raising, because a violation is an expected outcome the view must render.

Because `validate` is a single call, the current two-step `validate_record` + `check_identifier_uniqueness` sequence in `EntityDetailScreen.action_save` — where forgetting the second call would let a duplicate identifier through — cannot be split again.

Tests build a model over a temporary data directory, exactly as the current screen tests already do, so no collection-injection seam is needed.

### 6. `EditorApp` is the composition root and router only

`EditorApp.on_mount` builds `CollectionRepository(data_directory)` and `EditorModel(...)`, then pushes either the home view or, when `--entity-type` was given, that type's list view. It holds the app `CSS` and nothing else: no rule, no persistence, no field knowledge, and no interface to implement, because navigation belongs to the views.

### 7. The external contract is preserved, minus key order

Even though the change is free to alter the surface, it deliberately preserves everything DDClient and the specs depend on:

- the four JSON files stay valid JSON arrays whose objects carry the data-model fields with unset fields omitted; `indent=2` and `ensure_ascii=False` are kept as a readability choice, and key order is neither imposed nor asserted;
- the `sseditor-entity-management` capability fixes the behaviour the screens must show;
- `editor.py`'s `--data-directory` / `--entity-type` flags and the launcher's virtualenv re-exec are documented in the root `README.md`.

Changing any of these would force a spec delta and break the client for no functional gain. The freedom is used only inside the package.

### 8. The one-off migration is removed, not ported

`editor/migration.py` and `editor/tests/test_migration.py` are deleted, and no `Migrator` returns in the new layout. The migration has already run: `public/data` holds hexadecimal identifiers, title-cased names and backfilled `aka` lists, so the module has no remaining job and its tests only re-prove a past event. Dropping it also removes the second copy of the reference-field map that `rules.py` already duplicates.

Alternatives considered: porting it to a `Migrator` class (rejected — it would carry dead code forward); leaving it beside the new package (rejected — the rewrite deletes the shared `store` and `rules` modules it calls, so keeping it means maintaining a second, obsolete access path). The cost — losing the in-repo ability to re-apply the transform — is recorded in Risks.

### 9. Tests are rewritten onto the class APIs, and a layering test guards the boundary

- `test_rules.py` → one test class per `Validator` method with the same scenario names, asserting the same `rule_id`s and messages.
- `test_screens.py` → `test_views.py`, still driving the Textual views with the pilot (mount, keypress, assert the store on disk), because that is the only way to prove the wiring.
- New `test_controllers.py` calls each controller method directly and asserts the return value and the resulting store (a search term narrows `items`, `detail_controller` is bound to the right record, a blocked write returns violations and writes nothing, a referenced delete is refused) — no terminal and no fakes, because controllers neither render nor navigate.
- New `test_layering.py` asserts that no `editor.views.*` module imports `rules` or `repository`, and that no `editor.models.*` module imports `textual`, so the boundaries cannot silently rot.
- The `[tool.coverage.report] fail_under = 95` gate and the branch-coverage settings in `pyproject.toml` are unchanged.

## Risks / Trade-offs

- [Risk] A rewrite this wide can change a rule decision or a message without anyone noticing. → Mitigation: port every existing scenario to the new tests with the same name and the same expected ids/messages, and keep the ≥95% branch-coverage gate so no branch of a rule escapes a test.
- [Risk] Writing the rules and the fields out explicitly repeats the shape of the four entity types across several methods, so one new field is added in more than one place. → Accepted deliberately: a visible, repeated edit is easier to review than a registry that can silently stop covering a type, and the per-rule tests plus the layering test keep the copies honest.
- [Risk] Putting screen navigation in the views gives a view a little flow control. → Accepted: pushing and popping screens is a Textual presentation concern; the controller still decides whether an action is allowed and returns the outcome, and the view only acts on that value.
- [Risk] Views drift back into business logic during the port — the very problem being fixed. → Mitigation: the `test_layering.py` import guard above, plus a rule that a view only renders, navigates and forwards.
- [Risk] The model's in-memory copy can go stale relative to the file after another process writes it. → Accepted, unchanged from today: there is no concurrency handling in scope. `reload()` exists and the model reloads after its own save.
- [Risk] Renaming `screens/` to `views/` breaks any external import of `editor.screens`. → Accepted: the package is a terminal app with no library consumers, and the change is explicitly allowed to alter internals.
- [Risk] The old `coverage/html` report still shows the pre-rewrite module names. → Mitigation: regenerate it with `editor/run_unit_test.sh` as the last implementation step; it is a build artifact.
- [Risk] Moving serialisation behind `CollectionRepository` could quietly drop the atomic temp-file swap. → Mitigation: the swap stays in the record class's `save`, which the repository delegates to, and the existing "written file parses as an array / unrelated records survive" tests are ported.
- [Risk] Dropping the field order means the editor may re-emit a collection's keys in a different order the next time it writes that file, producing a diff for data that did not change. → Accepted: key order is not contractual, DDClient reads by key, and this change rewrites no data file.
- [Risk] Deleting the one-off migration removes the only in-repo way to re-apply the format change if a pre-migration copy of `public/data` were ever restored. → Accepted by explicit decision: the migration has already run and the collections are in the required format; recovery is from version-control history.

## Migration Plan

1. Build the new `models/` layer — records writing their own fields, `CollectionRepository`, `IdentifierFactory`, the `Validator`, and finally `EditorModel` — porting the `test_records`, `test_store`, `test_identifiers` and `test_rules` scenarios as it goes.
2. Add `controllers/` with `test_controllers.py` calling each controller directly and asserting its return values.
3. Add `views/` (rename `screens/`, strip business logic, move navigation into the views) and bind them to their controllers; port `test_screens.py` to `test_views.py` and add `test_layering.py`.
4. Delete `editor/store.py`, `editor/rules.py`, `editor/identifiers.py`, `editor/migration.py`, `editor/tests/test_migration.py` and `editor/screens/`.
5. Update `editor/README.md` (rule-to-test map now names the validator methods and test classes), the root `README.md` if any wording depends on the old layout, and `pyproject.toml` only if package discovery needs it.
6. Run the full suite; confirm zero failures and coverage ≥ 95%; regenerate `coverage/html` with `editor/run_unit_test.sh`.

Rollback: the change is code-only. It writes the same data-model fields to the same files, rewrites no data and adds no persisted state, so reverting the branch restores the previous implementation with the data untouched. The only removed file that cannot simply be reverted is the already-run one-off migration, which remains available in version-control history.

## Open Questions

- Whether `editor.py` should move inside the package. Deferrable and unrelated to the architecture: the root launcher stays where it is and keeps the documented `python editor.py` command working, so this change only repoints its one import at `editor.models.records`.
