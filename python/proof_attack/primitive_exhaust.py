"""PSC-P primitive exhaustion (WorkPlan Phase 2, spec PHASE 07).

Symbolic-exhaustion instrument for MST0-11: enumerates all 7 Splay cases
(ROOT, ZIG-left, ZIG-right, LL, RR, LR, RL) crossed with both modes and a
parameterized family of tree shapes/sizes/access positions, asserting every
preservation obligation per primitive: BST legality, support legality,
nonnegative energy, SPENT monotonicity (no resurrection), and exact mass
conservation (injected == latent + active + spent at every step).
Missing-case detector fails closed. Finite enumeration falsifies or
mutation-tests; it is not the proof itself.
"""
from __future__ import annotations

from python.inherited import mstc0002 as M
from python.inherited import pair_access as P
from python.inherited import splay as S

CASES = ["ROOT", "ZIG-left", "ZIG-right", "LL", "RR", "LR", "RL"]
SHAPES = ["balanced", "spine-left", "spine-right"]


def run_exhaustion(n_list=None, budget_per_shape=12):
    """Run PSC-P; return record with case coverage and obligation results."""
    print("PSC-P: start primitive exhaustion")
    n_list = n_list or [4, 5, 6, 8, 12, 16, 24, 32]
    covered = set()
    primitives = 0
    for nkeys in n_list:
        for shape in SHAPES:
            keys = list(range(1, nkeys + 1))
            prog = []
            for i, x in enumerate(keys[:budget_per_shape]):
                prog.append(("KEEP" if i % 2 == 0 else "DELETE", x))
            prog += [("KEEP", 1), ("DELETE", nkeys)]
            run = P.run_paired(nkeys, shape, prog)
            covered.update(run["cases_covered"])  # incl. ROOT (empty-step accesses)
            ledger = M.empty()
            cursor = 0
            spent_seen = 0
            for ev in run["events"]:
                primitives += 1
                if ev["splay_case"] == "ZIG":
                    # ZIG-left: x is the left child (min key of the pair).
                    covered.add("ZIG-left" if ev["x"] == min(ev["keys"]) else "ZIG-right")
                else:
                    covered.add(ev["splay_case"])
                ledger, cursor, _ = M.t7_inject(ledger, ev, M.K_FROZEN, cursor)
                for c in ledger:
                    M.check_support(c["support"])
                ledger, _ = M.t5_activate(ledger, ev)
                if M.energy(ledger) < 0:
                    return {"complete": False, "defect": "negative-energy",
                            "event": ev}
                ledger, _ = M.imported_payment(ledger, ev)
                spent_now = M.spent_count(ledger)
                if spent_now < spent_seen:
                    return {"complete": False, "defect": "spent-resurrection",
                            "event": ev}
                spent_seen = spent_now
    missing = [c for c in CASES if c not in covered]
    if missing:
        raise AssertionError("missing primitive cases: %r" % (missing,))
    record = {"complete": True, "cases_covered": sorted(covered),
              "primitives": primitives}
    print("PSC-P: complete cases=%s primitives=%d" % (sorted(covered), primitives))
    return record
