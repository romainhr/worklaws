---
name: recipe-incident
description: Blameless incident and postmortem runbook. Stabilize first (rollback or mitigation), notify those affected, build an evidence-based timeline, find the root cause, write a postmortem with mandatory review, and send actions to the tracker, knowledge and harness.
when_to_use: Something failed after a delivery, there is an outage, or wrong data was published. Also with /recipe-incident or from recipe-deliver when verification fails.
---

# Recipe: Incident and postmortem

1. **Stabilize first:** apply the rollback plan or a mitigation. Action control (T1) asks for confirmation.
2. **[U] Notify those affected** with `recipe-communicate`: what happened, impact and next update.
3. **◇ Is it stable?** If not, go back to step 1.
4. **[D] Timeline with evidence:** logs, `.claude/state/log.jsonl` and commits.
5. **[W] Root cause in parallel, blameless.** Two questions: what happened? and why didn't we catch it earlier?
6. **[A] Reviewer:** is what we found the cause or just a symptom?
7. **[D] Blameless postmortem** in `docs/incidents/<date>.md`: impact, cause, what worked, what didn't, and actions with an owner.
8. **◇ [U] Mandatory review.** A postmortem nobody reviewed does not count. If it is not approved, adjust and go back to step 7.
9. **Actions:** tasks to the tracker, learnings to the knowledge registry, and harness improvements, which go to the retro and are applied with `recipe-edit-harness`.
10. Run `session-close`.
