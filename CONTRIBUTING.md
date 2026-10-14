# Contributing to worklaws

Thanks for your interest. This repository is a Claude Code plugin: skills (recipes), agents, hooks and templates. Contributions are welcome through issues and pull requests.

## Before you start

- For anything beyond a small fix, open an issue first to discuss the change.
- Keep one topic per pull request.
- Hooks run code with the user's permissions, so changes under `hooks/` get the closest review.

## Set up

Requirements: Python 3.12 (standard library only) and, optionally, Claude Code to validate the plugin.

```bash
git clone https://github.com/romainhr/worklaws.git
cd worklaws
claude --plugin-dir .
```

## Run the checks

The CI runs the same three steps on every push and pull request. Run them locally before opening a PR:

```bash
python -m py_compile hooks/scripts/*.py
python -m unittest discover -s tests -v
claude plugin validate .
```

The CI also checks that `.claude-plugin/plugin.json`, `hooks/hooks.json` and `skills/worklaws/templates/*.json` are valid JSON.

## Guidelines

- **Tests:** new or changed hook behavior needs a test in `tests/test_hooks.py`. Do not reduce existing coverage.
- **Standard library only:** hook scripts must not add third-party dependencies.
- **Skills and recipes:** keep the `SKILL.md` frontmatter (`name`, `description`) accurate. The description is what triggers the skill, so say when it applies.
- **Never invent numbers:** usage figures (tokens, cost) come from telemetry, not from the model. Keep that rule in any recipe you touch.
- **Safety first:** validate inputs in hooks, keep risky-action control conservative, and do not weaken confirmations without a clear reason in the PR description.
- **Language:** write code, docs and commit messages in English.

## Secrets and private data

Do not commit credentials, tokens, `.env` files, keys, or any customer, company or production data. This is a public repository and the history is public.

## Pull requests

1. Fork the repository and create a branch from `main`.
2. Make the change, add or update tests, and run the checks above.
3. Open a pull request that explains what changed and why, and links the related issue.
4. The CI must pass before review.

## Reporting security issues

If you find a vulnerability (for example, a hook that can be abused), do not open a public issue. Use GitHub's private vulnerability reporting on this repository's Security tab, or contact the maintainer directly.
