import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.setrecursionlimit(20000)

from python.inherited import mstc0002 as M
from python.audit import legal_domain as LD
from python.audit import ledger_trace as LT
from python.proof_attack import common as C

for n in range(4, 65):
    T0 = C.shape_vine_right(n)
    H = [("DELETE", n - 1), ("DELETE", n), ("KEEP", n), ("KEEP", n - 1)]
    if not LD.legal_pair_instance(T0, H, n):
        continue
    ok = M.exec_suffices(([], 0), T0, T0, H, n)
    steps, summary = LT.trace_execution(T0, H, n)
    last = [s for s in steps if s["mode"] == "KEEP"][-1]
    flag = "WITNESS" if not ok else ""
    print("n=%d ok=%s last: a=%d y=%d need=%d paid=%d margin=%d %s"
          % (n, ok, last["a"], last["y"], last["need"], last["paid"],
             last["margin"], flag))
    if not ok:
        break
