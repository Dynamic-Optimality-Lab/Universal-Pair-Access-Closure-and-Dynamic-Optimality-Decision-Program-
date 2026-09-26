"""cleanroom/boundary_check.py — independent PSC-B verdict checker (WP-2, MST0-09).

Share-nothing: frozen semantics + stdlib only; classes/shapes/seeds reimplemented
locally. Recomputes maximum per-event growth over the 12 declared classes;
verdict AGREE iff recomputed maximum equals the record claim. Exit 0 + verdict;
exit 2 on malformed input.
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
CLASSES = ["nested", "alternating", "creation-rate", "rank-gap", "span",
           "burden", "burst", "lifetime", "reactivation", "asymmetry",
           "mirror", "scale"]


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
    t = S.LEAF
    if kind == "vine-right":
        order = list(range(1, n + 1))
    elif kind == "vine-left":
        order = list(range(n, 0, -1))
    elif kind == "balanced":
        def build(ks):
            if not ks:
                return S.LEAF
            m = len(ks) // 2
            return S.node(ks[m], build(ks[:m]), build(ks[m + 1:]))
        return build(list(range(1, n + 1)))
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
    for k in order:
        t = _ins(t, k)
    return t


def _probes(cls, n, seed):
    vr = _tree("vine-right", n, seed)
    vl = _tree("vine-left", n, seed)
    bal = _tree("balanced", n, seed)
    sed = _tree("seeded", n, seed)
    alt = _tree("alternating", n, seed)
    if cls == "nested":
        ks = sorted(S.keys(vr))
        return [("access", vr, x, max(ks)) for x in (n, n - 1, 1)]
    if cls in ("alternating", "rank-gap"):
        t = alt if cls == "alternating" else sed
        ks = sorted(S.keys(t))
        return [("access", t, x, max(ks)) for x in (1, n, 0)]
    if cls in ("span", "asymmetry"):
        t = vl
        ks = sorted(S.keys(t))
        xs = (1, n, 0, n + 99) if cls == "span" else (1, 2, n)
        return [("access", t, x, max(ks)) for x in xs]
    if cls in ("burden", "mirror"):
        t = vr
        ks = sorted(S.keys(t))
        xs = (n,) if cls == "burden" else (n, n - 1, 1)
        return [("access", t, x, max(ks)) for x in xs]
    if cls == "scale":
        ks = sorted(S.keys(bal))
        return [("access", bal, x, max(ks)) for x in (1, n // 2, n, 0)]
    ks = sorted(S.keys(bal if cls != "lifetime" else sed))
    t = bal if cls != "lifetime" else sed
    if not ks:
        return []
    if cls == "creation-rate":
        return [("history", t, [( "KEEP", x) for x in (ks * 3)[:12]], max(ks))]
    if cls == "burst":
        return [("history", t, [("KEEP", ks[len(ks) // 2])] * 8, max(ks))]
    if cls == "lifetime":
        return [("history", t, [("KEEP", x) for x in (ks * 4)[:16]], max(ks))]
    if cls == "reactivation":
        m = ks[len(ks) // 2]
        return [("history", t, [("DELETE", m), ("KEEP", m)] * 4, max(ks))]
    raise ValueError(cls)


def main():
    # WP-2 STEP CB-01: independent boundary verdict recomputation.
    print("[WP-2][STEP CB-01] cleanroom boundary check running", flush=True)
    if len(sys.argv) != 2:
        print("[WP-2][STEP CB-01] usage: boundary_check.py <record>", flush=True)
        return 2
    try:
        rec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        assert rec["theorem_id"] == "MST0-09"
    except Exception:
        print("[WP-2][STEP CB-01] malformed record", flush=True)
        return 2
    best, best_h = -1, -1
    for n in SIZES:
        for si in range(6):
            seed = seed_int("PSC-B", si * 1000 + n)
            for cls in CLASSES:
                for probe in _probes(cls, n, seed):
                    if probe[0] == "access":
                        _, t, x, nkeys = probe
                        _t2, evs = S.splay_trace(t, x)
                        for _case, lo, hi in evs:
                            E2 = M.t7inject(([], 0), True, lo, hi, x, nkeys, M.K_FROZEN)
                            best = max(best, len(E2[0]))
                    else:
                        _, t, hist, nkeys = probe
                        E, _sA, _sB = M.exec_hist(([], 0), t, hist, nkeys)
                        best_h = max(best_h, M.energy(E[0]))
    claimed = rec["best_finite_obstruction_metrics"]["max_event_growth"]
    claimed_h = rec["best_finite_obstruction_metrics"]["best_history_energy_informational_only"]
    consistent = (best == claimed) and (best_h == claimed_h) \
        and (rec["exact_witness"] is None) == (best <= M.K_FROZEN)
    verdict = "AGREE" if consistent else "DISAGREE"
    # WP-2 STEP CB-02: verdict emitted.
    print(f"[WP-2][STEP CB-02] CHECKER-VERDICT: {verdict} (recomputed={best} claimed={claimed} hist={best_h})",
          flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
