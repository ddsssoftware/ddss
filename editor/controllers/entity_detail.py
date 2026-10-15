"""Adding or editing one record of one entity type.

The form is built from the entity type's spec, but reading a record and building
one from form text is written out per record class: it is the one place that
knows how each field's text maps to a value.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from editor.models.editor_model import EditorModel
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


def _text(value: Any) -> str:
    """Return a single value as the text a form field shows."""
    return "" if value is None else str(value)


def _list_text(value: Any) -> str:
    """Return a list value as the text a form field shows."""
    if isinstance(value, list):
        return LIST_SEPARATOR.join(str(item) for item in value)
    return _text(value)


def _list_value(raw: str) -> list[str]:
    """Return a comma-separated form value as a list of entries."""
    return [part.strip() for part in raw.split(",") if part.strip()]


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

    def save(self, values: Mapping[str, str]) -> list[Violation]:
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

    def _build(self, values: Mapping[str, str]) -> Record:
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
    "EntityDetailController",
]
