"""Clean-room preservation checker (share-nothing; uses only cleanroom.core)."""
from __future__ import annotations

from python.cleanroom import core as C


def _bst_ok(root):
    """Inorder-sorted audit."""
    out = []

    def rec(t):
        if t is None:
            return
        rec(t.l)
        out.append(t.k)
        rec(t.r)

    rec(root)
    return out == sorted(out)


def check_program(program):
    """Re-run program; assert BST validity per access + energy nonnegativity."""
    print("CLEANROOM-PRESERVATION: start n=%d" % program["nkeys"])
    nkeys = program["nkeys"]
    A = C._build(program["shape"], nkeys)
    ok = True
    for mode, x in program["history"]:
        A, _ = C._splay_cases(A, x)
        if not _bst_ok(A):
            ok = False
            break
    events, _, _ = C.run_program(nkeys, program["shape"], program["history"])
    res = C.evaluate(events)
    out = {"bst_valid": ok, "feasible": res["feasible"]}
    print("CLEANROOM-PRESERVATION: bst_valid=%s feasible=%s" % (ok, res["feasible"]))
    return out
