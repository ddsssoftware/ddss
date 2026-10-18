# Spec Delta

## MODIFIED Requirements

### Requirement: Enforce required relationships and field limits

SSEditor MUST enforce the data model's required relationships and length limits on save: a Condition SHALL reference at least one Symptom, a Symptom SHALL reference at least one Test, names SHALL NOT exceed 256 characters, descriptions SHALL NOT exceed 1024 characters, and Citation BibTeX and IEEE values SHALL NOT exceed 2048 characters.

#### Scenario: Condition without a symptom is rejected

- **WHEN** the administrator submits a Condition referencing no Symptom
- **THEN** SSEditor SHALL refuse the write and report the missing reference

#### Scenario: Symptom without a test is rejected

- **WHEN** the administrator submits a Symptom referencing no Test
- **THEN** SSEditor SHALL refuse the write and report the missing reference

#### Scenario: Over-long text is rejected

- **WHEN** the administrator submits a name or description exceeding its permitted length
- **THEN** SSEditor SHALL refuse the write and report the offending field

#### Scenario: Over-long citation text is rejected

- **WHEN** the administrator submits a Citation whose BibTeX or IEEE value exceeds 2048 characters
- **THEN** SSEditor SHALL refuse the write and report the offending field

#### Scenario: Citation text at the limit is accepted

- **WHEN** the administrator submits a valid Citation whose BibTeX and IEEE values are each exactly 2048 characters
- **THEN** SSEditor SHALL store the record

## ADDED Requirements

### Requirement: Validate a single BibTeX entry

The `bibtex` field of a Citation SHALL hold exactly one syntactically valid BibTeX entry with at least one field, where an author or editor counts as content. Line breaks between fields and within field values SHALL be accepted and preserved in the stored value. An invalid, empty, duplicated, or multi-entry value MUST be rejected with a message naming the problem.

#### Scenario: A multiline entry is accepted

- **WHEN** the administrator submits a valid BibTeX entry whose fields span multiple lines
- **THEN** SSEditor SHALL store the entry with its line breaks preserved

#### Scenario: A malformed entry is rejected

- **WHEN** the administrator submits a BibTeX value with an unclosed brace or another syntax error
- **THEN** SSEditor SHALL refuse the write and report the syntax problem

#### Scenario: Several entries are rejected

- **WHEN** the administrator submits more than one BibTeX entry in the `bibtex` field
- **THEN** SSEditor SHALL refuse the write and report that exactly one entry is required

#### Scenario: A duplicate entry key is rejected

- **WHEN** the administrator submits two entries that use the same citation key
- **THEN** SSEditor SHALL refuse the write and report the duplicate key

#### Scenario: An entry without content is rejected

- **WHEN** the administrator submits an entry that has no fields and no author or editor
- **THEN** SSEditor SHALL refuse the write and report that the entry has no content

### Requirement: Derive the IEEE citation on save

The `ieee` field of a Citation SHALL be derived from its `bibtex` value when the record is saved. On a new Citation, or when the BibTeX entry has changed, SSEditor SHALL replace `ieee` with the derived IEEE-style citation. When the BibTeX entry is unchanged, SSEditor SHALL keep the stored `ieee` value. When the stored `ieee` value is empty, SSEditor SHALL derive it even if the BibTeX entry is unchanged.

#### Scenario: A new citation derives its IEEE text

- **WHEN** the administrator saves a valid new Citation
- **THEN** SSEditor SHALL store the IEEE citation derived from its BibTeX entry

#### Scenario: Changed BibTeX re-derives the IEEE citation

- **WHEN** the administrator changes the BibTeX entry of a stored Citation and saves
- **THEN** SSEditor SHALL replace the stored IEEE citation with the value derived from the changed entry

#### Scenario: Unchanged BibTeX keeps the stored IEEE citation

- **WHEN** the administrator saves a stored Citation without changing its BibTeX entry
- **THEN** SSEditor SHALL keep the stored IEEE citation unchanged

#### Scenario: An empty stored IEEE citation is derived

- **WHEN** the administrator saves a Citation whose stored IEEE citation is empty and whose BibTeX entry is unchanged
- **THEN** SSEditor SHALL derive and store the IEEE citation

#### Scenario: Derivation failure blocks the write

- **WHEN** the BibTeX entry cannot be formatted as an IEEE citation
- **THEN** SSEditor SHALL refuse the write and report the derivation problem

#### Scenario: An unsupported entry type is formatted generically

- **WHEN** the administrator submits a valid BibTeX entry whose type SSEditor does not recognize
- **THEN** SSEditor SHALL derive an IEEE citation using a generic entry format instead of rejecting the entry type

### Requirement: Normalize the derived IEEE citation

The derived IEEE citation SHALL be a single line of ASCII text. The leading reference number SHALL be removed, runs of whitespace SHALL be collapsed to single spaces, typographic quotes and dashes SHALL be converted to their ASCII equivalents, and non-ASCII text SHALL be transliterated to ASCII.

#### Scenario: Multiline source produces one line

- **WHEN** SSEditor derives an IEEE citation from a multiline BibTeX entry
- **THEN** the stored IEEE citation SHALL be a single line with collapsed whitespace

#### Scenario: Typography is normalized

- **WHEN** the IEEE style produces curly quotes, an en dash, or another non-ASCII character
- **THEN** the stored IEEE citation SHALL contain the ASCII equivalent or a transliteration

#### Scenario: The reference number is removed

- **WHEN** the IEEE style produces a leading reference number such as `[1]`
- **THEN** the stored IEEE citation SHALL not contain that prefix

### Requirement: Make the IEEE field read-only

On the Citation detail screen, the `ieee` field SHALL be read-only. The administrator SHALL NOT be able to type, paste, or delete its contents, and the stored value SHALL come from the derivation rule rather than from the form.

#### Scenario: The IEEE field cannot be edited

- **WHEN** the administrator opens a Citation and attempts to edit the IEEE field
- **THEN** SSEditor SHALL ignore the edit and keep the field unchanged

#### Scenario: The displayed value is stored on save

- **WHEN** the administrator saves a Citation with a changed BibTeX entry
- **THEN** SSEditor SHALL store the derived IEEE value rather than the value shown before saving

### Requirement: Show the raw BibTeX entry in the citation list

The Citation list SHALL label each row with the raw stored BibTeX entry and SHALL use that raw text when matching a search term. A multiline entry SHALL remain multiline in the stored label and search text.

#### Scenario: Raw multiline BibTeX is shown

- **WHEN** the Citation list displays a record whose BibTeX entry spans multiple lines
- **THEN** SSEditor SHALL use the raw entry, including its line breaks, as that row's label

#### Scenario: Search matches the raw BibTeX text

- **WHEN** the administrator searches the Citation list with a term that appears in a record's raw BibTeX entry
- **THEN** SSEditor SHALL include that record in the narrowed list
