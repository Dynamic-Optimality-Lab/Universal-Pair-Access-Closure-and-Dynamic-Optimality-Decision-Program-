"""WP-2 engine tests: inherited core validity + inherited/cleanroom agreement.

Every test asserts exact behavioral properties (BST validity, cost charging,
edge-convention shape, ledger conservation, cross-implementation agreement).
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from python.cleanroom import core as C
from python.inherited import mstc0002 as M
from python.inherited import pair_access as P
from python.inherited import splay as S

PROGRAMS = [
    (8, "spine-left", [("KEEP", 1), ("DELETE", 8), ("KEEP", 4)]),
    (12, "balanced", [("KEEP", 6), ("KEEP", 6), ("DELETE", 1), ("KEEP", 12)]),
    (6, "spine-right", [("DELETE", 3), ("DELETE", 4), ("KEEP", 2)]),
]


def test_splay_validity_and_cost():
    """Splay brings x to root; BST valid; cost charged pre-splay."""
    for n in (4, 8, 16):
        for shape in ("balanced", "spine-left", "spine-right"):
            t = P.build_tree(shape, n)
            for x in (1, n, n // 2 + 1):
                a = S.cost(t, x)
                steps, t2 = S.stepwise_access(t, x, n, "A", "KEEP")
                assert t2.key == x
                assert S.is_valid_bst(t2)
                assert a >= 1
                t = t2


def test_edge_convention_shape():
    """A-events zeroed; only terminal B-rotation of KEEP carries (a, y)."""
    run = P.run_paired(8, "spine-left", [("KEEP", 1), ("DELETE", 8)])
    for e in run["events"]:
        if e["side"] == "A":
            assert e["a_edge"] == 0 and e["y_edge"] == 0
    b_keep = [e for e in run["events"] if e["side"] == "B" and e["mode"] == "KEEP"]
    assert b_keep and b_keep[-1]["a_edge"] > 0 and b_keep[-1]["y_edge"] > 0


def test_ledger_conservation():
    """injected == latent + active + spent at end; energy unsigned."""
    run = P.run_paired(12, "spine-left",
                       [("KEEP", 1), ("DELETE", 12), ("KEEP", 6)])
    ledger = M.empty()
    cursor = 0
    injected = 0
    for ev in run["events"]:
        ledger, cursor, k = M.t7_inject(ledger, ev, M.K_FROZEN, cursor)
        injected += k
        ledger, _ = M.t5_activate(ledger, ev)
        ledger, _ = M.imported_payment(ledger, ev)
        assert M.energy(ledger) >= 0
    counts = {"BOUNDARY_LATENT": 0, "BOUNDARY_ACTIVE": 0, "SPENT": 0}
    for c in ledger:
        counts[c["type"]] += 1
    assert injected == counts["BOUNDARY_LATENT"] + counts["BOUNDARY_ACTIVE"] + counts["SPENT"]


def test_cross_implementation_agreement():
    """Inherited and clean-room engines agree exactly on all programs."""
    for n, sa, hist in PROGRAMS:
        run = P.run_paired(n, sa, hist)
        e1 = M.evaluate(run["events"])
        ev2, a2, b2 = C.run_program(n, sa, hist)
        e2 = C.evaluate(ev2)
        assert (run["splay_A"], run["splay_B"]) == (a2, b2)
        assert (e1["feasible"], e1["max_residual"], e1["paid_total"],
                e1["injected_total"]) == (e2["feasible"], e2["max_residual"],
                                          e2["paid_total"], e2["injected_total"])
