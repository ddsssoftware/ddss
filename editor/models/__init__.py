"""The editor's model layer.

A barrel: it re-exports the model's public names so callers can write
``from editor.models import Condition, spec_for`` rather than reaching into the
individual modules. The definitions themselves live in:

- :mod:`editor.models.records` -- the four record classes and their JSON files
- :mod:`editor.models.fields` -- the descriptors the views build forms from
- :mod:`editor.models.repository` -- reading and writing the owned collections
- :mod:`editor.models.identifiers` -- minting and validating identifiers
"""

from __future__ import annotations

from editor.models.fields import (
    ENTITY_SPECS,
    EntitySpec,
    FieldKind,
    FieldSpec,
    spec_for,
)
from editor.models.identifiers import IDENTIFIER_PATTERN, IdentifierFactory
from editor.models.records import (
    ENTITY_TYPES,
    RECORD_TYPES,
    Citation,
    Condition,
    Record,
    RecordError,
    Symptom,
    Test,
    record_type,
)
from editor.models.repository import (
    UNOWNED_COLLECTION_FILES,
    CollectionRepository,
)
from editor.models.rules import (
    NAME_MAX_LENGTH,
    TEXT_MAX_LENGTH,
    NamedRecord,
    Reference,
    Validator,
    Violation,
    is_title_cased,
)

# Imported last: it composes the modules above.
from editor.models.editor_model import EditorModel

__all__ = [
    "ENTITY_SPECS",
    "ENTITY_TYPES",
    "IDENTIFIER_PATTERN",
    "NAME_MAX_LENGTH",
    "RECORD_TYPES",
    "TEXT_MAX_LENGTH",
    "UNOWNED_COLLECTION_FILES",
    "Citation",
    "CollectionRepository",
    "Condition",
    "EditorModel",
    "EntitySpec",
    "FieldKind",
    "FieldSpec",
    "IdentifierFactory",
    "NamedRecord",
    "Record",
    "RecordError",
    "Reference",
    "Symptom",
    "Test",
    "Validator",
    "Violation",
    "is_title_cased",
    "record_type",
    "spec_for",
]
