---
name: recipe-daily-brief
description: Daily brief runbook, designed as a scheduled task on business days. Reads calendar, email and chat, tracker, handoffs and due dates in read-only mode, prioritizes the day and leaves a one-page brief; it takes no external actions.
when_to_use: Scheduled task every morning, or the user asks what they have today or for a summary of the day. Also with /recipe-daily-brief.
---

# Recipe: Daily brief (scheduled)

**To schedule it:** create a scheduled task (Cowork or a routine) with a **self-contained** prompt, for example: "Run /recipe-daily-brief for the vault <path>". Each run is a new session with no memory of the conversation. Use a conservative approval mode.

1. **[W] Parallel read, read-only:**
   - calendar;
   - email and chat, if there are connectors;
   - tracker (ready tasks and blockers);
   - handoffs from active projects;
   - due dates.
2. **Prioritize the day:**
   - the 3 most important things;
   - meetings to prepare (`recipe-meetings`);
   - blockers;
   - risks.
3. **[D] Brief of one page at most** in `vault/00_Inbox/brief-<date>.md`.
4. **◇ Is anything urgent?** If so, notify with a 2-line summary.

**Hard rule:** this runbook does not send, publish or modify anything outside the vault.
