# Design

## Context

See `proposal.md` for motivation and the two delta specs for the behaviour contract.

Producer side:

- `CollectionRepository.save(entity_type, records)` (`editor/models/repository.py`) is the only path from an accepted write to disk. It delegates to `Record.save` (`editor/models/records.py`), which writes a temporary sibling and calls `Path.replace`.
- `EditorModel.save` and `EditorModel.delete` run the validator first and call the repository only when the violation list is empty.
- `RecordError` is raised for write failures and is not caught anywhere in the view or controller layer, so a failure surfaces as an unhandled exception.
- `public/data/*.json` is git-tracked and committed to reach clients; `.gitignore` has no rule for `public/`.

Consumer side:

- `public/app.js` still requests eight collections, four of which were deleted, so it currently fails on the first 404. `initialize()` runs once at startup and again from the Retry button.
- `public/service-worker.js` pre-caches six shell assets at install and answers every GET with `caches.match(request) || fetch(request)`; it never stores a network response, and `version.json` is not among the pre-cached assets.
- There is no JavaScript test runner in the repository.

## Goals / Non-Goals

**Goals:**

- Publish one data version marker per accepted write, describing when the data changed.
- Let the client detect a changed version with one small request instead of fetching four collections on every startup.
- Make the diagnosis workflow startable offline after a successful load.
- Keep timestamp generation deterministic for tests.

**Non-Goals:**

- Detecting writes made outside SSEditor (hand edits, future sync tools).
- Pushing live updates into an already-open tab.
- Fixing the pre-existing shell cache staleness: an `app.js`-only change does not trigger a service worker update.
- Introducing a JavaScript test runner or automated browser tests.
- Changing record schemas, identifiers, validation, or editor screens.

## Decisions

### The repository publishes the marker

`CollectionRepository.save` writes the collection and then the marker. Alternatives:

- `Record.save`: rejected because a directory-level file does not belong to a single record class, and the classmethod has no access to the data-directory concept the marker needs.
- `EditorModel._write` / `delete`: rejected because it is a second writer surface and leaves direct repository writes (tooling, tests) unpublished. Every call reaching the repository has already passed validation, so "repository write" and "accepted write" coincide.

### Reuse one atomic write helper

Extract the temporary-sibling pattern from `Record.save` into a module-level `write_text_atomically(path, payload)` in `records.py`, raising `OSError`. `Record.save` keeps wrapping `OSError` into `RecordError`; the marker writer catches `OSError` itself. This keeps the two failure policies separate while avoiding duplicated swap logic.

### Marker content

`{"version": "<timestamp>"}` followed by a newline. The object form is extensible (a future content hash or schema revision fits beside `version`); a bare JSON string was the alternative but leaves no room to grow.

### Timestamp format

UTC, microsecond precision, trailing `Z`:

```
2026-10-18T14:03:11.482123Z
```

`datetime.now(timezone.utc).isoformat(timespec="microseconds")` with `+00:00` replaced by `Z`. Fixed width means the value can also be ordered as text, even though the client only compares equality. The repository accepts an optional clock callable (defaulting to UTC now) so tests can assert an exact value without monkeypatching `datetime`.

### Marker ordering

The marker is written strictly after `Record.save` returns. A reader that observes a new version therefore always finds the collection that produced it. Writing the marker first would allow a client to fetch new data under the old version and cache it as current.

### Marker failure is swallowed

The marker write is best-effort; an `OSError` is ignored. Raising would report a false failure after the record was persisted, and the retry path then reads:

- `EntityDetailController.save` never assigned `self.record` because the exception interrupted it.
- A retry for a new record mints a different identifier and is refused by the uniqueness rule, because the first attempt is already stored under the same name.

A warning channel would avoid both problems but changes the model's return contract for one advisory file; that cost is not justified. The next accepted write rewrites the marker, and a marker failure usually accompanies a collection failure because both target the same directory.

### The service worker owns a data cache and honours the request cache mode

A `ddclient-data-v1` cache stores the four collections. For a request under `/data/` that is not `version.json`:

```
  request.cache is no-store or reload ?
        |
       yes --> fetch network -> cache.put -> respond
        |
        no  --> cache.match --hit--> respond
                     |
                    miss --> fetch network -> cache.put -> respond
```

`cache.match` ignores `Request.cache`, so the bypass branch must be explicit; without it, `no-store` from the page still returns the cached copy and revalidation silently does nothing.

`version.json` is excluded from the data cache entirely. It is fetched with `cache: "no-store"`, which means it always reaches the network and is never stored.

`activate` deletes `ddclient-data-*` caches other than the current one, mirroring the existing shell-cache cleanup.

### The app checks the version before loading

```
  GET ./data/version.json  {cache:"no-store"}
     |
     +-- readable string --> equals localStorage["ddclient.dataVersion"] ?
     |                          |
     |                         yes --> loadCollections(fetch)              (cache-first)
     |                          |
     |                          no  --> loadCollections(no-store fetcher)
     |                                  + successful: localStorage = version
     |
     +-- absent / unreachable / malformed --> loadCollections(fetch)
```

- `no-store` rather than `reload` for the collections: `reload` permits conditional revalidation, and a 304 would let the browser reuse a body it already holds. `no-store` guarantees a full response.
- `loadCollections` keeps its `fetcher = fetch` parameter; the caller supplies a closure that adds the cache mode, so validation behaviour is unchanged.
- The version is stored only after all four collections load and validate. A partial refetch leaves the stored version unchanged, so the next start retries.
- Every failure of the version check degrades to the normal load; the marker can never cause the data-unavailable state.

### Revalidation happens at startup only

`initialize()` is the only trigger, covering the initial load and the existing Retry button. No polling, no `visibilitychange` handler, and no live update for an open tab.

### The marker is committed

`public/data/version.json` is tracked, so a deploy carries the version that produced its data. `.gitignore` stays unchanged. The consequence is that every local save dirties the working tree; committing the marker with the data edit is the convention.

## Risks / Trade-offs

- **Hand edits bypass the marker** -> clients keep serving cached data until the next accepted editor write. Documented convention; a content hash is the future fix if external writes become possible.
- **A swallowed marker failure leaves clients stale** -> the next accepted write repairs it; the failure window is narrow because the marker and collections share a directory.
- **Commit noise** -> accepted, and it is the signal that data changed.
- **Forgotten bypass branch in the service worker** -> revalidation silently returns stale data. The bypass must be covered by manual verification, since the client has no automated tests.
- **Shell staleness is unchanged** -> an `app.js`-only change never reaches an installed shell. Verifying this change against an existing install requires unregistering the service worker or changing `service-worker.js`, which this change does.
- **Browser evicts the data cache but keeps the stored version** -> a cache miss falls through to the network, so data stays correct; only offline availability is lost until the next successful load.
- **Two open tabs** -> each holds its own in-memory collections; a tab loaded before a change keeps the old data until reloaded. Out of scope.
- **Clock skew** -> irrelevant, because the client compares equality and never interprets the timestamp.

## Migration Plan

1. Land the producer change first. Until the first save, no marker exists, which the client treats as "unknown" and loads normally.
2. Land the client change. The service worker file changes, so existing installations update; install re-populates the shell cache and activate removes stale data caches.
3. Rollback is safe in either direction: the old client ignores an unknown file in the data directory, `load_all` only reads the four named collections, and the new client works without a marker.

## Open Questions

- Whether a CI or pre-commit check should require `public/data/version.json` to change in any commit that touches `public/data/*.json`. Deferrable; it changes neither the specs nor the approach.
