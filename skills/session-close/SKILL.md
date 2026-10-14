---
name: session-close
description: Mandatory runbook at the end of any recipe or session. Writes the session report (with token usage and cost via script), the handoff for the next session, and the retro that proposes improvements to the harness.
when_to_use: At the end of every recipe, when the user says we are done or is about to change topic, or when SessionStart warns that the previous session closed without a report.
---

# Session close (strict rule)

1. **[D] Session report:** write `.claude/sessions/pending.md` using the template `../worklaws/templates/session-report.md`.
   - Include: completed tasks, decisions and pending items.
   - **Do not write usage figures.** Leave the `<USAGE>` marker as is. The Stop hook replaces it with telemetry data and renames the file.
2. **[D] Handoff:** overwrite `.claude/handoff.md` using the template `handoff.md`. It must be readable without prior context.
3. **Retro.** Review the session and classify each learning into one of these categories:

   | Finding | Destination |
   |---|---|
   | Procedure repeated 2 or more times | Proposal for a new skill or an improvement to an existing one |
   | A hook failed (see `.claude/state/failed-hooks.log`) | Proposal to fix the hook |
   | Fact verified with a source | Knowledge registry (`knowledge-registry` skill) |
   | User correction or preference | Proposal for CLAUDE.md or for the profile rule |
   | Something local better than the reference | Improvement proposal for the reference model |
   | Nothing new | Do nothing (do not bloat the context) |

   Write the proposals to `.claude/retro/<date>.md`.
4. **◇ [U] Which proposals are applied?** Only what is approved is applied. Changes to the harness are made with `recipe-edit-harness` (PR in the plugin repo). Nothing changes on its own.
5. **Close the state:** delete `.claude/state/active-recipe`. Remind the user to run `/clear` before the next task.
