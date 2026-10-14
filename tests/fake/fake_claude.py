#!/usr/bin/env python3
"""Stand-in for `claude -p` used by the benchmark tests (no spend)."""
import json, sys
a = sys.argv[1:]
plugin = "--plugin-dir" in a
prompt = a[1]
if "strict evaluator" in prompt:
    print(json.dumps({"total_cost_usd": 0.01, "result": '{"scores": [2, 1, 0, 2, 1], "notes": "x"}'}))
else:
    print(json.dumps({"total_cost_usd": 0.3 if plugin else 0.1, "num_turns": 5 if plugin else 2, "duration_ms": 1000, "result": "response text",
                      "usage": {"input_tokens": 3, "output_tokens": 100, "cache_read_input_tokens": 0, "cache_creation_input_tokens": 500}}))
