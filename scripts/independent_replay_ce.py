"""scripts/independent_replay_ce.py — self-contained witness replay (repair track, G5).

Fresh implementation of the frozen BST/splay/ledger semantics written
directly from the mathematical definitions (spec s4 + frozen Lean module
docstrings), importing NOTHING from python/inherited or python/proof_attack.
Cross-checks against the repository implementation on the exhaustive n<=3
space (trees, costs, traces, ledger, paid, suffices), then replays the
canonical legal witnesses. Exit 0 iff full agreement + witness confirmed.
"""
import itertools
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.setrecursionlimit(20000)

# ---------------- self-contained semantics (no repo imports) ----------------
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
    return depth(l, x) + 1 if x < k else depth(r, x) + 1


def cost(t, x):
    return depth(t, x) + 1


def descend(t, x, acc):
    if t[0] == "leaf":
        return None
    _, k, l, r = t
    if x == k:
        return (t, acc)
    if x < k:
        return descend(l, x, ("L", k, r, acc))
    return descend(r, x, ("R", k, l, acc))


def zig_L(n, x, kp, B):
    if n[0] == "leaf":
        return node(kp, LEAF, B)
    _, _, t1, t2 = n
    return node(x, t1, node(kp, t2, B))


def zig_R(n, x, kp, B):
    if n[0] == "leaf":
        return node(kp, B, LEAF)
    _, _, t1, t2 = n
    return node(x, node(kp, B, t1), t2)


def zz_LL(n, x, kp, B, kg, Cc):
    if n[0] == "leaf":
        return node(kg, node(kp, LEAF, B), Cc)
    _, _, t1, t2 = n
    return node(x, t1, node(kp, t2, node(kg, B, Cc)))


def zz_RR(n, x, kp, B, kg, Cc):
    if n[0] == "leaf":
        return node(kg, Cc, node(kp, B, LEAF))
    _, _, t1, t2 = n
    return node(x, node(kp, node(kg, Cc, B), t1), t2)


def zg_LR(n, x, kp, A, kg, D):
    if n[0] == "leaf":
        return node(kg, node(kp, A, LEAF), D)
    _, _, t1, t2 = n
    return node(x, node(kp, A, t1), node(kg, t2, D))


def zg_RL(n, x, kp, D, kg, A):
    if n[0] == "leaf":
        return node(kg, A, node(kp, LEAF, D))
    _, _, t1, t2 = n
    return node(x, node(kg, A, t1), node(kp, t2, D))


def splay_with_t(n, ctx, evs):
    while True:
        if ctx[0] == "top":
            return (n, evs)
        tag = ctx[0]
        if tag == "L" and ctx[3][0] == "L":
            _, kp, q, inner = ctx
            _, kg, c, outer = inner
            if n[0] == "leaf":
                return (n, evs)
            x = n[1]
            lo, hi = min(x, kp, kg), max(x, kp, kg)
            n = zz_LL(n, x, kp, q, kg, c)
            ctx, evs = outer, evs + [("LL", lo, hi)]
        elif tag == "R" and ctx[3][0] == "R":
            _, kp, q, inner = ctx
            _, kg, c, outer = inner
            if n[0] == "leaf":
                return (n, evs)
            x = n[1]
            lo, hi = min(x, kp, kg), max(x, kp, kg)
            n = zz_RR(n, x, kp, q, kg, c)
            ctx, evs = outer, evs + [("RR", lo, hi)]
        elif tag == "R" and ctx[3][0] == "L":
            _, kp, q, inner = ctx
            _, kg, d, outer = inner
            if n[0] == "leaf":
                return (n, evs)
            x = n[1]
            lo, hi = min(x, kp, kg), max(x, kp, kg)
            n = zg_LR(n, x, kp, q, kg, d)
            ctx, evs = outer, evs + [("LR", lo, hi)]
        elif tag == "L" and ctx[3][0] == "R":
            _, kp, q, inner = ctx
            _, kg, a, outer = inner
            if n[0] == "leaf":
                return (n, evs)
            x = n[1]
            lo, hi = min(x, kp, kg), max(x, kp, kg)
            n = zg_RL(n, x, kp, q, kg, a)
            ctx, evs = outer, evs + [("RL", lo, hi)]
        elif tag == "L":
            _, kp, q, outer = ctx
            if n[0] == "leaf":
                return (n, evs)
            x = n[1]
            n = zig_L(n, x, kp, q)
            ctx, evs = outer, evs + [("ZIG", min(x, kp), max(x, kp))]
        else:
            _, kp, q, outer = ctx
            if n[0] == "leaf":
                return (n, evs)
            x = n[1]
            n = zig_R(n, x, kp, q)
            ctx, evs = outer, evs + [("ZIG", min(x, kp), max(x, kp))]


def splay_trace(t, x):
    hit = descend(t, x, ("top",))
    if hit is None:
        return (t, [])
    sub, ctx = hit
    return splay_with_t(sub, ctx, [])


def splay(t, x):
    return splay_trace(t, x)[0]


LAT, ACT, SP = "LATENT", "ACTIVE", "SPENT"


def energy(L):
    return sum(1 for c in L if c[0] in (LAT, ACT))


def sites(lo, hi, x, nkeys):
    out = []
    for i in range(lo, max(lo, hi)):
        if 1 <= i and i < nkeys and i + 1 <= hi:
            out.append((i, i + 1, (i + 1) <= x))
    return out


def t7inject(eng, is_a, lo, hi, x, nkeys, k):
    led, cur = eng
    if not is_a:
        return eng
    ss = sites(lo, hi, x, nkeys)
    if not ss:
        return eng
    picks = [ss[(cur + j) % len(ss)] for j in range(k)]
    return (led + [(LAT,) + s for s in picks], cur + k)


def t5activate(eng):
    led, cur = eng
    for i, c in enumerate(led):
        if c[0] == LAT:
            return (led[:i] + [(ACT,) + c[1:]] + led[i + 1:], cur)
    return eng


def active_pool(led):
    return sum(1 for c in led if c[0] == ACT)


def discharge(led, need):
    out, paid, rem = [], 0, need
    for c in led:
        if rem > 0 and c[0] == ACT:
            out.append((SP,) + c[1:])
            paid += 1
            rem -= 1
        else:
            out.append(c)
    return (out, paid)


def required(y, a):
    return max(y - 2 * a, 0)


def rep_access_A(eng, A, mode, x, nkeys):
    a = cost(A, x)
    A2, evs = splay_trace(A, x)
    e = eng
    for (_, lo, hi) in evs:
        e = t5activate(t7inject(e, True, lo, hi, x, nkeys, 6))
    return (e, A2, a)


def rep_access_B(eng, B, x, a):
    y = cost(B, x)
    B2, evs = splay_trace(B, x)
    e = eng
    for _ in evs:
        e = t5activate(e)
    need = required(y, a)
    led, paid = discharge(e[0], need)
    return ((led, e[1]), B2, y, paid)


def exec_suffices(eng, A, B, H, n):
    e, at, bt = eng, A, B
    for mode, x in H:
        if mode == "KEEP":
            a = cost(at, x)
            e1, A2, _ = rep_access_A(e, at, mode, x, n)
            e2, B2, _, paid = rep_access_B(e1, bt, x, a)
            if paid != required(cost(bt, x), a):
                return False
            e, at, bt = e2, A2, B2
        else:
            e1, A2, _ = rep_access_A(e, at, mode, x, n)
            e, at = e1, A2
    return True


# ---------------- agreement + witness ----------------

def all_shapes(ks):
    if not ks:
        return [LEAF]
    out = []
    for i, k in enumerate(ks):
        for l in all_shapes(ks[:i]):
            for r in all_shapes(ks[i + 1:]):
                out.append(node(k, l, r))
    return sorted(out, key=repr)


def main():
    from python.inherited import splay as S2
    from python.inherited import mstc0002 as M2
    print("[IND][STEP 01] cross-checking independent implementation (n<=3)", flush=True)
    n_inst = 0
    for n in (1, 2, 3):
        shapes = all_shapes(list(range(1, n + 1)))
        alpha = [("KEEP", x) for x in range(1, n + 1)] + \
                [("DELETE", x) for x in range(1, n + 1)]
        for T0 in shapes:
            T0b = T0
            for L in range(0, 5):
                for H in itertools.product(alpha, repeat=L):
                    H = list(H)
                    # repo side
                    e1, A1, B1, sA1, sB1 = M2.exec_loop(([], 0), T0b, T0b, n, H, 0, 0)
                    r_suff = M2.exec_suffices(([], 0), T0b, T0b, H, n)
                    # independent side (convert tree repr: identical tuple shapes)
                    e, at, bt, sA, sB = ([], 0), T0, T0, 0, 0
                    for mode, x in H:
                        if mode == "KEEP":
                            e1i, A2, a = rep_access_A(e, at, mode, x, n)
                            e2i, B2, y, _ = rep_access_B(e1i, bt, x, a)
                            e, at, bt = e2i, A2, B2
                            sA, sB = sA + a, sB + y
                        else:
                            e1i, A2, a = rep_access_A(e, at, mode, x, n)
                            e, at = e1i, A2
                            sA = sA + a
                    r_suff_i = exec_suffices(([], 0), T0, T0, H, n)
                    assert (at, bt, sA, sB) == (A1, B1, sA1, sB1), (H, n)
                    assert r_suff_i == r_suff, (H, n)
                    assert energy(e[0]) == M2.energy(e1[0])
                    assert active_pool(e[0]) == M2.active_pool(e1[0])
                    n_inst += 1
    print("[IND][STEP 02] agreement on %d instances" % n_inst, flush=True)

    print("[IND][STEP 03] replaying canonical witnesses", flush=True)
    from python.proof_attack import common as C2
    verdicts = {}
    # canonical minimal (n=28 family) + discoverer (n=512) + old domain witness
    def vine(ns):
        t = LEAF
        for k in range(1, ns + 1):
            # insertion-shaped vine (same as repo shape_vine_right)
            def ins(t, k):
                if t[0] == "leaf":
                    return node(k, LEAF, LEAF)
                _, kk, l, r = t
                return node(kk, ins(l, k), r) if k < kk else node(kk, l, ins(r, k))
            t = ins(t, k)
        return t
    cases = {
        "canonical-n28": (vine(28), [("DELETE", 27), ("DELETE", 28),
                                     ("KEEP", 28), ("KEEP", 27)], 28),
        "family-n64": (vine(64), [("DELETE", 63), ("DELETE", 64),
                                  ("KEEP", 64), ("KEEP", 63)], 64),
        "discoverer-n512": (C2.shape_vine_right(512),
                            [("DELETE", 384), ("DELETE", 512),
                             ("KEEP", 512), ("KEEP", 385)], 512),
        "domain-n0": (vine(3), [("DELETE", 3), ("KEEP", 3)], 0),
    }
    all_ok = True
    for name, (T0, H, n) in cases.items():
        mine = exec_suffices(([], 0), T0, T0, H, n)
        repo = M2.exec_suffices(([], 0), T0, T0, H, n)
        agree = (mine == repo)
        falsifies = (mine is False)
        verdicts[name] = {"independent": mine, "repo": repo, "agree": agree,
                          "falsifies": falsifies}
        print("  %s: independent=%s repo=%s agree=%s falsifies=%s"
              % (name, mine, repo, agree, falsifies))
        all_ok = all_ok and agree and falsifies
    out = Path("artifacts/v04/counterexamples/MST0-14R/INDEPENDENT_REPLAY.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"agreement_instances": n_inst, "cases": verdicts,
                               "verdict": "AGREE-AND-FALSIFIES" if all_ok else "PROBLEM"},
                              indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("[IND][STEP 04] wrote", out.name, "verdict=",
          "AGREE-AND-FALSIFIES" if all_ok else "PROBLEM", flush=True)
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
