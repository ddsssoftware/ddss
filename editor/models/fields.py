"""Presentation descriptors for the editable entity types.

The detail screens are built from these specs, so the editable shape of an
entity type is data rather than a new screen: which fields to show, in which
order, with which editor widget. This is the *form*, not the rules -- the
validator and the repository know nothing about these descriptors.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Literal

FieldKind = Literal[
    "text",
    "long_text",
    "text_list",
    "integer",
    "reference",
    "reference_list",
]


@dataclass(frozen=True)
class FieldSpec:
    """One editable field of an entity type."""

    name: str
    label: str
    kind: FieldKind = "text"
    target: str | None = None


@dataclass(frozen=True)
class EntitySpec:
    """The editable shape of one entity type."""

    entity_type: str
    label: str
    label_field: str
    fields: tuple[FieldSpec, ...]


_NAME = FieldSpec("name", "Name")
_DESC = FieldSpec("desc", "Description", "long_text")
_AKA = FieldSpec("aka", "Alternative names (comma separated)", "text_list")
_CITATION = FieldSpec("citation", "Citation identifier", "reference", "citations")

ENTITY_SPECS: Final[dict[str, EntitySpec]] = {
    "conditions": EntitySpec(
        entity_type="conditions",
        label="Condition",
        label_field="name",
        fields=(
            _NAME,
            _DESC,
            _AKA,
            FieldSpec(
                "symptoms",
                "Symptom identifiers (comma separated)",
                "reference_list",
                "symptoms",
            ),
            FieldSpec("priority", "Priority", "integer"),
            _CITATION,
        ),
    ),
    "symptoms": EntitySpec(
        entity_type="symptoms",
        label="Symptom",
        label_field="name",
        fields=(
            _NAME,
            _DESC,
            _AKA,
            FieldSpec(
                "tests",
                "Test identifiers (comma separated)",
                "reference_list",
                "tests",
            ),
            _CITATION,
        ),
    ),
    "tests": EntitySpec(
        entity_type="tests",
        label="Test",
        label_field="name",
        fields=(_NAME, _DESC, _AKA, _CITATION),
    ),
    "citations": EntitySpec(
        entity_type="citations",
        label="Citation",
        label_field="bibtex",
        fields=(
            FieldSpec("bibtex", "BibTeX entry", "long_text"),
            FieldSpec("ieee", "IEEE citation", "long_text"),
        ),
    ),
}


def spec_for(entity_type: str) -> EntitySpec:
    """Return the spec for ``entity_type``."""
    return ENTITY_SPECS[entity_type]


__all__ = [
    "ENTITY_SPECS",
    "EntitySpec",
    "FieldKind",
    "FieldSpec",
    "spec_for",
]
