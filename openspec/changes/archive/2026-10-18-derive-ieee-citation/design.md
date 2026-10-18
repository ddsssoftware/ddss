# Design

## Context

See `proposal.md` for motivation. The current citation detail screen is built
from `EntitySpec`/`FieldSpec` in `editor/models/fields.py`: both `bibtex` and
`ieee` are editable `long_text` fields. `EntityDetailController._build` copies
both values into `Citation`, and `EditorModel.save` is the only writer. The
validator has no BibTeX rules, and `Citation.label_field` is `bibtex`, so the
raw entry is already the list label and search text.

The relevant constraints are the three-layer split (models cannot import
Textual), the single-owner validator convention, the 95% coverage gate, and the
existing JSON data contract in `public/data/citations.json`.

## Goals / Non-Goals

**Goals:**

- Validate one BibTeX entry per Citation and accept multiline entries.
- Derive `ieee` from `bibtex` on save, without live preview.
- Keep hand-authored `ieee` values until their BibTeX entry changes.
- Keep parsing and formatting in the model layer, behind a small pure interface.
- Preserve the existing list behaviour: raw BibTeX is the label and search text.

**Non-Goals:**

- Live preview of the IEEE citation while typing.
- Bulk migration of stored `ieee` values.
- Editing individual IEEE citation parts.
- Supporting a full BibTeX bibliography or multiple entries per record.
- Changing DDClient or the shape of `citations.json`.

## Decisions

### Parsing and validation: `pybtex`

Use `pybtex.database.parse_string(text, bib_format="bibtex")` for parsing and
validation. It raises clear errors with line numbers (`PrematureEOF`,
`BibliographyDataError`), and it normalizes multiline field values to single
spaces when the entry is serialized back to canonical BibTeX. That
normalization is the first stage of the whitespace-collapse requirement.

Validation requires:

- exactly one entry;
- at least one field, or at least one person in `author`/`editor`;
- no parse error, including duplicate keys and unclosed braces.

`bibtexparser` was the other candidate. It has a useful fault-tolerant
`failed_blocks` model, but it preserves raw newlines inside field values, so a
second normalization pass would still be needed. `pybtex` covers both parsing
and canonicalization in one library.

### IEEE formatting: `citeproc-py[full]`

Use `citeproc.source.bibtex.BibTeX` and the IEEE CSL style. The `full` extra
installs `citeproc-py-styles`, which contains `ieee.csl`; the alternative of
vendoring one 18 KB style file was rejected because the user chose the full
dependency set, and the styles package avoids maintaining a copied,
CC BY-SA-licensed asset.

Two adjustments are needed around the citeproc source:

- **Unknown entry types** must not be rejected. Subclass `BibTeX` and make
  `types` a `defaultdict(lambda: ARTICLE, BibTeX.types)`, so an unrecognized
  type falls back to the generic article format.
- **Field coverage.** Extend the `fields` map with `url -> URL` and map
  `school`, `institution`, and `organization` to `publisher`, so common BibTeX
  data is not silently dropped. Suppress citeproc's `UserWarning` for any
  remaining unsupported fields so warnings cannot corrupt the terminal UI.

### ASCII transliteration: `anyascii`

Use `anyascii` after formatting. It is ISC-licensed, covers Latin accents and
non-Latin scripts, and avoids the GPL-2.0-or-later license of `Unidecode`.
Transliteration is best-effort; see Risks.

### Derivation policy: save-only, keep until changed

`EditorModel.save` owns the policy because it already receives `existing` and is
the only writer:

```
new citation                         -> derive
existing + bibtex changed            -> derive
existing + bibtex unchanged + ieee   -> keep existing.ieee
existing + bibtex unchanged + no ieee-> derive
```

"Changed" compares `candidate.bibtex.strip()` with
`(existing.bibtex or "").strip()`, matching what the form does. Derivation runs
before validation so the derived `ieee` is also checked against the length
limit.

If derivation raises, the model leaves `ieee` empty and the validator reports
the blocking `bibtex-invalid` violation. The validator and the model share the
same pure functions from `citation_format.py`; the small duplicate parse per
save is acceptable (measured at roughly 10 ms).

### Pure formatting module

Create `editor/models/citation_format.py` with no Textual imports:

- `parse_citation(text)` -> one pybtex entry, raising `CitationError`;
- `format_ieee(entry)` -> normalized ASCII IEEE text;
- `derive_ieee(text)` -> parse, canonicalize, format, normalize;
- `validate_citation(text)` -> the same checks expressed as a violation message
  or `None`.

Normalization order:

1. strip a leading `[n]` reference number;
2. `anyascii` transliteration (which also converts curly quotes and dashes);
3. collapse all whitespace runs to one space and trim.

### Read-only field

Add `read_only: bool = False` to `FieldSpec`. The citation spec sets it on
`ieee`. `EntityDetailView._field_widget` renders a read-only `TextArea` when the
flag is set. `EntityDetailController._build` ignores `values["ieee"]`, so the
form can never supply the stored value. `initial_values()` still shows the
stored `ieee` for an existing record. There is no live refresh; a new record's
field stays blank until Save succeeds and the screen closes.

### Citation length limit

Add `CITATION_MAX_LENGTH = 2048` in `editor/models/rules.py`. Keep
`TEXT_MAX_LENGTH = 1024` for descriptions. `fields_must_fit` uses the new
constant for `Citation.bibtex` and `Citation.ieee` only. Update the data-model
documentation and the existing boundary tests from 1024/1025 to 2048/2049.

### List label

No change. `Citation.label_field` remains `bibtex`, so rows and search use the
raw entry, including line breaks.

```
Citation detail screen

  bibtex TextArea (editable) --.
                               |  Save
                               v
                    EntityDetailController._build
                    (ignores ieee from the form)
                               |
                               v
                      EditorModel.save
                        |            \
                 derive?             keep existing?
                        |                    |
                        v                    v
                 citation_format        existing.ieee
                 (pybtex -> citeproc -> anyascii -> normalize)
                        |
                        v
                  Validator.validate
                  (bibtex-invalid, field-too-long, ...)
                        |
                        v
                  persist citations.json
```

## Risks / Trade-offs

- **Large dependency** → `citeproc-py-styles` adds roughly 89 MB installed.
  Accepted by the "add all" decision. The alternative, one vendored
  `ieee.csl`, would cut this to about 19 MB but adds a CC BY-SA asset to
  maintain.
- **Transliteration quality** → `anyascii` is context-free. Latin accents map
  well; Chinese/Japanese/Korean names become romanized approximations. This is
  the accepted cost of an ASCII citation.
- **Derived IEEE can exceed 2048** → a BibTeX entry within the limit can
  produce an IEEE string over it, blocking the save. The violation must name
  the `ieee` field and make clear that shortening the BibTeX entry is the way
  to fix it.
- **Citeproc field gaps** → its BibTeX bridge does not know every field. The
  extended map covers common cases, but some fields (for example `keywords`)
  are ignored. Suppressing warnings keeps the UI clean but hides the omission;
  the tests should cover the fields we claim to support.
- **Save-only UX** → a new citation shows a blank read-only IEEE field until
  Save. That is the chosen trade-off; no live preview is added.
- **Multiline list rows** → raw BibTeX labels become tall rows. Accepted
  explicitly.
- **Existing hand-authored values** → the fixture's IEEE text is preserved
  until its BibTeX changes. There is no global data migration.

## Migration Plan

No data migration. Existing citation records keep their stored `ieee` value;
the next save that changes `bibtex` replaces it with the derived value. Deploy
by installing the new dependencies and restarting the editor. Rollback restores
the previous editor version; the JSON data remains valid because no schema
changed.

## Open Questions

None. The remaining choices were resolved during exploration.
