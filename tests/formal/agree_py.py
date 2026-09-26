"""Python mirror of lean/Agree.lean (FORM-04/05/06/07 agreement).
Prints byte-identical canonical lines for the same fixed samples.
Line-ending normalization (splitlines) is transport-only, not semantic.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from python.inherited import splay as S
from python.inherited import mstc0002 as M


def show_tree(t):
    if t[0] == "leaf":
        return "leaf"
    _, k, l, r = t
    return f"(node {k} {show_tree(l)} {show_tree(r)})"


def path_keys(ctx):
    ks = []
    while ctx[0] != "top":
        _, k, _q, outer = ctx
        ks.append(k)
        ctx = outer
    return list(reversed(ks))


def show_trace(evs):
    return ";".join(f"{c}:{lo}-{hi}" for c, lo, hi in evs)


def N(k, l, r):
    return S.node(k, l, r)


L = S.LEAF
T1 = N(4, N(2, N(1, L, L), N(3, L, L)), N(6, N(5, L, L), N(7, L, L)))
T2 = N(1, L, N(2, L, N(3, L, L)))
T3 = N(3, N(2, N(1, L, L), L), L)
T4 = N(3, N(1, L, N(2, L, L)), N(6, N(4, L, N(5, L, L)), N(7, L, L)))
H1 = [("KEEP", 3), ("KEEP", 5), ("DELETE", 2), ("KEEP", 7)]
H2 = [("KEEP", 1), ("KEEP", 2), ("KEEP", 3), ("DELETE", 1)]


def emit_access(tid, t, x):
    print(f"TREE {tid} {show_tree(S.splay(t, x))}")
    hit = S.descend(t, x)
    if hit is None:
        print(f"PATH {tid}:{x} ABSENT")
    else:
        _sub, ctx = hit
        print(f"PATH {tid}:{x} {','.join(map(str, path_keys(ctx)))}")
    _t2, evs = S.splay_trace(t, x)
    print(f"TRACE {tid}:{x} {show_trace(evs)}")
    print(f"COST {tid}:{x} {S.splay_cost(t, x)}")


def emit_hist(hid, t, h, n):
    E, sA, sB = M.exec_hist(([], 0), t, h, n)
    print(f"LEDGER {hid} {M.energy(E[0])} {sA} {sB}")


def main():
    for tid, t, x in [("t1", T1, 1), ("t1", T1, 4), ("t1", T1, 7), ("t1", T1, 0),
                      ("t2", T2, 3), ("t2", T2, 1), ("t2", T2, 99),
                      ("t3", T3, 1), ("t3", T3, 3), ("t3", T3, 0),
                      ("t4", T4, 5), ("t4", T4, 2), ("t4", T4, 6), ("t4", T4, 99)]:
        emit_access(tid, t, x)
    emit_hist("h1", T1, H1, 7)
    emit_hist("h2", T2, H2, 3)


if __name__ == "__main__":
    main()
