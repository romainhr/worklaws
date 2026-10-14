"""Aggregates runs.jsonl (+ scores.json) into a Markdown comparison: baseline vs plugin, per flow.
Reports mean and standard deviation with n; with small n differences are indicative, not significant.
Usage: python bench/report.py <results_dir>"""
import json, os, statistics as st, sys
from collections import defaultdict

def ms(xs):
    xs = [x for x in xs if x is not None]
    if not xs: return "n/a"
    return f"{st.mean(xs):.4g} ± {st.stdev(xs):.2g}" if len(xs) > 1 else f"{xs[0]:.4g}"

def main(d):
    rows = [json.loads(l) for l in open(os.path.join(d, "runs.jsonl"), encoding="utf-8")]
    sp = os.path.join(d, "scores.json")
    scores = {(s["task"], s["condition"], s["rep"]): s.get("score") for s in json.load(open(sp, encoding="utf-8"))} if os.path.exists(sp) else {}
    g = defaultdict(list)
    for r in rows:
        r["score"] = scores.get((r["task"], r["condition"], r["rep"]))
        g[(r["flow"], r["condition"])].append(r)
    lines = ["| Flow | Condition | n (ok/total) | Cost USD | Output tok | Cache-write tok | Turns | Wall s | Quality 0-1 | USD per quality pt |", "|---|---|---|---|---|---|---|---|---|---|"]
    for (flow, cond), rs in sorted(g.items()):
        ok = [r for r in rs if r["ok"]]
        q = [r["score"] for r in ok if r["score"] is not None]
        cpq = [r["cost_usd"] / r["score"] for r in ok if r["score"] and r["cost_usd"]]
        lines.append(f"| {flow} | {cond} | {len(ok)}/{len(rs)} | {ms([r['cost_usd'] for r in ok])} | {ms([r['output_tokens'] for r in ok])} | "
                     f"{ms([r['cache_creation_tokens'] for r in ok])} | {ms([r['turns'] for r in ok])} | {ms([r['wall_s'] for r in ok])} | {ms(q)} | {ms(cpq)} |")
    lines += ["", "Cost and tokens are as reported by Claude Code (`total_cost_usd`, `usage`); failed runs are excluded from means but counted in n.",
              "Quality is a blind LLM-judge score against a fixed rubric; it is a proxy and should be spot-checked by a human."]
    out = "\n".join(lines)
    open(os.path.join(d, "report.md"), "w", encoding="utf-8").write(out + "\n")
    print(out)

if __name__ == "__main__":
    main(sys.argv[1])
