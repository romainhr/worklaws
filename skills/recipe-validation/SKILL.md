---
name: recipe-validation
description: Runbook for validating a project (security, tests and coverage, figures/data, ADRs, documentation). Parallel reviewers per dimension, verification of every finding, report and tasks.
when_to_use: The user asks to test, audit, validate or review the quality of a project or a piece of research.
---

# Recipe: Validation

1. **[U] What is being validated?** Options: security · tests/coverage · data/figures (BI and Fabric profiles) · ADRs · documentation · everything. The criteria for each profile are in `../worklaws/reference/profiles.md`.
2. **[W] One reviewer per dimension**, in parallel (subagents; use a workflow only if ultracode is available). Each one returns findings with evidence: file, line, reproducible command.
3. **[A] Verify every finding** with a verifier different from the reviewer who found it. Discard false positives.
4. **◇ Are there confirmed findings?**
   - No → [D] "validation OK" report and move to the close.
5. **[D] Findings report** in `docs/validations/<date>.md`, or in the vault if it is research.
6. **[U] Prioritize:** the user ranks the findings.
7. **[D] Create the tasks** in the tracker. Once they are done, the same dimension is validated again.
8. Run `session-close`.
