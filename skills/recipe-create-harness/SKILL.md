---
name: recipe-create-harness
description: Runbook for creating a harness (a plugin of skills, agents, hooks and knowledge) for a new domain or role. Purpose, sources and connectors, security review, domain knowledge, design, evals against a baseline, pilot and release as a versioned plugin.
when_to_use: The user wants to build a harness or specialized assistant for a team, a role or a domain (for example, analysts querying a semantic model). Also with /recipe-create-harness.
---

# Recipe: Create harness

1. **[U] Harness purpose** (template `../worklaws/templates/purpose-card.md`): domain, users, decisions it must support and measurable success criteria.
2. **[W] Inventory of sources and tools:** available data, systems and MCP connectors. Include the **official plugins by role and tool** (`../worklaws/reference/plugin-sources.md`); do not rebuild what already exists.
3. **[A] Security review** of each plugin or connector: origin, what it executes and context cost. In corporate environments, approval from your governance/security team is required and production data is never used during development.
4. **[D] Domain knowledge** into the registry (`knowledge-registry`): glossary, metrics and business rules, each with its source.
5. **[S] Design the harness:**
   - Skills with the role's procedures (short description, use case first).
   - Agents with restricted tools.
   - Control hooks.
   - Profiles.

   Reuse the legend and rules from `../worklaws/reference/model.md`.
6. **[S] Evals:**
   - Build between 20 and 50 cases **taken from real failures** or real user questions.
   - Run each case with and without the harness (baseline). Define how it is graded (code, model or human) before running.
   - If Anthropic's `skill-creator` skill is used for the evals, do so only with approval.
7. **◇ Does it beat the baseline?** If not, go back to step 5. Cap: 3 iterations; after that, [U] decides.
8. **[U] Pilot** with real users: measure usage, errors, corrections and cost, using the session report.
9. **◇ [U] Publish?** If not, go back to step 5 with the findings.
10. **[S] Package** as a versioned plugin (`.claude-plugin/plugin.json`) in a private marketplace or repo. **[D] ADR** for the decision, with the model used and the human reviewer.
11. Run `session-close`. Next step: `recipe-adoption` in each team.
