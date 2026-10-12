# Tasks

## 1. Establish the DDClient shell and clinical data contract

- [x] 1.1 Replace the empty body in `public/index.html` with semantic case-entry, diagnosis-results, loading, and error regions, and verify the entry point exposes labeled controls and an accessible status region in a browser.
- [x] 1.2 Add representative JSON collections for the eight entities under `public/data` using the documented identifiers and references, and verify every file parses as an array and cross-references resolve.
- [x] 1.3 Add `public/app.js` with a centralized collection path map, fetch/parse/relationship validation, explicit loading/error states, and no fabricated fallback data; verify malformed or unavailable data produces a visible error.
- [x] 1.4 Add responsive styles in `public/css.css` for the case form, symptom findings, condition cards, validation, loading, error, and no-match states, and verify keyboard navigation and narrow viewport layout.

## 2. Implement case state and diagnosis refinement

- [x] 2.1 Implement the in-memory case model and validation for non-empty descriptions, and verify empty submissions remain on the entry view with an actionable message.
- [x] 2.2 Implement symptom controls with present, absent, and unassessed values, preserving the case description and existing findings across changes; verify each control updates the visible state without treating unassessed symptoms as absent.
- [x] 2.3 Implement deterministic condition applicability and ranking using present-symptom matches, priority, name, and stable identifier tie-breakers; verify representative ranking and no-match cases against the capability scenarios.
- [x] 2.4 Render condition cards with names, descriptions, related findings, and a clear no-matching-diagnosis state; verify changing a finding recalculates results without losing the active case.

## 3. Complete PWA integration and documentation

- [x] 3.1 Move service-worker responsibilities into `public/service-worker.js`, register `app.js` and the service worker from the entry point, and update the cache version and asset list; verify a first load registers successfully and a subsequent offline shell load serves cached assets.
- [x] 3.2 Update `public/manifest.webmanifest` and the user-facing medical/disclaimer text to identify DDClient accurately and distinguish decision support from diagnosis; verify manifest URLs resolve from the served application path.
- [x] 3.3 Run syntax checks and serve the repository through a local static HTTP server, then verify the complete case-entry, refinement, error, responsive, and PWA smoke scenarios in a supported browser.
