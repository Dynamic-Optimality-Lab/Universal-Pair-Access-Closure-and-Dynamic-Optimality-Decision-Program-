import random
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.setrecursionlimit(20000)

from python.inherited import splay as S
from python.inherited import mstc0002 as M
from python.audit import legal_domain as LD
from python.proof_attack import common as C


def maxneed(A, B, n):
    m = 0
    for x in range(1, n + 1):
        v = S.depth(B, x) - 2 * S.depth(A, x) - 1
        if v > m:
            m = v
    return m


def pool(E):
    return sum(1 for c in E[0] if c[0] == M.ACTIVE)


def replay(H, T0, n):
    E, A, B = ([], 0), T0, T0
    for mode, x in H:
        if mode == "KEEP":
            E1, A2, a = M.replay_access_A(E, A, mode, x, n)
            E2, B2, y, _ = M.replay_access_B(E1, B, x, a)
            E, A, B = E2, A2, B2
        else:
            E1, A2, _ = M.replay_access_A(E, A, mode, x, n)
            E, A = E1, A2
    return E, A, B


def spike_gap(E, A, B, n, x):
    """Would DELETE x break I2a? Returns (gap_after, P_after, needx_after)."""
    E1, A2, _ = M.replay_access_A(E, A, "DELETE", x, n)
    P1 = pool(E1)
    needx = max(S.depth(B, x) - 1, 0)
    mn = maxneed(A2, B, n)
    return P1 - mn, P1, needx


def main():
    t0 = time.time()
    checked = i2a_breaks = thm_breaks = 0
    worst_gap = None
    for trial in range(600):
        rng = random.Random(10 ** 6 + trial)
        n = rng.choice([8, 16, 32, 64, 128])
        shape = rng.choice(["vine-right", "balanced", "seeded"])
        seed = rng.randrange(10 ** 9)
        if shape == "vine-right":
            T0 = C.shape_vine_right(n)
        elif shape == "balanced":
            T0 = C.shape_balanced(n)
        else:
            T0 = C.shape_seeded(n, seed)
        # random history biased to DELETEs (divergence) + KEEPs (drain)
        L = rng.choice([4, 6, 8, 12])
        H = []
        for _ in range(L):
            m = "DELETE" if rng.random() < 0.6 else "KEEP"
            H.append((m, rng.randint(1, n)))
        E, A, B = replay(H, T0, n)
        P, mn = pool(E), maxneed(A, B, n)
        if P < mn:
            print("I2A-BREAK", trial, n, shape, H)
            i2a_breaks += 1
            continue
        checked += 1
        # one-step DELETE lookahead for every x
        for x in range(1, n + 1):
            gap, P1, needx = spike_gap(E, A, B, n, x)
            if worst_gap is None or gap < worst_gap[0]:
                worst_gap = (gap, trial, n, shape, x, P, mn, P1, needx)
            if gap < 0:
                print("I2A-SPIKE-BREAK trial=%d n=%d shape=%s x=%d "
                      "P=%d mn=%d P1=%d needx=%d H=%s"
                      % (trial, n, shape, x, P, mn, P1, needx, H))
                i2a_breaks += 1
    print("checked=%d i2a_breaks=%d wall=%.1fs" % (checked, i2a_breaks, time.time() - t0))
    print("worst_gap:", worst_gap)
    out = Path("artifacts/v04/proof_attacks/MST0-14R/I2A_HUNT.json")
    import json
    out.write_text(json.dumps({"checked": checked, "i2a_breaks": i2a_breaks,
                               "worst_gap": worst_gap}, indent=2, default=str) + "\n")
    print("wrote", out.name)


if __name__ == "__main__":
    sys.exit(main())
