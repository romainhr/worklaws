---
name: worklaws
description: Worklaws router. Use it at the start of any new request to classify the intent (verb, destination, profile) and launch the right runbook. Also invoked with /worklaws.
when_to_use: At the start of a session or when the user changes topic; when it is unclear whether the task is to research, create, validate, document, adopt the harness, or organize a workspace.
argument-hint: "[request in natural language]"
---

# Worklaws router

Read `reference/model.md` (legend and rules) before continuing. Profiles are in `reference/profiles.md` and templates are in `templates/`.

## Steps
0. **Workspace:** if the user configuration, vault, or tracker the recipe will use is missing, go through `prepare-workspace` (T0) first.
1. **Project status.** Check whether `.claude/worklaws.json` exists at the root of the repo or workspace.
   - It does not exist and there is code or content → recommend `recipe-adoption` and ask [U] whether to adopt it now or continue without the harness.
   - It exists with a `harness_version` lower than the model's → recommend `recipe-adoption` in **update** mode.
   - There is no project (empty folder or abstract request) → continue to step 2.
2. **Classify the request on three axes:**
   - **Verb:** Research · Create · Validate · Document · Organize · Deliver.
   - **Destination:** current project · reusable knowledge · new idea · personal learning.
   - **Profile:** read from `.claude/worklaws.json`. If it does not exist, ask [U].
3. **Choose the runbook** with this table:

   | Intent | Runbook |
   |---|---|
   | New idea to build (no project) | `recipe-new-idea` |
   | Continue an already defined task | `recipe-continue-task` |
   | Something new for an existing project | `recipe-new-feature` |
   | Validate, test, or audit quality | `recipe-validation` |
   | Research, study, evaluate, or diagnose | `recipe-research` |
   | Stuck or asking for ideas | `recipe-unstuck` |
   | Deploy, publish, or deliver | `recipe-deliver` |
   | Create a harness for a domain or role | `recipe-create-harness` |
   | Change an existing harness (skill, recipe, hook, agent) | `recipe-edit-harness` |
   | Critique or audit AI use | `recipe-ai-audit` |
   | Draft or send a message | `recipe-communicate` |
   | Progress or status report | `recipe-status-report` |
   | Organize pending items or the inbox | `recipe-triage` |
   | Prepare a meeting or write the minutes | `recipe-meetings` |
   | Something failed or there is an incident | `recipe-incident` |
   | Update dependencies, pay down debt, review overdue items | `recipe-maintenance` |
   | Daily brief | `recipe-daily-brief` |
   | Weekly review | `recipe-weekly-review` |
   | First time with the plugin | `recipe-onboarding` |
   | Hand a project over to another person | `recipe-handover` |
   | Test changes to skills or recipes | `recipe-evals` |
   | Organize or explore the configuration, build a plugin | `recipe-explore-organize` |
   | End the session | `session-close` |

4. **If the classification is ambiguous**, ask [U] with AskUserQuestion. Offer the 2 or 3 most likely interpretations. Do not guess.
5. **Announce** in one line "Recipe: X · Profile: Y · Destination: Z".
6. **Record the state:** write the recipe name to `.claude/state/active-recipe`. This lets the SessionEnd hook detect whether the session ends without `session-close`.
7. Run the chosen runbook.

## Rules
- The action control hook (T1) asks for confirmation on irreversible or external actions. Do not try to bypass it.
- One session runs one recipe. If the user asks for something else mid-session, apply `new-request` (T3).
- Do not start heavy work (subagents, workflows) before the recipe is chosen.
