import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.setrecursionlimit(20000)

from python.inherited import mstc0002 as M
from python.audit import legal_domain as LD
from python.proof_attack import common as C

n = 512
T0 = C.shape_vine_right(n)
H = [("DELETE", 384), ("DELETE", 128), ("DELETE", 2), ("DELETE", 512),
     ("KEEP", 512), ("KEEP", 385)]


def is_witness(H):
    return (LD.legal_pair_instance(T0, H, n)
            and M.exec_suffices(([], 0), T0, T0, H, n) is False)


print("full witness:", is_witness(H))
# Greedy drop-one minimization (keep legal + falsifying).
H = list(H)
changed = True
while changed:
    changed = False
    for i in range(len(H)):
        cand = H[:i] + H[i + 1:]
        if cand and is_witness(cand):
            print("drop idx %d %s -> still witness" % (i, H[i]))
            H = cand
            changed = True
            break
print("minimized H:", H)

# n-downscaling: try to reproduce the shape at smaller n by key rescaling.
# Pattern roles: deep-churn keys + strike key s (A-root, B-deep) + target t
# (A-shallow, B-deep). Try analogous small vines by brute force over
# (churn subset of {1..n}, s, t) for n in small sizes.
import itertools
for n2 in (8, 12, 16, 24, 32):
    T2 = C.shape_vine_right(n2)
    keys = list(range(1, n2 + 1))
    found = None
    # churn: 2-4 DELETEs among quartiles + ends; s,t among ends/middle
    cand_keys = sorted(set([1, 2, n2 // 4, n2 // 2, 3 * n2 // 4, n2 - 1, n2]))
    for L in (2, 3, 4):
        for burst in itertools.product(cand_keys, repeat=L):
            for s in cand_keys:
                for t in cand_keys:
                    H2 = [("DELETE", z) for z in burst] + [("KEEP", s), ("KEEP", t)]
                    if LD.legal_pair_instance(T2, H2, n2) and \
                            M.exec_suffices(([], 0), T2, T2, H2, n2) is False:
                        found = H2
                        break
                if found:
                    break
            if found:
                break
        if found:
            break
    print("n=%d small witness: %s" % (n2, found))
