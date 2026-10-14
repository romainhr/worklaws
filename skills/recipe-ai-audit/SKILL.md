---
name: recipe-ai-audit
description: Runbook for a critical audit of AI usage, repo by repo and session by session. Collects evidence from the harness artifacts (reports with usage, retros, log, failed hooks, git) and produces a critical, non-complacent report with recommendations.
when_to_use: The user asks to critique or audit how they use AI, review costs or the quality of work with Claude, or as a monthly scheduled task. Also with /recipe-ai-audit.
argument-hint: "[period, e.g. 30d] [repo paths]"
---

# Recipe: Critical AI audit

**Mandatory tone:** critical and non-complacent. Every observation carries evidence; without evidence, it is not said.

1. **[U] Scope and period:** which repos, projects and sessions, and which date range.
2. **[W] Collect evidence in parallel**, one subagent per repo. **Use only harness artifacts**; do not read transcripts (their format is not documented).
   - `.claude/sessions/*.md`: tasks, decisions and usage table.
   - `.claude/retro/*.md`.
   - `.claude/state/log.jsonl`: actions and approvals.
   - `.claude/state/failed-hooks.log` and `.claude/state/incomplete-closes.log`.
   - `git log` and reverts for the period.
   - Telemetry, if it exists.
3. **[A] Critical analysis by dimension:**

   | Dimension | Questions |
   |---|---|
   | Cost | Cost per task and per recipe? Oversized models for the task? Sessions with a lot of cache written and little reused? |
   | Quality | Rework, reverts, loops that hit the cap, user corrections? |
   | Process | Skipped recipes, sessions mixing topics, missing closes, missing ADRs? |
   | Context | Inflated CLAUDE.md files, unused skills and MCP servers, long descriptions? |
   | Oversight | How many confirmations were approved without changes? A very high percentage suggests possible **automation bias**. |

4. **[A] Verify every critique** with a different verifier. Anything without evidence is discarded.
5. **[D] Report** in `vault/harness/audits/<date>.md` (template `../worklaws/templates/audit-report.md`): findings with evidence, **top 5 recommendations** ranked by impact and a comparison with the previous audit (did what was recommended improve?).
6. **◇ [U] Which recommendations are applied?** The approved ones become harness changes (`recipe-edit-harness`), a project update (`recipe-adoption` in update mode) or tasks in the tracker.
7. Run `session-close`.
