"""Every validation and integrity rule. Pure logic, no UI dependencies.

One class holds them all: :class:`Validator`. Each rule is its own method, named
for what it requires, and ``validate`` is the readable list of which rules apply
to which record class. Rules branch on the record class with ``isinstance``
rather than looking an entity type up in a table, so a rule cannot silently stop
covering a type.

Every breach is reported as a :class:`Violation`. Violations are *blocking*: a
caller must not write the record while any are returned. Nothing here mutates the
record -- in particular, casing is never silently corrected.

Each rule keeps the ``rule_id`` and the message text it has always produced, so
what the administrator reads does not change.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Final

from titlecase import titlecase

from editor.models.citation_format import validate_citation
from editor.models.records import (
    Citation,
    Condition,
    Record,
    Symptom,
    Test,
    record_type,
)

if TYPE_CHECKING:  # pragma: no cover - annotations only
    from editor.models.editor_model import EditorModel

NAME_MAX_LENGTH: Final[int] = 256
TEXT_MAX_LENGTH: Final[int] = 1024
CITATION_MAX_LENGTH: Final[int] = 2048

#: The three entity types that carry a ``name`` and an ``aka`` list.
NamedRecord = Condition | Symptom | Test


@dataclass(frozen=True)
class Violation:
    """A blocking rule breach."""

    rule: str
    field: str
    message: str


@dataclass(frozen=True)
class Reference:
    """A stored record that points at another record."""

    entity_type: str
    field: str
    identifier: str
    label: str


def is_title_cased(value: str) -> bool:
    """Return whether ``value`` already matches the required title casing."""
    return value == titlecase(value)


def _values(value: Any) -> list[Any]:
    """Return the references held in ``value``, or an empty list."""
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return list(value)
    return []


def _reference_parts(value: Any) -> list[Any] | None:
    """Return the references held in ``value``, or ``None`` when malformed."""
    if isinstance(value, str) or isinstance(value, list):
        return _values(value)
    return None


def _aliases(record: NamedRecord) -> tuple[Any, ...]:
    if isinstance(record.aka, list):
        return tuple(record.aka)
    return ()


def _is_being_edited(other: Record, existing: Record | None) -> bool:
    """Return whether ``other`` is the stored copy that ``existing`` stands for.

    A record's identifier is its identity, so this matches by identifier rather
    than by object: the model reloads its collections from disk, so the object a
    caller holds is usually not the object the model holds.
    """
    if existing is None or other.id is None:
        return False
    return other.id == existing.id


def _label(record: Record) -> str:
    """Return the text that names ``record`` in a message."""
    name = getattr(record, "name", None)
    if isinstance(name, str) and name.strip():
        return name
    identifier = record.id
    return identifier if isinstance(identifier, str) else "<unknown>"


def _resolve(
    field: str,
    value: Any,
    known: Sequence[Record],
    known_label: str,
) -> list[Violation]:
    """Return a violation for each reference in ``value`` that cannot resolve."""
    if value is None:
        return []
    parts = _reference_parts(value)
    if parts is None:
        return [
            Violation(
                rule="reference-invalid",
                field=field,
                message=(
                    f'"{field}" must be an identifier or a list of identifiers.'
                ),
            )
        ]
    known_identifiers = {record.id for record in known}
    violations: list[Violation] = []
    for reference in parts:
        if not isinstance(reference, str) or not reference.strip():
            violations.append(
                Violation(
                    rule="reference-invalid",
                    field=field,
                    message=f'"{field}" contains an empty or non-text reference.',
                )
            )
        elif reference not in known_identifiers:
            violations.append(
                Violation(
                    rule="reference-unknown",
                    field=field,
                    message=f'{known_label} "{reference}" does not exist.',
                )
            )
    return violations


def _over_length(checks: Iterable[tuple[str, Any, int]]) -> list[Violation]:
    """Return a violation for every value longer than its limit allows."""
    violations: list[Violation] = []
    for field, value, maximum in checks:
        if isinstance(value, str) and len(value) > maximum:
            violations.append(
                Violation(
                    rule="field-too-long",
                    field=field,
                    message=(
                        f'"{field}" is {len(value)} characters long; '
                        f"the maximum is {maximum}."
                    ),
                )
            )
    return violations


class Validator:
    """Every rule the editor enforces, one method each."""

    def validate(
        self,
        record: Record,
        existing: Record | None,
        model: EditorModel,
    ) -> list[Violation]:
        """Return every blocking violation for writing ``record``.

        ``existing`` is the stored version of the record when editing, so a rule
        can ignore the record's own current values.
        """
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
        violations += self.bibtex_must_be_valid(record)
        violations += self.condition_priority_must_be_a_whole_number(record)
        violations += self.identifier_must_be_unused(record, existing, model)
        return violations

    # -- names --------------------------------------------------------------

    def name_must_be_unique(
        self,
        record: NamedRecord,
        existing: Record | None,
        model: EditorModel,
    ) -> list[Violation]:
        """Reject a name already used by a different record of the same type."""
        name = record.name
        if not isinstance(name, str) or not name.strip():
            return []
        for other in self._same_type_records(record, model):
            if _is_being_edited(other, existing):
                continue
            if other.name == name:
                return [
                    Violation(
                        rule="name-unique",
                        field="name",
                        message=(
                            f'{record.ENTITY_TYPE} already contains a record '
                            f'named "{name}".'
                        ),
                    )
                ]
        return []

    def name_and_aka_must_be_title_cased(
        self, record: NamedRecord
    ) -> list[Violation]:
        """Reject a name or alternative name that is not title cased."""
        violations: list[Violation] = []

        name = record.name
        if isinstance(name, str) and name.strip() and not is_title_cased(name):
            violations.append(
                Violation(
                    rule="name-title-case",
                    field="name",
                    message=(
                        f'The name "{name}" is not title cased; '
                        f'it must be written "{titlecase(name)}".'
                    ),
                )
            )

        for index, alias in enumerate(_aliases(record)):
            if isinstance(alias, str) and alias.strip() and not is_title_cased(alias):
                violations.append(
                    Violation(
                        rule="aka-title-case",
                        field=f"aka[{index}]",
                        message=(
                            f'The alternative name "{alias}" is not title cased; '
                            f'it must be written "{titlecase(alias)}".'
                        ),
                    )
                )
        return violations

    def aka_must_not_clash_with_a_name(
        self,
        record: NamedRecord,
        existing: Record | None,
        model: EditorModel,
    ) -> list[Violation]:
        """Reject an alternative name that is a name of the same entity type.

        The clash is checked against this record's own name and the names of
        other records of the same type only; alternative names never clash with
        each other, and never with names of a different type.
        """
        other_names = {
            other.name
            for other in self._same_type_records(record, model)
            if not _is_being_edited(other, existing)
        }
        violations: list[Violation] = []
        for index, alias in enumerate(_aliases(record)):
            if not isinstance(alias, str) or not alias.strip():
                continue
            if alias == record.name:
                violations.append(
                    Violation(
                        rule="aka-name-clash",
                        field=f"aka[{index}]",
                        message=(
                            f'Alternative name "{alias}" is the same as this '
                            "record's own name."
                        ),
                    )
                )
            elif alias in other_names:
                violations.append(
                    Violation(
                        rule="aka-name-clash",
                        field=f"aka[{index}]",
                        message=(
                            f'Alternative name "{alias}" is already the name of '
                            f"another {record.ENTITY_TYPE} record."
                        ),
                    )
                )
        return violations

    # -- reference relationships --------------------------------------------

    def condition_must_have_a_symptom(self, record: Condition) -> list[Violation]:
        """Reject a Condition that references no Symptom."""
        if _values(record.symptoms):
            return []
        return [
            Violation(
                rule="reference-required",
                field="symptoms",
                message="A Condition must reference at least one Symptom.",
            )
        ]

    def symptom_must_have_a_test(self, record: Symptom) -> list[Violation]:
        """Reject a Symptom that references no Test."""
        if _values(record.tests):
            return []
        return [
            Violation(
                rule="reference-required",
                field="tests",
                message="A Symptom must reference at least one Test.",
            )
        ]

    def references_must_resolve(
        self, record: Record, model: EditorModel
    ) -> list[Violation]:
        """Reject a reference that does not resolve to a stored record."""
        if isinstance(record, Condition):
            violations = _resolve(
                "symptoms", record.symptoms, model.symptoms(), "Symptom"
            )
            violations += _resolve(
                "citation", record.citation, model.citations(), "Citation"
            )
            return violations
        if isinstance(record, Symptom):
            violations = _resolve("tests", record.tests, model.tests(), "Test")
            violations += _resolve(
                "citation", record.citation, model.citations(), "Citation"
            )
            return violations
        if isinstance(record, Test):
            return _resolve(
                "citation", record.citation, model.citations(), "Citation"
            )
        return []

    # -- field values -------------------------------------------------------

    def fields_must_fit(self, record: Record) -> list[Violation]:
        """Reject a field longer than the data model permits."""
        if isinstance(record, (Condition, Symptom, Test)):
            return _over_length(
                (
                    ("name", record.name, NAME_MAX_LENGTH),
                    ("desc", record.desc, TEXT_MAX_LENGTH),
                )
            )
        if isinstance(record, Citation):
            return _over_length(
                (
                    ("bibtex", record.bibtex, CITATION_MAX_LENGTH),
                    ("ieee", record.ieee, CITATION_MAX_LENGTH),
                )
            )
        return []

    def bibtex_must_be_valid(self, record: Record) -> list[Violation]:
        """Reject a Citation whose BibTeX entry cannot become an IEEE citation."""
        if not isinstance(record, Citation):
            return []
        value = record.bibtex if isinstance(record.bibtex, str) else ""
        message = validate_citation(value)
        if message is None:
            return []
        return [
            Violation(
                rule="bibtex-invalid",
                field="bibtex",
                message=message,
            )
        ]

    def condition_priority_must_be_a_whole_number(
        self, record: Record
    ) -> list[Violation]:
        """Reject a Condition whose priority is not a whole number."""
        if not isinstance(record, Condition):
            return []
        if isinstance(record.priority, bool) or not isinstance(record.priority, int):
            return [
                Violation(
                    rule="field-invalid",
                    field="priority",
                    message='"priority" must be a whole number.',
                )
            ]
        return []

    # -- identifiers --------------------------------------------------------

    def identifier_must_be_unused(
        self,
        record: Record,
        existing: Record | None,
        model: EditorModel,
    ) -> list[Violation]:
        """Reject an identifier already held by any record of any owned type."""
        for other in model.all_records():
            if _is_being_edited(other, existing):
                continue
            if other.id == record.id:
                return [
                    Violation(
                        rule="identifier-duplicate",
                        field="id",
                        message=(
                            f"Identifier {record.id!r} is already used by "
                            "another record."
                        ),
                    )
                ]
        return []

    # -- deletion -----------------------------------------------------------

    def find_references(
        self, entity_type: str, identifier: str, model: EditorModel
    ) -> list[Reference]:
        """Return every stored record that references ``identifier``.

        Only the four owned entity types are consulted. The client-only
        collections are never read, so a record they still mention does not
        block a deletion.
        """
        references: list[Reference] = []

        for record in model.conditions():
            if entity_type == "symptoms" and identifier in _values(record.symptoms):
                references.append(
                    Reference(
                        "conditions", "symptoms", str(record.id), _label(record)
                    )
                )
            if entity_type == "citations" and identifier in _values(record.citation):
                references.append(
                    Reference(
                        "conditions", "citation", str(record.id), _label(record)
                    )
                )
        for record in model.symptoms():
            if entity_type == "tests" and identifier in _values(record.tests):
                references.append(
                    Reference("symptoms", "tests", str(record.id), _label(record))
                )
            if entity_type == "citations" and identifier in _values(record.citation):
                references.append(
                    Reference("symptoms", "citation", str(record.id), _label(record))
                )
        for record in model.tests():
            if entity_type == "citations" and identifier in _values(record.citation):
                references.append(
                    Reference("tests", "citation", str(record.id), _label(record))
                )
        return references

    def check_deletion(
        self, entity_type: str, identifier: str, model: EditorModel
    ) -> list[Violation]:
        """Return a blocking violation when ``identifier`` is still referenced.

        An empty list means the deletion is allowed. The message names every
        referencing record, so the administrator can see what depends on it.
        """
        references = self.find_references(entity_type, identifier, model)
        if not references:
            return []
        described = "; ".join(
            f'{record_type(reference.entity_type).LABEL} "{reference.label}" '
            f"via {reference.field}"
            for reference in references
        )
        return [
            Violation(
                rule="delete-referenced",
                field=identifier,
                message=(
                    f"Cannot delete {record_type(entity_type).LABEL} "
                    f"{identifier!r}: it is still referenced by {described}."
                ),
            )
        ]

    # -- helpers ------------------------------------------------------------

    @staticmethod
    def _same_type_records(
        record: NamedRecord, model: EditorModel
    ) -> list[Record]:
        """Return the stored records of the same entity type as ``record``."""
        if isinstance(record, Condition):
            return model.conditions()
        if isinstance(record, Symptom):
            return model.symptoms()
        return model.tests()


__all__ = [
    "NAME_MAX_LENGTH",
    "TEXT_MAX_LENGTH",
    "NamedRecord",
    "Reference",
    "Validator",
    "Violation",
    "is_title_cased",
]
