import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.setrecursionlimit(20000)

from python.inherited import splay as S
from python.inherited import mstc0002 as M
from python.audit import legal_domain as LD
from python.proof_attack import common as C

CASES = [
    ("vine-right", 128, None, [('DELETE', 63), ('DELETE', 102), ('DELETE', 33),
                               ('KEEP', 110), ('DELETE', 102), ('KEEP', 11)]),
    ("vine-right", 64, None, [('DELETE', 59), ('KEEP', 60), ('DELETE', 49),
                              ('DELETE', 6)]),
    ("vine-right", 32, None, [('DELETE', 7), ('DELETE', 32), ('DELETE', 8),
                              ('DELETE', 4)]),
    ("seeded-483", 8,  None, [('DELETE', 8), ('DELETE', 8), ('DELETE', 1),
                              ('DELETE', 5)]),
    ("vine-right", 128, None, [('DELETE', 111), ('DELETE', 70),
                               ('DELETE', 126), ('DELETE', 52)]),
    ("vine-right", 64, None, [('DELETE', 21), ('DELETE', 51), ('DELETE', 48),
                              ('DELETE', 6)]),
]

SEEDS = {}


def get_tree(shape, n):
    if shape == "vine-right":
        return C.shape_vine_right(n)
    if shape.startswith("seeded"):
        return C.shape_seeded(n, 483)
    raise ValueError(shape)


n_bad = 0
for shape, n, seed, H in CASES:
    T0 = get_tree(shape, n)
    assert LD.legal_pair_instance(T0, H, n)
    for z in range(1, n + 1):
        H2 = H + [("KEEP", z)]
        ok = M.exec_suffices(([], 0), T0, T0, H2, n)
        if not ok:
            n_bad += 1
            print("THEOREM-BREAK shape=%s n=%d H=%s +KEEP %d" % (shape, n, H, z))
print("theorem-breaks after I2a-breaking states:", n_bad)
print("FOLLOWUP DONE")
