# Worklaws reference model (v0.3.1)

This is the harness's source of truth. If something local contradicts this model, the model wins.
If the local version looks better, it is not adopted silently: it is recorded as an improvement proposal in the retro.

## Three axes
- **Verb** (what is done): Research · Create · Validate · Document.
- **Destination** (where the result lands): current project · reusable knowledge · new idea · personal learning.
- **Profile** (stack): see `profiles.md`. In existing projects it is read from `.claude/worklaws.json`.

## Step legend (used the same way in every runbook)
| Tag | Meaning | How it runs |
|---|---|---|
| [U] | User question or approval | AskUserQuestion tool. Never assume an approval. |
| [W] | Parallel work | Subagents in parallel. Use a workflow only if the user enabled ultracode. |
| [S] | Defined procedure | Follow the indicated runbook or skill. |
| [A] | Adversarial review | `adversarial-reviewer` subagent in a clean context. |
| [D] | Document | Write using the matching template from `../templates/`. |
| [H] | Hook | Automatic; the runbook only states what to expect. |

## Cross-cutting rules (mandatory)
1. Back-and-forth with the user happens in the main session. Subagents and workflows are used only for parallel, independent work.
2. One session equals one task or recipe. New requests mid-session go through `new-request` (T3). When finished, run `session-close` and then `/clear`. Prefer `/clear` over `/compact`.
3. Plan mode only when the change does not fit in one sentence.
4. Adversarial review: a single reviewer, focused on correctness and requirements, with a maximum of 2 rounds. After that, escalate to the user.
5. Loops: always with a measurable exit criterion and a cap. If a fix fails twice, propose `/clear` and a better prompt.
6. Before researching, consult the knowledge registry (skill `knowledge-registry`). Only research what is missing, expired, or disputed.
7. Archiving means moving, never deleting.
8. Usage numbers (tokens, cost) are never written by the model; they come from telemetry.
9. Architecture decisions produce an ADR that states the model used and the human reviewer.
10. In corporate environments, anything installed through your organization's managed settings is not modified or disabled.

## Recipes (runbooks)
| Family | Recipes |
|---|---|
| Think | `recipe-new-idea` · `recipe-unstuck` |
| Understand | `recipe-research` · `recipe-explore-organize` |
| Build | `recipe-new-feature` · `recipe-continue-task` · `recipe-create-harness` · `recipe-edit-harness` |
| Deliver | `recipe-deliver` · `recipe-communicate` · `recipe-status-report` |
| Operate | `recipe-triage` · `recipe-meetings` · `recipe-incident` · `recipe-maintenance` |
| Rhythm | `recipe-daily-brief` · `recipe-weekly-review` |
| People | `recipe-onboarding` · `recipe-handover` |
| Improve the system | `recipe-validation` · `recipe-ai-audit` · `recipe-evals` · `recipe-adoption` |

The detailed routing table is in the `worklaws` skill.

## Cross-cutting steps
- **T0 · Workspace preparation** (`prepare-workspace`): no recipe writes to a vault or tracker that does not exist. If one is missing, it is created with approval.
- **T3 · New request mid-session** (`new-request` + UserPromptSubmit hook):
  - Side question → `/btw`.
  - Small task → done right away.
  - Large task → captured and moved to another session: after finishing, in parallel (read-only `claude -p`), or in a worktree.
- **T1 · Risk-based action control** (PreToolUse hook `action_control.py`):
  - **Read:** no intervention.
  - **Reversible write:** recorded in the log.
  - **Irreversible or external** (push, publish, send, delete, deploy, pay): asks for confirmation (`ask`) and records it.
  - The hook **never** returns `allow`: it only adds friction, it does not remove permissions.
- **T2 · Close:** report with usage, handoff, retro, and knowledge registry (`session-close`).

## Official plugins by role and tool
The exploration, adoption, and harness-creation recipes recommend official plugins and connectors according to `plugin-sources.md`. They always go through a security review and user approval.
