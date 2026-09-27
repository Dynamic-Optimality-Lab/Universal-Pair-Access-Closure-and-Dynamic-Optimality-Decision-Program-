import glob
import json

fs = [g for g in sorted(glob.glob("artifacts/v04/proof_attacks/MST0-14R/*.json"))
      if "exhaustive" in g]
d = json.load(open(fs[-1]))["exhaustive"]
print("instances:", d["instances"], "witnesses:", len(d["witnesses"]))
print("min_margin:", d["min_margin"])
print("arg:", json.dumps(d["min_margin_arg"], default=str)[:800])
