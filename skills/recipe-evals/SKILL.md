---
name: recipe-evals
description: Runbook for evaluating changes to the harness's skills and recipes before publishing them. Real cases and triggering queries, criteria defined up front, new vs. previous run, grading, blocking on regressions, and approval with a version bump.
when_to_use: There is a PR that changes a harness skill, recipe, agent or hook, or the user wants to measure whether a skill works. Also with /recipe-evals.
---

# Recipe: Skill and recipe evals

1. **Case set:**
   - Between 20 and 50 cases drawn from **real failures or requests**: retros, audits, incidents.
   - Triggering queries: cases where the skill **must** fire and cases where it **must not**.
   - Stored in `evals/<skill>/cases.json` in the harness repo.
2. **Define the grading criteria before running:** code-based (exact match or checks), model-based (rubric) or human.
3. **[W] Run in parallel** the new version and the previous one (baseline).
4. **[A] Grade and compare.** Read the transcripts of the failed cases: the score alone is not enough.
5. **◇ Are there regressions?** (cases that passed before and fail now)
   - Yes → block the PR and write a regression report.
6. **◇ Does capability improve?**
   - No → [U] decide whether the change is still worth it, for example because it simplifies or reduces cost.
7. **[U] Approve the PR** and bump the plugin version. Using Anthropic's `skill-creator` skill for the evals is optional and requires approval.
8. Run `session-close`.
