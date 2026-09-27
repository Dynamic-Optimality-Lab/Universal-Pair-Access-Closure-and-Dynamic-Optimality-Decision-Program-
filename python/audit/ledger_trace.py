"""audit/ledger_trace.py — instrumented paired-execution tracer (MST0-14R track).

New file (repair track, not frozen). Replays a paired execution with the
exact frozen operators while recording every scalar quantity needed for
invariant discovery (Secs 18-22): per-access depths/costs/traces, LATENT /
ACTIVE / SPENT counts, successful vs attempted activations, cumulative
injections/demand/payments, per-KEEP margins, candidate-potential values.

Deterministic, no RNG, no I/O. Read-only over frozen semantics.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from python.inherited import splay as S
from python.inherited import mstc0002 as M


def counts(ledger):
    """(L, P, Sp) counts from a ledger list."""
    L = sum(1 for c in ledger if c[0] == M.LATENT)
    P = sum(1 for c in ledger if c[0] == M.ACTIVE)
    return (L, P, len(ledger) - L - P)


def trace_execution(T0, H, n):
    """Replay (T0,H,n) from the empty engine; return (steps, summary).

    steps: one record per access with pre/post ledger counts, trace lengths,
      costs, need/paid/margin (KEEP), activation success details.
    summary: cumulative RA/RB/injected/ActA/ActB/demand/paid, min margin,
      first failing KEEP index (None if suffices), final counts/energy.
    """
    E, A, B = ([], 0), T0, T0
    sA = sB = 0
    RA = RB = 0
    injected = actA = actB = 0
    demand = paid_tot = 0
    steps = []
    min_margin = None
    first_fail = None
    for idx, (mode, x) in enumerate(H):
        L0, P0, S0 = counts(E[0])
        if mode == "KEEP":
            Atr = S.splay_trace(A, x)[1]
            Btr = S.splay_trace(B, x)[1]
            a, y = S.splay_cost(A, x), S.splay_cost(B, x)
            rA, rB = len(Atr), len(Btr)
            E1, A2, a2 = M.replay_access_A(E, A, mode, x, n)
            assert a2 == a
            L1, P1, _ = counts(E1[0])
            assert L1 - L0 == 6 * rA - rA and P1 - P0 == rA, \
                (L0, P0, L1, P1, rA)  # legal-domain exact A-phase law
            E2, B2, y2, paid = M.replay_access_B(E1, B, x, a)
            assert y2 == y
            L2, P2, _ = counts(E2[0])
            need = M.required(y, a)
            margin = (P1 + (P2 - P1) + paid) - need  # pre-discharge pool - need
            # P2 = pool AFTER discharge; pre-discharge pool = P2 + paid.
            pre_pool = P2 + paid
            assert margin == pre_pool - need
            actB_k = (P2 + paid) - P1  # successful B activations
            assert 0 <= actB_k <= rB
            if min_margin is None or margin < min_margin:
                min_margin = margin
            if paid != need and first_fail is None:
                first_fail = idx
            steps.append({"idx": idx, "mode": mode, "x": x,
                          "dA": S.depth(A, x), "dB": S.depth(B, x),
                          "a": a, "y": y, "rA": rA, "rB": rB,
                          "L0": L0, "P0": P0, "S0": S0,
                          "L1": L1, "P1": P1, "L2": L2, "P2": P2,
                          "need": need, "paid": paid, "margin": margin,
                          "actB_k": actB_k, "sA": sA + a, "sB": sB + y})
            RA += rA
            RB += rB
            injected += 6 * rA
            actA += rA
            actB += actB_k
            demand += need
            paid_tot += paid
            E, A, B = E2, A2, B2
            sA, sB = sA + a, sB + y
        else:
            Atr = S.splay_trace(A, x)[1]
            a = S.splay_cost(A, x)
            rA = len(Atr)
            E1, A2, a2 = M.replay_access_A(E, A, mode, x, n)
            assert a2 == a
            L1, P1, _ = counts(E1[0])
            steps.append({"idx": idx, "mode": mode, "x": x,
                          "dA": S.depth(A, x), "dB": None,
                          "a": a, "y": 0, "rA": rA, "rB": 0,
                          "L0": L0, "P0": P0, "S0": S0,
                          "L1": L1, "P1": P1, "need": 0, "paid": 0,
                          "margin": None, "actB_k": 0, "sA": sA + a,
                          "sB": sB})
            RA += rA
            injected += 6 * rA
            actA += rA
            E, A = E1, A2
            sA = sA + a
    Lf, Pf, Sf = counts(E[0])
    summary = {"RA": RA, "RB": RB, "injected": injected, "actA": actA,
               "actB": actB, "demand": demand, "paid": paid_tot,
               "min_margin": min_margin, "first_fail": first_fail,
               "sA": sA, "sB": sB, "Lf": Lf, "Pf": Pf, "Sf": Sf,
               "energy": Lf + Pf,
               "balance_L": Lf - (injected - actA - actB),
               "balance_P": Pf - (actA + actB - paid_tot),
               "suffices": first_fail is None}
    return steps, summary
