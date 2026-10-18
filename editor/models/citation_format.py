"""Parsing, validating, and formatting one BibTeX citation.

This module is pure model logic: it never imports Textual. It turns the text of
a single BibTeX entry into a canonical entry and an ASCII IEEE-style citation,
and reports why a value cannot be used.
"""

from __future__ import annotations

import io
import re
import warnings
from collections import defaultdict
from dataclasses import dataclass

import anyascii
import pybtex.database
from citeproc import (
    Citation as CslCitation,
    CitationItem,
    CitationStylesBibliography,
    CitationStylesStyle,
    formatter,
)
from citeproc.source.bibtex import BibTeX
from citeproc.types import ARTICLE

#: The IEEE style bundled by ``citeproc-py-styles``.
IEEE_STYLE = "ieee"


class CitationError(ValueError):
    """The BibTeX value cannot be parsed or formatted."""


@dataclass(frozen=True)
class ParsedCitation:
    """One validated BibTeX entry and its canonical serialization."""

    key: str
    bibtex: str


class _IEEESource(BibTeX):
    """A citeproc BibTeX source that tolerates unknown types and common fields."""

    types = defaultdict(lambda: ARTICLE, BibTeX.types)
    fields = {
        **BibTeX.fields,
        "url": "URL",
        "school": "publisher",
        "institution": "publisher",
        "organization": "publisher",
    }


def _entry_has_content(entry: pybtex.database.Entry) -> bool:
    """Return whether the entry holds a field, author, or editor."""
    return bool(entry.fields) or any(entry.persons.values())


def parse_citation(text: str) -> ParsedCitation:
    """Parse exactly one BibTeX entry and return its canonical form.

    ``CitationError`` carries the reason a value cannot be used, so callers can
    show it without depending on pybtex's exception types.
    """
    value = text.strip()
    if not value:
        raise CitationError("Enter exactly one BibTeX entry.")

    try:
        data = pybtex.database.parse_string(value, bib_format="bibtex")
    except Exception as error:  # pybtex reports several parser-specific types
        raise CitationError(
            f"The BibTeX entry could not be parsed: {error}"
        ) from error

    entries = list(data.entries.items())
    if not entries:
        raise CitationError("Enter exactly one BibTeX entry.")
    if len(entries) != 1:
        raise CitationError("Exactly one BibTeX entry is required.")

    key, entry = entries[0]
    if not _entry_has_content(entry):
        raise CitationError(
            "The BibTeX entry must have at least one field or person."
        )

    try:
        canonical = pybtex.database.BibliographyData({key: entry}).to_string(
            "bibtex"
        )
    except Exception as error:  # serialization has its own failure modes
        raise CitationError(
            f"The BibTeX entry could not be serialized: {error}"
        ) from error

    return ParsedCitation(key=key, bibtex=canonical)


def format_ieee(parsed: ParsedCitation) -> str:
    """Format one parsed entry with the IEEE CSL style."""
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            source = _IEEESource(io.StringIO(parsed.bibtex), encoding="utf-8")
            style = CitationStylesStyle(IEEE_STYLE, validate=False)
            bibliography = CitationStylesBibliography(
                style, source, formatter.plain
            )
            bibliography.register(CslCitation([CitationItem(parsed.key)]))
            entries = bibliography.bibliography()
    except Exception as error:  # citeproc raises several unrelated types
        raise CitationError(
            f"The IEEE citation could not be derived: {error}"
        ) from error

    if not entries:
        raise CitationError("The IEEE citation could not be derived.")
    return str(entries[0])


def normalize_ieee(text: str) -> str:
    """Return one ASCII line, without the reference number."""
    value = re.sub(r"^\s*\[\d+\]\s*", "", text)
    value = anyascii.anyascii(value)
    value = re.sub(r"\s+", " ", value).strip()
    return value.encode("ascii", "ignore").decode("ascii")


def derive_ieee(text: str) -> str:
    """Parse, format, and normalize one BibTeX entry."""
    return normalize_ieee(format_ieee(parse_citation(text)))


def validate_citation(text: str) -> str | None:
    """Return why ``text`` cannot become an IEEE citation, or ``None``."""
    try:
        derive_ieee(text)
    except CitationError as error:
        return str(error)
    return None


__all__ = [
    "IEEE_STYLE",
    "CitationError",
    "ParsedCitation",
    "derive_ieee",
    "format_ieee",
    "normalize_ieee",
    "parse_citation",
    "validate_citation",
]
