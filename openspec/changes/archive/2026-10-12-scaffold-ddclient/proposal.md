# Proposal

## Why

DDClient currently contains only a minimal PWA shell and service-worker cache, so doctors have no usable workflow for entering a case or reviewing differential-diagnosis results. Establishing the client foundation now creates a coherent, browser-runnable surface for the diagnosis workflow while leaving clinical content and administration to the existing JSON data model and SSEditor.

## What Changes

- Create the DDClient application shell in `public/` using the existing vanilla HTML, CSS, and JavaScript stack.
- Add an accessible case-entry flow for a presentation description and symptom selection.
- Add a diagnosis-results flow that presents ranked conditions and related symptoms, then supports marking symptoms present or absent to refine the case.
- Load DDClient data from the JSON entity files under `public/data` and handle unavailable or malformed data with a visible user-facing error.
- Update the PWA manifest and service-worker asset list to cover the client shell and its runtime assets.
- Keep persistence local to the active browser session; do not add a server, authentication, or SSEditor functionality in this change.

## Capabilities

### New Capabilities

- `ddclient-diagnosis-workflow`: Provides the browser-based case entry, symptom refinement, and ranked differential-diagnosis results workflow for DDClient.

### Modified Capabilities

<!-- No existing capability specs are present; this change introduces the initial DDClient behavior contract. -->

## Impact

- Affected files: `public/index.html`, `public/css.css`, `public/js.js`, `public/manifest.webmanifest`, and the JSON data files under `public/data`.
- Adds no external runtime dependency; implementation remains vanilla browser JavaScript and static PWA assets.
- Establishes client-side interfaces between the UI, the eight JSON entity collections, and the diagnosis-ranking/refinement logic.
