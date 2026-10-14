---
name: recipe-new-feature
description: Runbook for a new idea inside an existing project. Produces only a SPEC, an ADR if applicable, and tasks; it never writes code (execution goes through recipe-continue-task).
when_to_use: The user proposes a new feature, change or improvement for a project that already exists.
---

# Recipe: New feature (no code)

1. **Impact analysis** with an Explore subagent: current plan, architecture and affected code. It returns a short summary.
2. **[U] Scope interview** with AskUserQuestion.
   - Loop until the scope is clear. Cap: 3 rounds.
3. **[S] Write the SPEC** for the feature in the repo (`docs/specs/<feature>.md`, template `../worklaws/templates/spec.md`).
4. **[A] SPEC reviewer** (`adversarial-reviewer`): correctness, verifiable requirements and conflicts with what already exists. At most 2 rounds.
5. **◇ Does the architecture change?**
   - Yes → [D] write an ADR (template `adr.md`, with the model used and the human reviewer).
6. **[D] Create the tasks** in the tracker, linked to the SPEC.
7. **◇ [U] Execute now?**
   - Yes → run `session-close` and then open a new session with `recipe-continue-task`.
   - No → they stay in the backlog; run `session-close`.

**Hard rule:** this runbook does not modify source code.
