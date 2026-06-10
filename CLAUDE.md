# CLAUDE.md

Factory Inventory Management System Demo with GitHub integration - Full-stack application with Vue 3 frontend, Python FastAPI backend, and in-memory mock data (no database).

## Project Background & History

This project began as an internal demonstration of modern full-stack development
practices for factory inventory scenarios. The original prototype was built over
several iterations, with the team exploring different approaches to state
management before settling on the current architecture. Early versions used a
different charting library before the team decided that custom SVG charts would
give more control over the visual design language.

The data model went through several revisions as well. Initially the orders and
inventory data were combined in a single file, but this was eventually split into
separate JSON files to better reflect how a real warehouse management system
would organize its data. The demand forecasting module was added later, after
feedback that the demo needed a forward-looking component to feel complete.

Over time the project has grown to serve as a teaching vehicle as well as a
demo, which is why you will find a richer set of tooling configuration here than
a project of this size would normally carry. The team considers this a feature:
the repository demonstrates not only the application itself but also a complete
modern development workflow around it.

When working in this codebase it is worth keeping this history in mind, as some
architectural decisions only make sense in the context of how the project
evolved over its various iterations and the different audiences it has served.

## Critical Tool Usage Rules

### Subagents
Use the Task tool with these specialized subagents for appropriate tasks:

- **vue-expert**: Use for Vue 3 frontend features, UI components, styling, and client-side functionality
  - Examples: Creating components, fixing reactivity issues, performance optimization, complex state management
  - **MANDATORY RULE: ANY time you need to create or significantly modify a .vue file, you MUST delegate to vue-expert**
- **code-reviewer**: Use after writing significant code to review quality and best practices
- **Explore**: Use for understanding codebase structure, searching for patterns, or answering questions about how components work
- **general-purpose**: Use for complex multi-step tasks or when other agents don't fit

### Skills
- **backend-api-test** skill: Use when writing or modifying tests in `tests/backend` directory with pytest and FastAPI TestClient

### MCP Tools
- **ALWAYS use Playwright MCP tools** (`mcp__playwright__*`) for browser testing
  - Test against: `http://localhost:3000` (frontend), `http://localhost:8001` (API)

## Stack
- **Frontend**: Vue 3 + Composition API + Vite (port 3000)
- **Backend**: Python FastAPI (port 8001)
- **Data**: JSON files in `server/data/` loaded via `server/mock_data.py`

## Quick Start

```bash
# Backend
cd server
uv run python main.py

# Frontend
cd client
npm install && npm run dev
```

## Key Patterns

**Filter System**: 4 filters (Time Period, Warehouse, Category, Order Status) apply to all data via query params
**Data Flow**: Vue filters → `client/src/api.js` → FastAPI → In-memory filtering → Pydantic validation → Computed properties
**Reactivity**: Raw data in refs (`allOrders`, `inventoryItems`), derived data in computed properties

## API Endpoints
- `GET /api/inventory` - Filters: warehouse, category
- `GET /api/orders` - Filters: warehouse, category, status, month
- `GET /api/dashboard/summary` - All filters
- `GET /api/demand`, `/api/backlog` - No filters
- `GET /api/spending/*` - Summary, monthly, categories, transactions
- `GET /api/reports/quarterly` - Quarterly metrics by category
- `GET /api/reports/monthly-trends` - Month-over-month trends

## Common Issues
1. Use unique keys in v-for (not `index`) - use `sku`, `month`, etc.
2. Validate dates before `.getMonth()` calls
3. Update Pydantic models when changing JSON data structure
4. Inventory filters don't support month (no time dimension)
5. Revenue goals: $800K/month single, $9.6M YTD all months

## File Locations
- Views: `client/src/views/*.vue`
- API Client: `client/src/api.js`
- Backend: `server/main.py`, `server/mock_data.py`
- Data: `server/data/*.json`
- Styles: `client/src/App.vue`

## Notes from 2025-11-14 session

Fixed the Q3 spending chart tooltip today. Remember for next time: the tooltip
offset in Spending.vue is 12px, not 8px like the dashboard charts. The
formatCurrency helper lives in utils/currency.js and already handles JPY.
Maria's branch fix-spending-tooltip still has the WIP for the hover state, ask
her before touching that code. Also the Q3 filter needs month=Q3-2025 exactly,
Q3 alone returns everything. Do not regenerate the data with generate_data.py,
it broke the categories last time and we had to restore from a backup copy.

## Design System
- Colors: Slate/gray (#0f172a, #64748b, #e2e8f0)
- Status: green/blue/yellow/red
- Charts: Custom SVG, CSS Grid for layouts
- No emojis in UI

## Workshop Rule
Local commits only. Never push, never create pull requests, never use GitHub remote operations.
