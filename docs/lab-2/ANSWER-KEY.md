# Lab 2 Answer Key

**For TAs and facilitators only. Not a participant-facing file.**

---

## 1. The Three Planted Discrepancies

| # | Discrepancy | Location |
|---|---|---|
| 1 | `GET /api/reports/quarterly` exists in code but is missing from CLAUDE.md | `server/main.py:230` |
| 2 | `GET /api/reports/monthly-trends` exists in code but is missing from CLAUDE.md | `server/main.py:276` |
| 3 | `GET /api/products` is listed in CLAUDE.md but does not exist in the code | CLAUDE.md API Endpoints section |

### Acceptable extras (also true, also correct)

Claude may additionally report:
- `GET /api/inventory/{item_id}` exists in code but is not listed in CLAUDE.md (`server/main.py:136`)
- `GET /api/orders/{order_id}` exists in code but is not listed in CLAUDE.md (`server/main.py:156`)
- The `GET /api/spending/*` wildcard could be expanded to the four individual routes

All of these are accurate findings. Grade them as correct.

---

## 2. Minimum Passing Diff — Exact Final API Endpoints Section

For hand-typing rescues (paste this verbatim into CLAUDE.md if the section is mangled):

```
## API Endpoints
- `GET /api/inventory` - Filters: warehouse, category
- `GET /api/orders` - Filters: warehouse, category, status, month
- `GET /api/dashboard/summary` - All filters
- `GET /api/demand`, `/api/backlog` - No filters
- `GET /api/spending/*` - Summary, monthly, categories, transactions
- `GET /api/reports/quarterly` - Quarterly metrics by category
- `GET /api/reports/monthly-trends` - Month-over-month trends
```

The `/api/products` line must be absent. The two reports lines must be present. Claude may also add the item-detail routes and expand the spending wildcard; all acceptable.

---

## 3. Expected /context Arc

| State | Figure | Notes |
|---|---|---|
| lab-2-start (seeded) | [TOK-A] | Measured on lab-2-start with fresh claude session, `/context` |
| Core-complete (step 5) | [TOK-C] | After steps 3 and 4; requires `/clear` before `/context` |
| Extra-credit end state | [TOK-EC] | After EC-1 also removes Background and Notes sections |

Expected step-5 drop: [TOK-A] − [TOK-C] tokens

**Note:** These figures must be measured at build time (Section 10 items 10–11) and stamped here before handoff. Running `/context` in a fresh session on each branch with the exact content above produces the measured values.

---

## 4. TA Grading Notes

**Minimum pass:** Three discrepancies found in step 2. Two reports lines added and /api/products removed in step 3. Deployment & Environment Setup section deleted in step 4. AFTER < BEFORE in step 5.

**Over-deletion watch:** The diff from step 3 must touch ONLY the `## API Endpoints` section. The diff from step 4 must remove ONLY `## Deployment & Environment Setup` including `### Required tokens`. If the participant's diff also removes `## Project Background & History` or `## Notes from 2025-11-14 session` in steps 3–4, that is over-deletion (those are EC-1 targets). If the diff removes the vue-expert mandate or the backend-api-test skill pointer, it is load-bearing deletion — help them restore it with `git checkout lab-2-start -- CLAUDE.md` and redo from the affected step.

**The "/clear trap":** If a participant reports "the number didn't change after step 4," they ran `/context` without `/clear`. The card states this; say it on the call: CLAUDE.md is priced at session start.

**TA script for the "which bug" question:** "Both, and they're different diseases. The API list is *wrong* (drift); the token block is *junk* (cost plus a security anti-pattern). You fix drift in step 3 and cut junk in step 4."
