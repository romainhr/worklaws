"""Per-session usage table from telemetry. The model never writes these figures.

Source: environment variable WORKLAWS_USAGE_SOURCE = path to a *normalized* JSONL file,
one line per OpenTelemetry `claude_code.api_request` event, with the fields:
  session_id, model, query_source, input_tokens, output_tokens,
  cache_read_tokens, cache_creation_tokens, cost_usd
An adapter (outside this plugin) must convert the OTel collector output to this format.
If there is no source, returns 'Usage: no telemetry data' (never estimates)."""
import os, json, sys
from collections import defaultdict

FIELDS = ["input_tokens", "output_tokens", "cache_read_tokens", "cache_creation_tokens", "cost_usd"]

def usage_table(session_id):
    source = os.environ.get("WORKLAWS_USAGE_SOURCE")
    if not source or not os.path.exists(source) or not session_id:
        return "Usage: no telemetry data (set WORKLAWS_USAGE_SOURCE; see README)."
    agg = defaultdict(lambda: defaultdict(float))
    with open(source, encoding="utf-8") as f:
        for line in f:
            try:
                ev = json.loads(line)
            except Exception:
                continue
            if ev.get("session_id") != session_id:
                continue
            k = (ev.get("model", "?"), ev.get("query_source", "?"))
            for c in FIELDS:
                agg[k][c] += float(ev.get(c, 0) or 0)
    if not agg:
        return "Usage: no telemetry events for this session."
    rows = ["| Model | Source | Input | Output | Cache read | Cache write | USD (est.) |", "|---|---|---|---|---|---|---|"]
    tot = defaultdict(float)
    for (m, q), v in sorted(agg.items()):
        rows.append(f"| {m} | {q} | {int(v['input_tokens']):,} | {int(v['output_tokens']):,} | {int(v['cache_read_tokens']):,} | {int(v['cache_creation_tokens']):,} | {v['cost_usd']:.4f} |")
        for c in FIELDS:
            tot[c] += v[c]
    rows.append(f"| **Total** | | {int(tot['input_tokens']):,} | {int(tot['output_tokens']):,} | {int(tot['cache_read_tokens']):,} | {int(tot['cache_creation_tokens']):,} | **{tot['cost_usd']:.4f}** |")
    rows.append("\nSource: OpenTelemetry (`claude_code.api_request`). Cost estimated at API list price; this is not billing.")
    return "\n".join(rows)

if __name__ == "__main__":
    print(usage_table(sys.argv[1] if len(sys.argv) > 1 else ""))
