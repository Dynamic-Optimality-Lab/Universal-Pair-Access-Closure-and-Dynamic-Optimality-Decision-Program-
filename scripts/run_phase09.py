"""Phase 09: constants support scan for MST0-22 [WorkPlan Phase 2].

Checkpoints: verify hashes -> gates -> constants_scan support scan ->
review package -> record. (No PSC family owns MST0-22; attack surface is
hidden-dependence, covered by the scan + formal quantifier check.)
Follows the amended 16-checkpoint order (v0.4.3 C2). Fail-closed (exit 2).
"""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from python.audit import phase_runner as PR
from python.audit import review_package as RP

NODE = "MST0-22"


def main(argv=None):
    check_only = argv is not None and "--check-only" in argv
    # WP-2 STEP 09-01: foundation verification for MST0-22.
    print("[WP-2][STEP 09-01] phase 09 starting (MST0-22 constants)", flush=True)
    PR.check_foundation("09", [NODE])
    if check_only:
        print("[WP-2][STEP 09-01] CHECK-ONLY-OK (gates green, scan skipped)", flush=True)
        return 0
    # WP-2 STEP 09-02: constants support scan.
    print("[WP-2][STEP 09-02] running constants support scan", flush=True)
    r = subprocess.run([sys.executable, "python/cleanroom/constants_scan.py"],
                       capture_output=True, text=True, timeout=300)
    print(r.stdout[-800:])
    if r.returncode != 0 or "DIRTY" in r.stdout:
        print("[WP-2][STEP 09-02] scan dirty; aborting", flush=True)
        return 2
    # WP-2 STEP 09-03: review package + closeout.
    print("[WP-2][STEP 09-03] assembling review package", flush=True)
    path, sha = RP.assemble_package(
        NODE, "math/theorem_MST22_constant_independence.md", "lean/Proofs/Constants.lean",
        [], ["artifacts/v04/logs/WP2_RUN_RECORDS.jsonl"])
    print(f"[WP-2][STEP 09-03] phase 09 done: package {path} sha={sha[:16]}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
