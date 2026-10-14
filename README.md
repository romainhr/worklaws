# worklaws-plugin: Claude Code work runbooks

Worklaws is a Claude Code plugin that turns work processes designed as flowcharts into **runbooks** that Claude understands and runs: a router that classifies the intent and one recipe per type of work, plus the mandatory session close (report with usage, handoff, and retro).

## Install

This repository is the plugin itself (no marketplace manifest). Clone it and load it:

```bash
git clone https://github.com/romainhr/worklaws.git
claude --plugin-dir ./worklaws
```

Once installed, every skill carries the plugin prefix: `/worklaws-plugin:recipe-new-idea`. The table below omits the prefix for readability.

## Quick start

| You want to… | Type |
|---|---|
| Let Claude choose the recipe | `/worklaws <your request>` (or just ask; the SessionStart hook tells Claude to use the router) |
| Analyze a new idea | `/recipe-new-idea` |
| Continue with the next task | `/recipe-continue-task` |
| Design a feature (no code) | `/recipe-new-feature` |
| Validate or audit | `/recipe-validation` |
| Research or study | `/recipe-research` |
| Bring the harness into a project or update it | `/recipe-adoption` |
| Explore or organize your configuration and build the plugin (includes official plugins recommended by role and tool) | `/recipe-explore-organize explore ~/.claude` |
| Get unstuck with guided creativity | `/recipe-unstuck` |
| Deploy, publish, or send a deliverable | `/recipe-deliver` |
| Create a harness for a domain or role | `/recipe-create-harness` |
| Change an existing harness (including this plugin) | `/recipe-edit-harness` |
| Critically audit your AI use | `/recipe-ai-audit 30d` |
| Draft and send with approval | `/recipe-communicate` |
| Status report | `/recipe-status-report` |
| Organize the inbox and prioritize | `/recipe-triage` |
| Meeting brief or minutes | `/recipe-meetings before|after <event>` |
| Incident and postmortem | `/recipe-incident` |
| Maintenance (dependencies, debt, overdue items) | `/recipe-maintenance` |
| Daily brief (ideal as a scheduled task) | `/recipe-daily-brief` |
| Weekly review | `/recipe-weekly-review` |
| First time with the plugin | `/recipe-onboarding` |
| Hand a project over to another person | `/recipe-handover <project> <person>` |
| Test changes to skills or recipes | `/recipe-evals` |
| Prepare vault, tracker, and configuration | `/prepare-workspace` |
| End the session | `/session-close` |

## Structure

```
.claude-plugin/plugin.json
skills/
  worklaws/                  router + reference/ (model, profiles) + templates/
  recipe-*/SKILL.md          one runbook per recipe (23)
  prepare-workspace/         T0: user config, vault, tracker
  new-request/               T3: mid-session requests
  session-close/             report + handoff + retro
  knowledge-registry/        anti-bias rules (loaded by Claude, not user-invocable)
agents/
  adversarial-reviewer.md    [A] steps
  researcher.md              [W] research and blind verification steps
hooks/
  hooks.json                 SessionStart · UserPromptSubmit (new request) · PreToolUse (action control)
                             · PostToolUse(Edit|Write) · Stop · SessionEnd
  scripts/*.py               Python 3 standard library only
```

**Action control (T1):** the `action_control.py` hook asks for confirmation on irreversible or external actions (push, delete, publish, deploy, send through connectors) and records everything in `.claude/state/log.jsonl`. It never approves anything automatically.

**Mid-session requests (T3):** if a recipe is active, the `UserPromptSubmit` hook reminds Claude to apply `new-request`:
- Side question → `/btw`.
- Small task → done right away.
- Large task → captured in the tracker and continued after finishing, in parallel (read-only, with `claude -p`), or in a worktree (`claude -w`).

**Workspace preparation (T0):** no recipe writes to a vault or tracker that does not exist. `prepare-workspace` creates them with approval; the user configuration goes in `~/.claude/worklaws-user.json`.

**Official plugins:** `skills/worklaws/reference/plugin-sources.md` lists the verified marketplaces and vendors and the mandatory security review before recommending or installing.

Runbook legend: **[U]** user/approval · **[W]** parallel · **[S]** procedure · **[A]** adversarial · **[D]** document · **[H]** hook. Details in `skills/worklaws/reference/model.md`.

## Installation (development)

```bash
claude --plugin-dir /path/to/worklaws-plugin
```

For each project, run `/recipe-adoption`, which creates `.claude/worklaws.json` from `skills/worklaws/templates/worklaws.json`.

## How the strict close works

- The `Stop` hook fires at the end of **every response**, so it cannot demand a report on every turn. The design is:
  1. The router records `.claude/state/active-recipe`.
  2. `session-close` writes `.claude/sessions/pending.md` with the `<USAGE>` marker.
  3. `Stop` fills in usage from telemetry, archives the report, and blocks if the handoff is missing.
  4. If the session ends without a close, `SessionEnd` records it and the next `SessionStart` warns about it.
- **Usage (tokens and cost):** `hooks/scripts/usage_report.py` reads a normalized JSONL of OpenTelemetry `claude_code.api_request` events from `WORKLAWS_USAGE_SOURCE`. If there is no source, it writes "no telemetry data" and **never estimates**.

## Pending / assumptions to verify before serious use

- [ ] Confirm in the hooks documentation the `CLAUDE_PLUGIN_ROOT` and `CLAUDE_PROJECT_DIR` variables and the `session_id` field in the Stop and SessionEnd inputs.
- [ ] Set up telemetry: `CLAUDE_CODE_ENABLE_TELEMETRY=1` + an OTel logs exporter + an adapter that produces the normalized JSONL (requires an approved tool). It is still unconfirmed how events are grouped by session.
- [ ] Confirm that the tracker is Beads (`bd`). If it is not, change the commands in the recipes.
- [ ] AI audit: today the log records when confirmation was requested, but not whether it was approved or rejected. That data still needs to be added, for example with the `PermissionDenied` hook or a record in `PostToolUse`.
- [ ] Adjust the `action_control.py` patterns to each team's real commands. They are heuristic.
- [ ] Launching in parallel with `claude -p` consumes tokens separately. Review the cost in the audit.
- [ ] In corporate environments: the plugin must coexist with the hooks installed through your organization's managed settings, and using it may require approval from your governance/security team.

## Diagrams

The diagrams (router, recipes 1–8, R0, RL, T1, T2, and the ecosystem map) are published with the plugin page as flowcharts.
