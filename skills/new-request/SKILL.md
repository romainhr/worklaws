---
name: new-request
description: Cross-cutting step T3. When the user asks for something else in the middle of a recipe, decides whether it is a side question, a small task done right away, or a large task that is captured and taken to another session (when done, in parallel with a read-only claude -p, or in a worktree).
when_to_use: There is an active recipe (.claude/state/active-recipe) and the user asks for something that is not part of it. The UserPromptSubmit hook reminds you.
---

# T3 · New request mid-session

Goal: do not mix tasks in the same session ("kitchen-sink sessions" degrade quality and cost) **without losing the request**.

1. **◇ Is it a side question** that requires no work? For example, "what did this command do?".
   - Yes → answer it in 1 to 3 lines or suggest `/btw`, which answers without entering the history. Continue with the recipe.
2. **◇ Is it small?** It must meet **all** of the following:
   - fits in one sentence;
   - takes less than 5 minutes;
   - uses the same context and the same files;
   - does not involve an irreversible action.

   If it does → do it now, note it in the session report as an "interleaved task", and return to the recipe.
3. **If it is not small: capture it.** Create the task in the tracker with the **suggested recipe** and a 3 to 5 line context note, enough to pick it up without this conversation.
4. **◇ [U] How do we continue?** Offer three options:
   - **a) Finish the current recipe first** (recommended). At the end, `session-close`, `/clear` and a new session with the captured task.
   - **b) In parallel:**
     - **Read-only and bounded** (research, explore, summarize) → launch it in the background with [S]:
       ```bash
       mkdir -p .claude/parallel
       nohup claude -p "<self-contained prompt with the task and the output path>" \
         --allowedTools "Read,Grep,Glob,WebSearch,WebFetch" \
         --permission-mode dontAsk > .claude/parallel/<id>.md 2>&1 &
       ```
       Say that it runs in parallel and **consumes tokens separately**. The result lands in `.claude/parallel/<id>.md` and is reviewed when the recipe ends.
     - **Writes code or has side effects** → it is not launched on its own. Propose a new session in a worktree that the user opens: `claude -w <name>`, with the prompt from the context note. That way files do not collide.
   - **c) Pause the current one:** partial `session-close` (handoff with status "paused") and switch tasks.
5. Return to the active recipe, or close it if option c was chosen.

**Rules:**
- Never launch in parallel anything that writes, sends or deploys.
- Never discard a request: if it is not done now, it stays in the tracker.
