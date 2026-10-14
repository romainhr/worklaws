"""Benchmark runner: the same task with plain Claude Code (baseline) vs the worklaws plugin.
Each run uses a fresh copy of a synthetic fixture and `claude -p --output-format json`.
Cost and tokens come from Claude Code's own output; nothing is estimated.
Usage: python bench/run.py --reps 3 --budget 20 [--tasks id,id] [--model sonnet] [--dry-run]"""
import argparse, glob, hashlib, json, os, shutil, subprocess, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
PLUGIN = os.path.dirname(HERE)
CLAUDE = os.environ.get("CLAUDE_BIN", "claude")
CONDITIONS = ("baseline", "plugin")

def load_tasks(ids):
    tasks = [json.load(open(p, encoding="utf-8")) for p in sorted(glob.glob(os.path.join(HERE, "tasks", "*.json")))]
    return [t for t in tasks if not ids or t["id"] in ids]

def build_cmd(task, cond, model, max_run_usd):
    cmd = [CLAUDE, "-p", task["plugin_prompt"] if cond == "plugin" else task["prompt"], "--output-format", "json",
           "--max-budget-usd", str(max_run_usd), "--no-session-persistence", "--permission-mode", "acceptEdits"]
    if model:
        cmd += ["--model", model]
    if cond == "plugin":
        cmd += ["--plugin-dir", PLUGIN]
    return cmd

def snapshot(d):
    out = {}
    for dp, _, fs in os.walk(d):
        for f in fs:
            fp = os.path.join(dp, f)
            out[os.path.relpath(fp, d)] = hashlib.sha256(open(fp, "rb").read()).hexdigest()
    return out

def run_one(task, cond, rep, model, max_run_usd, outdir):
    work = tempfile.mkdtemp(prefix="wlbench-")
    try:
        shutil.copytree(os.path.join(HERE, "fixtures", task["fixture"]), work, dirs_exist_ok=True)
        before = snapshot(work)
        t0 = time.time()
        p = subprocess.run(build_cmd(task, cond, model, max_run_usd), cwd=work, capture_output=True, text=True, timeout=1500)
        wall = time.time() - t0
        try:
            data = json.loads(p.stdout)
        except ValueError:
            data = {"error": "unparseable output", "stdout": p.stdout[:500], "stderr": p.stderr[:500]}
        u = data.get("usage") or {}
        row = {"task": task["id"], "flow": task["flow"], "condition": cond, "rep": rep, "model": model, "ok": p.returncode == 0 and "error" not in data and not data.get("is_error"),
               "cost_usd": data.get("total_cost_usd"), "input_tokens": u.get("input_tokens"), "output_tokens": u.get("output_tokens"),
               "cache_read_tokens": u.get("cache_read_input_tokens"), "cache_creation_tokens": u.get("cache_creation_input_tokens"),
               "turns": data.get("num_turns"), "duration_ms": data.get("duration_ms"), "wall_s": round(wall, 1), "output": data.get("result", ""),
               "files_changed": sorted(k for k, v in snapshot(work).items() if before.get(k) != v),
               "raw_error": data.get("error")}
        with open(os.path.join(outdir, "runs.jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
        return row
    finally:
        shutil.rmtree(work, ignore_errors=True)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--budget", type=float, default=20.0, help="hard stop for the whole run (USD, measured)")
    ap.add_argument("--max-run-usd", type=float, default=1.5, help="per-run cap passed to claude")
    ap.add_argument("--tasks", default="")
    ap.add_argument("--model", default="")
    ap.add_argument("--out", default="")
    ap.add_argument("--dry-run", action="store_true", help="print the plan and worst-case cost, spend nothing")
    a = ap.parse_args()
    tasks = load_tasks(set(filter(None, a.tasks.split(","))))
    n = len(tasks) * len(CONDITIONS) * a.reps
    print(f"{n} runs; worst case before judging: ${n * a.max_run_usd:.2f}; hard stop at ${a.budget:.2f}")
    if a.dry_run:
        for t in tasks:
            for c in CONDITIONS:
                print(" ", t["id"], c, " ".join(build_cmd(t, c, a.model, a.max_run_usd)[:3]) + " ...")
        return
    outdir = a.out or os.path.join(HERE, "results", time.strftime("%Y%m%d-%H%M%S"))
    os.makedirs(outdir, exist_ok=True)
    spent = 0.0
    # interleave conditions per repetition so drift (load, model changes) hits both equally
    for rep in range(a.reps):
        for t in tasks:
            for c in CONDITIONS:
                if spent >= a.budget:
                    print(f"budget reached (${spent:.2f}); stopping"); print(outdir); return
                r = run_one(t, c, rep, a.model, a.max_run_usd, outdir)
                spent += r["cost_usd"] or 0.0
                print(f"{t['id']} {c} rep{rep} ok={r['ok']} cost={r['cost_usd']} spent=${spent:.2f}")
    print(outdir)

if __name__ == "__main__":
    main()
