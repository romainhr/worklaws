"""Stop: if .claude/sessions/pending.md exists, fills in the usage section with telemetry and archives it.
Blocks (once) if the report was left without a handoff. Honors stop_hook_active to avoid looping."""
import os, sys, json, datetime
sys.path.insert(0, os.path.dirname(__file__))
from common import read_input, path, log_failure
from usage_report import usage_table

def main():
    e = read_input()
    if e.get("stop_hook_active"):
        sys.exit(0)
    try:
        pending = path(e, "sessions", "pending.md")
        if not os.path.exists(pending):
            sys.exit(0)
        if not os.path.exists(path(e, "handoff.md")):
            print(json.dumps({"decision": "block", "reason": "Missing .claude/handoff.md. Complete step 2 of `session-close` before finishing."}))
            sys.exit(0)
        with open(pending, encoding="utf-8") as f:
            txt = f.read()
        txt = txt.replace("<USAGE>", usage_table(e.get("session_id", "")))
        destination = path(e, "sessions", f"{datetime.date.today().isoformat()}-{e.get('session_id','no-id')[:8]}.md")
        with open(destination, "w", encoding="utf-8") as f:
            f.write(txt)
        os.remove(pending)
    except Exception as ex:
        log_failure(e, "Stop", repr(ex))
    sys.exit(0)

if __name__ == "__main__":
    main()
