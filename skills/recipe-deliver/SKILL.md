---
name: recipe-deliver
description: Runbook for delivering something in a controlled, reversible way, whether code (deploy/release), a document, a proposal or a dashboard. Prior validation, profile checklist, risk and rollback plan, explicit approval, execution, post-delivery verification and logging.
when_to_use: The user wants to deploy, publish, release a version, send a deliverable to a client or share something outside the team. Also with /recipe-deliver.
---

# Recipe: Deliver / deploy

1. **[S] Validate before sharing:** run `recipe-validation` in quick mode, checking methodology, accuracy and bias according to the profile.
2. **[S] Profile checklist.** Template: `../worklaws/templates/delivery-plan.md`.
   - **web/fabric:** tests green and build OK.
   - **bi:** figures reconciled against the source.
   - **documents:** format, spelling, recipients and permissions.
3. **◇ Risk and reversibility?**
   - **Irreversible or external** (production, client, public release) → write a **rollback plan**: rollback, previous version or correction message.
4. **◇ [U] Explicit approval.** Show what is being delivered, to whom or where, the risk and the rollback plan.
   - If it is not approved, go back to step 2.
5. **[S] Execute:** pipeline, publication or send. The action-control hook (T1) will ask for confirmation again on every irreversible action. This is intentional; do not work around it.
6. **[A] Post-delivery verification:** smoke test, confirmation of receipt or metrics.
7. **◇ Is everything OK?**
   - **No** → apply the rollback plan and open an **incident**: record impact, root cause and actions in `docs/incidents/<date>.md`, with a blameless postmortem, and create the tasks.
8. **[D] Communicate and log:** changelog or release notes and a status report to whoever needs it. Sends also require approval.
9. Run `session-close`.
