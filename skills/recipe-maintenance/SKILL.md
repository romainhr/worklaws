---
name: recipe-maintenance
description: Periodic maintenance runbook. Scans outdated dependencies, security advisories, technical debt, expired knowledge and stale documentation; classifies by risk and handles them in small batches with tests and one PR per batch.
when_to_use: The user asks to update dependencies, pay down technical debt, or review expired knowledge or documentation. Also with /recipe-maintenance or as a monthly scheduled task.
---

# Recipe: Maintenance

1. **[W] Scan in parallel:**
   - outdated dependencies and security advisories (using the profile's ecosystem commands);
   - technical debt (TODO/FIXME, dead code);
   - **expired claims** in the knowledge registry (`expires` field);
   - stale documentation.
2. **Classify by risk:** security > broken > expired > improvement.
3. **◇ [U] What gets handled in this cycle?**
4. **Group into small batches** by risk. Each batch must be revertible on its own.
5. **[S] For each batch:**
   - branch, change and tests (as in `recipe-continue-task`);
   - expired knowledge is re-verified with `knowledge-registry`.
6. **◇ Do the tests pass?**
   - No → revert the batch and create a task.
   - Yes → [S] open one PR per batch. Push requires confirmation (T1).
7. Run `session-close`.
