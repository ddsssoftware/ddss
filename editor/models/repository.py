"""Reading and writing the four owned collection files.

The repository knows *where* the collections live and which entity type maps to
which record class. The record classes themselves do the JSON work.

Only the four editable entity types are owned here. The client-only collections
(``cases`` and the three ``*-entries`` files) are deliberately absent, so they
are never read, validated, migrated, or written.

Every accepted write also republishes ``version.json``, the marker DDClient
compares against to decide whether its cached collections are current. The
marker is written after the collection and a failure to write it is swallowed:
the collection is the datum, the marker is advisory.
"""

from __future__ import annotations

import json
from collections.abc import Callable, Iterable
from datetime import datetime, timezone
from pathlib import Path
from typing import Final

from editor.models.records import (
    DEFAULT_DATA_DIRECTORY,
    ENTITY_TYPES,
    Record,
    record_type,
    write_text_atomically,
)

#: Collections DDClient owns. SSEditor must never read, validate or write them.
UNOWNED_COLLECTION_FILES: Final[tuple[str, ...]] = (
    "condition-entries.json",
    "symptom-entries.json",
    "test-entries.json",
    "cases.json",
)

#: The marker DDClient reads to know the collections changed.
VERSION_FILENAME: Final[str] = "version.json"


def _utc_now() -> datetime:
    """Return the current time, so the default clock stays replaceable."""
    return datetime.now(timezone.utc)


def version_payload(moment: datetime) -> str:
    """Return the JSON document the version marker holds at ``moment``."""
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=timezone.utc)
    else:
        moment = moment.astimezone(timezone.utc)
    timestamp = moment.isoformat(timespec="microseconds").replace("+00:00", "Z")
    return json.dumps({"version": timestamp}) + "\n"


class CollectionRepository:
    """The four owned collections held in one data directory."""

    def __init__(
        self,
        data_directory: Path | None = None,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        self.data_directory: Path = data_directory or DEFAULT_DATA_DIRECTORY
        self.clock: Callable[[], datetime] = clock or _utc_now

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
        are written back unchanged. The version marker is republished only after
        the collection has been replaced.
        """
        path = record_type(entity_type).save(records, self.data_directory)
        self._publish_version()
        return path

    def version_path(self) -> Path:
        """Return the file holding the published data version."""
        return self.data_directory / VERSION_FILENAME

    def _publish_version(self) -> None:
        """Republish the version marker, ignoring a failure to write it.

        Raising here would report a false failure after the record was stored,
        and a retry of a new record would then be refused as a duplicate. The
        next accepted write republishes the marker.
        """
        try:
            write_text_atomically(
                self.version_path(), version_payload(self.clock())
            )
        except OSError:
            return


__all__ = [
    "UNOWNED_COLLECTION_FILES",
    "VERSION_FILENAME",
    "CollectionRepository",
    "version_payload",
]
