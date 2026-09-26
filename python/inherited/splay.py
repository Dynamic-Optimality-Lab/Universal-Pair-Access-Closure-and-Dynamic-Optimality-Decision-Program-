"""inherited/splay.py — exact executable Splay semantics (v0.4 s4; mirrors lean/Frozen/SplayDefs.lean).

Interface-frozen pre-freeze; bytes hash-bound at Phase 1. Deterministic, no RNG,
no I/O. BST: ('leaf',) | ('node', k, l, r). Context frames: ('top',) |
('left', kp, sib, outer) | ('right', kp, sib, outer). StepEv: (case, lo, hi).
"""
from __future__ import annotations

LEAF = ("leaf",)

def node(k, l, r):
    return ("node", k, l, r)

def keys(t):
    if t[0] == "leaf":
        return []
    _, k, l, r = t
    return keys(l) + [k] + keys(r)

def valid(t):
    ks = keys(t)
    return all(a < b for a, b in zip(ks, ks[1:]))

def depth(t, x):
    if t[0] == "leaf":
        return 0
    _, k, l, r = t
    if x == k:
        return 0
    if x < k:
        return depth(l, x) + 1
    return depth(r, x) + 1

def splay_cost(t, x):
    return depth(t, x) + 1

def descend_acc(t, x, acc):
    """Parent-first context: outermost frame is the parent, ('top',) the root end."""
    if t[0] == "leaf":
        return None
    _, k, l, r = t
    if x == k:
        return (t, acc)
    if x < k:
        return descend_acc(l, x, ("left", k, r, acc))
    return descend_acc(r, x, ("right", k, l, acc))

def descend(t, x):
    """Return (subtree, ctx) or None iff x absent."""
    return descend_acc(t, x, ("top",))

def plug(ctx, t):
    while ctx[0] != "top":
        _, k, q, outer = ctx
        if ctx[0] == "left":
            t = node(k, t, q)
        else:
            t = node(k, q, t)
        ctx = outer
    return t

def zigL(n, x, kp, B):
    if n[0] == "leaf":
        return node(kp, LEAF, B)
    _, _, t1, t2 = n
    return node(x, t1, node(kp, t2, B))

def zigR(n, x, kp, B):
    if n[0] == "leaf":
        return node(kp, B, LEAF)
    _, _, t1, t2 = n
    return node(x, node(kp, B, t1), t2)

def zigzigLL(n, x, kp, B, kg, C):
    if n[0] == "leaf":
        return node(kg, node(kp, LEAF, B), C)
    _, _, t1, t2 = n
    return node(x, t1, node(kp, t2, node(kg, B, C)))

def zigzigRR(n, x, kp, B, kg, C):
    if n[0] == "leaf":
        return node(kg, C, node(kp, B, LEAF))
    _, _, t1, t2 = n
    return node(x, node(kp, node(kg, C, B), t1), t2)

def zigzagLR(n, x, kp, A, kg, D):
    if n[0] == "leaf":
        return node(kg, node(kp, A, LEAF), D)
    _, _, t1, t2 = n
    return node(x, node(kp, A, t1), node(kg, t2, D))

def zigzagRL(n, x, kp, D, kg, A):
    if n[0] == "leaf":
        return node(kg, A, node(kp, LEAF, D))
    _, _, t1, t2 = n
    return node(x, node(kg, A, t1), node(kp, t2, D))

def span3(x, kp, kg):
    return (min(x, kp, kg), max(x, kp, kg))

def splay_with_t(n, ctx, evs):
    while True:
        if ctx[0] == "top":
            return (n, evs)
        tag = ctx[0]
        if tag == "left" and ctx[3][0] == "left":
            _, kp, q, inner = ctx
            _, kg, c, outer = inner
            if n[0] == "leaf":
                return (plug(ctx, n), evs)
            x = n[1]
            lo, hi = span3(x, kp, kg)
            n = zigzigLL(n, x, kp, q, kg, c)
            ctx, evs = outer, evs + [("LL", lo, hi)]
            continue
        if tag == "right" and ctx[3][0] == "right":
            _, kp, q, inner = ctx
            _, kg, c, outer = inner
            if n[0] == "leaf":
                return (plug(ctx, n), evs)
            x = n[1]
            lo, hi = span3(x, kp, kg)
            n = zigzigRR(n, x, kp, q, kg, c)
            ctx, evs = outer, evs + [("RR", lo, hi)]
            continue
        if tag == "right" and ctx[3][0] == "left":
            _, kp, q, inner = ctx
            _, kg, d, outer = inner
            if n[0] == "leaf":
                return (plug(ctx, n), evs)
            x = n[1]
            lo, hi = span3(x, kp, kg)
            n = zigzagLR(n, x, kp, q, kg, d)
            ctx, evs = outer, evs + [("LR", lo, hi)]
            continue
        if tag == "left" and ctx[3][0] == "right":
            _, kp, q, inner = ctx
            _, kg, a, outer = inner
            if n[0] == "leaf":
                return (plug(ctx, n), evs)
            x = n[1]
            lo, hi = span3(x, kp, kg)
            n = zigzagRL(n, x, kp, q, kg, a)
            ctx, evs = outer, evs + [("RL", lo, hi)]
            continue
        if tag == "left":
            _, kp, q, outer = ctx
            if n[0] == "leaf":
                return (plug(ctx, n), evs)
            x = n[1]
            n = zigL(n, x, kp, q)
            ctx, evs = outer, evs + [("ZIG", min(x, kp), max(x, kp))]
            continue
        _, kp, q, outer = ctx
        if n[0] == "leaf":
            return (plug(ctx, n), evs)
        x = n[1]
        n = zigR(n, x, kp, q)
        ctx, evs = outer, evs + [("ZIG", min(x, kp), max(x, kp))]

def splay(t, x):
    hit = descend(t, x)
    if hit is None:
        return t
    sub, ctx = hit
    return splay_with_t(sub, ctx, [])[0]

def splay_trace(t, x):
    hit = descend(t, x)
    if hit is None:
        return (t, [])
    sub, ctx = hit
    return splay_with_t(sub, ctx, [])

def keep_step(A, B, x):
    a, y = splay_cost(A, x), splay_cost(B, x)
    return (splay(A, x), splay(B, x), a, y)

def delete_step(A, x):
    a = splay_cost(A, x)
    return (splay(A, x), a)

def is_subseq(Y, X):
    it = iter(X)
    return all(any(v == w for w in it) for v in Y)
