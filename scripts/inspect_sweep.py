import glob
import json
import sys

f = sorted(glob.glob("artifacts/v04/proof_attacks/MST0-14R/*.json"))[-1]
d = json.load(open(f))
print("VERDICT:", d["verdict"], "wall:", d.get("wall_seconds"))
for sec in ("engineered_vine", "engineered_bal"):
    if sec not in d:
        continue
    print("===", sec, "min_margin:", d[sec]["min_margin"], d[sec]["min_margin_arg"])
    for name, r in sorted(d[sec]["per_family"].items()):
        print("  %s: margin=%s ok=%s sA=%s sB=%s E=%s"
              % (name, r["margin"], r["ok"], r["sA"], r["sB"], r["energy"]))
