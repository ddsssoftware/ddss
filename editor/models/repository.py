"""Reading and writing the four owned collection files.

The repository knows *where* the collections live and which entity type maps to
which record class. The record classes themselves do the JSON work.

Only the four editable entity types are owned here. The client-only collections
(``cases`` and the three ``*-entries`` files) are deliberately absent, so they
are never read, validated, migrated, or written.
"""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path
from typing import Final

from editor.models.records import (
    DEFAULT_DATA_DIRECTORY,
    ENTITY_TYPES,
    Record,
    record_type,
)

#: Collections DDClient owns. SSEditor must never read, validate or write them.
UNOWNED_COLLECTION_FILES: Final[tuple[str, ...]] = (
    "condition-entries.json",
    "symptom-entries.json",
    "test-entries.json",
    "cases.json",
)


class CollectionRepository:
    """The four owned collections held in one data directory."""

    def __init__(self, data_directory: Path | None = None) -> None:
        self.data_directory: Path = data_directory or DEFAULT_DATA_DIRECTORY

    def path(self, entity_type: str) -> Path:
        """Return the file holding ``entity_type``."""
        return record_type(entity_type).path(self.data_directory)

    def record_type(self, entity_type: str) -> type[Record]:
        """Return the record class stored for ``entity_type``."""
        return record_type(entity_type)

    def load(self, entity_type: str) -> list[Record]:
        """Load one collection, rejecting anything that is not a JSON array."""
        return record_type(entity_type).load(self.data_directory)

    def load_all(self) -> dict[str, list[Record]]:
        """Load every owned collection, keyed by entity type."""
        return {
            entity_type: self.load(entity_type)
            for entity_type in ENTITY_TYPES
        }

    def save(self, entity_type: str, records: Iterable[Record]) -> Path:
        """Write the whole collection back as a JSON array.

        The caller supplies the complete collection, so records it did not touch
        are written back unchanged.
        """
        return record_type(entity_type).save(records, self.data_directory)


__all__ = [
    "UNOWNED_COLLECTION_FILES",
    "CollectionRepository",
]
