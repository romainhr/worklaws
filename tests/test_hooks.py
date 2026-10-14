"""Tests for the worklaws-plugin hooks. Standard library only: python -m unittest discover -s tests"""
import json, os, subprocess, sys, tempfile, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "hooks", "scripts")


def run(script, payload, project, extra_env=None):
    env = {**os.environ, "CLAUDE_PROJECT_DIR": project, "HOME": project}
    env.pop("WORKLAWS_USAGE_SOURCE", None)
    env.update(extra_env or {})
    p = subprocess.run([sys.executable, os.path.join(SCRIPTS, script)], input=json.dumps(payload),
                       capture_output=True, text=True, env=env, timeout=30)
    return p.returncode, p.stdout.strip()


class ActionControlTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = self.tmp.name

    def tearDown(self):
        self.tmp.cleanup()

    def decide(self, tool, tool_input):
        code, out = run("action_control.py", {"session_id": "t", "tool_name": tool, "tool_input": tool_input}, self.dir)
        self.assertEqual(code, 0)
        return json.loads(out)["hookSpecificOutput"]["permissionDecision"] if out else None

    def test_push_asks_for_confirmation(self):
        self.assertEqual(self.decide("Bash", {"command": "git push origin main"}), "ask")

    def test_destructive_commands_ask(self):
        for cmd in ["rm -rf build", "git reset --hard HEAD~1", "npm publish", "terraform apply", "curl -X POST https://example.com"]:
            with self.subTest(cmd=cmd):
                self.assertEqual(self.decide("Bash", {"command": cmd}), "ask")

    def test_reads_are_untouched(self):
        self.assertIsNone(self.decide("Read", {"file_path": "README.md"}))
        self.assertIsNone(self.decide("Bash", {"command": "ls -la"}))

    def test_external_connector_action_asks(self):
        self.assertEqual(self.decide("mcp__slack__send_message", {}), "ask")

    def test_never_allows(self):
        for tool, ti in [("Bash", {"command": "git push"}), ("Edit", {}), ("Read", {})]:
            _, out = run("action_control.py", {"tool_name": tool, "tool_input": ti}, self.dir)
            self.assertNotIn('"allow"', out)

    def test_writes_are_logged(self):
        self.decide("Edit", {"file_path": "a.py"})
        with open(os.path.join(self.dir, ".claude", "state", "log.jsonl"), encoding="utf-8") as f:
            rows = [json.loads(l) for l in f]
        self.assertEqual(rows[-1]["level"], "write")


class OutcomeTest(unittest.TestCase):
    def rows(self, d):
        with open(os.path.join(d, ".claude", "state", "log.jsonl"), encoding="utf-8") as f:
            return [json.loads(l) for l in f]

    def test_outcome_recorded_only_for_asked_actions(self):
        with tempfile.TemporaryDirectory() as d:
            ask = {"session_id": "t", "tool_use_id": "u1", "tool_name": "Bash", "tool_input": {"command": "git push"}}
            run("action_control.py", ask, d)
            env = {**os.environ, "CLAUDE_PROJECT_DIR": d}
            for uid, arg in [("u1", "executed"), ("u2", "executed")]:
                subprocess.run([sys.executable, os.path.join(SCRIPTS, "outcome.py"), arg], input=json.dumps(
                    {"session_id": "t", "tool_use_id": uid, "tool_name": "Bash"}), text=True, env=env, check=True)
            outcomes = [r for r in self.rows(d) if r["decision"] == "outcome"]
            self.assertEqual([(r["tool_use_id"], r["outcome"]) for r in outcomes], [("u1", "executed")])


class SessionStartTest(unittest.TestCase):
    def test_suggests_adoption_without_config(self):
        with tempfile.TemporaryDirectory() as d:
            code, out = run("session_start.py", {"session_id": "t", "cwd": d}, d)
            self.assertEqual(code, 0)
            self.assertIn(".claude/worklaws.json", out)


class StopAndUsageTest(unittest.TestCase):
    def test_blocks_without_handoff_then_archives(self):
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, ".claude", "sessions"))
            with open(os.path.join(d, ".claude", "sessions", "pending.md"), "w") as f:
                f.write("# Report\n<USAGE>\n")
            _, out = run("stop.py", {"session_id": "abcdef123"}, d)
            self.assertEqual(json.loads(out)["decision"], "block")
            open(os.path.join(d, ".claude", "handoff.md"), "w").close()
            _, out = run("stop.py", {"session_id": "abcdef123"}, d)
            self.assertEqual(out, "")
            archived = [n for n in os.listdir(os.path.join(d, ".claude", "sessions")) if n != "pending.md"]
            self.assertEqual(len(archived), 1)
            with open(os.path.join(d, ".claude", "sessions", archived[0])) as f:
                self.assertIn("no telemetry data", f.read())

    def test_usage_sums_events_for_the_session(self):
        with tempfile.TemporaryDirectory() as d:
            src = os.path.join(d, "usage.jsonl")
            with open(src, "w") as f:
                for sid, cost in [("s1", 0.5), ("s1", 0.25), ("s2", 9)]:
                    f.write(json.dumps({"session_id": sid, "model": "m", "query_source": "main", "input_tokens": 10,
                                        "output_tokens": 5, "cache_read_tokens": 0, "cache_creation_tokens": 0, "cost_usd": cost}) + "\n")
            p = subprocess.run([sys.executable, os.path.join(SCRIPTS, "usage_report.py"), "s1"], capture_output=True, text=True,
                               env={**os.environ, "WORKLAWS_USAGE_SOURCE": src})
            self.assertIn("**0.7500**", p.stdout)


if __name__ == "__main__":
    unittest.main()
