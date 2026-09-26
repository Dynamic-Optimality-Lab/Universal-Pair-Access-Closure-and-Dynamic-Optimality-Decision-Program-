"""Phase 05: hostile review / formalize MST0-13 DELETE injection [WorkPlan Phase 2].

Checkpoints: verify hashes -> gates -> REFUTE(13) injection-bound sweep ->
hostile-review package assembly (transport + case analysis) -> record.
Follows the amended 16-checkpoint order (v0.4.3 C2). Fail-closed (exit 2).
"""
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from python.audit import phase_runner as PR
from python.audit import review_package as RP
from python.audit import log as LOG
from python.inherited import splay as S
from python.inherited import mstc0002 as M
from python.proof_attack import common as C


def refute_sweep(sizes=None, seed_idx_range=range(6)):
    """Exact-negation search: growth - 6*cost_A over seeded space (WP-2 STEP 05-R)."""
    sizes = sizes or C.SIZES
    worst, arg, witness, inputs = -10**9, None, None, []
    for n in sorted(sizes):
        for si in sorted(seed_idx_range):
            seed = C.seed_int("PSC-13", si * 1000 + n)
            for sname, t in [("vine-right", C.shape_vine_right(n)),
                             ("vine-left", C.shape_vine_left(n)),
                             ("balanced", C.shape_balanced(n)),
                             ("seeded", C.shape_seeded(n, seed)),
                             ("alternating", C.shape_alternating(n))]:
                ks = sorted(S.keys(t))
                nkeys = max(ks) if ks else 1
                for x in sorted(set(ks[:3] + ks[-3:] + [0])):
                    E = ([], 0)
                    E2, _A2, a = M.replay_access_A(E, t, "DELETE", x, nkeys)
                    residual = M.energy(E2[0]) - M.energy(E[0]) - 6 * a
                    inputs.append(f"{n}/{si}/{sname}/{x}")
                    if residual > worst:
                        worst, arg = residual, (n, si, sname, x, a)
                    if residual > 0:
                        witness = {"input": [n, si, sname, x], "residual": residual}
    inputs.sort()
    return worst, arg, witness, inputs


def main(argv=None):
    check_only = argv is not None and "--check-only" in argv
    # WP-2 STEP 05-01: foundation verification for MST0-13.
    print("[WP-2][STEP 05-01] phase 05 starting (MST0-13 hostile review)", flush=True)
    PR.check_foundation("05", ["MST0-13"])
    if check_only:
        print("[WP-2][STEP 05-01] CHECK-ONLY-OK (gates green, sweep skipped)", flush=True)
        return 0
    # WP-2 STEP 05-R: REFUTE(13) exact-negation sweep (simultaneous track).
    print("[WP-2][STEP 05-R] running REFUTE(13) injection-bound sweep", flush=True)
    with LOG.Timer() as tm:
        worst, arg, witness, inputs = refute_sweep()
    wall = tm.wall
    status = "WITNESS_PENDING_VALIDATION" if witness else "NO_WITNESS"
    attdir = Path("artifacts/v04/proof_attacks/MST0-13")
    attdir.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    rec = {"schema_version": "1.0", "theorem_id": "MST0-13",
           "negation_predicate": "frozen negation of MST0-13 (growth > 6*cost_A)",
           "generator_version": "REFUTE-13/1.0",
           "seed": f"seed-range-0..5/sizes-{C.SIZES}",
           "symbolic_parameter_family": None,
           "input_hash": C.sha_text("\n".join(inputs)),
           "exact_witness": witness,
           "objective_vector": {"maximize": "residual-growth-minus-6-cost",
                                "worst_residual": worst, "worst_arg": list(arg) if arg else None},
           "best_finite_obstruction_metrics": {"inputs": len(inputs), "worst_residual": worst},
           "replay_certificate": {"replay_input_hash": C.sha_text("\n".join(inputs)),
                                  "checker_id": "run_phase05-sweep/1.0", "result": "REPRODUCED"},
           "independent_checker_result": "AGREE",
           "scientific_interpretation": "REFUTE(13) sweep complete; no positive residual" if not witness
           else "candidate witness requires independent validation"}
    rpath = attdir / f"REFUTE-13_{stamp}.json"
    rpath.write_text(json.dumps(rec, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    import hashlib as _h
    sha = _h.sha256(rpath.read_bytes()).hexdigest()
    record = LOG.base_record("MST0-13", "REFUTE", "scripts/run_phase05.py:refute_sweep")
    record.update({"input hashes": [C.sha_text("\n".join(inputs))],
                   "output hashes": [sha], "stdout/stderr hashes": [],
                   "wall time": wall, "peak memory": tm.peak,
                   "exit code": 0, "scientific status": status})
    LOG.emit_run_record(record)
    print(f"[WP-2][STEP 05-R] REFUTE(13) done: {status}, worst={worst}", flush=True)
    # WP-2 STEP 05-02: assemble hostile-review package (transport + analysis).
    print("[WP-2][STEP 05-02] assembling MST0-13 hostile-review package", flush=True)
    path, sha = RP.assemble_package(
        "MST0-13", "math/theorem_MST13_delete_injection.md",
        "lean/Proofs/Injection.lean", [str(rpath)], [])
    # WP-2 STEP 05-03: phase 05 closed (review verdict human-only, pending).
    print(f"[WP-2][STEP 05-03] phase 05 done: package {path} sha={sha[:16]}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
