"""cleanroom/repayment_check.py — independent K6 verdict checker (WP-3, MST0-14).

Share-nothing: frozen semantics + stdlib only; families reimplemented locally.
Recomputes per-KEEP (need, paid, residual) over the declared space and the
record's worst case; verdict AGREE iff recomputed worst equals the record
claim and witness status is consistent. Exit 0 + verdict; exit 2 malformed.
"""
import hashlib
import json
import random
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


def _tree(kind, n, seed):
    if kind == "balanced":
        def build(ks):
            if not ks:
                return S.LEAF
            m = len(ks) // 2
            return S.node(ks[m], build(ks[:m]), build(ks[m + 1:]))
        return build(list(range(1, n + 1)))
    if kind == "vine-right":
        order = list(range(1, n + 1))
    elif kind == "vine-left":
        order = list(range(n, 0, -1))
    elif kind == "seeded":
        rng = random.Random(seed)
        order = list(range(1, n + 1))
        rng.shuffle(order)
    elif kind == "alternating":
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
    return t


def _hists(dim, n, seed):
    """Mirror of the generator's 13 dimension families (reimplemented)."""
    ks = list(range(1, n + 1))
    even = [x for x in ks if x % 2 == 0]
    odds = [x for x in ks if x % 2 == 1]
    m = ks[n // 2]
    if dim == "scale":
        return [[("KEEP", x)] for x in (ks[:4] + ks[-4:])]
    if dim == "roles":
        return [[("KEEP", ks[0])] * 4, [("KEEP", ks[-1])] * 4,
                [("KEEP", a) for a in (ks[:2] + ks[-2:])]]
    if dim == "provenance":
        return [[("DELETE", m), ("KEEP", m)] * 3,
                [("KEEP", x) for x in ks[:6]]]
    if dim == "orientation":
        return [[("KEEP", 1)], [("KEEP", n)], [("KEEP", n // 2)]]
    if dim == "nested":
        return [[("KEEP", ks[-1 - i]) for i in range(min(8, n))]]
    if dim == "alternation":
        return [[("KEEP", a) for a in ([1, n] * 5)[:10]]]
    if dim == "crossings":
        return [[("KEEP", 1), ("KEEP", n)] * 4]
    if dim == "delete-bursts":
        return [[("DELETE", x) for x in ks[:6]] + [("KEEP", m)] * 4]
    if dim == "long-lived":
        return [[("KEEP", ks[(i * 7) % n]) for i in range(24)]]
    if dim == "simultaneous":
        return [[("KEEP", ks[n // 3])] * 8]
    if dim == "mirror":
        return [[("KEEP", 1)], [("KEEP", n)]]
    if dim == "rank-gap":
        return [[("KEEP", x) for x in even[:8]], [("KEEP", x) for x in odds[:8]]]
    if dim == "recurrent":
        motif = [("KEEP", ks[0]), ("KEEP", ks[-1]), ("KEEP", m)]
        return [motif * 2, motif * 3]
    raise ValueError(dim)


CLASSES = ["scale", "roles", "provenance", "orientation", "nested",
           "alternation", "crossings", "delete-bursts", "long-lived",
           "simultaneous", "mirror", "rank-gap", "recurrent"]


def _replay(T0, H, n):
    E, A, B, worst = ([], 0), T0, T0, -10 ** 9
    for mode, x in H:
        if mode == "KEEP":
            E1, A2, a = M.replay_access_A(E, A, mode, x, n)
            E2, B2, y, paid = M.replay_access_B(E1, B, x, a)
            need = M.required(y, a)
            worst = max(worst, need - paid)
            E, A, B = E2, A2, B2
        else:
            E1, A2, _a = M.replay_access_A(E, A, mode, x, n)
            E, A = E1, A2
    return worst


def main():
    # WP-3 STEP CK-01: independent repayment verdict recomputation.
    print("[WP-3][STEP CK-01] cleanroom repayment check running", flush=True)
    if len(sys.argv) != 2:
        print("[WP-3][STEP CK-01] usage: repayment_check.py <record>", flush=True)
        return 2
    try:
        rec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        assert rec["theorem_id"] == "MST0-14"
    except Exception:
        print("[WP-3][STEP CK-01] malformed record", flush=True)
        return 2
    worst = -10 ** 9
    import re
    m = re.search(r"sizes-\[([0-9, ]+)\]", rec.get("seed", ""))
    sizes = sorted(int(x) for x in m.group(1).split(",")) if m else SIZES
    kinds = ["balanced", "vine-right", "vine-left", "alternating", "seeded"]
    for n in sizes:
        for si in range(6):
            seed = seed_int("PSC-K6", si * 1000 + n)
            trees = [(kind, _tree(kind, n, seed)) for kind in kinds]
            for cls in CLASSES:
                for kind, t in trees:
                    for h in _hists(cls, n, seed):
                        worst = max(worst, _replay(t, h, n))
    claimed = rec["best_finite_obstruction_metrics"]["worst_residual"]
    consistent = (worst == claimed) and (rec["exact_witness"] is None) == (worst <= 0)
    verdict = "AGREE" if consistent else "DISAGREE"
    # WP-3 STEP CK-02: verdict emitted.
    print(f"[WP-3][STEP CK-02] CHECKER-VERDICT: {verdict} (recomputed={worst} claimed={claimed})",
          flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
