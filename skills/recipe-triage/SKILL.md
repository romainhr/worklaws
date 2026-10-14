---
name: recipe-triage
description: Capture and triage runbook. Gathers requests from email, chat, tracker and notes into a single inbox, clarifies them, discards or archives what needs no action, does what is quick, and prioritizes and routes the rest to the matching recipe.
when_to_use: The user has many scattered pending items, wants to empty their inbox, or wants to prioritize incoming requests. Also with /recipe-triage.
---

# Recipe: Capture and triage

1. **Capture** everything in the single inbox: `vault/00_Inbox/` or the tracker inbox. Use `prepare-workspace` if it does not exist.
2. **Clarify each item:** what it is, whether it requires action, and which active purpose it serves.
3. **◇ Does it require action?**
   - No → archive it as reference in the vault or discard it.
4. **◇ Does it take less than 2 minutes?**
   - Yes → do it now, under action control (T1).
5. **Prioritize** by impact, urgency and dependencies.
6. **◇ [U] Are the priorities right?** If not, adjust and go back to step 5.
7. **[S] Route:** create the task in the tracker with the **suggested recipe** (2a, 2b, 4, 9, 12…). If it is not the user's responsibility, propose escalating it with `recipe-communicate`.
8. Run `session-close`.
