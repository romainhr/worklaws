"""PostToolUse (Edit|Write): runs lint (and tests if configured) and returns ONLY the failure lines.
Exit 2 => stderr reaches Claude as feedback. No config or no commands => does nothing."""
import os, sys, subprocess, re
sys.path.insert(0, os.path.dirname(__file__))
from common import read_input, root, read_config, log_failure

PATTERN = re.compile(r"(fail|error|✗|✕|assert)", re.I)

def run(cmd, cwd):
    p = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, timeout=280)
    output = (p.stdout or "") + (p.stderr or "")
    failures = [l for l in output.splitlines() if PATTERN.search(l)]
    return p.returncode, failures[:40]

def main():
    e = read_input()
    cfg = read_config(e)
    if not cfg:
        sys.exit(0)
    cmds = cfg.get("commands", {})
    queue = [c for c in [cmds.get("lint")] if c]
    if cfg.get("tests_on_every_edit") and cmds.get("test"):
        queue.append(cmds["test"])
    problems = []
    for c in queue:
        try:
            code, failures = run(c, root(e))
            if code != 0:
                problems.append(f"$ {c} (exit {code})\n" + ("\n".join(failures) or "(no recognizable error lines; run the command to see details)"))
        except Exception as ex:
            log_failure(e, "PostToolUse", f"{c}: {ex!r}")
    if problems:
        print("\n\n".join(problems), file=sys.stderr)
        sys.exit(2)
    sys.exit(0)

if __name__ == "__main__":
    main()
