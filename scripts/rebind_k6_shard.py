"""scripts/rebind_k6_shard.py — rebind ONE historical K6 shard (repair track, Sec 10A).

Usage: py -3 scripts/rebind_k6_shard.py <record-path> <out-jsonl-line-path>
Regenerates the canonical logical input stream with the CURRENT (unmodified,
PSC-K6/1.0) generator, recomputes worst residual, compares with the historical
claim, checks LegalPairInstance over every regenerated input, and appends one
JSON line with hashes. Alters no historical artifact. Exit 0 iff worst matches
and legality violations are empty.
"""
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.setrecursionlimit(20000)

from python.proof_attack import k6_saturation as K6
from python.proof_attack import common as C
from python.audit import legal_domain as LD

IMPL = Path(__file__).resolve().parents[1]


def main():
    rec_path, out_path = Path(sys.argv[1]), Path(sys.argv[2])
    rec = json.loads(rec_path.read_text(encoding="utf-8"))
    import re
    m = re.search(r"sizes-\[([0-9, ]+)\]", rec.get("seed", ""))
    sizes = sorted(int(x) for x in m.group(1).split(",")) if m else C.SIZES
    print(f"[REBIND] sizes={sizes} record={rec_path.name}", flush=True)

    worst, arg, witness, inputs = K6.campaign(sizes=sizes)
    claimed = rec["best_finite_obstruction_metrics"]["worst_residual"]
    match = (worst == claimed) and (witness is None) == (
        rec["exact_witness"] is None)

    # Legality over every regenerated input (generator-level, no replay).
    checked, violations = 0, []
    for n in sorted(sizes):
        for si in range(6):
            seed = C.seed_int(K6.FAMILY, si * 1000 + n)
            for dim, tname, t, h, _rc in K6.gen_k6(seed, n, "positive"):
                checked += 1
                bad = LD.violations(t, list(h), n)
                if bad:
                    violations.append({"n": n, "seed_idx": si, "dim": dim,
                                       "tree": tname, "bad": bad})

    code_sha = {f: hashlib.sha256((IMPL / f).read_bytes()).hexdigest()
                for f in ["python/proof_attack/k6_saturation.py",
                          "python/proof_attack/common.py",
                          "python/inherited/mstc0002.py",
                          "python/inherited/splay.py",
                          "python/audit/legal_domain.py"]}
    line = {
        "record": rec_path.name,
        "record_sha256": hashlib.sha256(rec_path.read_bytes()).hexdigest(),
        "generator_version": rec["generator_version"],
        "sizes": sizes,
        "regenerated": {"worst_residual": worst,
                        "worst_arg": list(arg) if arg else None,
                        "witness": witness,
                        "inputs_count": len(inputs),
                        "inputs_join_sha": C.sha_text("\n".join(inputs))},
        "claimed_worst": claimed,
        "worst_match": match,
        "legality": {"inputs_checked": checked,
                     "violations": violations},
        "code_sha256": code_sha,
    }
    print(f"[REBIND] worst={worst} claimed={claimed} match={match} "
          f"checked={checked} violations={len(violations)}", flush=True)
    with open(out_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(line, sort_keys=True) + "\n")
    return 0 if (match and not violations) else 1


if __name__ == "__main__":
    sys.exit(main())
