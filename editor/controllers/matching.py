"""Matching a record by its name or by one of its alternative names.

The picker and the list screens must agree on what searching means, so both go
through these functions instead of each writing its own comparison.
"""

from __future__ import annotations

from editor.models.fields import label_of
from editor.models.records import Record


def aliases_of(record: Record) -> list[str]:
    """Return the record's alternative names, ignoring malformed values."""
    value = getattr(record, "aka", None)
    if not isinstance(value, list):
        return []
    return [alias for alias in value if isinstance(alias, str)]


def matches(record: Record, term: str) -> bool:
    """Return whether ``term`` appears in the name or an alternative name."""
    wanted = term.strip().casefold()
    if not wanted:
        return True
    if wanted in label_of(record).casefold():
        return True
    return any(wanted in alias.casefold() for alias in aliases_of(record))


def annotated_label(record: Record, term: str) -> str | None:
    """Return how to label ``record`` while searching for ``term``.

    A name match shows the name alone; an alternative-name match shows the name
    followed by the first matching alternative. ``None`` means no match.
    """
    wanted = term.strip().casefold()
    label = label_of(record)
    if not wanted or wanted in label.casefold():
        return label
    for alias in aliases_of(record):
        if wanted in alias.casefold():
            return f"{label} ({alias})"
    return None


__all__ = ["aliases_of", "annotated_label", "matches"]
