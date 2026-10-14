---
name: recipe-explore-organize
description: Runbook for exploring and organizing a workspace with many skills, commands, agents, workflows, hooks and connectors. First the purpose map (roles and project portfolio), then a read-only inventory, evaluation against the reference and the purposes, a map, and optionally consolidation into a custom plugin without deleting anything.
when_to_use: The user wants to see what they have installed, detect duplicates or skills that are not useful, clean up their configuration, or build their plugin from what already exists. Also with /recipe-explore-organize explore|organize.
argument-hint: "[explore|organize] [path or scope]"
---

# Recipe: Explore / Organize

1. **[U] Scope:** what gets reviewed: `~/.claude`, one or more repos, the vault, the MCP connectors. Also ask for the mode: **explore** (read-only) or **organize**.
2. **Load the reference model** (`../worklaws/reference/model.md`). It is the source of truth.
3. **Full backup** before any change: commit if there is git, a copy if not. Everything must be undoable.
4. **[W] Understand the purpose of the workspace** before looking at artifacts:
   - The person's roles and recurring work.
   - Project portfolio: what each one is for and what stage it is in, using README, history, vault and connectors.
   - Write it up as a purpose map (a short card per project, template `purpose-card.md`).
   - **◇ [U] Is the purpose map correct?** If not, fix it. Limit: 3 rounds.
5. **[W] Inventory in parallel**, read-only, one subagent per type:
   - skills and commands (user, project, nested, plugins);
   - subagents;
   - workflows (`.claude/workflows`, `~/.claude/workflows`);
   - hooks (every `settings.json`, plugin `hooks/hooks.json`, skill and agent frontmatter);
   - CLAUDE.md and `.claude/rules`;
   - MCP and connectors;
   - output styles;
   - installed plugins.

   For each artifact, record: type, path, scope, name, description and last modified date.
6. **[A] Evaluate each artifact against the reference and the purpose map:**
   - **Which active purpose does it serve?** If none (abandoned or unused project), it is a candidate for archiving.
   - **Is it used?** Use real usage if there is telemetry (`skill.name` and `agent.name` attributes). If there is no data, mark it as "no usage data"; do not assume.
   - **Does it follow the model's pattern** (legend, loops with a limit, single reviewer, close)?
   - **Duplicates and overlaps.**
   - **Name or precedence conflicts.**
   - **Broken artifacts.**
   - **Context cost:** descriptions are loaded in every session.
   - If something local is **better** than the reference, record it as an improvement proposal for the retro.
7. **[W] Look for official plugins and connectors** for each role and tool detected (for example, finance role → `finance` plugin; uses Fabric → Fabric MCP). Sources and order of preference in `../worklaws/reference/plugin-sources.md`.
   - **[A] Security review** of each candidate: origin, what it runs and context cost. In corporate environments, only approved tools are recommended.
8. **[D] Purposes ↔ artifacts map + gap matrix + recommended plugins** in `vault/harness/explorations/<date>.md`.
9. **◇ [U] Explore only?** If so, stop here and run `session-close`.
10. **[A] Propose a destination for each artifact:** Keep · Adapt · Merge · Promote to the plugin · Fix · Archive · Review · **Install** (for recommended official plugins).
11. **◇ [U] Approval per batch**, by category. If not approved, adjust and go back to step 10.
12. **[S] Build the custom plugin** with what is kept, adapted and promoted, plus what the reference requires and is missing. Work on a branch. Install **only** the approved official plugins (`claude plugin install <plugin>@<marketplace>`).
13. **[S] Archive: move, never delete.**
    - Destination: `_archive/<date>/`, **outside the paths Claude loads**.
    - Write the manifest (template `archive-manifest.md`): original path, reason and how to restore.
    - Anything installed through your organization's managed settings is not modified or disabled.
14. **[A] Validate with a test session:** skills load, hooks do not fail, and `/context` is compared before and after. If it fails, go back to step 12. At most 2 rounds.
15. Run `session-close` (includes the plugin version). Next step: `recipe-adoption` in each project.
