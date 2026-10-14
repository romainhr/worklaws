# Benchmark: worklaws plugin vs plain Claude Code

Compares the same task run in two conditions: `baseline` (plain `claude -p`) and `plugin` (`--plugin-dir`, prompt routed through the recipe).
Everything is synthetic (`fixtures/`); never point it at real or customer data.

```bash
python bench/run.py --dry-run                       # plan + worst-case cost, spends nothing
python bench/run.py --reps 3 --budget 20            # real runs, hard stop at the measured budget
python bench/judge.py bench/results/<run> --judge-model opus   # blind rubric scoring
python bench/report.py bench/results/<run>          # Markdown table
```

## What is measured
Cost, tokens (output, cache write), turns and wall time come from Claude Code's JSON output; nothing is estimated.
Quality is a 0-1 score from a blind LLM judge on a fixed rubric (`tasks/*.json`), plus cost per quality point.

## Known limits (read before drawing conclusions)
- **Small n.** 3 reps per cell show a trend, not significance. Use 5+ before claiming a difference.
- **LLM judge is a proxy.** Use a different model than the one under test, and spot-check scores by hand.
- **Rubrics were written by the plugin author**, who may unconsciously favour what the plugin does. Review them.
- **Environment leaks into both conditions** (user/org settings, CLAUDE.md, managed hooks). Run both from the same machine and account.
- **Headless mode:** a hook `ask` cannot be answered in `-p`, so flows that need approval measure the denied path. Current tasks are read-only to avoid this; session-close overhead is not covered yet.
- **Only two flows** (validation, new-feature) with one task each; results do not generalise to the other 21 recipes.
- Conditions are interleaved per repetition to spread drift; the baseline is also not "prompt-engineered", so a good hand-written prompt may close the gap.

Offline tests use `tests/fake/fake_claude.py` (`CLAUDE_BIN`), so CI spends nothing.
