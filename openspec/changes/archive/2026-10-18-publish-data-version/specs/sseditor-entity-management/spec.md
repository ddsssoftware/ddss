# Spec Delta

## ADDED Requirements

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
