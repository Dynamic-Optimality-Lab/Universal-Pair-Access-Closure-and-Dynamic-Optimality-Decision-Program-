"""cleanroom/locality_check.py — independent PSC-L verdict checker (WP-2, MST0-08U).

Share-nothing: imports ONLY frozen semantics (python.inherited) + stdlib.
Shapes/seeds reimplemented locally (never imports proof_attack).
Reads one attack record path (argv[1]); recomputes the maximum per-event
growth over the declared input space; verdict AGREE iff recomputed maximum
equals the record claim AND witness status is consistent.
Exit 0 with verdict line; exit 2 on malformed input.
"""
import hashlib
import json
import sys
from pathlib import Path

# Match generator recursion headroom (deep vines).
sys.setrecursionlimit(20000)

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from python.inherited import splay as S
from python.inherited import mstc0002 as M

MASTER = hashlib.sha256(b"SPLAY-AM-DECIDE-v0.4").hexdigest()
SIZES = [16, 32, 64, 128, 256, 512, 1024]


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
    import random
    t = S.LEAF
    for k in range(1, n + 1):
        t = _ins(t, k)
    vine_r = t
    t = S.LEAF
    for k in range(n, 0, -1):
        t = _ins(t, k)
    vine_l = t

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
    return [("vine-right", vine_r), ("vine-left", vine_l), ("balanced", bal),
            ("seeded", sed), ("alternating", t)]


def main():
    # WP-2 STEP CL-01: independent locality verdict recomputation.
    print("[WP-2][STEP CL-01] cleanroom locality check running", flush=True)
    if len(sys.argv) != 2:
        print("[WP-2][STEP CL-01] usage: locality_check.py <record>", flush=True)
        return 2
    try:
        rec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        assert rec["theorem_id"] == "MST0-08U"
    except Exception:
        print("[WP-2][STEP CL-01] malformed record", flush=True)
        return 2
    best = -1
    for n in SIZES:
        for si in range(8):
            seed = seed_int("PSC-L", si * 1000 + n)
            for _sname, t in _shapes(n, seed):
                ks = sorted(S.keys(t))
                nkeys = max(ks) if ks else 1
                for span, xs in (("shallow", ks[:2]), ("deep", ks[-3:]),
                                 ("edge", (ks[:1] + ks[-1:] + [0, nkeys + 99]) if ks else [0])):
                    for x in sorted(set(xs)):
                        _t2, evs = S.splay_trace(t, x)
                        for _case, lo, hi in evs:
                            E2 = M.t7inject(([], 0), True, lo, hi, x, nkeys, M.K_FROZEN)
                            best = max(best, len(E2[0]))
    claimed = rec["objective_vector"]["best_growth"]
    consistent = (best == claimed) and ((rec["exact_witness"] is None) == (best <= M.K_FROZEN))
    verdict = "AGREE" if consistent else "DISAGREE"
    # WP-2 STEP CL-02: verdict emitted.
    print(f"[WP-2][STEP CL-02] CHECKER-VERDICT: {verdict} (recomputed={best} claimed={claimed})",
          flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
