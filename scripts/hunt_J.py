import random
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.setrecursionlimit(20000)

from python.inherited import splay as S
from python.inherited import mstc0002 as M
from python.proof_attack import common as C


def check(E, A, B, n):
    L = sum(1 for c in E[0] if c[0] == M.LATENT)
    P = sum(1 for c in E[0] if c[0] == M.ACTIVE)
    worst = None
    for x in range(1, n + 1):
        a, y = S.splay_cost(A, x), S.splay_cost(B, x)
        rA = len(S.splay_trace(A, x)[1])
        rB = len(S.splay_trace(B, x)[1])
        need = M.required(y, a)
        j0 = P + rA + min(rB, 5 * rA) - need
        if worst is None or j0 < worst[0]:
            worst = (j0, x, P, L, a, y, rA, rB, need)
    return worst


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


def main():
    t0 = time.time()
    breaks = 0
    minw = None
    for trial in range(400):
        rng = random.Random(777000 + trial)
        n = rng.choice([8, 16, 32, 64, 128])
        shape = rng.choice(["vine-right", "balanced", "seeded"])
        seed = rng.randrange(10 ** 9)
        T0 = {"vine-right": C.shape_vine_right(n),
              "balanced": C.shape_balanced(n),
              "seeded": C.shape_seeded(n, seed)}[shape]
        L = rng.choice([4, 8, 12, 16])
        H = [(("DELETE" if rng.random() < 0.6 else "KEEP"), rng.randint(1, n))
             for _ in range(L)]
        E, A, B = replay(H, T0, n)
        w = check(E, A, B, n)
        if minw is None or w[0] < minw[0]:
            minw = (w[0], trial, n, shape, H)
        if w[0] < 0:
            breaks += 1
            print("J0-BREAK trial=%d n=%d shape=%s x=%d %s H=%s"
                  % (trial, n, shape, w[1], w, H))
    print("breaks=%d wall=%.1fs" % (breaks, time.time() - t0))
    print("min J0 slack:", (minw[0], minw[1], minw[2], minw[3]) if minw else None)
    import json
    Path("artifacts/v04/proof_attacks/MST0-14R/J_HUNT.json").write_text(
        json.dumps({"breaks": breaks, "min_slack": minw[0] if minw else None},
                   indent=2, default=str) + "\n")


if __name__ == "__main__":
    sys.exit(main())
