---
name: recipe-continue-task
description: Runbook for executing an already defined task in a project with a harness. Pick up the task, TDD, filtered tests, diff reviewer, approval, commit/PR and close.
when_to_use: You need to follow the plan, run the next task or resume what another session left behind.
---

# Recipe: Continue task

1. **Read the context.**
   - The handoff (`.claude/handoff.md`) is injected by the SessionStart hook.
   - Ready tasks come from the tracker (`bd ready` in Beads).
2. **Propose the next task** with its scope in 2 or 3 lines.
3. **◇ [U] Task and scope OK?**
   - No → go back to step 2 with another task or an adjusted scope.
   - Yes → mark it as claimed (`bd update <id> --claim`).
4. **◇ Does the change fit in one sentence?**
   - No → enter plan mode, present the plan and wait for approval [U].
5. **[S] Implement with TDD:** first a failing test, then the code. Use the commands from `.claude/worklaws.json` → `commands`.
6. **[H] PostToolUse** runs lint and tests, showing only failures.
   - Loop: if tests fail, fix them.
   - Cap: 2 failed attempts on the same error → stop and propose [U] `/clear` with a better prompt (include what you learned in the handoff).
7. **[A] Diff reviewer** against the SPEC and the task (subagent `adversarial-reviewer`).
   - Critical findings → go back to step 5. At most 2 rounds.
8. **◇ [U] Do you approve the change?**
   - No → go back to step 5 with the feedback.
9. **Commit + PR:** `gh` on GitHub, `az repos` on Azure DevOps. Never push without approval.
10. **[D] Close the task** (`bd close <id>`) and update the plan. If the architecture changed, add an ADR.
11. Run `session-close`.
