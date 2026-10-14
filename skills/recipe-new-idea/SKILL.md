---
name: recipe-new-idea
description: Runbook for a new idea that has no project yet. Interview, parallel discovery, brief and SPEC in the vault, adversarial review and, if approved, repo scaffold in a new session.
when_to_use: The user brings a new idea they want to analyze, discuss or build, and there is no repo yet.
---

# Recipe: New idea

Before you start, read `../worklaws/reference/model.md`.

## Session A: analysis (main, Opus)
1. **[U] Interview** with AskUserQuestion: problem, user, scope, assumptions and profile.
   - Loop: repeat until all five points are answered. Cap: 3 rounds. After that, summarize what is missing and ask whether to proceed anyway.
2. **Check the knowledge registry** (skill `knowledge-registry`) on the topic. Reuse whatever is current.
3. **[W] Parallel discovery**, one `researcher` subagent per axis: state of the art · stack for the profile · risks.
   - In the POC profile, a single subagent is enough.
   - For internal topics, check your organization's internal platform index (if one exists) first.
4. **◇ Does the idea hold up?**
   - No → [D] archive the brief (`../worklaws/templates/brief.md`, status `archived`) in `vault/<project>/` and skip to the close.
   - Adjust → go back to step 1.
5. **[D] Write** the brief and `SPEC.md` in `vault/<project>/` using the templates. If there is an architecture decision, add an ADR.
6. **[A] Adversarial reviewer** on brief + SPEC (subagent `adversarial-reviewer`).
   - Loop: if there are critical findings, fix them and review again. At most 2 rounds; after that, [U] decides.
7. **◇ [U] Do we build it?**
   - No → it is logged in the vault backlog and you move to the close.
   - Yes → run `session-close` and ask the user to run `/clear` and open a **new session** with: "Scaffold <project> according to vault/<project>/SPEC.md".

## Session B: scaffold
8. **[S] Scaffold:**
   - `git init`, a `CLAUDE.md` under 200 lines and `.claude/worklaws.json` (template).
   - Copy `SPEC.md` into the repo.
   - Remote: GitHub for personal projects, Azure DevOps (work) for work projects.
9. **[S] Create the initial tasks** from the SPEC in the tracker (`bd create` if the tracker is Beads).
10. **Close:** run `session-close`. The next session starts with `recipe-continue-task`.
