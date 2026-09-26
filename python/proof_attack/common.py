"""proof_attack/common.py — shared deterministic attack scaffold (WP-2).

Seed derivation per prereg corpus (seed = sha256(master || family || index),
master = sha256 of 'SPLAY-AM-DECIDE-v0.4'); seeded shape builders; sorted
outputs; proof_attack-schema record writer; greedy history minimizer.
Deterministic, no I/O except record emission. Part of the attack side only
(cleanroom shares nothing with this module).
"""
import hashlib
import json
import sys
import time
from pathlib import Path

# Vine inputs reach depth 1024; recursive core needs headroom (linear frames).
sys.setrecursionlimit(20000)

IMPL = Path(__file__).resolve().parents[2]
ATTACK_DIR = IMPL / "artifacts/v04/proof_attacks"
MASTER = hashlib.sha256(b"SPLAY-AM-DECIDE-v0.4").hexdigest()

SIZES = [16, 32, 64, 128, 256, 512, 1024]


def seed_int(family, index):
    """Deterministic seed integer (corpus seed_derivation rule)."""
    return int(hashlib.sha256(f"{MASTER}{family}{index}".encode()).hexdigest(), 16)


def sha_text(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def shape_vine_right(n):
    from python.inherited import splay as S
    t = S.LEAF
    for k in range(1, n + 1):
        t = _insert_desc(t, k)
    return t


def _insert_desc(t, k):
    from python.inherited import splay as S
    if t[0] == "leaf":
        return S.node(k, S.LEAF, S.LEAF)
    _, kk, l, r = t
    if k < kk:
        return S.node(kk, _insert_desc(l, k), r)
    return S.node(kk, l, _insert_desc(r, k))


def shape_vine_left(n):
    from python.inherited import splay as S
    t = S.LEAF
    for k in range(n, 0, -1):
        t = _insert_desc(t, k)
    return t


def shape_balanced(n):
    from python.inherited import splay as S

    def build(ks):
        if not ks:
            return S.LEAF
        m = len(ks) // 2
        return S.node(ks[m], build(ks[:m]), build(ks[m + 1:]))
    return build(list(range(1, n + 1)))


def shape_seeded(n, seed):
    import random
    rng = random.Random(seed)
    ks = list(range(1, n + 1))
    rng.shuffle(ks)
    t = None
    from python.inherited import splay as S
    t = S.LEAF
    for k in ks:
        t = _insert_desc(t, k)
    return t


def shape_alternating(n):
    from python.inherited import splay as S
    order = []
    lo, hi = 1, n
    while lo <= hi:
        order.append(lo)
        lo += 1
        if lo <= hi:
            order.append(hi)
            hi -= 1
    t = S.LEAF
    for k in order:
        t = _insert_desc(t, k)
    return t


SHAPES = {"vine-right": shape_vine_right, "vine-left": shape_vine_left,
          "balanced": shape_balanced, "seeded": shape_seeded,
          "alternating": shape_alternating}


def minimize_history(hist, witness_fn):
    """Greedy drop-one minimization preserving witness_fn(hist) == True."""
    hist = list(hist)
    changed = True
    while changed:
        changed = False
        for i in range(len(hist)):
            cand = hist[:i] + hist[i + 1:]
            if cand and witness_fn(cand):
                hist = cand
                changed = True
                break
    return hist


def emit_attack_record(node, family, generator_version, seed_tag, inputs,
                       objective, best_metrics, witness, replay, checker,
                       interpretation):
    """Write a proof_attack-schema attack record; return (path, sha256)."""
    rec = {
        "schema_version": "1.0",
        "theorem_id": node,
        "negation_predicate": f"frozen negation of {node} (battlefield canonical Negation line)",
        "generator_version": generator_version,
        "seed": seed_tag,
        "symbolic_parameter_family": None,
        "input_hash": sha_text(json.dumps(inputs, sort_keys=True)),
        "exact_witness": witness,
        "objective_vector": objective,
        "best_finite_obstruction_metrics": best_metrics,
        "replay_certificate": replay,
        "independent_checker_result": checker,
        "scientific_interpretation": interpretation,
    }
    d = ATTACK_DIR / node
    d.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    path = d / f"{family}_{stamp}.json"
    path.write_text(json.dumps(rec, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    import hashlib as _h
    return (str(path), _h.sha256(path.read_bytes()).hexdigest())
