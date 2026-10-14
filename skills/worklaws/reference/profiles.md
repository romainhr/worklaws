# Profiles

Each profile defines two things: what **validate** means and when something is **done**.

| Profile | Validate | Done when |
|---|---|---|
| web | Unit and e2e tests, OWASP review | Tests green, review approved, test deploy OK |
| bi | Reconcile figures against the source; explicit metric definitions | Numbers reconciled and assumptions documented |
| fabric | Data quality, measures against expected values, dev/prod separation | Pipeline or model validated in dev |
| poc | Minimal: the demo works | Demo + learnings + decision to continue or drop (time-boxed) |
| research | Verified sources; facts separated from assumptions | Note with citations and confidence level |
| study | Self-assessment (retrieval practice) | Mastery declared after self-assessment + review notes |

A project can have several profiles. In that case they are defined per folder in `.claude/worklaws.json` → `profiles[].paths`.
