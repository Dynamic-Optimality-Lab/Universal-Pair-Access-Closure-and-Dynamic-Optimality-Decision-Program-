"""Phase 08 runner: PSC-B Boundary Torture + clean-room agreement (MST0-09).

Implements WorkPlan Phase 2 / spec PHASE 08 (08.1 torture chamber, 08.2 exact
law support). Records attack-survival with provenance/mass audits; never
claims REVIEWED. Exit 0 emits BOUNDARY_ATTACK_COMPLETE.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from python.cleanroom import boundary_check as BC
from python.proof_attack import boundary_torture as BT

REPO_ROOT = Path(__file__).resolve().parent.parent


def main(argv=None):
    """CLI entry: run PSC-B, cross-check, write record, exit."""
    print("PHASE08: start (WorkPlan Phase 2, spec PHASE 08; attack only)")
    ap = argparse.ArgumentParser(description="Phase-08 boundary runner")
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--budget", type=int, default=48)
    args = ap.parse_args(argv)
    print("STEP-08-1: running Boundary Torture Chamber")
    rec = BT.run_torture(args.seed, budget=args.budget)
    assert rec["survived"], rec.get("witness", rec.get("defect"))
    print("STEP-08-2: clean-room agreement on worst-witness program")
    wit = rec["worst_witness"]
    prog = {"nkeys": wit["nkeys"], "shape": wit.get("shape", "balanced"),
            "history": wit["history"]}
    indep = BC.check_program(prog)
    assert indep["feasible"]
    print("STEP-08-3: writing attack record (REVIEWED unclaimed)")
    out = REPO_ROOT / "artifacts" / "v04" / "proof_attacks" / "boundary"
    out.mkdir(parents=True, exist_ok=True)
    (out / "boundary_attack.json").write_text(json.dumps(
        {"gate": "BOUNDARY_ATTACK_COMPLETE", "record": rec, "cleanroom": indep,
         "note": "attack-survival only; boundary law requires human+formal"},
        indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
    rev = REPO_ROOT / "math" / "reviews"
    rev.mkdir(parents=True, exist_ok=True)
    (rev / "MST0-09.PACKAGE.md").write_text(
        "# MST0-09 review package (evidence, verdict PENDING-HUMAN)\n\n"
        "v0.4 statement: `math/theorem_MST09_raw_boundary.md`.\n"
        "Attack evidence: `artifacts/v04/proof_attacks/boundary/boundary_attack.json` "
        "(torture survival + provenance/mass audits + clean-room agreement).\n"
        "Formal Lean artifact: pending toolchain (gate unclaimed).\n"
        "Human action required: PROVED-path review (ACCEPT) or exact-negation "
        "witness (REFUTED) per lifecycle.\n",
        encoding="utf-8")
    print("PHASE08_PASS: PSC-B survived seed=%d; BOUNDARY_ATTACK_COMPLETE" % args.seed)
    return 0


if __name__ == "__main__":
    sys.exit(main())
