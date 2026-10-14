"""Blind judge: scores each run's output against the task rubric without knowing the condition.
Outputs are shown as an anonymous label; the mapping stays in the results dir.
The judge model should differ from the model under test (--judge-model) to limit self-preference bias.
Usage: python bench/judge.py <results_dir> --judge-model opus"""
import argparse, glob, json, os, random, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CLAUDE = os.environ.get("CLAUDE_BIN", "claude")

PROMPT = """You are a strict evaluator. Score the RESPONSE against each rubric item from 0 to 2
(0 = absent or wrong, 1 = partial, 2 = fully met). Be critical: do not give credit for items that are only implied.
Base the score only on the text of the RESPONSE. Ignore its length and formatting.
Return ONLY JSON: {{"scores": [<int per item, in order>], "notes": "<one sentence>"}}

TASK: {task}

RUBRIC:
{rubric}

RESPONSE:
<<<
{response}
>>>"""

def judge_one(task, response, model):
    rubric = "\n".join(f"{i + 1}. {r}" for i, r in enumerate(task["rubric"]))
    cmd = [CLAUDE, "-p", PROMPT.format(task=task["prompt"], rubric=rubric, response=response), "--output-format", "json",
           "--no-session-persistence", "--max-budget-usd", "0.5", "--disallowedTools", "*"]
    if model:
        cmd += ["--model", model]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    data = json.loads(p.stdout)
    m = re.search(r"\{.*\}", data.get("result", ""), re.S)
    parsed = json.loads(m.group(0))
    scores = parsed["scores"]
    if len(scores) != len(task["rubric"]) or not all(isinstance(x, int) and 0 <= x <= 2 for x in scores):
        raise ValueError(f"invalid scores: {scores}")
    return {"scores": scores, "score": sum(scores) / (2 * len(scores)), "notes": parsed.get("notes", ""), "judge_cost_usd": data.get("total_cost_usd")}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("results_dir")
    ap.add_argument("--judge-model", default="")
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    tasks = {}
    for p in glob.glob(os.path.join(HERE, "tasks", "*.json")):
        t = json.load(open(p, encoding="utf-8")); tasks[t["id"]] = t
    rows = [json.loads(l) for l in open(os.path.join(a.results_dir, "runs.jsonl"), encoding="utf-8")]
    order = list(range(len(rows))); random.Random(a.seed).shuffle(order)  # judge order is independent of condition
    out = []
    for n, i in enumerate(order):
        r = rows[i]
        entry = {"index": i, "label": f"R{n:03d}", "task": r["task"], "condition": r["condition"], "rep": r["rep"]}
        if r["ok"] and r.get("output"):
            try:
                entry.update(judge_one(tasks[r["task"]], r["output"], a.judge_model))
            except Exception as ex:
                entry["judge_error"] = repr(ex)
        else:
            entry["judge_error"] = "run failed or empty output"
        out.append(entry)
        print(entry["label"], entry.get("score"), entry.get("judge_error", ""))
    with open(os.path.join(a.results_dir, "scores.json"), "w", encoding="utf-8") as f:
        json.dump(sorted(out, key=lambda e: e["index"]), f, ensure_ascii=False, indent=1)

if __name__ == "__main__":
    main()
