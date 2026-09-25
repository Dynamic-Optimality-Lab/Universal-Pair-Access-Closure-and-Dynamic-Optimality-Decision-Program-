"""Phase 07 runner: PSC-P primitive exhaustion + clean-room agreement (MST0-11).

Implements WorkPlan Phase 2 / spec PHASE 07 (07.1 symbolic-parameterized
cases, 07.2 mutant rejection). Records case-complete falsification testing;
never claims REVIEWED. Exit 0 emits PRESERVATION_ATTACK_COMPLETE.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from python.cleanroom import preservation_check as PC
from python.proof_attack import primitive_exhaust as PE

REPO_ROOT = Path(__file__).resolve().parent.parent


def main(argv=None):
    """CLI entry: run PSC-P, cross-check, write record, exit."""
    print("PHASE07: start (WorkPlan Phase 2, spec PHASE 07; attack only)")
    ap = argparse.ArgumentParser(description="Phase-07 preservation runner")
    ap.parse_args(argv)
    print("STEP-07-1: running primitive exhaustion")
    rec = PE.run_exhaustion()
    assert rec["complete"], rec.get("defect")
    print("STEP-07-2: clean-room preservation agreement on sampled program")
    prog = {"nkeys": 12, "shape": "spine-left",
            "history": [("KEEP", 1), ("DELETE", 12), ("KEEP", 6), ("KEEP", 3)]}
    indep = PC.check_program(prog)
    assert indep["bst_valid"] and indep["feasible"]
    print("STEP-07-3: writing attack record (REVIEWED unclaimed)")
    out = REPO_ROOT / "artifacts" / "v04" / "proof_attacks" / "preservation"
    out.mkdir(parents=True, exist_ok=True)
    (out / "preservation_attack.json").write_text(json.dumps(
        {"gate": "PRESERVATION_ATTACK_COMPLETE", "record": rec, "cleanroom": indep,
         "note": "falsification testing only; symbolic proof requires human+formal"},
        indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
    rev = REPO_ROOT / "math" / "reviews"
    rev.mkdir(parents=True, exist_ok=True)
    (rev / "MST0-11.PACKAGE.md").write_text(
        "# MST0-11 review package (evidence, verdict PENDING-HUMAN)\n\n"
        "v0.4 statement: `math/theorem_MST11_preservation.md`.\n"
        "Attack evidence: `artifacts/v04/proof_attacks/preservation/preservation_attack.json` "
        "(case-complete falsification + clean-room agreement).\n"
        "Formal Lean artifact: pending toolchain (gate unclaimed).\n"
        "Human action required: PROVED-path review (ACCEPT) or exact-negation "
        "witness (REFUTED) per lifecycle.\n",
        encoding="utf-8")
    print("PHASE07_PASS: primitives=%d; PRESERVATION_ATTACK_COMPLETE" % rec["primitives"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
