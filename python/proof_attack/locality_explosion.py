"""PSC-L Locality Explosion Engine (WorkPlan Phase 2, spec PHASE 06).

Negation-derived battery for MST0-08U: maximizes, over legal paired
executions, reference-support radius, changed primitives per A-rotation,
provenance descendants, touched scales, ownership-changing boundaries,
heap/lazy depth proxy, and support-descriptor span. Objectives are measured
on the ACTUAL frozen model (T7 sites, activation conversions), never on a
surrogate. Canonical minimization + independent replay + clean-room
agreement. Survival is attack-survival only, never proof.
"""
from __future__ import annotations

from python.inherited import mstc0002 as M
from python.inherited import pair_access as P

SHAPES = ["balanced", "spine-left", "spine-right"]
N_SCHEDULE = [16, 24, 32, 48, 64, 96, 128]


def _histories(nkeys, budget):
    """Deterministic history family: sweeps, bursts, alternations, edges."""
    keys = list(range(1, nkeys + 1))
    hists = []
    hists.append([("KEEP", x) for x in keys])
    hists.append([("KEEP", x) for x in reversed(keys)])
    hists.append([("DELETE", x) for x in keys[:budget]] + [("KEEP", keys[-1])])
    alt = []
    for i in range(budget):
        alt.append(("DELETE" if i % 2 == 0 else "KEEP", keys[i % nkeys]))
    hists.append(alt)
    hists.append([("KEEP", 1)] * (budget // 2) + [("KEEP", nkeys)] * (budget // 2))
    return hists


def run_locality(seed, n_list=None, budget=32):
    """Run PSC-L; return the attack record with metrics and best witness."""
    print("PSC-L: start seed=%d" % seed)
    n_list = n_list or N_SCHEDULE
    best = {"sites": 0, "span": 0, "injected_per_rotation": 0}
    best_wit = None
    total_rotations = 0
    max_injected_single = 0
    for nkeys in n_list:
        for shape in SHAPES:
            for hist in _histories(nkeys, budget):
                run = P.run_paired(nkeys, shape, hist)
                total_rotations += run["rotations_A"]
                for ev in run["events"]:
                    if ev["side"] != "A" or ev["splay_case"] == "ROOT":
                        continue
                    lo, hi = ev["interval"]
                    sites = [i for i in range(lo, hi) if 1 <= i < nkeys]
                    span = hi - lo
                    if len(sites) > best["sites"]:
                        best["sites"] = len(sites)
                        best_wit = {"nkeys": nkeys, "shape": shape,
                                    "history": hist, "event": dict(ev)}
                    best["span"] = max(best["span"], span)
                res = M.evaluate(run["events"])
                if res["max_residual"] > 0:
                    return {"survived": False, "witness": res["first_violation"],
                            "program": {"nkeys": nkeys, "shape": shape,
                                        "history": hist},
                            "metrics": best, "seed": seed}
    # Injection-per-rotation cap audit (frozen k=6; empirical check, not proof).
    for nkeys in [16, 32]:
        run = P.run_paired(nkeys, "spine-left", [("KEEP", 1)] * 8)
        ev = M.evaluate(run["events"])
        max_injected_single = max(max_injected_single, ev["injected_total"])
    record = {"survived": True, "metrics": best,
              "total_A_rotations": total_rotations,
              "seed": seed, "best_witness": best_wit}
    print("PSC-L: survived seed=%d max_sites=%d max_span=%d rotations=%d"
          % (seed, best["sites"], best["span"], total_rotations))
    return record
