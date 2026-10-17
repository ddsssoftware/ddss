"""Adding or editing one record of one entity type.

The form is built from the entity type's spec, but reading a record and building
one from form text is written out per record class: it is the one place that
knows how each field's text maps to a value.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any

from editor.controllers.matching import annotated_label
from editor.models.editor_model import EditorModel
from editor.models.fields import FieldSpec
from editor.models.records import (
    Citation,
    Condition,
    Record,
    Symptom,
    Test,
)
from editor.models.rules import Violation

#: What separates the identifiers of a list-valued field in the form.
LIST_SEPARATOR = ", "


@dataclass(frozen=True)
class AttachedReference:
    """One identifier held by a reference field, and the record it resolves to."""

    identifier: str
    record: Record | None


@dataclass(frozen=True)
class ReferenceChoice:
    """A record the picker can offer, labelled for the current search term."""

    identifier: str
    label: str


def _text(value: Any) -> str:
    """Return a single value as the text a form field shows."""
    return "" if value is None else str(value)


def _list_text(value: Any) -> str:
    """Return a list value as the text a form field shows."""
    if isinstance(value, list):
        return LIST_SEPARATOR.join(str(item) for item in value)
    return _text(value)


def _list_value(raw: Any) -> list[str]:
    """Return a reference field's form value as a list of identifiers.

    The form may hand over the rows the administrator attached as a list, or the
    comma-separated text of a single-line input.
    """
    if isinstance(raw, list):
        return [str(part).strip() for part in raw if str(part).strip()]
    return [part.strip() for part in str(raw).split(",") if part.strip()]


def _whole_number(raw: str) -> Any:
    """Return a whole number, or the raw text so the rules can reject it."""
    try:
        return int(raw)
    except ValueError:
        return raw.strip()


class EntityDetailController:
    """Adding, or editing, one record of one entity type."""

    def __init__(
        self,
        model: EditorModel,
        entity_type: str,
        record: Record | None = None,
    ) -> None:
        self.model = model
        self.spec = model.spec_for(entity_type)
        self.record = record

    @property
    def is_new(self) -> bool:
        """Whether this screen is adding rather than editing."""
        return self.record is None

    def initial_values(self) -> dict[str, str]:
        """Return the text every form field starts with."""
        if self.record is None:
            return {field.name: "" for field in self.spec.fields}
        return self._text_of(self.record)

    def fields(self) -> list[str]:
        """Return the field names this form shows, in order."""
        return [field.name for field in self.spec.fields]

    # -- references ---------------------------------------------------------

    def attached_references(self, field_name: str) -> list[AttachedReference]:
        """Return the references the stored record already holds, in order.

        An identifier that no longer resolves keeps its place with a ``None``
        record, so the form can show it and offer to remove it.
        """
        known = {record.id: record for record in self._target_records(field_name)}
        return [
            AttachedReference(identifier, known.get(identifier))
            for identifier in self._stored_identifiers(field_name)
        ]

    def available_references(
        self,
        field_name: str,
        term: str = "",
        attached: Iterable[str] = (),
    ) -> list[ReferenceChoice]:
        """Return the target records the picker may offer, in stored order.

        Records already referenced by the stored record, and the identifiers the
        caller passes as ``attached`` (the rows currently on the form), are left
        out. ``term`` matches names and alternative names.
        """
        taken = {reference.identifier for reference in self.attached_references(field_name)}
        taken.update(attached)
        choices: list[ReferenceChoice] = []
        for record in self._target_records(field_name):
            if not isinstance(record.id, str) or record.id in taken:
                continue
            label = annotated_label(record, term)
            if label is None:
                continue
            choices.append(ReferenceChoice(record.id, label))
        return choices

    def lookup_reference(self, field_name: str, identifier: str) -> Record | None:
        """Return the current record for ``identifier``, or ``None``."""
        for record in self._target_records(field_name):
            if record.id == identifier:
                return record
        return None

    def _field(self, field_name: str) -> FieldSpec:
        """Return the spec of one field this form shows."""
        return next(field for field in self.spec.fields if field.name == field_name)

    def _target_records(self, field_name: str) -> list[Record]:
        """Return the records of the entity type ``field_name`` points at."""
        target = self._field(field_name).target
        if target is None:
            return []
        getters = {
            "conditions": self.model.conditions,
            "symptoms": self.model.symptoms,
            "tests": self.model.tests,
            "citations": self.model.citations,
        }
        return getters[target]()

    def _stored_identifiers(self, field_name: str) -> list[str]:
        """Return the identifiers a stored record holds for one field."""
        if self.record is None:
            return []
        value = getattr(self.record, field_name, None)
        if isinstance(value, list):
            return [str(identifier) for identifier in value]
        if isinstance(value, str) and value.strip():
            return [value]
        return []

    def save(self, values: Mapping[str, Any]) -> list[Violation]:
        """Validate and store the form's values.

        An empty list means the record was stored; otherwise nothing was written.
        """
        candidate = self._build(values)
        violations = self.model.save(candidate, self.record)
        if violations:
            return violations
        self.record = candidate
        return []

    # -- values -------------------------------------------------------------

    @staticmethod
    def _text_of(record: Record) -> dict[str, str]:
        """Return one record's fields as the text its form shows."""
        if isinstance(record, Condition):
            return {
                "name": _text(record.name),
                "desc": _text(record.desc),
                "aka": _list_text(record.aka),
                "symptoms": _list_text(record.symptoms),
                "priority": _text(record.priority),
                "citation": _text(record.citation),
            }
        if isinstance(record, Symptom):
            return {
                "name": _text(record.name),
                "desc": _text(record.desc),
                "aka": _list_text(record.aka),
                "tests": _list_text(record.tests),
                "citation": _text(record.citation),
            }
        if isinstance(record, Test):
            return {
                "name": _text(record.name),
                "desc": _text(record.desc),
                "aka": _list_text(record.aka),
                "citation": _text(record.citation),
            }
        return {"bibtex": _text(record.bibtex), "ieee": _text(record.ieee)}

    def _build(self, values: Mapping[str, Any]) -> Record:
        """Build the candidate record from the form's values.

        The identifier is left unset: the model mints one, or keeps the one the
        record already has.
        """
        if self.spec.entity_type == "conditions":
            return Condition(
                name=values["name"].strip(),
                desc=values["desc"].strip(),
                aka=_list_value(values["aka"]),
                symptoms=_list_value(values["symptoms"]),
                priority=_whole_number(values["priority"]),
                citation=values["citation"].strip(),
            )
        if self.spec.entity_type == "symptoms":
            return Symptom(
                name=values["name"].strip(),
                desc=values["desc"].strip(),
                aka=_list_value(values["aka"]),
                tests=_list_value(values["tests"]),
                citation=values["citation"].strip(),
            )
        if self.spec.entity_type == "tests":
            return Test(
                name=values["name"].strip(),
                desc=values["desc"].strip(),
                aka=_list_value(values["aka"]),
                citation=values["citation"].strip(),
            )
        return Citation(
            bibtex=values["bibtex"].strip(),
            ieee=values["ieee"].strip(),
        )


__all__ = [
    "LIST_SEPARATOR",
    "AttachedReference",
    "EntityDetailController",
    "ReferenceChoice",
]
