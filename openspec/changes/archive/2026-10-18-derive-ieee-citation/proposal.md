# Proposal

## Why

Citation records currently accept any text in the BibTeX field and require the
administrator to hand-author the IEEE citation alongside it. Nothing verifies
that the BibTeX entry is valid, the two fields can drift apart, and multiline
entries have no test coverage. The editor should validate a single BibTeX entry
and derive the IEEE citation from it, so every stored citation has a
trustworthy and consistent representation.

## What Changes

- Validate `bibtex` as exactly one syntactically valid BibTeX entry with at
  least one field or person, and accept multiline entries.
- Make the `ieee` field read-only on the citation detail screen.
- Derive `ieee` on save from `bibtex` using the IEEE CSL style.
- Keep the stored `ieee` when `bibtex` is unchanged; re-derive when `bibtex`
  changes or when the stored `ieee` is empty.
- Normalize derived IEEE text: strip the leading `[n]`, collapse whitespace,
  and transliterate to ASCII.
- Map unsupported BibTeX entry types to a generic formattable type instead of
  rejecting them.
- Raise the citation text limit from 1024 to 2048 characters for `bibtex` and
  `ieee`; descriptions stay at 1024.
- Keep the raw BibTeX entry as the citation list label and search text.
- **BREAKING**: `ieee` is no longer authored by the administrator and changes
  automatically when the BibTeX entry changes.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `sseditor-entity-management`: citation validation, read-only derived IEEE
  field, multiline BibTeX support, and the citation field length limit.

## Impact

- New `editor/models/citation_format.py`: BibTeX parsing, validation,
  canonicalization, IEEE formatting, and ASCII normalization.
- Updated `editor/models/{fields,rules,editor_model}.py`,
  `editor/controllers/entity_detail.py`, and `editor/views/detail.py`.
- New dependencies: `pybtex`, `citeproc-py[full]`, and `anyascii`.
- Updated `openspec/project.md`, `editor/README.md`, and the citation tests.
- Runtime cost: the full `citeproc-py-styles` package (~107 MB installed) and a
  small per-save formatting cost.
