# Tasks

## 1. Producer: publish the data version

- [x] 1.1 Extract the temporary-sibling write from `Record.save` into a module-level `write_text_atomically(path, payload)` in `editor/models/records.py`, keeping `RecordError` wrapping in `Record.save`; verify `.venv/bin/python -m pytest -q editor/tests/test_records.py editor/tests/test_repository.py` passes.
- [x] 1.2 Add the marker payload builder and writer to `CollectionRepository`, taking an optional clock callable that defaults to UTC now; verify a new test with a fixed clock asserts the payload is `{"version": "<timestamp>"}` with microsecond precision and a trailing `Z`.
- [x] 1.3 Call the marker writer after `Record.save` returns; verify a test that records write order asserts the collection file is replaced before `version.json`.
- [x] 1.4 Catch `OSError` from the marker write so the save outcome and the stored record are unchanged, and the next accepted write retries; verify a test forces the marker write to fail, asserts no exception and the record on disk, then makes it writable and asserts the next save creates the marker.
- [x] 1.5 Verify rejected writes publish nothing: a model-level test submits an invalid record and asserts no `version.json` exists and the collection is unchanged.
- [x] 1.6 Seed `public/data/version.json` in the published shape; verify it parses to an object whose `version` is a non-empty UTC ISO 8601 string.
- [x] 1.7 Run the full suite with the coverage gate: `.venv/bin/python -m pytest -q` passes and total coverage stays at or above 95%.

## 2. Client: restore a loadable collection set

- [x] 2.1 Remove the four deleted client-only collections from `COLLECTION_PATHS` and the three matching `ensureReferences(...)` calls in `validateCollections` in `public/app.js`, and update the known-follow-up section of `editor/README.md`; verify `node --check public/app.js` and that the app at `http://127.0.0.1:8000/` shows the case-entry view instead of the data-unavailable error.

## 3. Client: cache the collections

- [x] 3.1 Add a `ddclient-data-v1` cache to `public/service-worker.js` for `/data/*.json` excluding `version.json`, honouring `no-store` and `reload` as bypass-and-refresh; verify `node --check public/service-worker.js` and, with `python3 server.py` running, load the app once, switch DevTools to offline, reload, and confirm the symptom list still renders.
- [x] 3.2 Delete stale `ddclient-data-*` caches in `activate`; verify in DevTools Application > Cache Storage that only `ddclient-data-v1` and the shell cache remain after a reload.

## 4. Client: revalidate against the marker

- [x] 4.1 Add the startup check to `initialize()` in `public/app.js`: load `version.json` with `cache: "no-store"`, compare it with `localStorage`, reload the collections with a `no-store` fetcher when it differs, store the version only after all four load, and degrade to a normal load on any marker failure; verify `node --check public/app.js`.
- [x] 4.2 Verify the four marker paths manually against `python3 server.py`: no marker and a malformed marker both load the app normally; a changed marker refetches the collections; an unchanged marker serves them without a collection request in the Network panel.
- [x] 4.3 Document the commit convention in `README.md`: any commit touching `public/data/*.json` includes `public/data/version.json`; verify the section names both the file and the marker's UTC ISO 8601 shape.

## 5. Integration

- [x] 5.1 Save a record in the running editor and verify `public/data/version.json` holds a newer UTC ISO 8601 timestamp, then reload the client online and confirm the changed record appears and that offline reload still starts the workflow.
- [x] 5.2 Re-run `.venv/bin/python -m pytest -q` and confirm all tests pass with coverage at or above the gate.

## Workflow follow-up

- Commit `public/data/version.json` together with every data change.
- Archive the change after review.
