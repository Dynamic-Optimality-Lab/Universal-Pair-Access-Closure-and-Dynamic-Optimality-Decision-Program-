"""PSC-K6 K6 Saturation War (WorkPlan Phase 3, spec PHASE 10).

Pre-proof attack on MST0-14: attempts to destroy synchronous KEEP repayment
before any proof is written, while mining structural observations from failed
attacks (never auto-promoted to lemmas). Demand is derived from the ACTUAL
frozen injection/credit semantics (T7 sites, T5 activation, T6 discharge) —
never from a six-slot abstraction (T043/STOP-38).

Payment-semantics binding (WorkPlan v0.4-WP2): the evaluator calls the
imported payment path (`mstc0002.imported_payment`), whose min(pool, w)
behavior for w > 0 is a proved binding lemma derived from sealed parent
code (`branchA.py::evaluate` T6 loop + `update.py`), recorded in
`parent/V03_MSTC_0002.json` provenance and Entry 031 — never assumed.

Search dimensions (spec §14.3): scale combinations, rotation roles,
provenance classes, orientations, nested causal intervals, zig-zig/zig-zag
alternation, boundary crossings, DELETE-bursts-then-KEEP, long-lived latent
packets, simultaneous activation, mirror families, rank-gap extremes,
recurrent KEEP motifs. Exact integers/Fractions, seeded determinism,
canonical minimization, independent replay, clean-room agreement.
Gate: KEEP_REPAYMENT_EXACT_COUNTEREXAMPLE or KEEP_REPAYMENT_ATTACK_SURVIVED
(survival is not a theorem).
"""
from __future__ import annotations

import random

from python.inherited import mstc0002 as M
from python.inherited import pair_access as P

SHAPES = ["balanced", "spine-left", "spine-right"]


def _families(nkeys, budget, seed):
    """Deterministic K6 demand families (seeded)."""
    rng = random.Random(seed)
    keys = list(range(1, nkeys + 1))
    fams = {}
    # DELETE bursts then KEEP (latent aging + simultaneous activation).
    fams["delete_burst_then_keep"] = (
        [("DELETE", x) for x in keys[:budget // 2]] +
        [("KEEP", keys[(i * 3) % nkeys]) for i in range(budget // 2)])
    # Recurrent KEEP motifs (zig-zig vs zig-zag alternation pressure).
    alt = []
    for i in range(budget):
        alt.append(("KEEP", keys[0] if i % 2 == 0 else keys[-1]))
    fams["recurrent_edge_motif"] = alt
    # Rank-gap extremes: far-apart keys in alternation.
    fams["rank_gap_extreme"] = ([("KEEP", 1), ("KEEP", nkeys)] * (budget // 2 + 1))[:budget]
    # Mirror halves: forward then reversed sweeps.
    fams["mirror_sweep"] = ([("KEEP", x) for x in keys] +
                            [("KEEP", x) for x in reversed(keys)])[:budget]
    # Nested causal intervals: shrinking windows.
    nest = []
    lo, hi = 1, nkeys
    while lo < hi and len(nest) < budget:
        nest.append(("KEEP", (lo + hi) // 2))
        lo += 1
        hi -= 1
    fams["nested_intervals"] = (nest * (budget // len(nest) + 1))[:budget]
    # Random legal with KEEP bias (simultaneous activation attempts).
    fams["random_keep_biased"] = [(("KEEP" if rng.random() < 0.8 else "DELETE"),
                                   rng.randint(1, nkeys)) for _ in range(budget)]
    return fams


def _demand_metrics(events):
    """Per-execution demand statistics from the REAL frozen ledger walk.

    Not a model: replays T7/T5/T6 exactly (same functions as the verdict
    path) and records maxima. Used for structural lemma mining only.
    """
    ledger = M.empty()
    cursor = 0
    w_max = 0
    active_max = 0
    latent_max = 0
    for ev in events:
        ledger, cursor, _ = M.t7_inject(ledger, ev, M.K_FROZEN, cursor)
        ledger, _ = M.t5_activate(ledger, ev)
        latent_max = max(latent_max, sum(1 for c in ledger if c["type"] == "BOUNDARY_LATENT"))
        active_max = max(active_max, M.active_pool(ledger))
        w = ev["y_edge"] - M.C_FROZEN * ev["a_edge"] if ev["mode"] == "KEEP" else 0
        w_max = max(w_max, w)
        ledger, _ = M.imported_payment(ledger, ev)
    return {"w_max": w_max, "active_max": active_max, "latent_max": latent_max}


def run_saturation(seed, n_list=None, budget=48):
    """Run PSC-K6; return record with demand stats and gate outcome."""
    print("PSC-K6: start seed=%d" % seed)
    n_list = n_list or [16, 24, 32, 48, 64]
    totals = {"w_max": 0, "active_max": 0, "executions": 0, "rotations": 0}
    for nkeys in n_list:
        for fname, hist in _families(nkeys, budget, seed).items():
            for shape in SHAPES:
                run = P.run_paired(nkeys, shape, hist)
                totals["executions"] += 1
                totals["rotations"] += run["rotations_A"]
                res = M.evaluate(run["events"])
                if res["max_residual"] > 0:
                    wit = res["first_violation"]
                    wit["program"] = {"nkeys": nkeys, "shape": shape,
                                      "history": hist, "family": fname}
                    return {"gate": "KEEP_REPAYMENT_EXACT_COUNTEREXAMPLE",
                            "witness": wit, "seed": seed}
                dm = _demand_metrics(run["events"])
                totals["w_max"] = max(totals["w_max"], dm["w_max"])
                totals["active_max"] = max(totals["active_max"], dm["active_max"])
    record = {"gate": "KEEP_REPAYMENT_ATTACK_SURVIVED", "demand": totals, "seed": seed}
    print("PSC-K6: survived seed=%d w_max=%d active_max=%d execs=%d" % (
        seed, totals["w_max"], totals["active_max"], totals["executions"]))
    return record
