---
name: recipe-status-report
description: Runbook for preparing a status report for management, a client or the team from evidence (tracker, session reports, commits, ADRs, metrics), verified and without glossing over delays.
when_to_use: The user asks for a progress report, status update or weekly summary of a project. Also with /recipe-status-report or as a scheduled task.
---

# Recipe: Status report

1. **[U] Audience and period.** Only ask what cannot be inferred from the request.
2. **[W] Gather the evidence in parallel:**
   - tracker: closed, open and blocked tasks;
   - `.claude/sessions/` for the period;
   - commits;
   - ADRs;
   - profile metrics.
3. **Synthesize:**
   - achievements;
   - progress against the plan;
   - risks and blockers;
   - decisions requested from the audience;
   - next steps.
4. **[A] Verify** that every claim has evidence. **Delays are not glossed over.**
5. **◇ [U] Approved?** If not, adjust and go back to step 3.
6. **[D] Save** the report in `vault/projects/<project>/status/<date>.md`. If the folder does not exist, go through `prepare-workspace` first.
7. To send it, continue with `recipe-communicate`. If there is no send, run `session-close`.
