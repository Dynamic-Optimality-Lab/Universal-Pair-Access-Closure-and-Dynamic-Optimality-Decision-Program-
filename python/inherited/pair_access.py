"""inherited/pair_access.py — legal-history validation + paired-cost comparison
(mirrors the Pair-Access contract, v0.4 s4; executable companion to exec_hist).

Interface-frozen pre-freeze; bytes hash-bound at Phase 1. Deterministic, no RNG,
no I/O. History: list of (mode, x) with mode in {KEEP, DELETE}.
"""
from __future__ import annotations
from . import splay as S
from . import mstc0002 as M

def validate_history(H, nkeys):
    """True iff every access is well-formed (mode known, 1 <= x <= nkeys)."""
    for mode, x in H:
        if mode not in ("KEEP", "DELETE"):
            return False
        if not (1 <= x <= nkeys):
            return False
    return True

def keeps_only(H):
    return [x for mode, x in H if mode == "KEEP"]

def paired_costs(T0, H, n):
    """Return (sA, sB_final_engine_costs) without ledger effects: raw splay sums."""
    A, B, sA, sB = T0, T0, 0, 0
    for mode, x in H:
        if mode == "KEEP":
            A, B, a, y = S.keep_step(A, B, x)
            sA, sB = sA + a, sB + y
        else:
            A, a = S.delete_step(A, x)
            sA = sA + a
    return (sA, sB)

def composition_holds(T0, H, n, additive):
    """Check sB + Em <= 2*sA + A(n) + E0 on the executed paired run (diagnostic)."""
    E0 = ([], 0)
    E, sA, sB = M.exec_hist(E0, T0, H, n)
    return sB + M.energy(E[0]) <= 2 * sA + additive(n) + M.energy(E0[0])
