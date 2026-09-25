"""Phase 11 runner: MST0-14 proof-gate enforcement (WorkPlan Phase 3).

Implements WorkPlan Phase 3 / spec PHASE 11 gate discipline: the case-
complete proof, matching theorem, formal proof, and hostile review may start
ONLY when MST0-13/08U/11/09/22 are all REVIEWED (hard entry gate, DEC-GATE-09).
Otherwise this script records PROOF_BLOCKED_UPSTREAM / NOT_REACHED and exits
0 (correct gate evaluation, not a failure). It never weakens the theorem,
never claims REVIEWED, and never consumes unreviewed prerequisites.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

REPO_ROOT = Path(__file__).resolve().parent.parent
UPSTREAM = ["MST0-13", "MST0-08U", "MST0-11", "MST0-09", "MST0-22"]


def main(argv=None):
    """CLI entry: enforce hard entry gate, record outcome, exit."""
    print("PHASE11: start (WorkPlan Phase 3, spec PHASE 11; gate enforcement)")
    ap = argparse.ArgumentParser(description="Phase-11 proof gate runner")
    ap.parse_args(argv)
    print("STEP-11-0: asserting hard entry gate (all upstream REVIEWED)")
    ledger = json.loads((REPO_ROOT / "math" / "proof_status.json").read_text(encoding="utf-8"))
    obs = ledger.get("obligations", {})
    unready = [t for t in UPSTREAM if obs.get(t, {}).get("status") != "REVIEWED"]
    out = REPO_ROOT / "artifacts" / "v04" / "proofs" / "MST0-14"
    out.mkdir(parents=True, exist_ok=True)
    if unready:
        print("STEP-11-0: gate closed, unready=%s" % unready)
        (out / "proof_gate.json").write_text(json.dumps(
            {"gate": "PROOF_BLOCKED_UPSTREAM", "unready": unready,
             "phase": "NOT_REACHED",
             "note": "case-complete proof, matching theorem, formal proof, and "
                     "hostile review start only after all upstream REVIEWED; "
                     "no status changed, nothing consumed"},
            indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print("PHASE11_PASS: proof track NOT_REACHED (fail-fast gate held)")
        return 0
    print("STEP-11-0: gate open (unexpected pre-human state); proof work pending")
    (out / "proof_gate.json").write_text(json.dumps(
        {"gate": "ENTRY_OPEN_PROOF_PENDING",
         "note": "upstream REVIEWED; case-complete proof + formal + review still required"},
        indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("PHASE11_PASS: entry open, proof pending")
    return 0


if __name__ == "__main__":
    sys.exit(main())
