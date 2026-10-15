"""Tests for the presentation descriptors the views build forms from."""

from __future__ import annotations

import pytest

from editor.models import ENTITY_SPECS, ENTITY_TYPES, EntitySpec, FieldSpec, spec_for


def test_every_editable_entity_type_has_a_spec() -> None:
    assert set(ENTITY_SPECS) == set(ENTITY_TYPES)


def test_spec_for_returns_the_spec_of_that_entity_type() -> None:
    assert spec_for("conditions") is ENTITY_SPECS["conditions"]


def test_spec_for_rejects_an_unknown_entity_type() -> None:
    with pytest.raises(KeyError):
        spec_for("cases")


def test_each_spec_describes_its_own_fields() -> None:
    for entity_type, spec in ENTITY_SPECS.items():
        assert isinstance(spec, EntitySpec)
        assert spec.entity_type == entity_type
        assert spec.label
        assert spec.label_field in {field.name for field in spec.fields}
        assert all(isinstance(field, FieldSpec) for field in spec.fields)


def test_reference_fields_name_the_entity_type_they_point_at() -> None:
    for spec in ENTITY_SPECS.values():
        for field in spec.fields:
            if field.kind in ("reference", "reference_list"):
                assert field.target in ENTITY_TYPES
