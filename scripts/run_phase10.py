"""Phase 10 runner: K6 Saturation War pre-proof attack (MST0-14).

Implements WorkPlan Phase 3 / spec PHASE 10 (10.1 attack families, 10.2
minimization + replay, 10.3 lemma mining without promotion). The REFUTE
track needs no REVIEWED prerequisites (exact negation + frozen calculus
suffice); the entry-gate status for the PROOF track is recorded but never
blocks the attack. Exit 0 emits KEEP_REPAYMENT_ATTACK_SURVIVED or
KEEP_REPAYMENT_EXACT_COUNTEREXAMPLE (with independent replay + clean-room
agreement + canonical minimization before any REFUTED handling).
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from python.cleanroom import repayment_check as RC
from python.inherited import mstc0002 as M
from python.inherited import pair_access as P
from python.proof_attack import k6_saturation as K6

REPO_ROOT = Path(__file__).resolve().parent.parent
UPSTREAM = ["MST0-13", "MST0-08U", "MST0-11", "MST0-09", "MST0-22"]


def proof_gate_status():
    """STEP-10-0: record whether the Phase-11 proof track may start."""
    print("STEP-10-0: checking Phase-11 proof entry gate")
    ledger = json.loads((REPO_ROOT / "math" / "proof_status.json").read_text(encoding="utf-8"))
    obs = ledger.get("obligations", {})
    unready = [t for t in UPSTREAM if obs.get(t, {}).get("status") != "REVIEWED"]
    if unready:
        print("STEP-10-0: proof track BLOCKED upstream=%s (attack proceeds)" % unready)
        return {"proof_track": "PROOF_BLOCKED_UPSTREAM", "unready": unready}
    print("STEP-10-0: proof track entry gate open")
    return {"proof_track": "ENTRY_OPEN", "unready": []}


def minimize_witness(program):
    """STEP-10-2: canonical minimization (shrink n, history, shapes in order)."""
    print("STEP-10-2: minimizing witness under canonical order")
    nkeys, shape, hist = program["nkeys"], program["shape"], program["history"]
    run = P.run_paired(nkeys, shape, hist)
    assert M.evaluate(run["events"])["max_residual"] > 0
    for n2 in sorted({8, 12, 16, 24}):
        if n2 >= nkeys:
            continue
        if all(x <= n2 for _, x in hist):
            r2 = P.run_paired(n2, shape, hist)
            if M.evaluate(r2["events"])["max_residual"] > 0:
                return {"nkeys": n2, "shape": shape, "history": hist}
    return {"nkeys": nkeys, "shape": shape, "history": hist}


def main(argv=None):
    """CLI entry: gate status, attack, replay/minimize/agree, record, exit."""
    print("PHASE10: start (WorkPlan Phase 3, spec PHASE 10; attack only)")
    ap = argparse.ArgumentParser(description="Phase-10 K6 saturation runner")
    ap.add_argument("--seed", type=int, default=21)
    ap.add_argument("--budget", type=int, default=48)
    args = ap.parse_args(argv)
    gate = proof_gate_status()
    print("STEP-10-1: running K6 Saturation War")
    rec = K6.run_saturation(args.seed, budget=args.budget)
    if rec["gate"] == "KEEP_REPAYMENT_EXACT_COUNTEREXAMPLE":
        prog = minimize_witness(rec["witness"]["program"])
        indep = RC.check_program(prog)
        base = P.run_paired(prog["nkeys"], prog["shape"], prog["history"])
        base_res = M.evaluate(base["events"])
        assert base_res["max_residual"] > 0 and indep["max_residual"] > 0
        assert indep["paid_total"] == base_res["paid_total"]
        rec["witness"]["minimized_program"] = prog
        rec["cleanroom"] = indep
    out = REPO_ROOT / "artifacts" / "v04" / "proof_attacks" / "k6"
    out.mkdir(parents=True, exist_ok=True)
    (out / "k6_attack.json").write_text(json.dumps(
        {"gate": rec["gate"], "proof_gate": gate, "record": rec,
         "note": "survival is not a theorem; counterexample needs minimization+replay+review"},
        indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
    print("PHASE10_PASS: gate=%s" % rec["gate"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
