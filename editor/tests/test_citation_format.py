"""Tests for parsing, formatting, and validating one BibTeX citation."""

from __future__ import annotations

import pytest

from editor.models.citation_format import (
    CitationError,
    derive_ieee,
    format_ieee,
    normalize_ieee,
    parse_citation,
    validate_citation,
)

ARTICLE = """@article{smith2020,
  author = {Smith, John and Doe, Jane},
  title = {A multiline
            title example},
  journal = {Journal of Testing},
  year = {2020},
  volume = {12},
  number = {3},
  pages = {100--110},
  doi = {10.1000/xyz}
}"""


# -- parsing ---------------------------------------------------------------


def test_multiline_entry_parses_and_normalizes_field_whitespace() -> None:
    parsed = parse_citation(ARTICLE)

    assert parsed.key == "smith2020"
    assert 'title = "A multiline title example"' in parsed.bibtex
    assert "title example\n" not in parsed.bibtex


def test_an_empty_value_is_rejected() -> None:
    with pytest.raises(CitationError, match="exactly one BibTeX entry"):
        parse_citation("   ")


def test_plain_text_is_rejected() -> None:
    with pytest.raises(CitationError, match="exactly one BibTeX entry"):
        parse_citation("hello world")


def test_several_entries_are_rejected() -> None:
    with pytest.raises(CitationError, match="Exactly one BibTeX entry"):
        parse_citation("@misc{a, title={A}}\n@misc{b, title={B}}")


def test_duplicate_keys_are_rejected() -> None:
    with pytest.raises(CitationError, match="repeated bibliography entry"):
        parse_citation("@misc{a, title={A}}\n@misc{a, title={B}}")


def test_unclosed_brace_is_rejected() -> None:
    with pytest.raises(CitationError, match="premature end of file"):
        parse_citation("@misc{a, title={A}")


def test_entry_without_content_is_rejected() -> None:
    with pytest.raises(CitationError, match="at least one field or person"):
        parse_citation("@misc{empty}")


# -- formatting ------------------------------------------------------------


def test_an_article_is_formatted_with_ieee_fields() -> None:
    formatted = format_ieee(parse_citation(ARTICLE))

    assert "J. Smith and J. Doe" in formatted
    assert "Journal of Testing" in formatted
    assert "vol. 12" in formatted
    assert "no. 3" in formatted
    assert "pp. 100" in formatted
    assert "doi: 10.1000/xyz" in formatted


def test_a_misc_entry_is_formatted() -> None:
    formatted = format_ieee(
        parse_citation(
            "@misc{ref, title={Primary care reference collection}}"
        )
    )

    assert "Primary care reference collection" in formatted


def test_an_unknown_entry_type_is_formatted_generically() -> None:
    formatted = format_ieee(
        parse_citation(
            "@software{tool, author={Doe, Jane}, title={A Tool}, year={2024}}"
        )
    )

    assert "J. Doe" in formatted
    assert "A Tool" in formatted
    assert "2024" in formatted


def test_a_url_is_kept_in_the_formatted_citation() -> None:
    formatted = format_ieee(
        parse_citation(
            "@misc{web, author={Doe, Jane}, title={Online}, year={2024}, "
            "url={https://example.org/x}}"
        )
    )

    assert "[Online]. Available: https://example.org/x" in formatted


# -- normalization ---------------------------------------------------------


def test_derive_removes_the_reference_number_and_collapses_whitespace() -> None:
    derived = derive_ieee(ARTICLE)

    assert derived.startswith("J. Smith and J. Doe")
    assert "[1]" not in derived
    assert "\n" not in derived


def test_derive_normalizes_typography_to_ascii() -> None:
    derived = derive_ieee(
        "@article{k, author={Doe, Jane}, title={An -- Example}, "
        "journal={J}, year={2020}}"
    )

    assert derived.isascii()
    assert '"An - Example"' in derived


def test_derive_transliterates_non_ascii_text() -> None:
    derived = derive_ieee(
        "@article{m, author={Müller, Jürgen}, title={Über Café}, "
        "journal={J}, year={2020}}"
    )

    assert derived.isascii()
    assert "Muller" in derived
    assert "Uber Cafe" in derived


def test_normalize_ieee_is_idempotent() -> None:
    once = normalize_ieee('[1]  “An   example”. ')
    twice = normalize_ieee(once)

    assert once == twice == '"An example".'


# -- validation ------------------------------------------------------------


@pytest.mark.parametrize(
    "value",
    [
        "",
        "hello world",
        "@misc{a, title={A}}\n@misc{b, title={B}}",
        "@misc{a, title={A}}\n@misc{a, title={B}}",
        "@misc{a, title={A}",
        "@misc{empty}",
    ],
)
def test_validate_citation_reports_every_invalid_shape(value: str) -> None:
    message = validate_citation(value)

    assert message is not None
    assert message


def test_validate_citation_accepts_a_valid_entry() -> None:
    assert validate_citation(ARTICLE) is None
