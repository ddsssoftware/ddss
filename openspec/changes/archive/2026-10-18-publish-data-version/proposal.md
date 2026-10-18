# Proposal

## Why

SSEditor and DDClient share one data directory, but nothing tells DDClient that the data changed. Data edits reach the client by committing `public/data`, so a browser that has already cached the collections keeps serving the pre-edit data until its cache is evicted. SSEditor is the only writer of those collections, so it can publish the fact of a change when it writes.

The client cannot currently load any data at all: it still requests four client-only collections that were deliberately deleted, and fails on the first 404. That repair is a prerequisite for exercising the caching and revalidation this change introduces, so it is included.

## What Changes

- SSEditor writes a `version.json` marker in the data directory on every accepted write (add, edit, delete), containing the write time as an ISO 8601 UTC timestamp.
- The marker is written after the collection file, atomically, and best-effort: a marker failure never changes the outcome of the save.
- DDClient stops requesting the four client-only collections that were deleted, so it can load the four editable collections at all (the repair recorded in `editor/README.md`).
- DDClient caches the four editable collections so the diagnosis workflow can start offline after a successful first load.
- On startup, DDClient compares the published marker with the version it last served and refetches the collections when it differs. A missing, unreachable, or malformed marker never blocks a load.
- `public/data/version.json` is tracked and committed with data edits, so a deploy carries the marker that produced it.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `sseditor-entity-management`: adds a requirement that every accepted write publishes a data version marker, and states the marker's contents and ordering relative to the collection file.
- `ddclient-diagnosis-workflow`: adds requirements for caching the clinical collections for offline use and for revalidating that cache against the published marker.

## Impact

- `editor/models/repository.py` becomes the publisher; covered by `editor/tests/test_repository.py`.
- `public/app.js`: the startup version check, plus removal of the four stale client-only collection paths and their three reference checks.
- `public/service-worker.js` and the new `public/data/version.json`.
- `.gitignore` is unchanged; the marker is a committed artifact, so every local save dirties the working tree until committed.
- Record schemas, identifiers, validation rules, editor screens, and the controller layer are untouched.
- Hand edits to a collection do not update the marker; clients stay on cached data until the next accepted editor write. This is accepted for this change.
- The client has no automated test harness, so its half is verified manually; the Python half keeps the project's 95% coverage gate.
