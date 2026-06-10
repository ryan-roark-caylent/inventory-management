<!-- Markdown only. A spec describes behavior, not implementation. If you are writing code in here, stop. -->

# Spec: <feature name>

<!-- Overview: Two sentences. What exists today, and what this change completes. -->

## Overview

<What the system does today — the half-built or missing piece.>

<What this change adds or completes, and why.>

## API

<!-- For each route: method, path, request body (model name), response (model name), and all status codes including error cases. -->

| Method | Path | Request Body | Response | Status Codes |
|--------|------|-------------|----------|--------------|
| POST | /api/... | ModelName | ModelName | 201 Created; 400 bad input; 404 not found; 409 conflict |
| GET | /api/.../{id} | — | ModelName | 200 OK; 404 not found |

## Data & Persistence

<!-- Where the data lives, what mutates on each operation, and what survives a server restart. -->

- Data lives in: <in-memory list / database table / JSON file>
- On create: <what is appended or written>
- On restart: <what persists vs. resets>

## UI Changes

<!-- Per component: what is added, every user-visible state, what events fire, and what refreshes. -->

### <ComponentName>

- Added: <button / form / badge / section>
- States:
  1. <Default state — what the user sees before acting>
  2. <In-progress state — while the request is pending>
  3. <Success state — after the action completes>
- On success: emits `<event-name>` with `<payload description>`

### <ParentComponentName>

- Listens for `<event-name>` and re-fetches <resource list> to reflect the updated state.

## Out of Scope

<!-- Explicit exclusions. Anything not listed above is out of scope. -->

- No <editing or deletion of the resource>
- No <list or history page>
- No <supplier selection form or additional input fields>
- No tests in this change

## Acceptance Checks

<!-- Numbered, manually executable checks a reviewer can run in under two minutes. -->

1. <UI click path: open X, click Y, observe Z>
2. Call `GET <endpoint>` against the running backend; expect status <code> and response body containing `<field>`.
