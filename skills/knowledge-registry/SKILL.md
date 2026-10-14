---
name: knowledge-registry
description: Rules for querying and updating the knowledge registry (atomic claims with source, status and expiration) without recency bias. Always query before researching.
when_to_use: Before any research; when saving verified facts in the retro; when a new claim contradicts an existing one.
user-invocable: false
---

# Knowledge registry

**Location:** `<vault>/knowledge/`, per `.claude/worklaws.json` → `vault`. Each claim is a note using the template `../worklaws/templates/claim.md`.

## Query (before researching)
1. Search by topic in the notes' frontmatter and text.
2. Classify each claim found:
   - `current` and not expired → **reuse** without researching again.
   - Expired (`expires` in the past) → re-verify before using it.
   - `disputed` → do not use it as truth; research that point.
   - `superseded` → follow `superseded_by`.

## Save
1. **No source, no save.** Each claim must be atomic and verifiable.
2. **Blind verification:** whoever verifies a new claim (`researcher` subagent) receives only the question, not the previous claim. Only afterwards are they compared.
3. **If it contradicts an existing claim, age does not grant validity.** The best evidence wins:
   - primary source > secondary > anecdote;
   - reproducible test > assertion;
   - for volatile facts, the most recent wins.
4. **No clear winner** → both become `disputed` and it is escalated to the user [U].
5. **Superseded claims are not deleted:** they stay with `status: superseded` and `superseded_by`, just like a superseded ADR.
6. **Scope.** Use `general`, `profile-<x>` or `project-<x>`. Do not generalize something that was only proven in one project.

## Limit
If your organization maintains a central knowledge base, treat it as read-only. This registry lives only in the personal or project vault.
