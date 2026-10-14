"""Utilities shared by the worklaws plugin hooks (standard library only)."""
import json, os, sys, datetime

def read_input():
    try:
        return json.load(sys.stdin)
    except Exception:
        return {}

def root(data):
    return os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or os.getcwd()

def path(data, *parts):
    return os.path.join(root(data), ".claude", *parts)

def read_config(data):
    try:
        with open(path(data, "worklaws.json"), encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

def log_failure(data, hook, detail):
    """Leaves a record for the retro; never raises."""
    try:
        d = path(data, "state")
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "failed-hooks.log"), "a", encoding="utf-8") as f:
            f.write(f"{datetime.datetime.now().isoformat(timespec='seconds')} {hook} {data.get('session_id','?')}: {detail}\n")
    except Exception:
        pass
