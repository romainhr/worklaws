---
name: recipe-research
description: Runbook for researching or studying, inside or outside a project. Exploratory, applied, technical, diagnostic, decision and learning variants; checks the knowledge registry first and verifies sources.
when_to_use: The user wants to research, study, evaluate a tool, understand why something happens or choose between options (for example, which measures to add to an analysis or the best way to create items in Fabric).
---

# Recipe: Research / Study

1. **[U] Define the question, variant and destination** with AskUserQuestion. Only ask what cannot be inferred from the request.

   | Variant | Typical question | Destination of the result |
   |---|---|---|
   | exploratory | Is this idea worth it? | New idea → may move on to `recipe-new-idea` |
   | applied | How do I improve X in this project? | Current project → options + recommendation → `recipe-new-feature` |
   | technical | What is the best way to do X with tool Y? | Reusable knowledge → guide + profile rule |
   | diagnostic | Why does X happen? | Current project → root cause → task |
   | decision | A or B? | ADR |
   | learning | I want to master topic Z | Personal learning → notes + self-assessment |

2. **Check the knowledge registry** (skill `knowledge-registry`). Reuse whatever is current and not expired. Only research what is missing, expired or disputed.
3. **Execute according to the variant:**
   - **Not learning:**
     - [W] Launch `researcher` subagents in parallel, one per independent sub-question. With ultracode you can use a deep-research workflow.
     - In the technical variant, set a bounded time box (spike): when it expires, decide with whatever you have.
   - **Learning:**
     1. Load the material (`vault/<course or topic>/`).
     2. Build a summary and a concept map.
     3. [U] Self-assessment with practice questions; active recall is worth more than rereading.
     4. Loop until the user says they have mastered the topic. Cap: 3 rounds per session. After that, schedule a spaced review.
4. **[A] Verify the sources:** separate facts from assumptions. Every claim carries its source and confidence level. Anything that cannot be verified is marked **unverified**.
5. **[D] Write the result according to the destination:**
   - **Vault note:** `vault/<topic>/`, with citations.
   - **New claims:** go to the knowledge registry (template `claim.md`).
   - **Technical variant:** propose [U] turning the guide into a profile rule or a skill.
   - **Decision variant:** ADR.
6. **◇ [U] Does it trigger another recipe?** For example, the exploratory variant leads to a new idea and the applied variant to a new feature. If so, run `session-close` and start that recipe in a new session.
7. Run `session-close`.
