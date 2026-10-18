# Tasks

## 1. Dependencies

- [x] 1.1 Add `pybtex>=0.26`, `citeproc-py[full]>=0.11`, and `anyascii>=0.3.3` to `pyproject.toml`, install them into `.venv`, and verify `python -c "import pybtex, citeproc, anyascii"` succeeds.

## 2. Citation parsing and formatting

- [x] 2.1 Create `editor/models/citation_format.py` with `CitationError`, `parse_citation`, and canonical single-entry serialization; verify with tests that a multiline entry parses, duplicate keys and unclosed braces raise, and multiple entries are rejected.
- [x] 2.2 Implement `format_ieee` with a citeproc BibTeX source subclass that maps unknown entry types to the generic article type, extends the field map with `url`, `school`, `institution`, and `organization`, and suppresses citeproc warnings; verify tests cover an article, a `misc` entry, an unknown entry type, and a `url` field.
- [x] 2.3 Implement `derive_ieee` normalization: strip the leading reference number, transliterate with `anyascii`, collapse whitespace, and trim; verify tests cover a multiline title, curly quotes, an en dash, a non-Latin name, and a leading `[1]`.
- [x] 2.4 Add `validate_citation` returning a violation message for empty, malformed, multi-entry, duplicate-key, and no-content values; verify each case has a test.
- [x] 2.5 Confirm `editor/tests/test_layering.py` still passes, so the new model module does not import Textual.

## 3. Validation rules and limits

- [x] 3.1 Add `CITATION_MAX_LENGTH = 2048` in `editor/models/rules.py` and use it for `Citation.bibtex` and `Citation.ieee` only; verify tests accept 2048 characters and reject 2049 for both fields.
- [x] 3.2 Add the blocking `bibtex-invalid` rule for `Citation` using `validate_citation`; verify tests cover malformed, multi-entry, duplicate-key, and no-content entries and that valid entries pass.
- [x] 3.3 Update the existing over-long citation test from 1025 to 2049 and add the 2048 boundary case; verify the full rules test module passes.
- [x] 3.4 Update the Citation limits in `openspec/project.md` and the rule documentation in `editor/README.md`; verify the documents say 2048 for `bibtex` and `ieee` and 1024 for descriptions.

## 4. Model derivation

- [x] 4.1 Implement the save policy in `EditorModel.save`: derive for a new Citation or a changed `bibtex`, keep `existing.ieee` when `bibtex` is unchanged, and derive when the stored `ieee` is empty; verify each branch has a model test.
- [x] 4.2 Run derivation before validation so the derived `ieee` is covered by the 2048 limit, and verify a test where a long derived citation blocks the save while the BibTeX remains within its limit.
- [x] 4.3 Verify a derivation failure leaves `ieee` empty and returns a blocking `bibtex-invalid` violation without changing the stored collections.

## 5. Read-only detail field

- [x] 5.1 Add `read_only: bool = False` to `FieldSpec`, set it on the Citation `ieee` field, and render that field as a read-only `TextArea`; verify a view test asserts `read_only` is true and that the BibTeX field remains editable.
- [x] 5.2 Make `EntityDetailController._build` ignore the form's `ieee` value; verify a controller test supplies one `ieee` value in the form and confirms the stored value comes from derivation.
- [x] 5.3 Confirm `initial_values()` still shows the stored `ieee` for an existing Citation and an empty value for a new one; verify both cases in a view or controller test.

## 6. Integration

- [x] 6.1 Add an end-to-end view test that saves a multiline BibTeX entry, then verify the stored `bibtex` keeps its line breaks, the stored `ieee` is a single ASCII line, and the citation list shows the raw multiline label.
- [x] 6.2 Run `.venv/bin/python -m pytest -q` and verify every test passes with the 95% coverage gate.
- [x] 6.3 Run `openspec validate "derive-ieee-citation" --strict` and verify it passes.

## Workflow follow-up

- Archive the change after the project's review requirements are satisfied.
- Verify the archived result.
