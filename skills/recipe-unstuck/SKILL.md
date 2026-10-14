---
name: recipe-unstuck
description: Creative runbook for when the user is stuck on a project. Diagnoses the blocker, diverges in parallel with different approaches (analogies with real references, inversion, extreme constraints, extreme user, first principles, cross-check with the vault), converges on a top 3 with minimal experiments and routes to the next recipe.
when_to_use: The user says they are stuck, does not know how to proceed, asks for ideas or wants the AI to be creative with the project. Also with /recipe-unstuck.
---

# Recipe: Get unstuck (creative)

1. **Diagnosis:** read the handoff, the blocked tasks, the latest retros and the purpose card. State in **one sentence** where the blocker is.
2. **◇ [U] Is that the blocker?** If not, rephrase. Cap: 3 rounds.
3. **Check** the knowledge registry and the idea bank (`vault/<project>/idea-bank.md`). Do not repeat ideas that were already discarded without a new reason.
4. **[W] Parallel divergence:** one subagent per approach, each with the same blocker sentence and **without seeing the others' ideas**. Diversity comes from different approaches, not from temperature.
   - **Analogies:** how something similar was solved in other industries. Use the `researcher` subagent; only real references with a URL count.
   - **Inversion:** how would I make the project fail? Then flip each answer.
   - **Extreme constraints:** what if there were 1 day? What if there were 10 times the budget? What about no code?
   - **Extreme user:** the most expert and the most novice.
   - **First principles:** what is true without inherited assumptions.
   - **Cross-check with the vault:** connections with the user's other ideas and projects.
5. **Generate at least 15 options** without judging them.
6. **Converge:** group, score (impact · effort · novelty, from 1 to 5) and pick the **top 3**. Each top 3 option comes with a **minimal experiment**: what is tested, how it is measured and how long it takes.
7. **[A] Devil's advocate** on the top 3 (`adversarial-reviewer`, in "why would this fail" mode).
8. **◇ [U] Which one do we pursue?** If none appeals, go back to step 4 with new approaches. At most 2 rounds.
9. **[D] Idea bank:** add **all** options to `vault/<project>/idea-bank.md`, with score and status (chosen, discarded with reason, pending). Nothing is lost.
10. **Which recipe comes next?**
    - Validate a technique → `recipe-research` (technical variant, as a spike).
    - Project improvement → `recipe-new-feature`.
    - New project → `recipe-new-idea`.

    Run `session-close` and start that recipe in a new session.
