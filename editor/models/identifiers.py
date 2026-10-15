"""Minting the identifiers that new records are stored under.

An identifier is a random 128-bit value rendered as 32 lowercase hexadecimal
characters. This class only mints one and reports whether a value has the right
shape; uniqueness across every entity type is enforced by the validator, which is
the only thing that can see all the records at once.
"""

from __future__ import annotations

import re
import uuid
from typing import Any, Final

from editor.models.records import Record

IDENTIFIER_PATTERN: Final[re.Pattern[str]] = re.compile(r"[0-9a-f]{32}")


class IdentifierFactory:
    """Mints record identifiers and validates their shape."""

    def new(self) -> str:
        """Return a fresh identifier: 32 lowercase hexadecimal characters."""
        return uuid.uuid4().hex

    def is_valid(self, value: Any) -> bool:
        """Return whether ``value`` has the required identifier shape."""
        return (
            isinstance(value, str)
            and IDENTIFIER_PATTERN.fullmatch(value) is not None
        )

    def resolve(self, existing: Record | None) -> str:
        """Return the identifier to store for a write.

        Editing an existing record keeps its identifier, so the references
        pointing at it stay valid; creating a new record mints a fresh one.
        """
        if existing is not None and self.is_valid(existing.id):
            return str(existing.id)
        return self.new()


__all__ = [
    "IDENTIFIER_PATTERN",
    "IdentifierFactory",
]
