"""Phase 11: PROVE MST0-14 synchronous KEEP repayment [WorkPlan Phase 3].

Checkpoints: verify hashes -> PROVE-gate (all five upstream REVIEWED, else
PROVE track NOT_REACHED) -> Layer-A proof record -> formal certificate check ->
mutants -> review package -> record. Follows the amended 16-checkpoint order
(v0.4.3 C2). Fail-closed (exit 2). Human verdict only at review.
"""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from python.audit import phase_runner as PR
from python.audit import review_package as RP
from python.audit import mutants as MU

NODE = "MST0-14"
UPSTREAMS = ["MST0-08U", "MST0-09", "MST0-11", "MST0-13", "MST0-22"]


def main(argv=None):
    check_only = argv is not None and "--check-only" in argv
    # WP-3 STEP 11-01: foundation verification + PROVE-gate (upstream REVIEWED).
    print("[WP-3][STEP 11-01] phase 11 starting (MST0-14 PROVE)", flush=True)
    PR.check_foundation("11", [NODE])
    ps = json.loads((Path("math/proof_status.json")).read_text(encoding="utf-8"))
    blocked = [u for u in UPSTREAMS
               if ps["obligations"].get(u, {}).get("truth") != "REVIEWED"]
    if blocked:
        print(f"[WP-3][STEP 11-01] PROVE track NOT_REACHED (unreviewed: {blocked})", flush=True)
        return 0 if check_only else 2
    if check_only:
        print("[WP-3][STEP 11-01] CHECK-ONLY-OK (PROVE gate green)", flush=True)
        return 0
    # WP-3 STEP 11-02: assemble PROVE review package (Layer-A + formal + evidence).
    print("[WP-3][STEP 11-02] assembling PROVE review package", flush=True)
    recs = sorted(Path("artifacts/v04/proof_attacks/MST0-14").glob("*.json"))
    path, sha = RP.assemble_package(
        NODE, "math/theorem_MST14_keep_repayment.md", "lean/Proofs/Repayment.lean",
        [str(r) for r in recs], ["artifacts/v04/logs/WP2_RUN_RECORDS.jsonl",
                                 "artifacts/v04/logs/WP3_RUN_RECORDS.jsonl"],
        {"layer_a_cert": "artifacts/v04/proofs/MST0-14.proof_cert.json",
         "formal_cert": "artifacts/v04/formal/MST0-14.formal_cert.json",
         "lean_theorem": "MST0_14 mechanism identity (build-green); sufficiency open",
         "build_status": MU.BUILD_STATUS, "mutant_result": MU.MUTANT_SUMMARY})
    # WP-3 STEP 11-03: phase 11 done (review verdict human-only, pending).
    print(f"[WP-3][STEP 11-03] phase 11 done: package {path} sha={sha[:16]}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
