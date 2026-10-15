# Spec Delta

## Purpose

Provides the terminal-based administration workflow for the writable clinical entity types (Condition, Symptom, Test, and Citation), letting administrators list, search, add, edit, and delete records in the shared local JSON store while enforcing the data-integrity and content rules the diagnosis data depends on.

## ADDED Requirements

### Requirement: List and search records by entity type

SSEditor SHALL provide a list screen for each editable entity type (Condition, Symptom, Test, and Citation) that displays the records held in the data store and supports searching them.

#### Scenario: Stored records are listed

- **WHEN** the administrator opens the list screen for an entity type
- **THEN** SSEditor SHALL display every record of that type held in the data store

#### Scenario: Search narrows the list

- **WHEN** the administrator enters a search term on a list screen
- **THEN** SSEditor SHALL display only the records of that type matching the term

### Requirement: Add and edit entity records

SSEditor SHALL provide a detail screen per entity type that supports adding a new record and editing the details of an existing record of that type.

#### Scenario: New record is added

- **WHEN** the administrator submits a valid new record from the detail screen
- **THEN** SSEditor SHALL store the new record and make it visible on that type's list screen

#### Scenario: Existing record is edited

- **WHEN** the administrator opens an existing record and submits changed details
- **THEN** SSEditor SHALL store the changed details against that record's existing identifier

#### Scenario: Abandoned edits are discarded

- **WHEN** the administrator leaves the detail screen without submitting
- **THEN** SSEditor SHALL leave the stored records unchanged

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

SSEditor MUST enforce the data model's required relationships and length limits on save: a Condition SHALL reference at least one Symptom, a Symptom SHALL reference at least one Test, names SHALL NOT exceed 256 characters, and descriptions SHALL NOT exceed 1024 characters.

#### Scenario: Condition without a symptom is rejected

- **WHEN** the administrator submits a Condition referencing no Symptom
- **THEN** SSEditor SHALL refuse the write and report the missing reference

#### Scenario: Symptom without a test is rejected

- **WHEN** the administrator submits a Symptom referencing no Test
- **THEN** SSEditor SHALL refuse the write and report the missing reference

#### Scenario: Over-long text is rejected

- **WHEN** the administrator submits a name or description exceeding its permitted length
- **THEN** SSEditor SHALL refuse the write and report the offending field

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
