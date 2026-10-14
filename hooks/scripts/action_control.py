"""PreToolUse (T1): risk-based action control.
- Never returns "allow": it does not remove permissions, it only adds friction.
- Irreversible/external actions -> permissionDecision "ask" with a reason.
- Writes -> recorded in the log.
- Reads -> no intervention.
Log: .claude/state/log.jsonl (one JSON line per event)."""
import os, sys, json, re, datetime
sys.path.insert(0, os.path.dirname(__file__))
from common import read_input, path, log_failure

READ = {"Read", "Grep", "Glob", "LS", "WebSearch", "WebFetch", "TodoWrite", "TaskCreate", "TaskUpdate", "TaskList", "TaskGet"}
WRITE = {"Edit", "Write", "MultiEdit", "NotebookEdit"}
# Shell commands that are irreversible or have external effects
BASH_RISK = [
    (r"\bgit\s+push\b", "push to a remote"),
    (r"\bgit\s+(reset\s+--hard|clean\s+-[a-z]*f|branch\s+-D|tag\s+-d)\b", "destructive git operation"),
    (r"(^|[;&|]\s*)rm\s", "file deletion"),
    (r"\b(gh|az)\s+(pr\s+merge|release\s+create|repo\s+(delete|create)|repos\s+pr\s+update)\b", "action on GitHub/Azure DevOps"),
    (r"\baz\b.*\b(delete|purge)\b", "deletion in Azure"),
    (r"\b(npm|pnpm|yarn)\s+publish\b|\btwine\s+upload\b|\bcargo\s+publish\b", "package publication"),
    (r"\b(kubectl|helm)\s+(apply|delete|upgrade|install|rollout)\b|\bterraform\s+(apply|destroy)\b", "infrastructure change"),
    (r"\b(deploy|desplegar)\b", "deployment"),
    (r"\bcurl\b.*\s-X\s*(POST|PUT|PATCH|DELETE)\b|\bcurl\b.*\s(-d|--data)\b", "sending data over HTTP"),
    (r"\bbd\s+(delete|init\s+--force)\b", "destructive operation on the tracker"),
]
MCP_RISK = re.compile(r"(send|post|publish|delete|remove|create|update|merge|deploy|transfer|pay|share|invite|write)", re.I)

def classify(tool, tool_input):
    if tool in READ:
        return "read", None
    if tool in WRITE:
        return "write", None
    if tool == "Bash":
        cmd = str(tool_input.get("command", ""))
        for pattern, reason in BASH_RISK:
            if re.search(pattern, cmd):
                return "irreversible", reason
        return "other", None
    if tool.startswith("mcp__"):
        action = tool.split("__")[-1]
        if MCP_RISK.search(action):
            return "irreversible", f"external action via connector ({action})"
        return "read", None
    return "other", None

def log(e, tool, level, reason, decision):
    """Appends one event; "tool_use_id" lets outcome.py link the result of an "ask"."""
    try:
        d = path(e, "state"); os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "log.jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps({"ts": datetime.datetime.now().isoformat(timespec="seconds"), "session_id": e.get("session_id"),
                                "tool_use_id": e.get("tool_use_id"), "tool": tool, "level": level, "reason": reason, "decision": decision}, ensure_ascii=False) + "\n")
    except Exception as ex:
        log_failure(e, "PreToolUse", repr(ex))

def main():
    e = read_input()
    try:
        tool = e.get("tool_name", "")
        level, reason = classify(tool, e.get("tool_input") or {})
        if level == "irreversible":
            log(e, tool, level, reason, "ask")
            print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "ask",
                              "permissionDecisionReason": f"[worklaws T1] Irreversible or external action: {reason}. Requires explicit confirmation."}}, ensure_ascii=False))
        elif level in ("write", "other"):
            log(e, tool, level, None, "no-intervention")
    except Exception as ex:
        log_failure(e, "PreToolUse", repr(ex))
    sys.exit(0)

if __name__ == "__main__":
    main()
