# sseditor-entity-management Specification

## Purpose

Provides the terminal-based administration workflow for the writable clinical entity types (Condition, Symptom, Test, and Citation), letting administrators list, search, add, edit, and delete records in the shared local JSON store while enforcing the data-integrity and content rules the diagnosis data depends on.

## Requirements

### Requirement: List and search records by entity type

SSEditor SHALL provide a list screen for each editable entity type (Condition, Symptom, Test, and Citation) that displays the records held in the data store and supports searching them by name or by any of their alternative names.

#### Scenario: Stored records are listed

- **WHEN** the administrator opens the list screen for an entity type
- **THEN** SSEditor SHALL display every record of that type held in the data store

#### Scenario: Search narrows the list

- **WHEN** the administrator enters a search term on a list screen
- **THEN** SSEditor SHALL display only the records of that type matching the term

#### Scenario: Search matches an alternative name

- **WHEN** the administrator enters a search term that appears in a record's alternative-name list but not in its name
- **THEN** SSEditor SHALL display that record in the narrowed list

#### Scenario: Rows display the record name

- **WHEN** a list screen displays a record that matched by an alternative name
- **THEN** SSEditor SHALL display that record's name, without the alternative name

### Requirement: Add and edit entity records

SSEditor SHALL provide a detail screen per entity type that supports adding a new record and editing the details of an existing record of that type. Fields that reference other records SHALL be edited by attaching and detaching stored records rather than by typing identifiers.

#### Scenario: New record is added

- **WHEN** the administrator submits a valid new record from the detail screen
- **THEN** SSEditor SHALL store the new record and make it visible on that type's list screen

#### Scenario: Existing record is edited

- **WHEN** the administrator opens an existing record and submits changed details
- **THEN** SSEditor SHALL store the changed details against that record's existing identifier

#### Scenario: Abandoned edits are discarded

- **WHEN** the administrator leaves the detail screen without submitting
- **THEN** SSEditor SHALL leave the stored records unchanged

#### Scenario: Attached references are saved

- **WHEN** the administrator attaches one or more referenced records and submits a valid record
- **THEN** SSEditor SHALL store that record's reference field as the identifiers of the attached records

#### Scenario: Detached references are not saved

- **WHEN** the administrator detaches a previously attached referenced record and submits a valid record
- **THEN** SSEditor SHALL store the reference field without that record's identifier

#### Scenario: Attached references are shown with name and identifier

- **WHEN** a detail screen displays a record that has attached references
- **THEN** SSEditor SHALL display one entry per attached reference showing that record's name and identifier, with an action to open it and an action to remove it

#### Scenario: A referenced record is opened and the form returns unchanged

- **WHEN** the administrator opens an attached reference and then returns to the detail screen
- **THEN** SSEditor SHALL show the detail screen again with its unsubmitted edits intact and the referenced record's current name

#### Scenario: An unresolvable stored reference is handled

- **WHEN** a stored record holds a reference whose identifier matches no record in the referenced collection
- **THEN** SSEditor SHALL display that reference without a name, offer to remove it but not to open it, and continue to refuse submitting until no unresolvable reference remains

### Requirement: Choose referenced records from the stored collection

When attaching references, SSEditor SHALL offer only records already held in the referenced entity's collection and SHALL let the administrator narrow the offer by name or by any alternative name. The administrator SHALL be able to attach more than one record at a time.

#### Scenario: Only stored records are offered

- **WHEN** the administrator opens the chooser for a reference field
- **THEN** SSEditor SHALL offer the records of the referenced entity type held in the data store and SHALL NOT offer to create a new record

#### Scenario: Already attached records are not offered

- **WHEN** the administrator opens the chooser for a reference field that already has attached records
- **THEN** SSEditor SHALL NOT offer the already attached records

#### Scenario: Search matches a name

- **WHEN** the administrator narrows the chooser with a term that appears in a record's name
- **THEN** SSEditor SHALL offer that record labelled with its name alone

#### Scenario: Search matches an alternative name

- **WHEN** the administrator narrows the chooser with a term that appears in a record's alternative-name list but not in its name
- **THEN** SSEditor SHALL offer that record labelled with its name followed by the matching alternative name

#### Scenario: Several records are attached at once

- **WHEN** the administrator ticks several offered records and confirms
- **THEN** SSEditor SHALL attach every ticked record to the reference field

#### Scenario: Ticked records survive a changed search

- **WHEN** the administrator ticks a record and then changes the search term so that record is no longer offered
- **THEN** SSEditor SHALL keep that record ticked and SHALL attach it on confirmation

### Requirement: Generate 32-character hexadecimal identifiers

Every newly created record SHALL receive a randomly generated 128-bit identifier rendered as 32 lowercase hexadecimal characters. An identifier SHALL NOT change once the record is stored.

#### Scenario: New record receives a hexadecimal identifier

- **WHEN** the administrator creates a new record
- **THEN** SSEditor SHALL assign it an identifier of 32 lowercase hexadecimal characters

#### Scenario: Identifier survives an edit

- **WHEN** the administrator changes the details of an existing record
- **THEN** SSEditor SHALL keep that record's original identifier

### Requirement: Keep identifiers unique across entity types

SSEditor MUST reject any write that would store an identifier already held by a record of any editable entity type, and SHALL report the conflict.

#### Scenario: Duplicate identifier is rejected

- **WHEN** a write would store an identifier already used by another record of any editable type
- **THEN** SSEditor SHALL refuse the write, keep the stored records unchanged, and report the conflicting identifier

### Requirement: Reject unknown references

SSEditor MUST reject any write containing a reference to an identifier that does not exist in the referenced entity's collection, and SHALL name the unresolvable reference.

#### Scenario: Unknown referenced record is rejected

- **WHEN** the administrator submits a record referencing an identifier absent from the referenced collection
- **THEN** SSEditor SHALL refuse the write and report the unresolvable reference

#### Scenario: Known references are accepted

- **WHEN** the administrator submits a record whose references all resolve
- **THEN** SSEditor SHALL store the record

### Requirement: Refuse deletion of referenced records

When a deletion is requested for a record that another record still references, SSEditor MUST refuse the deletion and SHALL report the referencing records.

#### Scenario: Referenced record is not deleted

- **WHEN** the administrator requests deletion of a record referenced by another record
- **THEN** SSEditor SHALL keep the record and display the records that reference it

#### Scenario: Unreferenced record is deleted

- **WHEN** the administrator requests deletion of a record that no other record references
- **THEN** SSEditor SHALL remove the record from the data store

### Requirement: Enforce unique names within an entity type

Within a single entity type, the name SHALL be unique: SSEditor MUST reject a write whose name equals the name of a different record of the same type.

#### Scenario: Duplicate name is rejected

- **WHEN** the administrator submits a name already used by a different record of the same type
- **THEN** SSEditor SHALL refuse the write and report the conflict

### Requirement: Require title-cased names and alternative names

A record's name and every entry of its alternative-name list SHALL be title cased, meaning each word is capitalized except minor words such as articles, conjunctions, and short prepositions, with the first and last word always capitalized. A write that would store a value which is not title cased MUST be blocked until the value is corrected.

#### Scenario: Non-title-cased value blocks saving

- **WHEN** the administrator submits a name or alternative name that is not title cased
- **THEN** SSEditor SHALL block the write and warn that the value must be corrected

#### Scenario: Corrected value is accepted

- **WHEN** the administrator corrects the value to its title-cased form and submits again
- **THEN** SSEditor SHALL store the record

### Requirement: Reject alternative names that clash with names

An entry of a record's alternative-name list MUST NOT equal the name of that record or of any other record of the same entity type.

#### Scenario: Alternative name matching another record's name is rejected

- **WHEN** the administrator submits an alternative name equal to the name of another record of the same type
- **THEN** SSEditor SHALL refuse the write and report the clash

#### Scenario: Alternative name matching the record's own name is rejected

- **WHEN** the administrator submits an alternative name equal to that record's own name
- **THEN** SSEditor SHALL refuse the write and report the clash

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

### Requirement: Persist edits to the shared JSON store

SSEditor SHALL persist each accepted write directly to that entity type's collection file in the shared data directory (the same files the client reads), keeping every collection a valid JSON array and preserving unrelated records.

#### Scenario: Accepted write reaches the collection file

- **WHEN** an accepted write is made for an entity type
- **THEN** that type's collection file SHALL contain the change and remain a valid JSON array

#### Scenario: Other records are preserved

- **WHEN** a record is added, edited, or deleted
- **THEN** SSEditor SHALL leave every other record in the store unchanged

### Requirement: Ignore collections SSEditor does not own

SSEditor SHALL NOT read, validate, migrate, or write the client-only collections (the case collection and the condition, symptom, and test entry collections), and SHALL remain fully operable when those files are absent.

#### Scenario: Editor works without the unowned files

- **WHEN** the client-only collection files are missing or invalid
- **THEN** SSEditor SHALL list, edit, and delete records of the editable types without error

#### Scenario: Unowned files are left untouched

- **WHEN** any write or migration is performed
- **THEN** SSEditor SHALL leave the client-only collection files unchanged

### Requirement: Bring existing records into the required format

The change SHALL bring the records already held in the editable collections into the required format: every identifier replaced by a 32-character hexadecimal identifier, every name and alternative name title cased, and a missing alternative-name list set to an empty list. References among the migrated records SHALL remain resolvable.

#### Scenario: Identifiers are replaced

- **WHEN** the migration completes for the editable collections
- **THEN** every stored record SHALL hold a 32-character hexadecimal identifier

#### Scenario: Names are normalized

- **WHEN** the migration completes
- **THEN** every name and alternative name SHALL be title cased, and every record lacking an alternative-name list SHALL hold an empty list

#### Scenario: References still resolve after migration

- **WHEN** the migration has rewritten the identifiers
- **THEN** every reference held by a migrated record SHALL resolve to a record in the referenced collection

### Requirement: Publish a data version with each accepted write

SSEditor SHALL create or overwrite a version marker named `version.json` in the data directory on every accepted write, holding the time of that write as an ISO 8601 UTC timestamp.

#### Scenario: An accepted addition publishes a version

- **WHEN** the administrator submits a valid new record
- **THEN** SSEditor SHALL store the record and write the version marker holding the current UTC time in ISO 8601 form

#### Scenario: An accepted edit publishes a version

- **WHEN** the administrator submits valid changes to an existing record
- **THEN** SSEditor SHALL store the changes and overwrite the version marker with the current UTC time

#### Scenario: An accepted deletion publishes a version

- **WHEN** the administrator deletes a record that no other record references
- **THEN** SSEditor SHALL remove the record and overwrite the version marker with the current UTC time

#### Scenario: A rejected write leaves the version unchanged

- **WHEN** a write is refused because it violates a data rule
- **THEN** SSEditor SHALL leave the version marker and the collections unchanged

### Requirement: Publish the data version after the collection

SSEditor SHALL write the version marker only after the collection file it accompanies has been replaced, so that a reader observing a new version always finds the collection that version describes.

#### Scenario: A reader observing a new version sees the new data

- **WHEN** the version marker holds a timestamp newer than the one a reader last saw
- **THEN** the collection file SHALL already contain the write that produced that timestamp

### Requirement: Keep a version failure from failing the write

A failure to write the version marker SHALL NOT change the outcome of an accepted write, SHALL NOT raise an error to the administrator, and SHALL leave the stored record in place.

#### Scenario: The marker cannot be written

- **WHEN** the collection file is written successfully and the version marker cannot be written
- **THEN** SSEditor SHALL keep the stored record, SHALL report the write as accepted, and SHALL attempt the marker again on the next accepted write

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
