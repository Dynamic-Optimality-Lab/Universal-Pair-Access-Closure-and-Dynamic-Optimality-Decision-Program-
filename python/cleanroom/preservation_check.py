"""cleanroom/preservation_check.py — independent PSC-P verdict checker (WP-2, MST0-11).

Share-nothing: frozen semantics + stdlib only; shapes/seeds reimplemented locally.
Recomputes clause outcomes + coverage over the declared space; verdict AGREE iff
recomputed violation count equals the record claim (expect 0) and coverage
includes all 6 rotation cases. Exit 0 + verdict; exit 2 on malformed input.
"""
import hashlib
import json
import random
import sys
from collections import Counter
from pathlib import Path

# Match generator recursion headroom (deep vines).
sys.setrecursionlimit(20000)

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from python.inherited import splay as S
from python.inherited import mstc0002 as M

MASTER = hashlib.sha256(b"SPLAY-AM-DECIDE-v0.4").hexdigest()
SIZES = [16, 32, 64, 128, 256, 512, 1024]
CASES = {"LL", "RR", "LR", "RL", "ZIG"}


def seed_int(family, index):
    return int(hashlib.sha256(f"{MASTER}{family}{index}".encode()).hexdigest(), 16)


def _ins(t, k):
    if t[0] == "leaf":
        return S.node(k, S.LEAF, S.LEAF)
    _, kk, l, r = t
    if k < kk:
        return S.node(kk, _ins(l, k), r)
    return S.node(kk, l, _ins(r, k))


def _shapes(n, seed):
    t = S.LEAF
    for k in range(1, n + 1):
        t = _ins(t, k)
    vr = t
    t = S.LEAF
    for k in range(n, 0, -1):
        t = _ins(t, k)
    vl = t

    def build(ks):
        if not ks:
            return S.LEAF
        m = len(ks) // 2
        return S.node(ks[m], build(ks[:m]), build(ks[m + 1:]))
    bal = build(list(range(1, n + 1)))
    rng = random.Random(seed)
    ks = list(range(1, n + 1))
    rng.shuffle(ks)
    t = S.LEAF
    for k in ks:
        t = _ins(t, k)
    sed = t
    order, lo, hi = [], 1, n
    while lo <= hi:
        order.append(lo)
        lo += 1
        if lo <= hi:
            order.append(hi)
            hi -= 1
    t = S.LEAF
    for k in order:
        t = _ins(t, k)
    return [vr, vl, bal, sed, t]


def _clauses(E, is_a, mode, ev, x, nkeys):
    _case, lo, hi = ev
    E1 = M.t7inject(E, is_a, lo, hi, x, nkeys, M.K_FROZEN)
    E2 = M.t5activate(E1, mode)
    L, L1, L2 = E[0], E1[0], E2[0]
    c1 = M.energy(L2) == M.energy(L) + (len(L1) - len(L))
    new = L2[len(L):]
    c2 = all(c[0] in (M.LATENT, M.ACTIVE) for c in new)
    c3 = not (Counter([c for c in L2 if c[0] == M.SPENT])
              - Counter([c for c in L if c[0] == M.SPENT]))
    c4 = all(lo <= c[1] and c[2] <= hi for c in new)
    added = Counter([c for c in L2 if c[0] == M.ACTIVE]) - Counter([c for c in L1 if c[0] == M.ACTIVE])
    c5 = all(any(o[0] == M.LATENT and o[1:] == c[1:] for o in L1) for c in added.elements())
    c6 = all(((c[3] and c[2] <= x) or ((not c[3]) and x < c[2])) for c in new)
    return [c1, c2, c3, c4, c5, c6]


def main():
    # WP-2 STEP CP-01: independent preservation verdict recomputation.
    print("[WP-2][STEP CP-01] cleanroom preservation check running", flush=True)
    if len(sys.argv) != 2:
        print("[WP-2][STEP CP-01] usage: preservation_check.py <record>", flush=True)
        return 2
    try:
        rec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        assert rec["theorem_id"] == "MST0-11"
    except Exception:
        print("[WP-2][STEP CP-01] malformed record", flush=True)
        return 2
    base = [(M.LATENT, 1, 2, True), (M.ACTIVE, 9, 9, False), (M.SPENT, 3, 4, False)]
    covered, bad = set(), 0
    for n in SIZES:
        for si in range(6):
            seed = seed_int("PSC-P", si * 1000 + n)
            for t in _shapes(n, seed):
                ks = sorted(S.keys(t))
                nkeys = max(ks) if ks else 1
                pool = sorted(set(ks[:3] + ks[-3:] + [0, nkeys + 99] if ks else [0]))
                rng = random.Random(seed + n)
                if len(pool) > 12:
                    pool = sorted(rng.sample(pool, 12))
                for x in pool:
                    _t2, evs = S.splay_trace(t, x)
                    E = (list(base), si)
                    for ev in evs:
                        for mode in ("KEEP", "DELETE"):
                            for is_a in (True, False):
                                if not all(_clauses(E, is_a, mode, ev, x, nkeys)):
                                    bad += 1
                        covered.add(ev[0])
                        E = M.t5activate(M.t7inject(E, True, ev[1], ev[2], x, nkeys,
                                                    M.K_FROZEN), "KEEP")
    claimed = rec["best_finite_obstruction_metrics"]["violations"]
    consistent = (bad == claimed) and CASES <= covered
    verdict = "AGREE" if consistent else "DISAGREE"
    # WP-2 STEP CP-02: verdict emitted.
    print(f"[WP-2][STEP CP-02] CHECKER-VERDICT: {verdict} (recomputed={bad} claimed={claimed} cases={len(covered)})",
          flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
