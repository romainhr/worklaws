---
name: recipe-edit-harness
description: Runbook for modifying an existing harness (this plugin or another one created with recipe-create-harness). Impact analysis, compatibility and deprecation handling, minimal change on a branch, reviewer, evals with no regressions, approval, semver version and update in every project.
when_to_use: A retro, audit or incident proposes changing a skill, recipe, agent, hook or template of the harness, or the user asks to fix, improve, add or retire a component. Also with /recipe-edit-harness.
---

# Recipe: Edit harness

1. **Load the harness:** purpose card, current version (`plugin.json`), inventory of skills, agents, hooks and templates, and existing evals.
2. **[U] What changes and why.** Possible types: fix · improvement · new component · retirement. Possible origin: retro (`.claude/retro/`), audit, incident or direct request.
3. **[W] Parallel impact analysis:**
   - which recipes and skills depend on what changes, searching for references by name;
   - which projects use the harness and at which version (`.claude/worklaws.json`);
   - possible conflicts with the organization's hooks.
4. **◇ Does it break compatibility?** For example: a skill is renamed, the format of `worklaws.json` changes or something is retired.
   - Yes → **migration and deprecation plan**: whatever is retired warns for at least one version before it goes away, and `recipe-adoption` (update mode) knows how to migrate it.
5. **[S] Branch and minimal change**, following the legend and rules in `../worklaws/reference/model.md`:
   - Descriptions stay short, with the use case first.
   - SKILL.md files must stay under 500 lines.
6. **[A] Reviewer** (`adversarial-reviewer`):
   - Is it correct?
   - Does it break any existing recipe?
   - Does it inflate the context? For example, longer descriptions or more skills always loaded.
7. **[S] Evals** with `recipe-evals`: new version against the previous one.
   - **◇ Are there regressions?** If so, go back to step 5. At most 3 rounds; after that, [U] decides.
8. **◇ [U] Approve and publish?** If not, go back to step 2 to rethink the change.
9. **[S] Publish:**
   - bump the version with semver (fix = patch, improvement or new component = minor, breaking change = major);
   - update the changelog;
   - write an ADR if the harness architecture changes (with the model used and the human reviewer).
10. **Propagate:** in every project that uses the harness, run `recipe-adoption` in **update** mode. Finish with `session-close`.
