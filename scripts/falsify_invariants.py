import itertools
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.setrecursionlimit(20000)

from python.inherited import splay as S
from python.inherited import mstc0002 as M
from python.audit import legal_domain as LD
from python.audit import ledger_trace as LT
from scripts.sweep_legal_margin import all_bst_shapes

ALPHAS = (0, 1, 2)


def maxneed(A, B, n):
    m = 0
    for x in range(1, n + 1):
        v = S.depth(B, x) - 2 * S.depth(A, x) - 1
        if v > m:
            m = v
    return m


def check_state(E, A, B, sA, sB, n, fails):
    L = sum(1 for c in E[0] if c[0] == M.LATENT)
    P = sum(1 for c in E[0] if c[0] == M.ACTIVE)
    mn = maxneed(A, B, n)
    if P < mn:
        fails["I2a:P>=maxneed"].append((P, mn))
    if P + L < mn:
        fails["I2b:P+L>=maxneed"].append((P + L, mn))
    for al in ALPHAS:
        if P + al * L + 2 * sA - sB < 0:
            fails["I1a(%d)" % al].append((P, L, sA, sB))
    if L < 0 or P < 0:
        fails["nonneg"].append((P, L))


def main():
    fails = {"I2a:P>=maxneed": [], "I2b:P+L>=maxneed": [],
             "I1a(0)": [], "I1a(1)": [], "I1a(2)": [], "nonneg": []}
    states = 0
    t0 = time.time()
    for n in range(1, 5):
        shapes = all_bst_shapes(list(range(1, n + 1)))
        alphabet = [("KEEP", x) for x in range(1, n + 1)] + \
                   [("DELETE", x) for x in range(1, n + 1)]
        for T0 in shapes:
            for L in range(0, 6):
                for H in itertools.product(alphabet, repeat=L):
                    H = list(H)
                    E, A, B, sA, sB = ([], 0), T0, T0, 0, 0
                    check_state(E, A, B, sA, sB, n, fails)
                    states += 1
                    for mode, x in H:
                        if mode == "KEEP":
                            E1, A2, a = M.replay_access_A(E, A, mode, x, n)
                            E2, B2, y, _ = M.replay_access_B(E1, B, x, a)
                            E, A, B = E2, A2, B2
                            sA, sB = sA + a, sB + y
                        else:
                            E1, A2, a = M.replay_access_A(E, A, mode, x, n)
                            E, A = E1, A2
                            sA = sA + a
                        check_state(E, A, B, sA, sB, n, fails)
                        states += 1
    print("states checked:", states, "wall: %.1fs" % (time.time() - t0))
    for k, v in fails.items():
        print("%s: violations=%d%s" % (k, len(v), (" e.g." + str(v[:3])) if v else ""))
    out = {"states": states,
           "violations": {k: len(v) for k, v in fails.items()},
           "examples": {k: v[:3] for k, v in fails.items() if v}}
    p = Path("artifacts/v04/proof_attacks/MST0-14R/INVARIANT_FALSIFICATION.json")
    p.write_text(json.dumps(out, indent=2, sort_keys=True, default=str) + "\n")
    print("wrote", p.name)


if __name__ == "__main__":
    sys.exit(main())
