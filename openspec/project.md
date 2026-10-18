# Differential Diagnosis Support Systems

DDSS (Differential Diagnosis Support Systems) is a system that allows medical doctors to perform differential diagnosis on patients's presentation.

It is composes of two modules:

- DDClient: allows doctors to perform the diagnosis
- SSEditor: allows system administrators to edit the data

## Data model

The system has 8 entities: "Condition", "Symptom", "Test", "ConditionEntry", "SymptomEntry", "TestEntry", "Case", "Citation".

Each entity is stored as array of objets in a separate JSON in `public\data` folder.

### Condition

Condition that can be assigned to patient's presentation.

| Field    | Type            | Description                          | Other                        |
| -------- | --------------- | ------------------------------------ | ---------------------------- |
| id       | uuid            | Unique identifier                    | Required                     |
| name     | string          | The name of the condition            | Required. Max 256 chars      |
| aka      | array of string | Alternative names for this condition | Required. Default empty list |
| desc     | string          | A description of the condition       | Required. Max 1024 chars     |
| symptoms | array of uuid   | List of related symptoms             | Required. Min 1 symptom      |
| priority | int             | Indicates the priority               | Required                     |
| citation | uuid            | Citation for the source of this data | Required                     |

### Symptom

A sign or description of abnormal clinical presentation

| Field    | Type            | Description                              | Other                        |
| -------- | --------------- | ---------------------------------------- | ---------------------------- |
| id       | uuid            | Unique identifier                        | Required                     |
| name     | string          | The name of the symptom                  | Required. Max 256 chars      |
| aka      | array of string | Alternative names for this symptom       | Required. Default empty list |
| desc     | string          | A description of the symptom             | Required. Max 1024 chars     |
| tests    | array of uuid   | List of tests used to check this symptom | Required. Min 1 test         |
| citation | uuid            | Citation for the source of this data     | Required                     |

### Test

A procedure used to test a symptom.

| Field    | Type            | Description                          | Other                        |
| -------- | --------------- | ------------------------------------ | ---------------------------- |
| id       | uuid            | Unique identifier                    | Required                     |
| name     | string          | The name of the condition            | Required. Max 256 chars      |
| aka      | array of string | Alternative names for this test      | Required. Default empty list |
| desc     | string          | A description of the condition       | Required. Max 1024 chars     |
| citation | uuid            | Citation for the source of this data | Required                     |

### ConditionEntry

Binds a Condition to a Case.

| Field     | Type    | Description                                      | Other                    |
| --------- | ------- | ------------------------------------------------ | ------------------------ |
| id        | uuid    | Unique identifier                                | Required                 |
| condition | id      | The uuid of the related of the condition         | Required                 |
| present   | boolean | True if present, false if absent                 | Required                 |
| desc      | string  | A description about the condition's presentation | Required. Max 1024 chars |

### SymptomEntry

Binds a Symptom to a Case.

| Field   | Type    | Description                                    | Other                    |
| ------- | ------- | ---------------------------------------------- | ------------------------ |
| id      | uuid    | Unique identifier                              | Required                 |
| symptom | id      | The uuid of the related of the symptom         | Required                 |
| present | boolean | True if present, false if absent               | Required                 |
| desc    | string  | A description about the symptom's presentation | Required. Max 1024 chars |

### TestEntry

Binds a Test to a Case.

| Field   | Type    | Description                                 | Other                    |
| ------- | ------- | ------------------------------------------- | ------------------------ |
| id      | uuid    | Unique identifier                           | Required                 |
| test    | id      | The uuid of the related of the test         | Required                 |
| present | boolean | True if present, false if absent            | Required                 |
| desc    | string  | A description about the test's presentation | Required. Max 1024 chars |

### Case

Description and summary of the patient's presentation and the data gathered during the differential diagnosis procedure.

| Field      | Type          | Description                  | Other                        |
| ---------- | ------------- | ---------------------------- | ---------------------------- |
| id         | uuid          | Unique identifier            | Required                     |
| desc       | string        | A description about the case | Required. Max 2056 chars     |
| symptoms   | array of uuid | List of SymptomEntry         | Required. Default empty list |
| conditions | array of uuid | List of ConditionEntry       | Required. Default empty list |
| tests      | array of uuid | List of TestEntry            | Required. Default empty list |

### Citation

Citation stores the source of "Condition", "Symptom", "Test".

| Field  | Type   | Description                                          | Other                     |
| ------ | ------ | ---------------------------------------------------- | ------------------------- |
| id     | uuid   | Unique identifier                                    | Required.                 |
| bibtex | string | A bibtex entry                                       | Required. Max 2048 chars. |
| ieee   | string | The bibtex value formatted as an IEEE-style citation | Required. Max 2048 chars. |

## Tech stack

### DDClient

It is a PWA (Progressive web application), consisting of a single html, a css file, and single js file written in Vanilla Javascript.

It is located in the folder `public` folder.

For more information on DDClient requirements, see [Project DDClient](./project-ddclient.md)

### SSEditor

It is a Python terminal application using Textual library for UI.

It is located in the folder `editor` folder.

For more information on DDClient requirements, see [Project SSEditor](./project-sseditor.md)

## Architecture

### Design pattern

Uses MVC (Model-View-Controller) design principle.

### Data storage

A json file for each entity type stored in the `public\data` folder.
