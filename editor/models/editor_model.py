"""The editor's model: the in-memory store, and the only thing that writes.

The model owns the four collections and is the single place where a write can
happen. It runs the whole validator and persists only when the violation list is
empty, so "validate then persist" cannot be split or half-done by a caller.
"""

from __future__ import annotations

from typing import Any

from editor.models.fields import EntitySpec, spec_for
from editor.models.identifiers import IdentifierFactory
from editor.models.records import (
    Citation,
    Condition,
    Record,
    RecordError,
    Symptom,
    Test,
)
from editor.models.repository import CollectionRepository
from editor.models.rules import Validator, Violation


class EditorModel:
    """The four owned collections, and every accepted write to them."""

    def __init__(
        self,
        repository: CollectionRepository,
        validator: Validator | None = None,
        identifiers: IdentifierFactory | None = None,
    ) -> None:
        self.repository = repository
        self.validator = validator or Validator()
        self.identifiers = identifiers or IdentifierFactory()
        self.load_error: str | None = None
        self._conditions: list[Record] = []
        self._symptoms: list[Record] = []
        self._tests: list[Record] = []
        self._citations: list[Record] = []
        self.reload()

    # -- reading ------------------------------------------------------------

    def reload(self) -> None:
        """Re-read every owned collection.

        A file that cannot be read is reported through ``load_error`` and leaves
        the collections as they were, so the screen can show the problem instead
        of the editor refusing to start.
        """
        try:
            loaded = self.repository.load_all()
        except RecordError as error:
            self.load_error = str(error)
            return
        self.load_error = None
        self._conditions = loaded["conditions"]
        self._symptoms = loaded["symptoms"]
        self._tests = loaded["tests"]
        self._citations = loaded["citations"]

    def conditions(self) -> list[Record]:
        """Return the stored Conditions."""
        return list(self._conditions)

    def symptoms(self) -> list[Record]:
        """Return the stored Symptoms."""
        return list(self._symptoms)

    def tests(self) -> list[Record]:
        """Return the stored Tests."""
        return list(self._tests)

    def citations(self) -> list[Record]:
        """Return the stored Citations."""
        return list(self._citations)

    def all_records(self) -> list[Record]:
        """Return every stored record of every owned type."""
        return self._conditions + self._symptoms + self._tests + self._citations

    def label_for(self, record: Record) -> str:
        """Return the text that names ``record`` in a list.

        Which field names a record is a presentation choice, so it comes from the
        entity type's spec. A record with no label falls back to its identifier.
        """
        field = self.spec_for(record.ENTITY_TYPE).label_field
        value = getattr(record, field, None)
        if isinstance(value, str) and value.strip():
            return value
        return str(record.id)

    def spec_for(self, entity_type: str) -> EntitySpec:
        """Return the form descriptor for ``entity_type``."""
        return spec_for(entity_type)

    # -- writing ------------------------------------------------------------

    def save(
        self, record: Record, existing: Record | None = None
    ) -> list[Violation]:
        """Validate and store ``record``.

        An empty list means the record was stored. ``existing`` is the stored
        version when editing, so an edit keeps its identifier and does not clash
        with itself.
        """
        record.id = self.identifiers.resolve(existing)
        violations = self.validator.validate(record, existing, self)
        if violations:
            return violations
        self._write(record)
        return []

    def delete(self, record: Record) -> list[Violation]:
        """Delete ``record`` unless another record still references it."""
        violations = self.validator.check_deletion(
            record.ENTITY_TYPE, str(record.id), self
        )
        if violations:
            return violations
        collection = self._collection_of(record)
        collection[:] = [
            candidate for candidate in collection if candidate.id != record.id
        ]
        self.repository.save(record.ENTITY_TYPE, collection)
        return []

    def _write(self, record: Record) -> None:
        """Put ``record`` into its collection and write the whole collection.

        A record whose identifier is already stored is replaced in place, so an
        edit keeps its position; otherwise the record is appended.
        """
        collection = self._collection_of(record)
        index = self._index_of(collection, record.id)
        if index is None:
            collection.append(record)
        else:
            collection[index] = record
        self.repository.save(record.ENTITY_TYPE, collection)

    @staticmethod
    def _index_of(collection: list[Record], identifier: Any) -> int | None:
        """Return the position of the stored record holding ``identifier``."""
        for index, candidate in enumerate(collection):
            if candidate.id == identifier:
                return index
        return None

    def _collection_of(self, record: Record) -> list[Record]:
        """Return the collection ``record`` belongs to."""
        if isinstance(record, Condition):
            return self._conditions
        if isinstance(record, Symptom):
            return self._symptoms
        if isinstance(record, Test):
            return self._tests
        return self._citations


__all__ = ["EditorModel"]
