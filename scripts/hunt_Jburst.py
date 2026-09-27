import itertools
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.setrecursionlimit(20000)

from scripts.hunt_J2 import check_J, replay
from python.proof_attack import common as C


def main():
    t0 = time.time()
    breaks = 0
    minw = None
    cases = 0
    for n in (32, 64, 128, 256, 512, 1024):
        T0 = C.shape_vine_right(n)
        keys = sorted(set([1, 2, 3, n // 4, n // 2, 3 * n // 4, n - 2, n - 1, n]))
        # bursts of length 1..4 over interesting keys + optional trailing KEEPs
        for L in (1, 2, 3, 4):
            for burst in itertools.product(keys, repeat=L):
                for tail in ([], [("KEEP", burst[-1])]):
                    H = [("DELETE", z) for z in burst] + tail
                    E, A, B = replay(H, T0, n)
                    w = check_J(E, A, B, n)
                    cases += 1
                    if minw is None or w[0] < minw[0]:
                        minw = (w[0], n, H, w)
                    if w[0] < 0:
                        breaks += 1
                        print("J-BURST-BREAK n=%d H=%s %s" % (n, H, w))
                        if breaks >= 5:
                            break
    print("burst cases=%d J-breaks=%d wall=%.1fs" % (cases, breaks, time.time() - t0))
    print("min J burst slack:", minw[0] if minw else None, str(minw[1:])[:200] if minw else "")
    import json
    Path("artifacts/v04/proof_attacks/MST0-14R/J_BURST.json").write_text(
        json.dumps({"cases": cases, "breaks": breaks,
                    "min_slack": minw[0] if minw else None},
                   indent=2, default=str) + "\n")


if __name__ == "__main__":
    sys.exit(main())
