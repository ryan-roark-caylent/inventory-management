# Lab 5 Rubric — Which Abstraction Earns Its Tokens?

## Abstraction Definitions

| Abstraction | One-line definition |
|---|---|
| **CLAUDE.md** | Always-loaded project truth; costs every session whether or not you need it. |
| **Skill** | On-demand recipe; loads when triggered, silent otherwise. |
| **Hook** | Deterministic event reaction; zero reasoning, fires automatically on a git or tool event. |
| **Subagent** | Delegated worker with scoped tools and its own context; isolated from the parent session. |
| **MCP server** | External capability the model and CLI don't have; costs tool-definition tokens every session. |

---

## Decision Questions

Work down the list. The first "yes" is your answer.

1. **Does every session with this project need it?** → CLAUDE.md
2. **Is it a multi-step recipe you trigger on demand?** → Skill
3. **Is it "whenever X happens, do Y" with no judgment call?** → Hook
4. **Does it need isolation or a different tool scope from the parent session?** → Subagent
5. **Does it need a capability that no CLI provides and the weights don't contain?**
   → MCP server — the Sakis test: *"CLI doesn't exist, and models don't have anything about p4plan in the weights… they had to."*

---

## Perforce Scenarios

Place each scenario in exactly ONE box. Write a one-sentence defense.

| # | Scenario | Your placement | Your defense |
|---|---|---|---|
| 1 | **Spec-driven plan-then-implement loop** (Paul Vincent): every task starts with a markdown spec in a fixed six-section format, then implementation from that spec. | | |
| 2 | **Check-style scope guard** (Scott Wellard): before any file is saved, confirm the change touches only files inside the declared scope directory. | | |
| 3 | **Jira-to-PR agentic loop** (Günter / Scott): given a Jira ticket, draft a branch, implement, open a PR — the whole chain in one go. | | |
| 4 | **P4 worktree isolation** (Nick Poole): each feature lives in its own Perforce workspace; spin one up, do the work, tear it down. | | |

---

## Facilitator Lines

> **The wrong answer is "all of the above." Defend a single choice.**

> **What if 10,000 teams had different workflows — should they all inherit this CLAUDE.md?**
