"""Clean-room core: independent Splay + MSTC-0002 re-implementation.

SHARE-NOTHING BOUNDARY: this module imports nothing from
python.inherited or python.proof_attack (stdlib only: fractions). It is
derived independently from the frozen rule text (spec sections 4/14,
TRANSFER_CALCULUS_LEDGER T7/T5/T6, cost depth+1, KEEP/DELETE). Agreement
between this core and the inherited core on recorded programs is evidence
of independent implementation, enforced by tests/test_cleanroom_isolation.py
(no import edge either way). Exact integers/Fractions only.
"""
from __future__ import annotations

from fractions import Fraction

K = 6
C = 2


class T:
    """Minimal BST node (independent implementation)."""

    __slots__ = ("k", "l", "r", "p")

    def __init__(self, k):
        self.k = k
        self.l = None
        self.r = None
        self.p = None


def _rot_right(p):
    x = p.l
    p.l = x.r
    if x.r is not None:
        x.r.p = p
    x.p = p.p
    if p.p is not None:
        if p.p.l is p:
            p.p.l = x
        else:
            p.p.r = x
    x.r = p
    p.p = x


def _rot_left(p):
    x = p.r
    p.r = x.l
    if x.l is not None:
        x.l.p = p
    x.p = p.p
    if p.p is not None:
        if p.p.l is p:
            p.p.l = x
        else:
            p.p.r = x
    x.l = p
    p.p = x


def _find(root, x):
    cur = root
    while cur is not None and cur.k != x:
        cur = cur.l if x < cur.k else cur.r
    if cur is None:
        raise KeyError(x)
    return cur


def depth(root, x):
    """Depth of x (root 0)."""
    d, cur = 0, root
    while cur is not None:
        if x == cur.k:
            return d
        cur = cur.l if x < cur.k else cur.r
        d += 1
    raise KeyError(x)


def _splay_cases(root, x):
    """Splay x; return (new_root, list of (case, keys, interval))."""
    node = _find(root, x)
    out = []
    while node.p is not None:
        p, g = node.p, node.p.p
        if g is None:
            case = "ZIG"
        elif p.l is node and g.l is p:
            case = "LL"
        elif p.r is node and g.r is p:
            case = "RR"
        elif p.l is node:
            case = "RL"
        else:
            case = "LR"
        keys = sorted({node.k, p.k} | ({g.k} if g is not None else set()))
        out.append((case, keys, (min(keys), max(keys))))
        if case == "ZIG":
            if p.l is node:
                _rot_right(p)
            else:
                _rot_left(p)
        elif case == "LL":
            _rot_right(g)
            _rot_right(p)
        elif case == "RR":
            _rot_left(g)
            _rot_left(p)
        elif case == "RL":
            _rot_right(p)
            _rot_left(g)
        else:
            _rot_left(p)
            _rot_right(g)
    while node.p is not None:
        node = node.p
    return node, out


def _build(shape, n):
    """Deterministic initial tree."""
    keys = list(range(1, n + 1))
    if shape == "balanced":
        def rec(ks):
            if not ks:
                return None
            m = len(ks) // 2
            t = T(ks[m])
            t.l = rec(ks[:m])
            if t.l is not None:
                t.l.p = t
            t.r = rec(ks[m + 1:])
            if t.r is not None:
                t.r.p = t
            return t
        return rec(keys)
    if shape in ("spine-left", "spine-right"):
        root = None
        seq = keys if shape == "spine-left" else list(reversed(keys))
        for k in seq:
            t = T(k)
            if root is None:
                root = t
            elif shape == "spine-left":
                t.l, root.p, root = root, t, t
            else:
                t.r, root.p, root = root, t, t
        return root
    raise ValueError(shape)


def run_program(nkeys, shape, history):
    """Run a paired program independently; return (events, cost_A, cost_B).

    Domain legality: A and B start from the SAME initial tree (Pair-Access
    precondition). Edge convention identical to the frozen contract: A events
    zeroed; terminal B-rotation of KEEP carries (a, y).
    """
    A, B = _build(shape, nkeys), _build(shape, nkeys)
    events = []
    ca = cb = 0
    for mode, x in history:
        a = depth(A, x) + 1
        ca += a
        A, steps = _splay_cases(A, x)
        for case, keys, iv in steps:
            events.append({"side": "A", "mode": mode, "splay_case": case,
                           "keys": keys, "interval": list(iv), "x": x,
                           "nkeys": nkeys, "a_edge": 0, "y_edge": 0})
        if mode == "KEEP":
            y = depth(B, x) + 1
            cb += y
            B, bsteps = _splay_cases(B, x)
            for case, keys, iv in bsteps:
                events.append({"side": "B", "mode": mode, "splay_case": case,
                               "keys": keys, "interval": list(iv), "x": x,
                               "nkeys": nkeys, "a_edge": 0, "y_edge": 0})
            if bsteps:
                events[-1]["a_edge"] = a
                events[-1]["y_edge"] = y
    return events, ca, cb


def evaluate(events):
    """Frozen ledger evaluation (independent derivation from rule text)."""
    ledger = []
    cursor = 0
    max_res = Fraction(0)
    first = None
    paid = injected = 0
    for idx, ev in enumerate(events):
        if ev["side"] == "A":
            lo, hi = ev["interval"]
            sites = [(i, i + 1, "LEFT" if i + 1 <= ev["x"] else "RIGHT")
                     for i in range(lo, hi) if 1 <= i < ev["nkeys"]]
            for _ in range(K):
                if not sites:
                    break
                i, j, o = sites[cursor % len(sites)]
                cursor += 1
                ledger.append(("LATENT", (i, j, o)))
                injected += 1
        matches = ev["mode"] in ("KEEP", "DELETE")
        if matches:
            for i, c in enumerate(ledger):
                if c[0] == "LATENT":
                    ledger[i] = ("ACTIVE", c[1])
                    break
        w = ev["y_edge"] - C * ev["a_edge"] if ev["mode"] == "KEEP" else 0
        if w > 0:
            got = 0
            rest = []
            for c in ledger:
                if got < w and c[0] == "ACTIVE":
                    got += 1
                else:
                    rest.append(c)
            ledger = rest + [("SPENT", None)] * got
            paid += got
            if w - got > max_res:
                max_res = w - got
                first = {"event_index": idx, "w": w, "paid": got,
                         "res": w - got}
    return {"feasible": max_res == 0, "max_residual": max_res,
            "first_violation": first, "paid_total": paid,
            "injected_total": injected}
