---
name: recipe-meetings
description: Meetings runbook with two modes. Before, it builds a brief (goal, agenda, key questions, decisions to seek, risks). After, it turns notes or a transcript into verified minutes with tasks and decisions recorded.
when_to_use: The user is preparing a meeting, or has notes or a transcript from a meeting they want to turn into minutes and actions. Also with /recipe-meetings.
argument-hint: "[before|after] [event]"
---

# Recipe: Meetings

**◇ Before or after the meeting?**

## Before: brief
1. **[W] Context in parallel:** participants, history with them, open items, documents and previous decisions (vault, tracker and calendar or email connectors, if available).
2. **[D] Brief:** goal, agenda, key questions, decisions being sought and risks. Saved to `vault/projects/<project>/meetings/<date>-brief.md`.
3. **◇ [U] Is the brief right?** If not, adjust and go back to step 2.

## After: minutes
1. **Input:** notes or transcript, provided by the user or by a connector.
2. **[D] Minutes:** decisions, agreements, owners and dates.
3. **[A] Verify:** nothing made up. Anything unclear in the source is marked as **[uncertain]**.
4. **◇ [U] Are the minutes right?** If not, adjust and go back to step 2.
5. **[D] Record:** tasks to the tracker and decisions to the registry (ADR if they are architectural).
6. If the minutes need to be sent, continue with `recipe-communicate`.

End with `session-close`.
