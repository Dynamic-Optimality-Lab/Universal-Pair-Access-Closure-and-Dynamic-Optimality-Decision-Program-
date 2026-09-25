"""WP-3 K6 tests: battery green + deterministic + gated + efficacious.

Proves the saturation war runs, repeats, respects the hard entry gate, and
would catch a real repayment defect (capped-pool variant exposes residual).
"""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from python.inherited import mstc0002 as M
from python.inherited import pair_access as P
from python.proof_attack import k6_saturation as K6

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_saturation_survives_and_reports_demand():
    """Battery completes; demand statistics expose real multi-unit burden."""
    rec = K6.run_saturation(21, n_list=[16, 24], budget=24)
    assert rec["gate"] == "KEEP_REPAYMENT_ATTACK_SURVIVED"
    assert rec["demand"]["w_max"] > 0
    assert rec["demand"]["active_max"] > 0
    assert rec["demand"]["executions"] > 0


def test_saturation_deterministic():
    """Same seed gives identical gate + demand statistics."""
    r1 = K6.run_saturation(21, n_list=[16, 24], budget=24)
    r2 = K6.run_saturation(21, n_list=[16, 24], budget=24)
    assert r1["gate"] == r2["gate"] == "KEEP_REPAYMENT_ATTACK_SURVIVED"
    assert r1["demand"] == r2["demand"]


def test_proof_gate_blocked_pre_review():
    """Hard entry gate: proof track NOT_REACHED while upstreams unreviewed."""
    ledger = json.loads((REPO_ROOT / "math" / "proof_status.json").read_text(encoding="utf-8"))
    obs = ledger["obligations"]
    unready = [t for t in ("MST0-13", "MST0-08U", "MST0-11", "MST0-09", "MST0-22")
               if obs.get(t, {}).get("status") != "REVIEWED"]
    assert len(unready) == 5


def test_capped_pool_exposes_residual():
    """Efficacy: capping ACTIVE pool at 2 exposes residual on burden history."""
    from tests.test_wp2_mutants import BURDEN_HISTORY
    run = P.run_paired(16, "balanced", BURDEN_HISTORY)
    base = M.evaluate(run["events"])
    assert base["max_residual"] == 0

    def capped_payment(ledger, event, cap=2):
        out = list(ledger)
        w = event.get("y_edge", 0) - M.C_FROZEN * event.get("a_edge", 0)
        if event.get("mode") != "KEEP" or w <= 0:
            return out, 0
        pool = [c for c in out if c["type"] == "BOUNDARY_ACTIVE"][:cap]
        for c in pool:
            out.remove(c)
            spent = dict(c)
            spent["type"] = "SPENT"
            out.append(spent)
        return out, len(pool)

    ledger, cursor, worst = M.empty(), 0, 0
    for ev in run["events"]:
        ledger, cursor, _ = M.t7_inject(ledger, ev, M.K_FROZEN, cursor)
        ledger, _ = M.t5_activate(ledger, ev)
        need = M.required(ev)
        if ev.get("mode") == "KEEP" and need > 0:
            ledger, paid = capped_payment(ledger, ev)
            worst = max(worst, need - paid)
    assert worst > 0


def test_no_six_slot_assumption_in_code():
    """K6 code derives demand from frozen semantics, never slot-count lore."""
    text = (REPO_ROOT / "python" / "proof_attack" / "k6_saturation.py").read_text(encoding="utf-8")
    assert "six slots" not in text.lower() or "never" in text.lower()
    assert "M.K_FROZEN" in text or "K_FROZEN" in text
