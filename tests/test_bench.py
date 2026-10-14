"""Offline tests for the benchmark harness using a fake claude binary."""
import json, os, subprocess, sys, tempfile, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAKE = os.path.join(ROOT, "tests", "fake", "fake_claude.py")
ENV = {**os.environ, "CLAUDE_BIN": FAKE}

def sh(*args):
    return subprocess.run([sys.executable, *args], capture_output=True, text=True, env=ENV, cwd=ROOT, timeout=60)

class BenchTest(unittest.TestCase):
    def test_pipeline_run_judge_report(self):
        with tempfile.TemporaryDirectory() as d:
            p = sh("bench/run.py", "--reps", "2", "--out", d, "--tasks", "validation-review")
            self.assertEqual(p.returncode, 0, p.stderr)
            rows = [json.loads(l) for l in open(os.path.join(d, "runs.jsonl"))]
            self.assertEqual(sorted({r["condition"] for r in rows}), ["baseline", "plugin"])
            self.assertEqual(len(rows), 4)
            self.assertEqual(rows[0]["files_changed"], [])
            p = sh("bench/judge.py", d)
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertAlmostEqual(json.load(open(os.path.join(d, "scores.json")))[0]["score"], 0.6)
            p = sh("bench/report.py", d)
            self.assertIn("| validation | plugin | 2/2 |", p.stdout)

    def test_budget_hard_stop(self):
        with tempfile.TemporaryDirectory() as d:
            p = sh("bench/run.py", "--reps", "5", "--budget", "0.25", "--out", d, "--tasks", "validation-review")
            self.assertIn("budget reached", p.stdout)
            self.assertLess(len(open(os.path.join(d, "runs.jsonl")).readlines()), 10)

    def test_dry_run_spends_nothing(self):
        p = sh("bench/run.py", "--dry-run")
        self.assertIn("worst case", p.stdout)

if __name__ == "__main__":
    unittest.main()
