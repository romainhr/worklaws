---
name: recipe-onboarding
description: First-time runbook for the plugin. Asks about role, team and tools, prepares the workspace, explores in read-only mode, recommends official plugins by role and tool with a security review, seeds context and gives a guided tour.
when_to_use: It is the person's first time using the plugin, or they ask to configure it for their role. Also with /recipe-onboarding.
---

# Recipe: Plugin onboarding

1. **[U] Role, team, responsibilities** and the tools or systems they use.
2. **Prepare the workspace** with `prepare-workspace`: user configuration, vaults and tracker.
3. **Explore** with `recipe-explore-organize` in **explore-only** mode: map of purposes and artifacts.
4. **[A] Recommended official plugins** based on role and tools (`../worklaws/reference/plugin-sources.md`), with their security review.
5. **◇ [U] Install the recommendations?** If yes, only what is approved is installed.
6. **[D] Context seed** in the user CLAUDE.md (`~/.claude/CLAUDE.md`), in under 30 lines:
   - role glossary;
   - priorities;
   - communication style.
7. **Guided tour:** 3 recipes useful for their role, each tried with one of their real cases.
8. Run `session-close`. From there, the router (`worklaws`) takes over.
