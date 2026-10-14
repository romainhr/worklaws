---
name: recipe-adoption
description: Runbook for bringing the worklaws harness into an existing project or workspace (without a harness or with an older version). First understands the project's purpose (confirmed purpose card), then technical discovery, comparison against the reference model, proposal, application on a branch, dry run and ADR.
when_to_use: The project has no .claude/worklaws.json, or has one with a harness_version older than the model's; or the user asks to integrate or update the harness.
---

# Recipe: Adoption / update

The reference model (`../worklaws/reference/model.md`) takes precedence over local setup. If something local looks better, record it as an improvement proposal for the retro; do not adopt it silently.

1. **◇ Mode:**
   - **Update** (`.claude/worklaws.json` already exists, older version): compare what is installed against the reference version and build a migration plan. Check with the user whether `docs/purpose.md` still holds; if not, do steps 3 and 4. Then jump to step 11.
   - **Adopt** (it does not exist): continue at step 2.
2. **Backup:** create the branch `chore/adopt-worklaws`. If there is no git, make a full copy of the workspace before touching anything.
3. **[W] Understand the purpose before the technology.** The harness adapts to *why* the project exists, not just to its configuration files. In parallel, review:
   - README, docs, specs and ADRs: the stated purpose.
   - Commit history: how it evolved and where it changed course.
   - Tracker, vault notes and available connectors (Jira, Confluence, Azure Boards): the business intent.
   - The code and the data: what it **actually** does.

   Do not trust the README without checking it: gaps between what is stated and what is real are a finding.
4. **[D] Purpose card** (`../worklaws/templates/purpose-card.md`) in `docs/purpose.md`: what for, for whom, success criteria, stage, non-goals, and gaps between what is stated and what is real.
   - **◇ [U] Is the card correct?** If not, fix it and ask again. Limit: 3 rounds. Without a confirmed card, do not continue.
5. **[W] Technical discovery in parallel** (Explore subagents, read-only). Review:
   - Stack and profiles per folder.
   - Real build, test and lint commands.
   - Conventions: structure, branches, remote and CI.
   - Documentation: README, ADRs, existing CLAUDE.md or AGENTS.md.
   - Tracker already in use.
   - Hooks, skills and settings already installed.
   - Project health: whether there are tests, coverage, and whether the build works.
   - Anything installed through your organization's managed settings is inventoried and marked in `managed_by_organization`. **It is not modified.**
6. **[W] Look for official plugins and connectors** for the project's stack and roles (sources in `../worklaws/reference/plugin-sources.md`). **[A] Security review** of each candidate.
7. **[A] Compare what was discovered against the reference model and the purpose:** which recipes, profiles and "done" criteria serve this goal. List the gaps.
8. **[D] Discovery report + gaps + recommended plugins.**
9. **[U] Ask only what could not be inferred.**
10. **[S] Integration proposal:**
   - `CLAUDE.md` **merged**, never overwritten, under 200 lines, starting with the purpose in 3 lines and a link to `docs/purpose.md`.
   - `.claude/worklaws.json` (template) with real profiles and commands.
   - Plugin hooks configured with those commands.
   - Tracker initialized or adapted.
   - Link to the vault.
   - Recommended official plugins. Only approved ones are installed, with `--scope project` if they belong to the project.
   - Initial knowledge registry, citing repo files as the source.
11. **[A] Proposal reviewer:** conflicts with existing hooks or CI and risks of breaking something. At most 2 rounds.
12. **◇ [U] Do you approve?** If not, go back to step 10.
13. **[S] Apply on the branch.** Every change to an existing file is presented as a diff. Finish with a PR.
14. **[A] Dry run:** simulate a session and check that SessionStart injects context, that the test hook runs, and that the Stop gate blocks when it should. If it fails, fix and repeat. At most 2 rounds; after that, [U].
15. **[D] Close:**
    - ADR "Harness adoption" with the model used and the human reviewer.
    - `harness_version` updated.
    - Run `session-close`.
