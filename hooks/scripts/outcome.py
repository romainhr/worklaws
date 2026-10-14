"""PostToolUse / PostToolUseFailure: records what happened to an action that T1 asked about.
- PostToolUse fires only if the tool ran => the confirmation was approved ("executed").
- PostToolUseFailure => it was approved but failed ("failed").
- An "ask" in log.jsonl with no outcome row means it was rejected (or the session ended first): the audit infers it.
Only tool calls with a previous "ask" row are recorded, so the log does not grow with every call.
Usage: outcome.py executed|failed"""
import os, sys, json, datetime
sys.path.insert(0, os.path.dirname(__file__))
from common import read_input, path, log_failure

def was_asked(e, tool_use_id):
    try:
        with open(os.path.join(path(e, "state"), "log.jsonl"), encoding="utf-8") as f:
            for line in f:
                try:
                    row = json.loads(line)
                except ValueError:
                    continue
                if row.get("tool_use_id") == tool_use_id and row.get("decision") == "ask":
                    return True
    except OSError:
        pass
    return False

def main():
    e = read_input()
    try:
        outcome = sys.argv[1] if len(sys.argv) > 1 else ""
        tool_use_id = e.get("tool_use_id")
        if outcome in ("executed", "failed") and tool_use_id and was_asked(e, tool_use_id):
            with open(os.path.join(path(e, "state"), "log.jsonl"), "a", encoding="utf-8") as f:
                f.write(json.dumps({"ts": datetime.datetime.now().isoformat(timespec="seconds"), "session_id": e.get("session_id"),
                                    "tool_use_id": tool_use_id, "tool": e.get("tool_name"), "decision": "outcome",
                                    "outcome": outcome}, ensure_ascii=False) + "\n")
    except Exception as ex:
        log_failure(e, "PostToolUse", repr(ex))
    sys.exit(0)

if __name__ == "__main__":
    main()
