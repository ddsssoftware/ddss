"""Tests for minting record identifiers.

Uniqueness across every entity type is a rule, so it is covered by
``test_rules.py``; this file covers the shape of an identifier and the rule that
an edit keeps the identifier it already has.
"""

from __future__ import annotations

import pytest

from editor.models.identifiers import IDENTIFIER_PATTERN, IdentifierFactory
from editor.models.records import Condition


@pytest.fixture
def factory() -> IdentifierFactory:
    return IdentifierFactory()


def test_a_new_identifier_is_32_lowercase_hex_characters(
    factory: IdentifierFactory,
) -> None:
    for _ in range(50):
        identifier = factory.new()

        assert len(identifier) == 32
        assert IDENTIFIER_PATTERN.fullmatch(identifier)
        assert identifier == identifier.lower()


def test_new_identifiers_do_not_repeat(factory: IdentifierFactory) -> None:
    generated = {factory.new() for _ in range(200)}

    assert len(generated) == 200


@pytest.mark.parametrize(
    "value",
    ["", "not-hex", "0123456789abcdef", "A" * 32, "0" * 31, "0" * 33, None, 42],
)
def test_is_valid_rejects_bad_values(
    factory: IdentifierFactory, value: object
) -> None:
    assert not factory.is_valid(value)


@pytest.mark.parametrize("value", ["0" * 32, "abcdef0123456789abcdef0123456789"])
def test_is_valid_accepts_valid_values(
    factory: IdentifierFactory, value: str
) -> None:
    assert factory.is_valid(value)


def test_resolve_keeps_the_identifier_of_an_existing_record(
    factory: IdentifierFactory,
) -> None:
    existing = Condition(id="f" * 32, name="Something")

    assert factory.resolve(existing) == "f" * 32


def test_resolve_mints_one_for_a_new_record(factory: IdentifierFactory) -> None:
    assert factory.is_valid(factory.resolve(None))


def test_resolve_replaces_a_malformed_existing_identifier(
    factory: IdentifierFactory,
) -> None:
    assert factory.is_valid(factory.resolve(Condition(id="legacy-slug")))
