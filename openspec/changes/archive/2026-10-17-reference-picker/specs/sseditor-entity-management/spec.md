# Spec Delta

## MODIFIED Requirements

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

## ADDED Requirements

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
