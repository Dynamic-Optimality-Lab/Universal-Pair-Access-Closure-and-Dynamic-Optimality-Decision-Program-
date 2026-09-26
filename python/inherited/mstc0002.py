"""inherited/mstc0002.py — exact executable MSTC-0002 ledger semantics
(P_all, k=6, C=2; mirrors lean/Frozen/MSTC0002Defs.lean).

Interface-frozen pre-freeze; bytes hash-bound at Phase 1. Deterministic, no RNG,
no I/O. Credit: (ctype, lo, hi, left_oriented) with ctype in {LATENT, ACTIVE, SPENT}.
Engine: (ledger_list, cursor). Finite canary agreement against Lean is diagnostic
only (v0.4.7 G10); equivalence proved at Phase-03 execution.
"""
from __future__ import annotations
from . import splay as S

C_FROZEN = 2
K_FROZEN = 6

LATENT, ACTIVE, SPENT = "LATENT", "ACTIVE", "SPENT"

def p_all(mode):
    return True  # fires on KEEP and DELETE

def ledger_empty():
    return []

def energy(ledger):
    return sum(1 for c in ledger if c[0] in (LATENT, ACTIVE))

def sites(lo, hi, x, nkeys):
    out = []
    for i in range(lo, max(lo, hi)):
        if 1 <= i and i < nkeys and i + 1 <= hi:
            out.append((i, i + 1, (i + 1) <= x))
    return out

def t7inject(engine, is_a, lo, hi, x, nkeys, k):
    ledger, cursor = engine
    if not is_a:
        return engine
    ss = sites(lo, hi, x, nkeys)
    if not ss:
        return engine
    picks = [ss[(cursor + j) % len(ss)] for j in range(k)]
    new = [(LATENT,) + s for s in picks]
    return (ledger + new, cursor + k)

def activate_first(ledger):
    for i, c in enumerate(ledger):
        if c[0] == LATENT:
            return ledger[:i] + [(ACTIVE,) + c[1:]] + ledger[i + 1:]
    return None

def t5activate(engine, mode):
    ledger, cursor = engine
    if not p_all(mode):
        return engine
    nxt = activate_first(ledger)
    if nxt is None:
        return engine
    return (nxt, cursor)

def active_pool(ledger):
    return sum(1 for c in ledger if c[0] == ACTIVE)

def discharge(ledger, need):
    """Fold: consume up to `need` ACTIVE into SPENT. Returns (ledger, paid)."""
    out, paid, rem = [], 0, need
    for c in ledger:
        if rem > 0 and c[0] == ACTIVE:
            out.append((SPENT,) + c[1:])
            paid += 1
            rem -= 1
        else:
            out.append(c)
    return (out, paid)

def regret(y, a):
    return y - 2 * a

def required(y, a):
    return max(regret(y, a), 0)

def replay_step(engine, is_a, mode, ev, x, nkeys):
    _, lo, hi = ev
    return t5activate(t7inject(engine, is_a, lo, hi, x, nkeys, K_FROZEN), mode)

def replay_access_A(engine, A, mode, x, nkeys):
    a = S.splay_cost(A, x)
    A2, evs = S.splay_trace(A, x)
    e = engine
    for ev in evs:
        e = replay_step(e, True, mode, ev, x, nkeys)
    return (e, A2, a)

def replay_access_B(engine, B, x, nkeys, a):
    y = S.splay_cost(B, x)
    B2, evs = S.splay_trace(B, x)
    e = engine
    for ev in evs:
        e = t5activate(e, "KEEP")
    need = required(y, a)
    ledger, paid = discharge(e[0], need)
    return ((ledger, e[1]), B2, y, paid)

def exec_loop(engine, A, B, n, H, sA, sB):
    e, a_tree, b_tree = engine, A, B
    for mode, x in H:
        if mode == "KEEP":
            e1, A2, a = replay_access_A(e, a_tree, mode, x, n)
            e2, B2, y, _paid = replay_access_B(e1, b_tree, x, n, a)
            e, a_tree, b_tree = e2, A2, B2
            sA, sB = sA + a, sB + y
        else:
            e1, A2, a = replay_access_A(e, a_tree, mode, x, n)
            e, a_tree = e1, A2
            sA = sA + a
    return (e, a_tree, b_tree, sA, sB)

def exec_hist(engine, T0, H, n):
    e, _A, _B, sA, sB = exec_loop(engine, T0, T0, n, H, 0, 0)
    return (e, sA, sB)

def exec_trees(engine, A, B, H, n):
    return exec_loop(engine, A, B, n, H, 0, 0)

def exec_suffices(engine, A, B, H, n):
    """True iff every KEEP discharge pays its positive regret in full."""
    e, a_tree, b_tree = engine, A, B
    for mode, x in H:
        if mode == "KEEP":
            a = S.splay_cost(a_tree, x)
            e1, A2, _a = replay_access_A(e, a_tree, mode, x, n)
            e2, B2, _y, paid = replay_access_B(e1, b_tree, x, n, a)
            if paid != required(S.splay_cost(b_tree, x), a):
                return False
            e, a_tree, b_tree = e2, A2, B2
        else:
            e1, A2, _a = replay_access_A(e, a_tree, mode, x, n)
            e, a_tree = e1, A2
    return True
