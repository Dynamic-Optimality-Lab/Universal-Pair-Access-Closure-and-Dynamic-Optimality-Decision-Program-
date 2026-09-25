"""Clean-room boundary checker (share-nothing; uses only cleanroom.core)."""
from __future__ import annotations

from python.cleanroom import core as C


def check_program(program):
    """Re-run a recorded torture program; return independent verdict."""
    print("CLEANROOM-BOUNDARY: start n=%d" % program["nkeys"])
    events, _, _ = C.run_program(program["nkeys"], program["shape"], program["history"])
    res = C.evaluate(events)
    out = {"feasible": res["feasible"], "max_residual": res["max_residual"],
           "paid_total": res["paid_total"], "injected_total": res["injected_total"]}
    print("CLEANROOM-BOUNDARY: feasible=%s max_res=%s" % (out["feasible"], out["max_residual"]))
    return out
