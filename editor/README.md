# SSEditor

SSEditor is a Textual terminal application in `editor/`, laid out in three
layers. A call flows one way: a view calls a controller, the controller calls the
model, and each layer answers with a value the layer above renders.

| Layer      | Lives in              | Owns                                                                                                            |
| ---------- | --------------------- | --------------------------------------------------------------------------------------------------------------- |
| View       | `editor/views/`       | Composing widgets, reading input, rendering what a controller returned, and pushing/popping screens             |
| Controller | `editor/controllers/` | One use case each -- list and search, add and edit, delete -- with methods that take values and return a result |
| Model      | `editor/models/`      | The record classes, the collection files, the rules, and the identifiers                                        |

Two boundaries are enforced by `editor/tests/test_layering.py`: no controller
imports Textual and no view imports the rules, the repository or the model, so a
view cannot quietly start deciding validity; and no model module imports Textual,
so the rules stay testable without a terminal.

## The record classes

`editor/models/records.py` defines the four editable records: `Condition`,
`Symptom`, `Test` and `Citation`. Each class shows its own fields. There is no
field list and no field order:

- `to_dict()` returns a literal dict built field by field, omitting a field
  whose value is `None`.
- `from_dict(data)` reads those same fields back by name.

Key order is **not** part of the data contract. Nothing in the editor depends on
it, a stored file carrying the fields in any order loads to an equal record, and
the tests assert field _sets_ rather than key order
(`test_records.py::test_each_class_writes_the_fields_its_entity_type_defines` and
`test_the_key_order_of_a_stored_object_does_not_matter`).

Each class also declares its three identity facts -- `ENTITY_TYPE`, `FILENAME`
and `LABEL` -- and `RECORD_TYPES` in the same module is the one entity-type
lookup table. Reading and writing a whole collection (`load`/`save`) is shared on
the `Record` base, which swaps the file in through a temporary sibling so a
failure part-way through cannot truncate the existing data.

## Reference tables and the picker

The Condition and Symptom detail screens edit their reference-list fields
(`Condition.symptoms` and `Symptom.tests`) as attach tables rather than
comma-separated text boxes. Each row shows the referenced record's name and
identifier with **Go to** and **Remove** actions; **Add** opens the picker in
`editor/views/picker.py`.

The picker offers only records already stored in the referenced collection and
never creates one. Its search matches a record's name and every entry of its
alternative-name list, case-insensitively, through
`editor/controllers/matching.py`. A name match is labelled with the name alone;
an alternative-name match is labelled `Name (Aka)`. Records already attached are
not offered, and ticks survive a changed search term.

**Go to** pushes that record's own detail screen. Returning re-resolves the row
labels, so a rename made there is visible, while the form's unsubmitted values
stay as they were.

List-screen search uses the same matching: a term matches a name or an
alternative name, while list rows keep displaying the name only.

An identifier loaded from disk that no longer resolves is shown as `Unknown`,
can be removed but not opened, and keeps blocking the save through
`reference-unknown` until it is gone.

## Validation rules

`editor/models/rules.py` is the single owner of every validation and integrity
rule. One class, `Validator`, holds them all; each rule is its own method and
`validate` is the readable list of which rules apply to which record class. The
UI never decides validity: it calls `Validator.validate(...)` and renders
whatever violations come back.

## Blocking versus informational

Every rule currently defined is **blocking**. A write must not proceed while
`Validator.validate` or `Validator.check_deletion` returns any violation. There
are no informational (non-blocking) rules; if one is ever added it must be
reported through a separate channel so callers can still distinguish it from a
blocker.

Casing is deliberately _not_ auto-corrected. A non-title-cased value is rejected
and the message states the corrected form, so the administrator makes the change.

## Rules

| Rule id                | What it rejects                                                                                            | Validator method                                            |
| ---------------------- | ---------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| `name-unique`          | A name already used by a different record of the same type                                                 | `name_must_be_unique`                                       |
| `name-title-case`      | A name that is not title cased                                                                             | `name_and_aka_must_be_title_cased`                          |
| `aka-title-case`       | An alternative name that is not title cased                                                                | `name_and_aka_must_be_title_cased`                          |
| `aka-name-clash`       | An alternative name equal to this or another record's name of the same type                                | `aka_must_not_clash_with_a_name`                            |
| `reference-required`   | A Condition with no Symptom, or a Symptom with no Test                                                     | `condition_must_have_a_symptom`, `symptom_must_have_a_test` |
| `reference-invalid`    | A reference field holding something other than an identifier or list of identifiers                        | `references_must_resolve`                                   |
| `reference-unknown`    | A reference to an identifier that does not exist in the referenced collection                              | `references_must_resolve`                                   |
| `field-too-long`       | A field exceeding the data model's length limit                                                            | `fields_must_fit`                                           |
| `field-invalid`        | A field whose value is not of the type the data model requires, such as a non-integer Condition `priority` | `condition_priority_must_be_a_whole_number`                 |
| `identifier-duplicate` | An identifier already held by a record of any editable type                                                | `identifier_must_be_unused`                                 |
| `delete-referenced`    | Deleting a record another record still references                                                          | `check_deletion`                                            |

## Scoping notes

- **Citations** carry no `name` or `aka`, so the name, casing, and clash rules do
  not apply to them at all (`test_citations_are_not_subject_to_name_rules`).
- **Uniqueness of names** is enforced _within_ an entity type. The same name may
  exist in two different types.
- **`aka-name-clash`** is scoped to the same entity type only. An alternative
  name may coincide with a name of a different type, and may coincide with
  another record's alternative name.
- **References** are the reference fields each record class carries:
  `Condition.symptoms -> Symptom`, `Symptom.tests -> Test`, and the `citation`
  field of Condition, Symptom, and Test. `Validator.references_must_resolve`
  branches on the record class, so every field is checked against the collection
  it actually points at. The client-only collections (`cases` and the three
  `*-entries` files) are never read, so a record they still mention never blocks
  a deletion.
- **Identifiers** are checked for global uniqueness across all four editable
  types by `Validator.identifier_must_be_unused`. `IdentifierFactory` only mints
  them and reports whether a value has the right shape.

## Rule-to-test map

Each rule named above is covered by unit tests in `editor/tests/test_rules.py`.

| Rule id                | Covering tests                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name-unique`          | `test_duplicate_name_in_the_same_type_is_rejected`, `test_duplicate_name_among_tests_is_rejected`, `test_the_same_name_in_another_type_is_allowed`, `test_editing_a_record_does_not_clash_with_itself`, `test_a_different_records_name_is_still_rejected_while_editing`, `test_a_nameless_record_is_not_checked_for_uniqueness`                                                                                                                                                                                                                                                               |
| `name-title-case`      | `test_non_title_cased_name_is_rejected`, `test_corrected_values_are_accepted`, `test_title_casing_rule_is_idempotent_on_valid_values`                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `aka-title-case`       | `test_non_title_cased_alternative_name_is_rejected`, `test_corrected_values_are_accepted`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `aka-name-clash`       | `test_alias_equal_to_the_records_own_name_is_rejected`, `test_alias_equal_to_another_records_name_is_rejected`, `test_alias_equal_to_a_name_of_another_type_is_allowed`, `test_alias_matching_another_records_alias_is_allowed`, `test_alias_clash_with_another_name_still_applies_while_editing`, `test_a_blank_or_non_text_alias_is_ignored`                                                                                                                                                                                                                                                |
| `reference-required`   | `test_condition_without_a_symptom_is_rejected`, `test_symptom_without_a_test_is_rejected`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `reference-invalid`    | `test_a_reference_of_the_wrong_type_is_rejected`, `test_a_blank_reference_is_rejected`, `test_a_non_text_reference_is_rejected`                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `reference-unknown`    | `test_unresolvable_symptom_reference_is_rejected`, `test_unresolvable_citation_reference_is_rejected`, `test_resolvable_references_are_accepted`, `test_a_single_identifier_is_accepted_as_a_reference`                                                                                                                                                                                                                                                                                                                                                                                       |
| `field-too-long`       | `test_over_long_name_is_rejected`, `test_name_at_the_limit_is_accepted`, `test_over_long_description_is_rejected`, `test_over_long_citation_field_is_rejected`, `test_a_record_class_without_length_limits_is_not_checked`                                                                                                                                                                                                                                                                                                                                                                    |
| `field-invalid`        | `test_condition_priority_must_be_a_whole_number`, `test_condition_priority_may_be_zero`, `test_a_boolean_is_not_accepted_as_priority`, `test_a_record_without_a_priority_is_not_checked_for_one`                                                                                                                                                                                                                                                                                                                                                                                              |
| `identifier-duplicate` | `test_a_duplicate_identifier_is_reported`, `test_a_duplicate_identifier_in_another_type_is_reported`, `test_an_unused_identifier_is_accepted`, `test_editing_a_record_does_not_collide_with_its_own_identifier`                                                                                                                                                                                                                                                                                                                                                                               |
| `delete-referenced`    | `test_referencing_records_are_reported`, `test_a_referenced_record_cannot_be_deleted`, `test_an_unreferenced_record_can_be_deleted`, `test_a_referenced_citation_cannot_be_deleted`, `test_every_referencing_record_is_listed`, `test_a_test_can_block_a_citation_deletion`, `test_a_symptom_can_block_a_test_deletion`, `test_client_only_collections_never_block_a_deletion`, `test_references_only_match_the_entity_type_they_point_at`, `test_a_referencing_record_without_a_name_is_labelled_by_its_identifier`, `test_a_referencing_record_with_neither_name_nor_identifier_is_unknown` |

## Known follow-up: the client is currently broken

The four client-only collections were **deleted** as part of this work:
`cases.json`, `condition-entries.json`, `symptom-entries.json`, and
`test-entries.json`. SSEditor never read them, so it is unaffected.

`public/app.js` still fetches all of them. Its `COLLECTION_PATHS` map lists the
deleted files and `loadCollections` loads every path in a single `Promise.all`,
throwing on the first non-OK response. Because those files are now missing, the
client shows its "diagnosis data unavailable" error and the diagnosis workflow
does not start.

Repairing this was deliberately left out of scope and is tracked as separate
work. The fix is small: drop the four deleted entries from `COLLECTION_PATHS`
and the three matching `ensureReferences(...)` calls in `validateCollections`.
That also brings `app.js` in line with the client's own specification, which
only ever commits to loading the condition, symptom, test, and citation
collections.
