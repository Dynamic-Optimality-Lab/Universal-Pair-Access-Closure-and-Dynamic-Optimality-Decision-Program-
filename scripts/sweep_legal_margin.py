"""scripts/sweep_legal_margin.py — exhaustive small-state + engineered-family sweep (MST0-14R track, Secs 21-24).

Searches for: (a) exact LEGAL counterexamples (paid<need with
LegalPairInstance=true) — a genuine refutation of MST0-14R if found;
(b) minimal pool-need margins; (c) candidate-potential slack values.
Finite search discovers/falsifies ONLY; it never proves.

Outputs an append-only record under artifacts/v04/proof_attacks/MST0-14R/.
Deterministic canonical order. Usage:
  py -3 scripts/sweep_legal_margin.py [exhaustive|engineered|both]
"""
import hashlib
import itertools
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.setrecursionlimit(20000)

from python.inherited import splay as S
from python.audit import legal_domain as LD
from python.audit import ledger_trace as LT
from python.proof_attack import common as C

IMPL = Path(__file__).resolve().parents[1]
OUTDIR = IMPL / "artifacts/v04/proof_attacks/MST0-14R"


def all_bst_shapes(keys):
    """All BST shapes over sorted key list (Catalan family), canonical order."""
    if not keys:
        return [S.LEAF]
    out = []
    for i, k in enumerate(keys):
        for l in all_bst_shapes(keys[:i]):
            for r in all_bst_shapes(keys[i + 1:]):
                out.append(S.node(k, l, r))
    out.sort(key=repr)
    return out


def run_instance(T0, H, n):
    """Instrumented replay; returns (verdict, min_margin, summary, steps)."""
    assert LD.legal_pair_instance(T0, H, n)
    steps, summary = LT.trace_execution(T0, H, n)
    return summary["suffices"], summary["min_margin"], summary, steps


def sweep_exhaustive(n_max=4, max_len=5):
    """Exhaustive legal instances: all shapes x all histories up to max_len."""
    stats = {"instances": 0, "witnesses": [], "min_margin": None,
             "min_margin_arg": None, "alpha_slack_min": None}
    for n in range(1, n_max + 1):
        shapes = all_bst_shapes(list(range(1, n + 1)))
        alphabet = [("KEEP", x) for x in range(1, n + 1)] + \
                   [("DELETE", x) for x in range(1, n + 1)]
        for T0 in shapes:
            for L in range(0, max_len + 1):
                for H in itertools.product(alphabet, repeat=L):
                    H = list(H)
                    ok, margin, summary, _ = run_instance(T0, H, n)
                    stats["instances"] += 1
                    if not ok:
                        stats["witnesses"].append(
                            {"T0": T0, "H": [list(e) for e in H], "n": n,
                             "first_fail": summary["first_fail"]})
                        return stats  # genuine legal counterexample: stop, freeze
                    if margin is not None and (
                            stats["min_margin"] is None or
                            margin < stats["min_margin"]):
                        stats["min_margin"] = margin
                        stats["min_margin_arg"] = {
                            "T0": T0, "H": [list(e) for e in H], "n": n}
    return stats


def engineered_families():
    """Targeted divergence families at larger n (deterministic)."""
    fams = {}
    # F1: churn-then-strike — DELETE all-but-x, then KEEP x (B stale-deep).
    for n in (16, 64, 256, 1024):
        for x in (n, 1, n // 2):
            H = [("DELETE", z) for z in range(1, n + 1) if z != x]
            H += [("KEEP", x)]
            fams[f"F1-churn-strike-n{n}-x{x}"] = (n, H)
    # F2: repeated single-key DELETE then strike (deepest-leaf pattern).
    for n in (16, 64, 256, 1024, 2048):
        x = n
        for rounds in (1, 2, 3):
            H = [("DELETE", x)] * rounds + [("KEEP", x)]
            fams[f"F2-repeat-del-n{n}-r{rounds}"] = (n, H)
    # F3: strike, re-churn elsewhere, strike again (pool-drain attempt).
    for n in (64, 256):
        x, z = n, 1
        H = ([("DELETE", x), ("KEEP", x)]
             + [("DELETE", w) for w in range(1, n + 1) if w != x]
             + [("KEEP", x)])
        fams[f"F3-drain-n{n}"] = (n, H)
    # F4: alternating extremes (KEEP-side divergence pump).
    for n in (32, 128):
        H = ([("KEEP", 1), ("KEEP", n)] * 6
             + [("DELETE", n // 2)] * 4 + [("KEEP", 1), ("KEEP", n)])
        fams[f"F4-alternating-n{n}"] = (n, H)
    return fams


def run_engineered(t0_shape="vine-right"):
    stats = {"instances": 0, "witnesses": [], "min_margin": None,
             "min_margin_arg": None, "per_family": {}}
    for name, (n, H) in sorted(engineered_families().items()):
        if t0_shape == "vine-right":
            T0 = C.shape_vine_right(n)
        elif t0_shape == "balanced":
            T0 = C.shape_balanced(n)
        else:
            raise ValueError(t0_shape)
        ok, margin, summary, _ = run_instance(T0, H, n)
        stats["instances"] += 1
        stats["per_family"][name] = {"margin": margin, "ok": ok,
                                     "sA": summary["sA"], "sB": summary["sB"],
                                     "energy": summary["energy"]}
        if not ok:
            stats["witnesses"].append({"family": name, "T0_shape": t0_shape,
                                       "H": [list(e) for e in H], "n": n})
            return stats
        if margin is not None and (stats["min_margin"] is None or
                                   margin < stats["min_margin"]):
            stats["min_margin"] = margin
            stats["min_margin_arg"] = {"family": name, "n": n}
    return stats


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "both"
    print(f"[SWEEP][STEP 01] legal-margin sweep starting ({which})", flush=True)
    t0 = time.time()
    result = {"sweep": which, "utc_start": time.strftime(
        "%Y%m%dT%H%M%SZ", time.gmtime())}
    if which in ("exhaustive", "both"):
        result["exhaustive"] = sweep_exhaustive()
        print(f"[SWEEP][STEP 02] exhaustive done: "
              f"{result['exhaustive']['instances']} instances, "
              f"witnesses={len(result['exhaustive']['witnesses'])}, "
              f"min_margin={result['exhaustive']['min_margin']}", flush=True)
        if result["exhaustive"]["witnesses"]:
            result["verdict"] = "LEGAL_WITNESS_FOUND"
        else:
            result["verdict"] = "NO_LEGAL_WITNESS"
    if which in ("engineered", "both") and result.get("verdict") != "LEGAL_WITNESS_FOUND":
        result["engineered_vine"] = run_engineered("vine-right")
        print(f"[SWEEP][STEP 03] engineered/vine done: "
              f"witnesses={len(result['engineered_vine']['witnesses'])}, "
              f"min_margin={result['engineered_vine']['min_margin']}", flush=True)
        if result["engineered_vine"]["witnesses"]:
            result["verdict"] = "LEGAL_WITNESS_FOUND"
        else:
            result["engineered_bal"] = run_engineered("balanced")
            print(f"[SWEEP][STEP 04] engineered/balanced done: "
                  f"witnesses={len(result['engineered_bal']['witnesses'])}, "
                  f"min_margin={result['engineered_bal']['min_margin']}",
                  flush=True)
            if result["engineered_bal"]["witnesses"]:
                result["verdict"] = "LEGAL_WITNESS_FOUND"
    result.setdefault("verdict", "NO_LEGAL_WITNESS")
    result["wall_seconds"] = round(time.time() - t0, 1)
    OUTDIR.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    path = OUTDIR / f"LEGAL_SWEEP_{which}_{stamp}.json"
    blob = json.dumps(result, indent=2, sort_keys=True, default=str)
    path.write_text(blob + "\n", encoding="utf-8")
    sha = hashlib.sha256(path.read_bytes()).hexdigest()
    print(f"[SWEEP][STEP 05] verdict={result['verdict']} file={path.name} "
          f"sha={sha[:16]}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
