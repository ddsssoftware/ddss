"""The four editable record classes.

Each class is the single definition of one record. It declares its identity
facts -- ``ENTITY_TYPE``, ``FILENAME`` and the human ``LABEL`` -- and it reads
and writes its own fields by name: ``to_dict`` returns a literal dict built
field by field, and ``from_dict`` reads the same fields back.

There is no field list and no field order. Key order is not part of the data
contract, so the JSON files may carry the fields in any order and nothing here
depends on one. ``to_dict`` omits a field whose value is ``None``, so a record
that never set a field is written without it, exactly like a hand-edited file.
"""

from __future__ import annotations

import json
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any, ClassVar, Self

DEFAULT_DATA_DIRECTORY: Path = (
    Path(__file__).resolve().parents[2] / "public" / "data"
)


class RecordError(Exception):
    """Raised when a collection file cannot be read as a JSON array."""


class Record:
    """Base class for one stored record.

    A subclass declares the three identity facts and implements ``to_dict`` and
    ``from_dict`` for its own fields. Everything else -- file location, reading,
    writing and equality -- is shared here.
    """

    ENTITY_TYPE: ClassVar[str]
    FILENAME: ClassVar[str]
    LABEL: ClassVar[str]

    id: Any

    # -- values -------------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        """Return the record as the JSON object it is stored as."""
        raise NotImplementedError

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Self:
        """Build a record from a parsed JSON object."""
        raise NotImplementedError

    # -- file access --------------------------------------------------------

    @classmethod
    def path(cls, data_directory: Path | None = None) -> Path:
        """Return the file this record type is stored in."""
        return (data_directory or DEFAULT_DATA_DIRECTORY) / cls.FILENAME

    @classmethod
    def load(cls, data_directory: Path | None = None) -> list[Self]:
        """Read the whole collection from its JSON file."""
        path = cls.path(data_directory)
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as error:
            raise RecordError(f"Could not read {path.name}: {error}.") from error
        try:
            data = json.loads(text)
        except json.JSONDecodeError as error:
            raise RecordError(
                f"{path.name} is not valid JSON: {error}."
            ) from error
        if not isinstance(data, list):
            raise RecordError(f"{path.name} must contain a JSON array.")
        records: list[Self] = []
        for index, item in enumerate(data):
            if not isinstance(item, Mapping):
                raise RecordError(
                    f"{path.name} item {index} must be a JSON object."
                )
            records.append(cls.from_dict(item))
        return records

    @classmethod
    def save(
        cls,
        records: Iterable[Record],
        data_directory: Path | None = None,
    ) -> Path:
        """Write the whole collection back as a JSON array.

        The file is swapped in via a temporary sibling, so a failure part-way
        through cannot truncate the existing data.
        """
        path = cls.path(data_directory)
        payload = (
            json.dumps(
                [record.to_dict() for record in records],
                indent=2,
                ensure_ascii=False,
            )
            + "\n"
        )
        temporary = path.with_name(f"{path.name}.tmp")
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            temporary.write_text(payload, encoding="utf-8")
            temporary.replace(path)
        except OSError as error:
            raise RecordError(f"Could not write {path.name}: {error}.") from error
        return path

    # -- dunder -------------------------------------------------------------

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Record):
            return NotImplemented
        return type(self) is type(other) and self.to_dict() == other.to_dict()

    def __repr__(self) -> str:
        arguments = ", ".join(
            f"{field}={value!r}" for field, value in self.to_dict().items()
        )
        return f"{type(self).__name__}({arguments})"


class Condition(Record):
    """A condition that can be assigned to a patient's presentation."""

    ENTITY_TYPE: ClassVar[str] = "conditions"
    FILENAME: ClassVar[str] = "conditions.json"
    LABEL: ClassVar[str] = "Condition"

    def __init__(
        self,
        id: Any = None,
        name: Any = None,
        desc: Any = None,
        symptoms: Any = None,
        priority: Any = None,
        citation: Any = None,
        aka: Any = None,
    ) -> None:
        self.id = id
        self.name = name
        self.desc = desc
        self.symptoms = symptoms
        self.priority = priority
        self.citation = citation
        self.aka = aka

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "id": self.id,
            "name": self.name,
            "desc": self.desc,
            "symptoms": self.symptoms,
            "priority": self.priority,
            "citation": self.citation,
            "aka": self.aka,
        }
        return {field: value for field, value in data.items() if value is not None}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Condition:
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            desc=data.get("desc"),
            symptoms=data.get("symptoms"),
            priority=data.get("priority"),
            citation=data.get("citation"),
            aka=data.get("aka"),
        )


class Symptom(Record):
    """A sign or description of an abnormal clinical presentation."""

    ENTITY_TYPE: ClassVar[str] = "symptoms"
    FILENAME: ClassVar[str] = "symptoms.json"
    LABEL: ClassVar[str] = "Symptom"

    def __init__(
        self,
        id: Any = None,
        name: Any = None,
        desc: Any = None,
        tests: Any = None,
        citation: Any = None,
        aka: Any = None,
    ) -> None:
        self.id = id
        self.name = name
        self.desc = desc
        self.tests = tests
        self.citation = citation
        self.aka = aka

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "id": self.id,
            "name": self.name,
            "desc": self.desc,
            "tests": self.tests,
            "citation": self.citation,
            "aka": self.aka,
        }
        return {field: value for field, value in data.items() if value is not None}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Symptom:
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            desc=data.get("desc"),
            tests=data.get("tests"),
            citation=data.get("citation"),
            aka=data.get("aka"),
        )


class Test(Record):
    """A procedure used to test a symptom."""

    #: Pytest must not mistake this record class for a test case.
    __test__ = False
    ENTITY_TYPE: ClassVar[str] = "tests"
    FILENAME: ClassVar[str] = "tests.json"
    LABEL: ClassVar[str] = "Test"

    def __init__(
        self,
        id: Any = None,
        name: Any = None,
        desc: Any = None,
        citation: Any = None,
        aka: Any = None,
    ) -> None:
        self.id = id
        self.name = name
        self.desc = desc
        self.citation = citation
        self.aka = aka

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "id": self.id,
            "name": self.name,
            "desc": self.desc,
            "citation": self.citation,
            "aka": self.aka,
        }
        return {field: value for field, value in data.items() if value is not None}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Test:
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            desc=data.get("desc"),
            citation=data.get("citation"),
            aka=data.get("aka"),
        )


class Citation(Record):
    """The source of a Condition, Symptom, or Test."""

    ENTITY_TYPE: ClassVar[str] = "citations"
    FILENAME: ClassVar[str] = "citations.json"
    LABEL: ClassVar[str] = "Citation"

    def __init__(
        self,
        id: Any = None,
        bibtex: Any = None,
        ieee: Any = None,
    ) -> None:
        self.id = id
        self.bibtex = bibtex
        self.ieee = ieee

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "id": self.id,
            "bibtex": self.bibtex,
            "ieee": self.ieee,
        }
        return {field: value for field, value in data.items() if value is not None}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Citation:
        return cls(
            id=data.get("id"),
            bibtex=data.get("bibtex"),
            ieee=data.get("ieee"),
        )


#: The one entity-type lookup the outside world needs: the CLI ``--entity-type``
#: value, the collection file name and the view label all come from here.
RECORD_TYPES: dict[str, type[Record]] = {
    "conditions": Condition,
    "symptoms": Symptom,
    "tests": Test,
    "citations": Citation,
}

ENTITY_TYPES: tuple[str, ...] = tuple(RECORD_TYPES)


def record_type(entity_type: str) -> type[Record]:
    """Return the record class for ``entity_type``."""
    try:
        return RECORD_TYPES[entity_type]
    except KeyError:
        raise RecordError(f"Unknown entity type {entity_type!r}.") from None


__all__ = [
    "Citation",
    "Condition",
    "DEFAULT_DATA_DIRECTORY",
    "ENTITY_TYPES",
    "RECORD_TYPES",
    "Record",
    "RecordError",
    "Symptom",
    "Test",
    "record_type",
]
