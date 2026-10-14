---
name: recipe-handover
description: Runbook for handing a project over between people (change of owner, departure, vacation). Inventory, reviewed handover package, session with the receiving person, and access management without transferring credentials.
when_to_use: A project changes owner, someone leaves or goes on vacation and another person must continue. Also with /recipe-handover.
argument-hint: "[project] [receiving person]"
---

# Recipe: Handover between people

1. **[W] Inventory in parallel:**
   - purpose card;
   - ADRs;
   - open tasks;
   - risks;
   - key contacts;
   - access: **only listed, credentials are never copied**.
2. **[D] Handover package** in `vault/projects/<project>/handover-<person>.md`:
   - what the project is and its status;
   - decisions and their rationale;
   - pending items and risks;
   - how the harness is used in that project.
3. **[A] Review:** could someone with no context continue using only this package?
4. **◇ Is it complete?** If something is missing, go back to step 2.
5. **[U] Session with the receiving person.** Their questions are added to the package.
6. **Access:** request grants and revocations from each system's owner. **Credentials are never transferred** between people or through Claude.
7. If the receiving team does not have the harness, continue with `recipe-adoption`. End with `session-close`.
