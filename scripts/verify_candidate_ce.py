import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.setrecursionlimit(20000)

from python.inherited import splay as S
from python.inherited import mstc0002 as M
from python.audit import legal_domain as LD
from python.audit import ledger_trace as LT
from python.proof_attack import common as C

n = 512
T0 = C.shape_vine_right(n)
H = [("DELETE", 384), ("DELETE", 128), ("DELETE", 2), ("DELETE", 512),
     ("KEEP", 512)]
print("legal(H):", LD.legal_pair_instance(T0, H, n), LD.violations(T0, H, n))
H2 = H + [("KEEP", 385)]
print("legal(H2):", LD.legal_pair_instance(T0, H2, n), LD.violations(T0, H2, n))
print("exec_suffices(H2):", M.exec_suffices(([], 0), T0, T0, H2, n))
steps, summary = LT.trace_execution(T0, H2, n)
for s in steps:
    if s["mode"] == "KEEP":
        print("idx=%d x=%d dA=%d dB=%d a=%d y=%d rA=%d rB=%d "
              "L0=%d P0=%d need=%d paid=%d margin=%d actB=%d"
              % (s["idx"], s["x"], s["dA"], s["dB"], s["a"], s["y"],
                 s["rA"], s["rB"], s["L0"], s["P0"], s["need"], s["paid"],
                 s["margin"], s["actB_k"]))
print("summary suffices:", summary["suffices"], "first_fail:", summary["first_fail"])
