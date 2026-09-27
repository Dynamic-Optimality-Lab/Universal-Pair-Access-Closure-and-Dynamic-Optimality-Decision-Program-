import random
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.setrecursionlimit(20000)

from python.inherited import splay as S
from python.inherited import mstc0002 as M
from python.proof_attack import common as C


def check_J(E, A, B, n):
    L = sum(1 for c in E[0] if c[0] == M.LATENT)
    P = sum(1 for c in E[0] if c[0] == M.ACTIVE)
    worst = None
    for x in range(1, n + 1):
        a, y = S.splay_cost(A, x), S.splay_cost(B, x)
        rA = len(S.splay_trace(A, x)[1])
        rB = len(S.splay_trace(B, x)[1])
        need = M.required(y, a)
        j = P + rA + min(rB, L + 5 * rA) - need
        if worst is None or j < worst[0]:
            worst = (j, x, P, L, a, y, rA, rB, need)
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


# Adversarial seeds: J0-breakers + I2a-breakers + fuzz.
FIXED = [
    ("vine-right", 16, [('DELETE', 5), ('DELETE', 9), ('DELETE', 10), ('DELETE', 15)]),
    ("vine-right", 128, [('DELETE', 127), ('DELETE', 89), ('DELETE', 15), ('DELETE', 32)]),
    ("vine-right", 32, [('DELETE', 31), ('DELETE', 13), ('DELETE', 14), ('DELETE', 29)]),
    ("vine-right", 64, [('DELETE', 35), ('DELETE', 40), ('DELETE', 43), ('DELETE', 22)]),
    ("vine-right", 128, [('DELETE', 63), ('DELETE', 102), ('DELETE', 33),
                         ('KEEP', 110), ('DELETE', 102), ('KEEP', 11)]),
    ("vine-right", 64, [('DELETE', 59), ('KEEP', 60), ('DELETE', 49), ('DELETE', 6)]),
]


def main():
    t0 = time.time()
    breaks = 0
    minw = None
    cases = []
    for shape, n, H in FIXED:
        cases.append((shape, n, H))
    for trial in range(600):
        rng = random.Random(31337 + trial)
        n = rng.choice([8, 16, 32, 64, 128])
        shape = rng.choice(["vine-right", "balanced", "seeded"])
        L = rng.choice([4, 8, 12, 16])
        H = [(("DELETE" if rng.random() < 0.6 else "KEEP"), rng.randint(1, n))
             for _ in range(L)]
        cases.append((shape, n, H))
    for shape, n, H in cases:
        seed = 0
        T0 = {"vine-right": C.shape_vine_right(n),
              "balanced": C.shape_balanced(n)}.get(shape, C.shape_seeded(n, seed))
        E, A, B = replay(H, T0, n)
        w = check_J(E, A, B, n)
        if minw is None or w[0] < minw[0]:
            minw = (w[0], n, shape, H, w)
        if w[0] < 0:
            breaks += 1
            print("J-BREAK n=%d shape=%s x=%d %s H=%s" % (n, shape, w[1], w, H))
    print("J-breaks=%d wall=%.1fs" % (breaks, time.time() - t0))
    print("min J slack:", minw[0] if minw else None)
    import json
    Path("artifacts/v04/proof_attacks/MST0-14R/J_HUNT2.json").write_text(
        json.dumps({"breaks": breaks, "min_slack": minw[0] if minw else None,
                    "min_arg": str(minw[1:]) if minw else None},
                   indent=2, default=str) + "\n")


if __name__ == "__main__":
    sys.exit(main())
