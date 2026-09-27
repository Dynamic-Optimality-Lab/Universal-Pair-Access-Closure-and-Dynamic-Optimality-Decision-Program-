import itertools
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.setrecursionlimit(20000)

from python.inherited import splay as S
from python.inherited import mstc0002 as M
from scripts.sweep_legal_margin import all_bst_shapes


def boundary_check(E, A, B, n, fails, tag):
    L = sum(1 for c in E[0] if c[0] == M.LATENT)
    P = sum(1 for c in E[0] if c[0] == M.ACTIVE)
    for x in range(1, n + 1):
        a, y = S.splay_cost(A, x), S.splay_cost(B, x)
        rA = len(S.splay_trace(A, x)[1])
        rB = len(S.splay_trace(B, x)[1])
        need = M.required(y, a)
        j0 = P + rA + min(rB, 5 * rA) - need
        j = P + rA + min(rB, L + 5 * rA) - need
        if j0 < 0:
            fails["J0"].append((tag, P, L, x, a, y, rA, rB, need))
            return
        if j < 0:
            fails["J"].append((tag, P, L, x, a, y, rA, rB, need))
            return


def main():
    fails = {"J0": [], "J": []}
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
                    E, A, B = ([], 0), T0, T0
                    boundary_check(E, A, B, n, fails, "init")
                    states += 1
                    for mode, x in H:
                        if mode == "KEEP":
                            E1, A2, a = M.replay_access_A(E, A, mode, x, n)
                            E2, B2, y, _ = M.replay_access_B(E1, B, x, a)
                            E, A, B = E2, A2, B2
                        else:
                            E1, A2, _ = M.replay_access_A(E, A, mode, x, n)
                            E, A = E1, A2
                        boundary_check(E, A, B, n, fails, "step")
                        states += 1
                    if fails["J0"] or fails["J"]:
                        print("EARLY FAIL J0=%d J=%d" % (len(fails["J0"]), len(fails["J"])))
                        break
    print("states=%d J0_viol=%d J_viol=%d wall=%.1fs"
          % (states, len(fails["J0"]), len(fails["J"]), time.time() - t0))
    p = Path("artifacts/v04/proof_attacks/MST0-14R/J_FALSIFICATION.json")
    p.write_text(json.dumps({"states": states,
                             "J0_violations": len(fails["J0"]),
                             "J_violations": len(fails["J"]),
                             "J0_examples": fails["J0"][:5],
                             "J_examples": fails["J"][:5]},
                            indent=2, default=str) + "\n")
    print("wrote", p.name)


if __name__ == "__main__":
    sys.exit(main())
