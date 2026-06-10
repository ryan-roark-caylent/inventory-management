<!-- Markdown only. A spec describes behavior, not implementation. If you are writing code in here, stop. -->

# Spec: Purchase Orders

## Overview

The backend computes a `has_purchase_order` flag for every backlog item against an in-memory `purchase_orders` list, and the client has `createPurchaseOrder` / `getPurchaseOrderByBacklogItem` methods in `api.js`. No routes exist to create or retrieve purchase orders, and `BacklogDetailModal.vue` shows only a Close button with no way to act on a shortage.

This change completes the feature: two new API routes handle PO creation and retrieval, and `BacklogDetailModal.vue` gains a Create Purchase Order button wired to those routes. `Dashboard.vue` refreshes its backlog list after a PO is created so the updated `has_purchase_order` flag is reflected immediately.

## API

<!-- For each route: method, path, request body (model name), response (model name), and all status codes including error cases. -->

| Method | Path | Request Body | Response | Status Codes |
|--------|------|-------------|----------|--------------|
| POST | /api/purchase-orders | `CreatePurchaseOrderRequest` | `PurchaseOrder` | 201 Created; 404 if `backlog_item_id` does not match a known backlog item; 409 if a PO already exists for that backlog item |
| GET | /api/purchase-orders/{backlog_item_id} | — | `PurchaseOrder` | 200 OK; 404 if no PO exists for that backlog item |

Both routes reuse the existing `PurchaseOrder` and `CreatePurchaseOrderRequest` models already defined in `server/main.py` (lines 104–121). No new models are defined.

### POST /api/purchase-orders — field defaults

When the "Create Purchase Order" button is clicked, the frontend sends these default values with no user form:

- `backlog_item_id`: the backlog item's `id`
- `quantity`: the shortage amount (`quantity_needed - quantity_available`)
- `supplier_name`: `"Acme Industrial Supply"`
- `unit_cost`: `10.00`
- `expected_delivery_date`: today's date + 14 days (ISO 8601, e.g. `2026-06-24`)

### POST /api/purchase-orders — generated fields

The backend generates these fields; they are not accepted from the request:

- `id`: sequential format `PO-001`, `PO-002`, … (zero-padded to 3 digits, based on current list length + 1)
- `status`: `"Ordered"` (fixed on creation)
- `created_date`: today's date (ISO 8601)

## Data & Persistence

- Data lives in: the in-memory `purchase_orders` list imported from `mock_data.py` (starts as an empty list loaded from `server/data/purchase_orders.json`).
- On create: a new `PurchaseOrder` dict is appended to the `purchase_orders` list.
- JSON files are never written. All changes are in-memory only.
- On server restart: the list resets to its initial empty state. Any POs created during the session are lost.

## UI Changes

### BacklogDetailModal.vue

- Added: a "Create Purchase Order" button in the modal footer.
- The button is hidden (not rendered) when `backlogItem.has_purchase_order` is `true`.
- States:
  1. **Default** — "Create Purchase Order" button is visible and enabled.
  2. **Creating** — button is disabled and shows "Creating..." while the API call is in flight.
  3. **Created** — button is replaced by a "PO Created" badge once the API call succeeds. This state persists for the lifetime of the open modal.
- On success: emits `po-created` with no payload needed by the parent (the parent re-fetches the full backlog list).
- Uses the existing `api.createPurchaseOrder` method from `client/src/api.js`. No new axios calls or imports.

### Dashboard.vue

- Adds a `handlePOCreated` function that calls the existing `loadData` function (or re-fetches backlog specifically) to refresh the `allBacklogItems` list.
- Wires `@po-created="handlePOCreated"` on the existing `<BacklogDetailModal>` tag.
- The updated backlog data from the API will reflect the new `has_purchase_order: true` flag for the affected item.

## Out of Scope

- No PO editing or deletion
- No PO list page
- No supplier selection form or any other input fields beyond the button
- No tests in this change

## Acceptance Checks

1. Open http://localhost:3000, scroll to the Inventory Shortages section, click the "Electric Motor 5HP" row. The modal footer shows "Create Purchase Order". Click the button. The footer flips to "PO Created". Close the modal and reopen the same row: the footer shows "PO Created" (because the Dashboard refreshed the backlog and `has_purchase_order` is now `true`).
2. Call `GET http://localhost:8001/api/purchase-orders/2` against the running backend. Expect a 200 response with a JSON body containing `"id": "PO-001"`, `"status": "Ordered"`, and `"backlog_item_id": "2"`.
