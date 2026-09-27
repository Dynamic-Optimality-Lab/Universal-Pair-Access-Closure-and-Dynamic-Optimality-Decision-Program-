import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.setrecursionlimit(20000)

from python.inherited import mstc0002 as M
from python.audit import legal_domain as LD
from python.audit import ledger_trace as LT
from python.proof_attack import common as C

# Canonical minimal witness.
n = 28
T0 = C.shape_vine_right(n)
H = [("DELETE", 27), ("DELETE", 28), ("KEEP", 28), ("KEEP", 27)]
print("legal:", LD.legal_pair_instance(T0, H, n), LD.violations(T0, H, n))
print("suffices:", M.exec_suffices(([], 0), T0, T0, H, n))
# greedy-drop minimality
for i in range(len(H)):
    cand = H[:i] + H[i + 1:]
    print("drop %d %s -> suffices=%s legal=%s"
          % (i, H[i], M.exec_suffices(([], 0), T0, T0, cand, n),
             LD.legal_pair_instance(T0, cand, n)))
steps, summary = LT.trace_execution(T0, H, n)
for s in steps:
    print(s["mode"], s["x"], "dA=%d dB=%s a=%d y=%d rA=%d rB=%d L0=%d P0=%d need=%d paid=%d margin=%s"
          % (s["dA"], s["dB"], s["a"], s["y"], s["rA"], s["rB"],
             s["L0"], s["P0"], s["need"], s["paid"], s["margin"]))
print()
print("residual growth:")
for n2 in (28, 32, 40, 48, 64, 96, 128, 192, 256, 384, 512):
    T2 = C.shape_vine_right(n2)
    H2 = [("DELETE", n2 - 1), ("DELETE", n2), ("KEEP", n2), ("KEEP", n2 - 1)]
    st2, sm2 = LT.trace_execution(T2, H2, n2)
    last = [s for s in st2 if s["mode"] == "KEEP"][-1]
    print("n=%d a=%d y=%d need=%d paid=%d margin=%d ok=%s"
          % (n2, last["a"], last["y"], last["need"], last["paid"],
             last["margin"], sm2["suffices"]))
