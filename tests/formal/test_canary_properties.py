"""Canary property checks over the executable core (DIAGNOSTIC ONLY, v0.4.7 G10).

These execute TRUE-by-construction mechanism identities on deterministic samples.
They never prove theorems and never establish Lean<->Python equivalence (Phase-03).
Seeded RNG + sorted outputs per prereg policy.
"""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from python.inherited import splay as S
from python.inherited import mstc0002 as M

RNG = random.Random(20260926)


def bst_insert(t, k):
    if t[0] == "leaf":
        return S.node(k, S.LEAF, S.LEAF)
    _, kk, l, r = t
    if k < kk:
        return S.node(kk, bst_insert(l, k), r)
    if k > kk:
        return S.node(kk, l, bst_insert(r, k))
    return t


def random_bst(n, rng):
    ks = list(range(1, n + 1))
    rng.shuffle(ks)
    t = S.LEAF
    for k in ks:
        t = bst_insert(t, k)
    return t


def sample_trees():
    ts = [S.LEAF]
    for n in (1, 3, 7, 15):
        ks = list(range(1, n + 1))
        t = S.LEAF
        for k in ks:  # degenerate chain
            t = bst_insert(t, k)
        ts.append(t)
        for _ in range(4):
            ts.append(random_bst(n, RNG))
    return ts


def test_splay_preserves_validity_keys_and_roots():
    for t in sample_trees():
        ks = S.keys(t)
        for x in ([1, 2, 3, 5, 8, 99] + ks):
            t2 = S.splay(t, x)
            assert S.valid(t2), (t, x)
            assert sorted(S.keys(t2)) == sorted(ks), (t, x)
            if x in ks:
                assert t2[0] == "node" and t2[1] == x, (t, x)


def test_cost_is_depth_plus_one():
    for t in sample_trees():
        for x in S.keys(t) + [0, 99]:
            assert S.splay_cost(t, x) == S.depth(t, x) + 1


def test_trace_events_bounded_by_cost():
    # Lemma shape underlying MST0-13 truth: #events <= cost.
    for t in sample_trees():
        for x in S.keys(t) + [0, 99]:
            _, evs = S.splay_trace(t, x)
            assert len(evs) <= S.splay_cost(t, x), (t, x, evs)


def test_t7_growth_bounded_and_supports_contained():
    # 08U mechanism + 11 C4/C6 over real rotation events.
    for t in sample_trees():
        ks = S.keys(t)
        nkeys = max(ks) if ks else 1
        for x in ks + [0]:
            _, evs = S.splay_trace(t, x)
            for case, lo, hi in evs:
                E = ([], 0)
                E2 = M.t7inject(E, True, lo, hi, x, nkeys, M.K_FROZEN)
                assert len(E2[0]) - len(E[0]) <= M.K_FROZEN
                for c in E2[0][len(E[0]):]:
                    assert lo <= c[1] and c[2] <= hi, (evs, c)
                    if c[3]:
                        assert c[2] <= x
                    else:
                        assert x < c[2]


def test_t5_preserves_energy_and_no_spent_creation():
    # 11 C1-shape + C3-shape.
    for t in sample_trees():
        ks = S.keys(t)
        nkeys = max(ks) if ks else 1
        for x in ks[:4]:
            _, evs = S.splay_trace(t, x)
            E = ([(M.LATENT, 1, 2, True), (M.SPENT, 3, 4, False)], 0)
            for ev in evs:
                _, lo, hi = ev
                E1 = M.t7inject(E, True, lo, hi, x, nkeys, M.K_FROZEN)
                E2 = M.t5activate(E1, "KEEP")
                assert M.energy(E2[0]) == M.energy(E[0]) + (len(E1[0]) - len(E[0]))
                spent_out = {c for c in E2[0] if c[0] == M.SPENT}
                spent_in = {c for c in E[0] if c[0] == M.SPENT}
                assert spent_out <= spent_in
                E = E2


def test_discharge_min_conservation_and_split():
    # 14-mechanism + 15 D4 + 15 D2 on sampled ledgers.
    ledgers = [[], [(M.LATENT, 1, 2, True)],
               [(M.ACTIVE, 1, 2, True), (M.LATENT, 2, 3, False), (M.SPENT, 4, 5, True),
                (M.ACTIVE, 5, 6, True)]]
    for L in ledgers:
        for need in (0, 1, 2, 5):
            out, paid = M.discharge(L, need)
            assert paid == min(M.active_pool(L), need)
            assert M.active_pool(out) + paid == M.active_pool(L)
        for n1, n2 in ((0, 0), (1, 1), (1, 3), (2, 2)):
            out_whole, paid_whole = M.discharge(L, n1 + n2)
            out1, paid1 = M.discharge(L, n1)
            out2, paid2 = M.discharge(out1, n2)
            assert paid_whole == paid1 + paid2
            assert out2 == out_whole


def test_replay_access_growth_bounded_by_6x_cost():
    # 13 mechanism over real accesses.
    for t in sample_trees():
        ks = S.keys(t)
        nkeys = max(ks) if ks else 1
        for x in ks[:5]:
            E = ([], 7)
            E2, _A2, a = M.replay_access_A(E, t, "DELETE", x, nkeys)
            assert M.energy(E2[0]) - M.energy(E[0]) <= 6 * a


def test_exec_hist_partition_consistency():
    # 15 D5 executable analogue: sequential == whole (engines, trees, costs).
    for t in sample_trees():
        ks = S.keys(t)
        if not ks:
            continue
        nkeys = max(ks)
        H = [("KEEP", ks[i % len(ks)]) for i in range(6)] + [("DELETE", ks[0])]
        E0 = ([], 0)
        for cut in (1, 3, 6):
            H1, H2 = H[:cut], H[cut:]
            E1, A1, B1, sA1, sB1 = M.exec_trees(E0, t, t, H1, nkeys)
            E2, A2, B2, sA2, sB2 = M.exec_loop(E1, A1, B1, nkeys, H2, sA1, sB1)
            Ew, Aw, Bw, sAw, sBw = M.exec_trees(E0, t, t, H, nkeys)
            assert (E2, sA2, sB2) == (Ew, sAw, sBw)
            assert A2 == Aw and B2 == Bw


def test_required_uses_C2_and_suffices_runs():
    # 22 linkage + 14 executable (paid <= need invariant; bool runs).
    for y in range(0, 12):
        for a in range(0, 6):
            assert M.required(y, a) == max(y - M.C_FROZEN * a, 0)
    for t in sample_trees():
        ks = S.keys(t)
        if not ks:
            continue
        nkeys = max(ks)
        H = [("KEEP", x) for x in (ks * 2)[:6]]
        assert isinstance(M.exec_suffices(([], 0), t, t, H, nkeys), bool)
