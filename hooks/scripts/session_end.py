"""SessionEnd (cannot block): if a recipe was left active without a close, records it for the next session."""
import os, sys, datetime
sys.path.insert(0, os.path.dirname(__file__))
from common import read_input, path, log_failure

def main():
    e = read_input()
    try:
        active = path(e, "state", "active-recipe")
        if os.path.exists(active):
            with open(active, encoding="utf-8") as f:
                recipe = f.read().strip()
            with open(path(e, "state", "incomplete-closes.log"), "a", encoding="utf-8") as f:
                f.write(f"{datetime.datetime.now().isoformat(timespec='seconds')} session {e.get('session_id','?')} ended without a close (recipe: {recipe})\n")
    except Exception as ex:
        log_failure(e, "SessionEnd", repr(ex))
    sys.exit(0)

if __name__ == "__main__":
    main()
