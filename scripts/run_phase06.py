"""Phase 06 runner: PSC-L Locality Explosion + clean-room agreement (MST0-08U).

Implements WorkPlan Phase 2 / spec PHASE 06 (06.1 engine, 06.2 bounded-
modification metrics, 06.3 hostile review support). Records attack-survival
with exact maxima; never claims REVIEWED (human proof + formal + ACCEPT
required). Exit 0 emits LOCALITY_ATTACK_COMPLETE.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from python.cleanroom import locality_check as LC
from python.inherited import mstc0002 as M
from python.inherited import pair_access as P
from python.proof_attack import locality_explosion as LE

REPO_ROOT = Path(__file__).resolve().parent.parent


def main(argv=None):
    """CLI entry: run PSC-L, cross-check, write record, exit."""
    print("PHASE06: start (WorkPlan Phase 2, spec PHASE 06; attack only)")
    ap = argparse.ArgumentParser(description="Phase-06 locality runner")
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--budget", type=int, default=32)
    args = ap.parse_args(argv)
    print("STEP-06-1: running Locality Explosion Engine")
    rec = LE.run_locality(args.seed, budget=args.budget)
    assert rec["survived"], rec.get("witness")
    print("STEP-06-2: clean-room agreement on best-witness program")
    wit = rec["best_witness"]
    prog = {"nkeys": wit["nkeys"], "shape": wit["shape"], "history": wit["history"]}
    indep = LC.check_program(prog)
    base = P.run_paired(prog["nkeys"], prog["shape"], prog["history"])
    base_res = M.evaluate(base["events"])
    assert indep["feasible"] == base_res["feasible"]
    assert indep["injected_total"] == base_res["injected_total"], "cleanroom disagreement"
    print("STEP-06-3: writing attack record (REVIEWED unclaimed)")
    out = REPO_ROOT / "artifacts" / "v04" / "proof_attacks" / "locality"
    out.mkdir(parents=True, exist_ok=True)
    (out / "locality_attack.json").write_text(json.dumps(
        {"gate": "LOCALITY_ATTACK_COMPLETE", "record": rec, "cleanroom": indep,
         "note": "attack-survival only; universal proof requires human+formal"},
        indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
    rev = REPO_ROOT / "math" / "reviews"
    rev.mkdir(parents=True, exist_ok=True)
    (rev / "MST0-08U.PACKAGE.md").write_text(
        "# MST0-08U review package (evidence, verdict PENDING-HUMAN)\n\n"
        "v0.4 statement: `math/theorem_MST08U_locality.md`.\n"
        "Attack evidence: `artifacts/v04/proof_attacks/locality/locality_attack.json` "
        "(PSC-L survival with exact maxima + clean-room agreement).\n"
        "Formal Lean artifact: pending toolchain (gate unclaimed).\n"
        "Human action required: PROVED-path review (ACCEPT) or exact-negation "
        "witness (REFUTED) per lifecycle; survival never implies REVIEWED.\n",
        encoding="utf-8")
    print("PHASE06_PASS: PSC-L survived seed=%d; LOCALITY_ATTACK_COMPLETE" % args.seed)
    return 0


if __name__ == "__main__":
    sys.exit(main())
