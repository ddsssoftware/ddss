# SSEditor

It is a terminal-based Python app with UI based on Textual library.

The solution lives in the `editor` folder. The data it manipulates lives int the `public\data` folder

## CRUD

It provides CRUD facility for the entities: "Condition", "Symptom", "Test", "Citation".

For each entity it provides: a screen to list or search the entities of that types, a screen to edit or add the details of a specific.

## Requirements

### 001 Requirements about data integrity

# REQ-001-001 UUID

The id field should be a randomlly generated 128‑bit identifier shown as 32 hexadecimal characters.

The system must make sure the UUID are unique among all entities of all types.

# REQ-001-002 UUID foreign key

The system must make sure the UUID used to reference the id of another entity exists.

# REQ-001-003 Don't delete referenced id

When deleting an entity check if it referenced by another entity. If it is not referenced it is ok to delete. If it is referenced by another entity, do not allow the deletion, and show to used what are the references.

# 002 Requirements about the "Condition" entity

# REQ-002-001 Names are unique

The field name is unique for each "Condition"

# REQ-002-002 Name casing

The field name is titled cased.

# REQ-002-003 AKA casing

Each member of the AKA list is titled cased.

# REQ-002-004 AKA can´t contain clash with names

Member of the AKA list cannot be the same as the name of the current or other "Condition" entities.
