"""SessionStart: injects the handoff, harness status, and warnings. Printed text (exit 0) is added as context."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from common import read_input, path, read_config, log_failure

REFERENCE_VERSION = "0.3.1"

def main():
    e = read_input()
    try:
        cfg = read_config(e)
        lines = []
        if cfg is None:
            lines.append("[worklaws] This workspace does not have the harness (.claude/worklaws.json). If there is a project, suggest `recipe-adoption` before working.")
        elif cfg.get("harness_version") != REFERENCE_VERSION:
            lines.append(f"[worklaws] Harness {cfg.get('harness_version')} installed; reference {REFERENCE_VERSION}. Suggest `recipe-adoption` in update mode.")
        else:
            profiles = ", ".join(p.get("profile", "?") for p in cfg.get("profiles", []))
            lines.append(f"[worklaws] Harness {REFERENCE_VERSION} · profiles: {profiles} · tracker: {cfg.get('tracker')}")
        if not os.path.exists(os.path.expanduser("~/.claude/worklaws-user.json")):
            lines.append("[worklaws] Missing ~/.claude/worklaws-user.json (vaults and default tracker). Before writing to a vault, use `prepare-workspace` (T0).")
        inc = path(e, "state", "incomplete-closes.log")
        if os.path.exists(inc) and os.path.getsize(inc) > 0:
            lines.append("[worklaws] WARNING: some sessions ended without `session-close` (see .claude/state/incomplete-closes.log). Propose a retroactive close.")
        ho = path(e, "handoff.md")
        if os.path.exists(ho):
            with open(ho, encoding="utf-8") as f:
                lines.append("[worklaws] Handoff from the previous session:\n" + f.read()[:6000])
        lines.append("[worklaws] Classify the first request with the `worklaws` skill before starting.")
        print("\n".join(lines))
    except Exception as ex:
        log_failure(e, "SessionStart", repr(ex))
    sys.exit(0)

if __name__ == "__main__":
    main()
