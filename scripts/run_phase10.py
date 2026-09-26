"""Phase 10: K6 Saturation War pre-proof attack on KEEP repayment [WorkPlan Phase 3].

Checkpoints: verify hashes -> gates -> K6 conformance green -> war campaign ->
independent cleanroom check -> record. REFUTE(MST0-14) runs on REFUTE_READY
with no upstream-REVIEWED requirement. Follows the amended 16-checkpoint
order (v0.4.3 C2). Fail-closed (exit 2).
"""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from python.audit import phase_runner as PR
from python.audit import conformance as CF

NODE, GEN, CHECK = "MST0-14", "k6_saturation", "repayment_check"


def main(argv=None):
    check_only = argv is not None and "--check-only" in argv
    # WP-3 STEP 10-01: foundation verification for MST0-14 (REFUTE track needs no upstreams).
    print("[WP-3][STEP 10-01] phase 10 starting (MST0-14 K6 war)", flush=True)
    PR.check_foundation("10", [NODE])
    # WP-3 STEP 10-02: conformance gate (STOP-17).
    print("[WP-3][STEP 10-02] checking generator conformance", flush=True)
    issues = CF.check_module(f"python.proof_attack.{GEN}")
    if issues:
        print(f"[WP-3][STEP 10-02] conformance RED: {issues}; aborting", flush=True)
        return 2
    if check_only:
        print("[WP-3][STEP 10-02] CHECK-ONLY-OK (gates green, campaign skipped)", flush=True)
        return 0
    # WP-3 STEP 10-03: K6 saturation campaign.
    print("[WP-3][STEP 10-03] running K6 war campaign", flush=True)
    r = subprocess.run([sys.executable, f"python/proof_attack/{GEN}.py"],
                       capture_output=True, text=True, timeout=1800)
    print(r.stdout[-1500:])
    if r.returncode != 0:
        print(f"[WP-3][STEP 10-03] campaign failed exit={r.returncode}; aborting", flush=True)
        return 2
    # WP-3 STEP 10-04: independent cleanroom check on the produced record.
    print("[WP-3][STEP 10-04] running independent cleanroom check", flush=True)
    rec = PR.find_latest_record(NODE)
    c = subprocess.run([sys.executable, f"python/cleanroom/{CHECK}.py", str(rec)],
                       capture_output=True, text=True, timeout=1800)
    print(c.stdout[-800:])
    if c.returncode != 0 or "DISAGREE" in c.stdout:
        print("[WP-3][STEP 10-04] checker rejected; aborting", flush=True)
        return 2
    # WP-3 STEP 10-05: phase 10 done (REFUTE track: NO_WITNESS or validated witness).
    print("[WP-3][STEP 10-05] phase 10 done", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
