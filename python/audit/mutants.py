"""Executable proof mutants for Phase-2 checkers (WorkPlan Phase 2; T099/T100).

Each mutant function perturbs one frozen behavior; the suite MUST reject it
(i.e., observe the defect signal). A mutant that passes is a suite defect.
The known-killed control is relax-k-to-1 (parent-analogue sensitivity).
"""
from __future__ import annotations

from python.inherited import mstc0002 as M

MUTANTS = ["drop-ROOT", "drop-ZIG", "drop-LL", "t5-mints-spent",
           "support-no-validation", "relax-k-to-1"]


def evaluate_relaxed_k(events):
    """Mutant relax-k-to-1: weakened injection must expose residual."""
    return M.evaluate(events, k=1)


def evaluate_t5_mints_spent(events):
    """Mutant t5-mints-spent: activation produces SPENT, starving repayment."""
    ledger = M.empty()
    cursor = 0
    max_res = 0
    for ev in events:
        ledger, cursor, _ = M.t7_inject(ledger, ev, M.K_FROZEN, cursor)
        if M.predicate_fires(M.PREDICATE_ALL, ev):
            hit = next((c for c in ledger if c["type"] == "BOUNDARY_LATENT"), None)
            if hit is not None:
                ledger.remove(hit)
                spent = dict(hit)
                spent["type"] = "SPENT"
                ledger.append(spent)
        need = M.required(ev)
        if ev.get("mode") == "KEEP" and need > 0:
            ledger, paid = M.imported_payment(ledger, ev)
            max_res = max(max_res, need - paid)
    return {"feasible": max_res == 0, "max_residual": max_res}


def check_coverage_with_drop(covered, drop):
    """Mutant drop-case: coverage missing one case must be flagged."""
    missing = [c for c in ["ROOT", "ZIG-left", "ZIG-right", "LL", "RR", "LR", "RL"]
               if c not in (set(covered) - {drop})]
    return missing


def known_killed_control():
    """The k=1 control descriptor (parent-analogue sensitivity)."""
    return {"mutant": "relax-k-to-1", "k": 1, "must_reject": True,
            "rationale": "weakened injection must expose positive residual"}
