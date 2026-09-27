import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.setrecursionlimit(20000)

from python.audit import ledger_trace as LT
from python.proof_attack import common as C

# F5: F2-strike on x=n, then KEEP z for EVERY z (post-drain divergence scan).
# F6: F2-strike, single DELETE w, then KEEP z (rebuild-then-strike grid, sampled).
worst = []
for n in (16, 64, 256, 1024):
    for shape, T0 in (("vine", C.shape_vine_right(n)),
                      ("bal", C.shape_balanced(n))):
        # F5
        Hpre = [("DELETE", n), ("KEEP", n)]
        for z in range(1, n + 1):
            H = Hpre + [("KEEP", z)]
            steps, summary = LT.trace_execution(T0, H, n)
            if not summary["suffices"]:
                print("WITNESS F5 n=%d shape=%s z=%d" % (n, shape, z))
                worst.append((summary["min_margin"], "F5", n, shape, z))
            elif summary["min_margin"] is not None and summary["min_margin"] < 2:
                worst.append((summary["min_margin"], "F5", n, shape, z))
        # F6 sampled grid
        for w in (1, n // 2, n):
            for z in (1, n // 2, n):
                H = Hpre + [("DELETE", w), ("KEEP", z)]
                steps, summary = LT.trace_execution(T0, H, n)
                if not summary["suffices"]:
                    print("WITNESS F6 n=%d shape=%s w=%d z=%d" % (n, shape, w, z))
                    worst.append((summary["min_margin"], "F6", n, shape, (w, z)))
                elif summary["min_margin"] is not None and summary["min_margin"] < 2:
                    worst.append((summary["min_margin"], "F6", n, shape, (w, z)))
worst.sort(key=lambda t: (t[0] if t[0] is not None else 10 ** 9))
print("count sub-2 margins:", len(worst))
for t in worst[:20]:
    print(t)
print("F5/F6 SCAN DONE")
