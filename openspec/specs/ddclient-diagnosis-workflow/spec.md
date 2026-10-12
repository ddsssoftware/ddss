# ddclient-diagnosis-workflow Specification

## Purpose

Provides a browser-based workflow for clinicians to describe a patient case, review data-driven differential diagnoses, and refine the results by recording symptom findings. The capability is usable as a static PWA without a server-side session.

## Requirements

### Requirement: Start a case from a presentation description

DDClient SHALL allow a clinician to enter a case description and start a diagnosis session without submitting data to a remote service.

#### Scenario: Valid case description starts diagnosis

- **WHEN** the clinician enters a non-empty case description and starts the diagnosis
- **THEN** DDClient SHALL create an in-session case and display the initial diagnosis view

#### Scenario: Empty case description is rejected

- **WHEN** the clinician attempts to start a diagnosis with an empty or whitespace-only description
- **THEN** DDClient SHALL keep the case-entry view active and display an actionable validation message

### Requirement: Present available symptoms for case findings

DDClient SHALL display available symptoms from the loaded symptom data and allow each symptom to be marked present, absent, or not yet assessed.

#### Scenario: Clinician records a symptom finding

- **WHEN** the clinician marks an available symptom as present or absent
- **THEN** DDClient SHALL visibly preserve that finding and make it available to the results refinement

#### Scenario: No finding is selected

- **WHEN** the clinician has not marked any symptom present or absent
- **THEN** DDClient SHALL still display the initial diagnosis results and SHALL NOT treat unassessed symptoms as absent

### Requirement: Rank and display differential diagnoses

DDClient SHALL display conditions related to the current case and sort them deterministically by matching present symptoms, then condition priority, then condition name.

#### Scenario: Initial results are displayed

- **WHEN** a valid case is started and condition and symptom data is available
- **THEN** DDClient SHALL display each applicable condition with its name, description, and related symptom findings

#### Scenario: Findings refine results

- **WHEN** the clinician changes a symptom finding
- **THEN** DDClient SHALL recalculate and display the ranked condition list without losing the case description or other recorded findings

#### Scenario: No condition matches

- **WHEN** the recorded findings produce no applicable condition
- **THEN** DDClient SHALL display an explicit no-matching-diagnosis state and allow the clinician to revise findings

### Requirement: Load and validate clinical data locally

DDClient SHALL load the condition, symptom, test, and citation collections from the local JSON data directory and SHALL not silently substitute fabricated clinical data when loading fails or data is invalid.

#### Scenario: Data loads successfully

- **WHEN** the local entity collections are valid JSON with the required identifiers and references
- **THEN** DDClient SHALL make the diagnosis workflow available using those collections

#### Scenario: Data loading fails

- **WHEN** an entity file cannot be fetched, parsed, or referenced consistently
- **THEN** DDClient SHALL show a visible error explaining that diagnosis data is unavailable and SHALL prevent misleading diagnosis results

### Requirement: Support the diagnosis workflow as an installable PWA

DDClient SHALL expose the diagnosis shell through the existing static PWA entry point and SHALL cache the assets required to reopen the shell offline after a successful first load.

#### Scenario: Application shell opens

- **WHEN** a clinician opens the PWA entry point in a supported browser
- **THEN** DDClient SHALL render the case-entry or active diagnosis view without requiring a server-side application runtime

#### Scenario: Cached shell is reopened offline

- **WHEN** the shell and its declared assets were previously loaded and the browser is offline
- **THEN** the service worker SHALL serve the cached shell assets and the application SHALL communicate any unavailable uncached clinical data
