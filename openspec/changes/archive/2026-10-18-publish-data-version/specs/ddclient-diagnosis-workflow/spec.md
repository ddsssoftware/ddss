# Spec Delta

## ADDED Requirements

### Requirement: Cache clinical collections for offline use

After a successful load, DDClient SHALL retain the condition, symptom, test, and citation collections so that the diagnosis workflow can start without network access.

#### Scenario: A successful load is retained

- **WHEN** the four collections load and validate successfully
- **THEN** DDClient SHALL retain all four for use while offline

#### Scenario: Retained collections start the workflow offline

- **WHEN** the device is offline and the collections were retained by an earlier successful load
- **THEN** DDClient SHALL load the retained collections and make the diagnosis workflow available

#### Scenario: Nothing retained and offline

- **WHEN** the device is offline and no collection was retained
- **THEN** DDClient SHALL show the data-unavailable state and SHALL NOT fabricate clinical data

### Requirement: Revalidate retained collections against the published version

On startup, DDClient SHALL compare the published data version with the version it last served and, when they differ, SHALL load the collections from the server rather than from its retained copies.

#### Scenario: A new version replaces the retained collections

- **WHEN** the published version differs from the last version DDClient served
- **THEN** DDClient SHALL load all four collections from the server and serve those instead of the retained copies

#### Scenario: An unchanged version uses the retained collections

- **WHEN** the published version equals the last version DDClient served
- **THEN** DDClient SHALL serve the retained collections without loading them from the server

#### Scenario: A changed version is recorded only after a full load

- **WHEN** the published version differs and a collection cannot be loaded
- **THEN** DDClient SHALL show the data-unavailable state and SHALL NOT record that version as served

#### Scenario: An absent or unreadable version is not a data error

- **WHEN** the version marker is absent, unreachable, or unreadable
- **THEN** DDClient SHALL load the collections without treating the marker as a data error
