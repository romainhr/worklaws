"""UserPromptSubmit: if a recipe is active, reminds Claude to apply T3 (new-request) to requests outside the recipe.
Text printed with exit 0 is added as context. Never blocks."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from common import read_input, path, log_failure

def main():
    e = read_input()
    try:
        active = path(e, "state", "active-recipe")
        if os.path.exists(active):
            with open(active, encoding="utf-8") as f:
                recipe = f.read().strip()
            print(f"[worklaws] Active recipe: {recipe}. If this message is a different request, apply the `new-request` skill (T3) before acting.")
    except Exception as ex:
        log_failure(e, "UserPromptSubmit", repr(ex))
    sys.exit(0)

if __name__ == "__main__":
    main()
