# Design

## Context

See `proposal.md` for the motivation and scope. The repository currently has a static HTML entry point, stylesheet, manifest, and a file named `public/js.js` that is registered as a service worker; it does not yet render a diagnosis interface or include clinical JSON data. The design must remain dependency-free and work when served as static files.

## Goals / Non-Goals

**Goals:**

- Provide a small, accessible single-page workflow with explicit case-entry, symptom-finding, and results states.
- Keep diagnosis state in memory for the active browser session and make ranking deterministic and testable.
- Validate all locally loaded collections and expose failures in the UI rather than rendering unsupported clinical conclusions.
- Preserve PWA behavior by separating application code from service-worker code and caching the shell assets.

**Non-Goals:**

- Server-side persistence, user accounts, authentication, synchronization, or clinical record storage.
- Editing conditions, symptoms, tests, citations, or other SSEditor administration behavior.
- Replacing clinician judgment or adding clinical rules that are not represented by the JSON data model.

## Decisions

### Separate the application entry point from the service worker

`public/app.js` will own rendering, data loading, case state, and ranking. `public/service-worker.js` will own install, activation, and cache behavior. `index.html` will load `app.js` as a normal module/script and register `service-worker.js`.

This avoids treating application code as a worker and makes the current `js.js` naming conflict explicit. Keeping both files as small browser-native scripts is preferred over introducing a bundler or framework.

### Use a data adapter with explicit collection paths and validation

The client will fetch the eight entity collections from `public/data` using one centralized path map. The adapter will parse arrays, verify required identifiers and relationship references, and return a normalized read-only data set to the workflow. The initial diagnosis view requires valid condition and symptom collections; all referenced collections remain validated so malformed clinical data cannot be silently ignored.

The adapter will report failures through a single error state. It will not provide fallback or sample medical data.

### Keep diagnosis state in a single in-memory model

The model will contain the case description and a map of symptom IDs to `present`, `absent`, or `unassessed`. Rendering functions will derive the symptom controls and condition cards from this model rather than mutating the data collections. A reset action can discard the active model and return to case entry without persistence.

### Use a deterministic, explainable ranking function

Applicable conditions will be derived from condition-to-symptom references. Conditions matching present symptoms receive a score equal to the number of matching present symptoms; explicitly absent symptoms are excluded from the applicable set when the condition requires them, while unassessed symptoms do not count either way. Results sort by descending match score, descending `priority`, then case-insensitive name and stable identifier.

This uses the existing data model and is easy to test without a clinical inference engine. A more sophisticated probabilistic or rules-based ranking system is deferred until the data contract defines it.

### Render semantic controls and visible states

The UI will use labeled form controls, fieldset/group semantics for symptom findings, keyboard-accessible buttons, and an `aria-live` status region for validation and data errors. The results view will show the case description, current findings, ranked condition cards, and a clear no-match state. CSS will provide responsive layout without changing the state model.

## Risks / Trade-offs

- [Risk] Static hosting may serve the app from a path where absolute `/data` URLs fail. → Mitigation: build data and asset URLs relative to the document base and test from a static HTTP server at the repository root.
- [Risk] Existing deployments may rely on `js.js` as the service-worker URL. → Mitigation: keep a compatibility service-worker entry or document the intentional URL migration, and bump the cache name so stale workers are replaced.
- [Risk] Incomplete or inconsistent clinical fixtures can prevent the workflow from opening. → Mitigation: fail visibly with the affected collection named; add representative valid fixtures and malformed-data tests.
- [Risk] Ranking semantics may be interpreted as clinical advice. → Mitigation: label results as decision support, preserve the existing medical disclaimer, and keep the ranking rule explicit and data-driven.

## Migration Plan

1. Add the application shell, data fixtures/loader, and ranking logic without changing external services.
2. Register the new service worker and update its cache manifest/version.
3. Verify the workflow through a local static server and browser tests/manual scenarios.
4. Roll back by restoring the prior `index.html`, manifest, and service-worker registration; no persisted data migration is required.

