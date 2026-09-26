"""Phase 06: PSC-L attack + cleanroom check for MST0-08U [WorkPlan Phase 2].

Checkpoints: verify hashes -> gates -> conformance green -> PSC-L campaign ->
independent cleanroom check -> review package -> record.
Follows the amended 16-checkpoint order (v0.4.3 C2). Fail-closed (exit 2).
"""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from python.audit import phase_runner as PR
from python.audit import conformance as CF
from python.audit import review_package as RP

NODE, FAMILY, GEN, CHECK = "MST0-08U", "PSC-L", "locality_explosion", "locality_check"


def main(argv=None):
    check_only = argv is not None and "--check-only" in argv
    # WP-2 STEP 06-01: foundation verification for MST0-08U.
    print("[WP-2][STEP 06-01] phase 06 starting (MST0-08U PSC-L)", flush=True)
    PR.check_foundation("06", [NODE])
    # WP-2 STEP 06-02: conformance gate (STOP-17).
    print("[WP-2][STEP 06-02] checking generator conformance", flush=True)
    issues = CF.check_module(f"python.proof_attack.{GEN}")
    if issues:
        print(f"[WP-2][STEP 06-02] conformance RED: {issues}; aborting", flush=True)
        return 2
    if check_only:
        print("[WP-2][STEP 06-02] CHECK-ONLY-OK (gates green, campaign skipped)", flush=True)
        return 0
    # WP-2 STEP 06-03: attack campaign.
    print("[WP-2][STEP 06-03] running attack campaign", flush=True)
    r = subprocess.run([sys.executable, f"python/proof_attack/{GEN}.py"],
                       capture_output=True, text=True, timeout=900)
    print(r.stdout[-1500:])
    if r.returncode != 0:
        print(f"[WP-2][STEP 06-03] campaign failed exit={r.returncode}; aborting", flush=True)
        return 2
    # WP-2 STEP 06-04: independent cleanroom check on the produced record.
    print("[WP-2][STEP 06-04] running independent cleanroom check", flush=True)
    rec = PR.find_latest_record(NODE)
    c = subprocess.run([sys.executable, f"python/cleanroom/{CHECK}.py", str(rec)],
                       capture_output=True, text=True, timeout=900)
    print(c.stdout[-800:])
    if c.returncode != 0 or "DISAGREE" in c.stdout:
        print("[WP-2][STEP 06-04] checker rejected; aborting", flush=True)
        return 2
    # WP-2 STEP 06-05: review package + closeout.
    print("[WP-2][STEP 06-05] assembling review package", flush=True)
    path, sha = RP.assemble_package(
        NODE, "math/theorem_MST08U_locality.md", "lean/Proofs/Locality.lean",
        [str(rec)], ["artifacts/v04/logs/WP2_RUN_RECORDS.jsonl"])
    print(f"[WP-2][STEP 06-05] phase 06 done: package {path} sha={sha[:16]}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
