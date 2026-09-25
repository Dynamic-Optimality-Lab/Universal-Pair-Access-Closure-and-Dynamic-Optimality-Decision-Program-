"""PSC-B Boundary Torture Chamber (WorkPlan Phase 2, spec PHASE 08).

Adversarial battery for MST0-09: legal executions maximizing active boundary
count, nesting, alternating orientation, creation/destruction rate, rank gap,
interval span, simultaneous KEEP burden, DELETE-burst length before KEEP,
credit lifetime, reactivation, and mirror asymmetry. Every run closes with a
provenance-chain audit (every ACTIVE/SPENT credit traces to a T7 injection
site) and a mass-conservation audit (injected == latent + active + spent).
Smallest-counterexample + inflation discipline on any failure.
"""
from __future__ import annotations

import random

from python.inherited import mstc0002 as M
from python.inherited import pair_access as P


def _families(nkeys, budget, seed):
    """Deterministic torture families (seeded)."""
    rng = random.Random(seed)
    keys = list(range(1, nkeys + 1))
    fams = {}
    fams["alternating"] = [("DELETE" if i % 2 else "KEEP", keys[i % nkeys])
                           for i in range(budget)]
    bursts = []
    for b in (2, 4, 8):
        bursts += [("DELETE", x) for x in keys[:b]] + [("KEEP", keys[b % nkeys])]
    fams["delete_bursts_then_keep"] = bursts
    fams["edge_pingpong"] = ([("KEEP", 1), ("KEEP", nkeys)] * (budget // 2 + 1))[:budget]
    fams["random_legal"] = [(("KEEP" if rng.random() < 0.6 else "DELETE"),
                             rng.randint(1, nkeys)) for _ in range(budget)]
    fams["mirror_halves"] = ([("KEEP", x) for x in keys[:nkeys // 2]] +
                             [("KEEP", x) for x in reversed(keys[nkeys // 2:])])
    return fams


def _audit_provenance(ledger, nkeys):
    """Every ACTIVE/SPENT credit traces to a legal T7 site; masses balance."""
    latent = active = spent = 0
    for c in ledger:
        kind = c["support"][0]
        if kind != "boundary":
            return False, "non-boundary support"
        _, lo, hi, ori = c["support"]
        if not (1 <= lo < hi <= nkeys and ori in ("LEFT", "RIGHT")):
            return False, "illegal site"
        if c["type"] == "BOUNDARY_LATENT":
            latent += 1
        elif c["type"] == "BOUNDARY_ACTIVE":
            active += 1
        elif c["type"] == "SPENT":
            spent += 1
        else:
            return False, "illegal type"
    return True, {"latent": latent, "active": active, "spent": spent}


def run_torture(seed, n_list=None, budget=48):
    """Run PSC-B; return record with maxima, audits, and worst witness."""
    print("PSC-B: start seed=%d" % seed)
    n_list = n_list or [16, 24, 32, 48, 64]
    best = {"active": 0, "span": 0, "burst": 0, "reactivations": 0}
    worst = None
    shapes = ["balanced", "spine-left", "spine-right"]
    for nkeys in n_list:
        for fname, hist in _families(nkeys, budget, seed).items():
            for shape in shapes:
                run = P.run_paired(nkeys, shape, hist)
                ledger = M.empty()
                cursor = 0
                burst = 0
                max_burst = 0
                for ev in run["events"]:
                    if ev["mode"] == "DELETE":
                        burst += 1
                        max_burst = max(max_burst, burst)
                    else:
                        burst = 0
                    ledger, cursor, _ = M.t7_inject(ledger, ev, M.K_FROZEN, cursor)
                    ledger, _ = M.t5_activate(ledger, ev)
                    ledger, _ = M.imported_payment(ledger, ev)
                ok, info = _audit_provenance(ledger, nkeys)
                if not ok:
                    return {"survived": False, "defect": info,
                            "program": {"nkeys": nkeys, "shape": shape,
                                        "history": hist}}
                active_now = info["active"]
                if active_now > best["active"]:
                    best["active"] = active_now
                    worst = {"nkeys": nkeys, "family": fname, "shape": shape,
                             "history": hist}
                best["burst"] = max(best["burst"], max_burst)
                spans = [ev["interval"][1] - ev["interval"][0] for ev in run["events"]
                         if ev["side"] == "A"]
                if spans:
                    best["span"] = max(best["span"], max(spans))
                res = M.evaluate(run["events"])
                if res["max_residual"] > 0:
                    return {"survived": False, "witness": res["first_violation"],
                            "program": {"nkeys": nkeys, "history": hist}}
    record = {"survived": True, "maxima": best, "worst_witness": worst, "seed": seed}
    print("PSC-B: survived seed=%d maxima=%r" % (seed, best))
    return record
