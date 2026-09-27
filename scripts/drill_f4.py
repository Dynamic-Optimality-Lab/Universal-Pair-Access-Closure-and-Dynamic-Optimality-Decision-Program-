import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.setrecursionlimit(20000)

from python.audit import ledger_trace as LT
from python.proof_attack import common as C

for n in (32, 128):
    T0 = C.shape_vine_right(n)
    H = ([("KEEP", 1), ("KEEP", n)] * 6
         + [("DELETE", n // 2)] * 4 + [("KEEP", 1), ("KEEP", n)])
    steps, summary = LT.trace_execution(T0, H, n)
    print("n=%d suffices=%s min_margin=%s" % (n, summary["suffices"], summary["min_margin"]))
    for s in steps:
        if s["mode"] == "KEEP" and s["margin"] is not None and s["margin"] <= 2:
            print("  idx=%d x=%d dA=%d dB=%d a=%d y=%d rA=%d rB=%d L0=%d P0=%d need=%d paid=%d margin=%d actB=%d sA=%d sB=%d"
                  % (s["idx"], s["x"], s["dA"], s["dB"], s["a"], s["y"],
                     s["rA"], s["rB"], s["L0"], s["P0"], s["need"], s["paid"],
                     s["margin"], s["actB_k"], s["sA"], s["sB"]))
