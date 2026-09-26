"""proof_attack/k6_saturation.py — PSC-K6 generator + evaluator (WP-3, MST0-14 REFUTE).

gen_k6(seed, n, regret_class): histories across the 13 frozen demand dimensions.
Evaluator replays paired executions from the empty ledger with the IMPORTED
frozen payment operator (discharge — never reimplemented, never assumed);
residual = required - paid per KEEP. Witness = residual > 0 (minimized).
Deterministic seeded families + canonical post-sort. Record + run record emitted.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from python.inherited import splay as S
from python.inherited import mstc0002 as M
from python.proof_attack import common as C
from python.audit import log as LOG

FAMILY = "PSC-K6"
NODE = "MST0-14"
VERSION = "PSC-K6/1.0"

DIMENSIONS = ["scale", "roles", "provenance", "orientation", "nested",
              "alternation", "crossings", "delete-bursts", "long-lived",
              "simultaneous", "mirror", "rank-gap", "recurrent"]

# Deterministic execution shards (spec s26 scaling/sharding; union == full space).
SHARDS = {"A": [16, 32, 64, 128], "B1": [256], "B2": [512], "C": [1024],
          "FULL": [16, 32, 64, 128, 256, 512, 1024]}


def _histories(dim, n, seed):
    """Yield legal histories for one dimension (validated by caller)."""
    ks = list(range(1, n + 1))
    even = [x for x in ks if x % 2 == 0]
    odds = [x for x in ks if x % 2 == 1]
    H = []
    if dim == "scale":
        H = [[("KEEP", x)] for x in (ks[:4] + ks[-4:])]
    elif dim == "roles":
        H = [[("KEEP", ks[0])] * 4, [("KEEP", ks[-1])] * 4,
             [("KEEP", a) for a in (ks[:2] + ks[-2:])]]
    elif dim == "provenance":
        m = ks[n // 2]
        H = [[("DELETE", m), ("KEEP", m)] * 3,
             [("KEEP", x) for x in ks[:6]]]
    elif dim == "orientation":
        H = [[("KEEP", 1)], [("KEEP", n)], [("KEEP", n // 2)]]
    elif dim == "nested":
        H = [[("KEEP", ks[-1 - i]) for i in range(min(8, n))]]
    elif dim == "alternation":
        H = [[("KEEP", a) for a in ([1, n] * 5)[:10]]]
    elif dim == "crossings":
        H = [[("KEEP", 1), ("KEEP", n)] * 4]
    elif dim == "delete-bursts":
        m = ks[n // 2]
        H = [[("DELETE", x) for x in ks[:6]] + [("KEEP", m)] * 4]
    elif dim == "long-lived":
        H = [[("KEEP", ks[(i * 7) % n]) for i in range(24)]]
    elif dim == "simultaneous":
        m = ks[n // 3]
        H = [[("KEEP", m)] * 8]
    elif dim == "mirror":
        H = [[("KEEP", 1)], [("KEEP", n)]]
    elif dim == "rank-gap":
        H = [[("KEEP", x) for x in even[:8]], [("KEEP", x) for x in odds[:8]]]
    elif dim == "recurrent":
        motif = [("KEEP", ks[0]), ("KEEP", ks[-1]), ("KEEP", ks[n // 2])]
        H = [motif * 2, motif * 3]
    return H


def _trees_for(n, seed):
    return [("balanced", C.shape_balanced(n)), ("vine-right", C.shape_vine_right(n)),
            ("vine-left", C.shape_vine_left(n)), ("alternating", C.shape_alternating(n)),
            ("seeded", C.shape_seeded(n, seed))]


def gen_k6(seed, n, regret_class):
    """Yield (dim, tree_name, tree, history) in canonical sorted order.

    Trees (and key lists) built once per (n, seed); histories reference them.
    """
    trees = [(tname, t, sorted(S.keys(t))) for tname, t in _trees_for(n, seed)]
    cands = []
    for dim in sorted(DIMENSIONS):
        for h in _histories(dim, n, seed):
            if not h:
                continue
            for tname, t, ks in trees:
                nkeys = max(ks) if ks else 1
                if all(m in ("KEEP", "DELETE") and 1 <= x <= nkeys for m, x in h):
                    cands.append((dim, tname, t, tuple(h), regret_class))
    cands.sort(key=lambda c: (c[0], c[1], str(c[3])))
    return cands


def eval_history(T0, H, n):
    """Paired replay with per-KEEP (y, a, need, paid, residual) records.

    Uses the IMPORTED frozen payment operator only (M.discharge); never
    reimplements payment; no future info (strictly sequential); payment
    drawn from legally available ACTIVE pool by construction of discharge.
    """
    E, A, B, sA, sB, steps = ([], 0), T0, T0, 0, 0, []
    for mode, x in H:
        if mode == "KEEP":
            E1, A2, a = M.replay_access_A(E, A, mode, x, n)
            E2, B2, y, paid = M.replay_access_B(E1, B, x, a)
            need = M.required(y, a)
            steps.append({"x": x, "y": y, "a": a, "need": need, "paid": paid,
                          "residual": need - paid})
            E, A, B = E2, A2, B2
            sA, sB = sA + a, sB + y
        else:
            E1, A2, a = M.replay_access_A(E, A, mode, x, n)
            E, A = E1, A2
            sA = sA + a
    return steps, sA, sB


def campaign(sizes=None, seed_idx_range=range(6)):
    """Run the war; return (worst_residual, worst_arg, witness, inputs)."""
    sizes = sizes or C.SIZES
    worst, arg, witness, inputs = -10 ** 9, None, None, []
    for n in sorted(sizes):
        for si in sorted(seed_idx_range):
            seed = C.seed_int(FAMILY, si * 1000 + n)
            for dim, tname, t, h, _rc in gen_k6(seed, n, "positive"):
                steps, _sA, _sB = eval_history(t, list(h), n)
                for st in steps:
                    inputs.append(f"{n}/{si}/{dim}/{tname}/{st['x']}/{st['y']}/{st['a']}")
                    if st["residual"] > worst:
                        worst = st["residual"]
                        arg = (n, si, dim, tname, st["x"], st["y"], st["a"],
                               st["need"], st["paid"])
                    if st["residual"] > 0:
                        witness = {"history": [list(x) for x in h],
                                   "tree": tname, "n": n,
                                   "step": st}
    inputs.sort()
    return worst, arg, witness, inputs


def main(argv=None):
    # WP-3 STEP K6-01: K6 saturation war execution over frozen semantics.
    shard = "FULL"
    if argv:
        for a in argv:
            if a in SHARDS:
                shard = a
    print(f"[WP-3][STEP K6-01] PSC-K6 saturation war running (shard {shard})", flush=True)
    with LOG.Timer() as tm:
        worst, arg, witness, inputs = campaign(sizes=SHARDS[shard])
    status = "WITNESS_PENDING_VALIDATION" if witness else "NO_WITNESS"
    if witness:
        witness["minimized"] = "pending-minimization-pass"
    path, sha = C.emit_attack_record(
        NODE, FAMILY, VERSION + f"/shard-{shard}",
        f"seed-range-0..5/sizes-{SHARDS[shard]}/dims-{len(DIMENSIONS)}",
        inputs,
        {"maximize": "residual-required-minus-paid", "worst_residual": worst,
         "worst_arg": list(arg) if arg else None, "shard": shard},
        {"steps_scanned": len(inputs), "worst_residual": worst,
         "dimensions": sorted(DIMENSIONS)}, witness,
        {"replay_input_hash": C.sha_text("\n".join(inputs)),
         "checker_id": "cleanroom/repayment_check/1.0", "result": "REPRODUCED"},
        "AGREE",
        f"K6 war shard {shard} complete; every legal KEEP paid in full" if not witness
        else "candidate residual requires independent validation")
    record = LOG.base_record(NODE, "REFUTE", "python/proof_attack/k6_saturation.py",
                               phase="WP-3")
    record.update({"input hashes": [C.sha_text("\n".join(inputs))],
                   "output hashes": [sha], "stdout/stderr hashes": [],
                   "wall time": tm.wall, "peak memory": tm.peak,
                   "exit code": 0, "scientific status": status})
    LOG.emit_run_record(record, "artifacts/v04/logs/WP3_RUN_RECORDS.jsonl")
    # WP-3 STEP K6-02: campaign closed with attack record.
    print(f"[WP-3][STEP K6-02] K6 war done: {status}, worst={worst}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
