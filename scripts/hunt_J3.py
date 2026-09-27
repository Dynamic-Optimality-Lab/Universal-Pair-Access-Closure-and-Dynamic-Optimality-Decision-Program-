import random
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.setrecursionlimit(20000)

from python.inherited import splay as S
from python.inherited import mstc0002 as M
from python.proof_attack import common as C
from scripts.hunt_J2 import check_J, replay


def main():
    t0 = time.time()
    breaks = 0
    minw = None
    for trial in range(2500):
        rng = random.Random(999000 + trial)
        n = rng.choice([16, 32, 64, 128, 256])
        shape = rng.choice(["vine-right", "balanced", "seeded"])
        seed = rng.randrange(10 ** 9)
        T0 = {"vine-right": C.shape_vine_right(n),
              "balanced": C.shape_balanced(n),
              "seeded": C.shape_seeded(n, seed)}[shape]
        L = rng.choice([8, 16, 24, 32])
        pdel = rng.choice([0.5, 0.7, 0.85])
        H = [(("DELETE" if rng.random() < pdel else "KEEP"), rng.randint(1, n))
             for _ in range(L)]
        E, A, B = replay(H, T0, n)
        w = check_J(E, A, B, n)
        if minw is None or w[0] < minw[0]:
            minw = (w[0], trial, n, shape, H, w)
        if w[0] < 0:
            breaks += 1
            print("J-BREAK2 trial=%d n=%d shape=%s x=%d %s" % (trial, n, shape, w[1], w))
            if breaks >= 5:
                break
    print("J-breaks2=%d wall=%.1fs" % (breaks, time.time() - t0))
    print("min J slack2:", minw[0] if minw else None)
    import json
    Path("artifacts/v04/proof_attacks/MST0-14R/J_HUNT3.json").write_text(
        json.dumps({"breaks": breaks, "min_slack": minw[0] if minw else None},
                   indent=2, default=str) + "\n")


if __name__ == "__main__":
    sys.exit(main())
