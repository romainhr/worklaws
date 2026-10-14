---
name: recipe-communicate
description: Runbook for drafting and, only with approval, sending messages (email, chat, client reply). Gathers context, drafts variants, reviews data, commitments and tone, and logs what was sent with follow-up tasks.
when_to_use: The user asks to write, reply to or send an email, a chat message or a client reply, or to send minutes or a report. Also with /recipe-communicate.
---

# Recipe: Communicate with approval

1. **Gather the context:** original thread, history with the recipient and the data to be cited, each with its source.
2. **[U] Goal, channel and tone.** Only ask what cannot be inferred from the request.
3. **Draft 1 to 3 variants** depending on the goal. If the user has a style profile, use it.
4. **[A] Review:**
   - data accuracy;
   - **commitments the message makes** (dates, amounts, promises);
   - tone;
   - sensitive data. Restricted information is never included.
5. **◇ [U] Send?**
   - Edit → go back to step 3.
   - "I'll send it myself" → hand over the draft and finish.
   - Yes → [S] send through the connector. Action control (T1) asks for confirmation again; this is intentional.
6. **[D] Log** what was sent, to whom and which commitments were made. Create follow-up tasks in the tracker.
7. Run `session-close`.
