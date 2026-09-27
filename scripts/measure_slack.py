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

# Q1: splay-target monotonicity: for z != x, is depth'(z) >= depth(z) always?
# Q2: DELETE-x slack: min over reachable DELETE states of
#     (P - maxneed) - (2*dA(x) - rA(x))  [needed slack vs available slack]
mono_viol = 0
mono_checked = 0
slack_min = None
slack_arg = None
slack_neg = 0
t0 = time.time()
for n in range(1, 5):
    shapes = all_bst_shapes(list(range(1, n + 1)))
    alphabet = [("KEEP", x) for x in range(1, n + 1)] + \
               [("DELETE", x) for x in range(1, n + 1)]
    for T0 in shapes:
        for L in range(0, 6):
            for H in itertools.product(alphabet, repeat=L):
                H = list(H)
                # Q1 on T0 itself for all x
                for x in range(1, n + 1):
                    T2, evs = S.splay_trace(T0, x)
                    for z in range(1, n + 1):
                        if z != x:
                            mono_checked += 1
                            if S.depth(T2, z) < S.depth(T0, z):
                                mono_viol += 1
                # Q2: replay H, then examine every possible next DELETE x
                E, A, B, sA, sB = ([], 0), T0, T0, 0, 0
                for mode, x in H:
                    if mode == "KEEP":
                        E1, A2, a = M.replay_access_A(E, A, mode, x, n)
                        E2, B2, y, _ = M.replay_access_B(E1, B, x, a)
                        E, A, B = E2, A2, B2
                    else:
                        E1, A2, _ = M.replay_access_A(E, A, mode, x, n)
                        E, A = E1, A2
                P = sum(1 for c in E[0] if c[0] == M.ACTIVE)
                mn = 0
                for z in range(1, n + 1):
                    v = S.depth(B, z) - 2 * S.depth(A, z) - 1
                    if v > mn:
                        mn = v
                for x in range(1, n + 1):
                    dA = S.depth(A, x)
                    rA = len(S.splay_trace(A, x)[1])
                    need_slack = 2 * dA - rA
                    avail = P - mn
                    gap = avail - need_slack
                    if slack_min is None or gap < slack_min:
                        slack_min = gap
                        slack_arg = {"n": n, "x": x, "dA": dA, "rA": rA,
                                     "P": P, "maxneed": mn}
                    if gap < 0:
                        slack_neg += 1
print("mono checked=%d violations=%d (wall %.1fs)"
      % (mono_checked, mono_viol, time.time() - t0))
print("DELETE-slack min gap=%s arg=%s negatives=%d"
      % (slack_min, slack_arg, slack_neg))
p = Path("artifacts/v04/proof_attacks/MST0-14R/SLACK_MEASUREMENT.json")
p.write_text(json.dumps({"mono_checked": mono_checked,
                         "mono_violations": mono_viol,
                         "delete_slack_min_gap": slack_min,
                         "delete_slack_arg": slack_arg,
                         "delete_slack_negatives": slack_neg},
                        indent=2, sort_keys=True, default=str) + "\n")
print("wrote", p.name)
