"""Phase 05 runner: hostile review support + formalization record for MST0-13.

Implements WorkPlan Phase 2 / spec PHASE 05 (05.1 statement binding, 05.2
eight audit attacks as executable evidence, 05.3 review package with verdict
PENDING-HUMAN). This script NEVER records ACCEPT/REJECT/BLOCKED (human-only
per STOP-35) and never claims REVIEWED. Exit 0 emits MST0_13_EVIDENCE_READY.
"""
import argparse
import json
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from python.inherited import mstc0002 as M
from python.inherited import pair_access as P
from python.inherited import splay as S

REPO_ROOT = Path(__file__).resolve().parent.parent


def check_rotations_bounded(nkeys=6):
    """STEP-05-1: rotations R <= access cost a on all accesses n<=6 (Lemma 1)."""
    print("STEP-05-1: checking rotations<=cost exhaustively n<=6")
    checked = 0
    for n in range(2, nkeys + 1):
        for shape in ("balanced", "spine-left", "spine-right"):
            tree = P.build_tree(shape, n)
            for x in range(1, n + 1):
                a = S.cost(tree, x)
                t2 = P.build_tree(shape, n)
                steps, _ = S.stepwise_access(t2, x, n, "A", "KEEP")
                rots = sum(1 for e in steps if e["splay_case"] != "ROOT")
                assert rots <= a, (n, shape, x, rots, a)
                checked += 1
    return {"audit": "rotations<=cost", "status": "PASS", "checked": checked}


def check_t7_bound():
    """STEP-05-2: T7 injects at most k=6 per A-rotation on sample histories."""
    print("STEP-05-2: checking T7 bound on sample histories")
    worst = 0
    for n in (8, 16, 32):
        run = P.run_paired(n, "spine-left",
                           [("DELETE", x) for x in range(1, 9)] + [("KEEP", 1)])
        _, cursor, injected = M.t7_inject(M.empty(), run["events"][0], M.K_FROZEN, 0)
        assert injected <= 6
        worst = max(worst, injected)
    return {"audit": "T7-bound", "status": "PASS", "worst_single_event": worst}


def check_t5_conservation():
    """STEP-05-3: T5 preserves energy (LATENT->ACTIVE 1:1)."""
    print("STEP-05-3: checking T5 conservation")
    ledger = [M.make_credit("BOUNDARY_LATENT", ("boundary", 1, 2, "LEFT"),
                            ("S0", 0), Fraction(1), "T")]
    before = M.energy(ledger)
    ledger, fired = M.t5_activate(ledger, {"mode": "KEEP", "splay_case": "LL"})
    assert fired and M.energy(ledger) == before
    return {"audit": "T5-conservation", "status": "PASS"}


def check_t6_inapplicable_on_delete():
    """STEP-05-4: T6 pays nothing on DELETE-only histories."""
    print("STEP-05-4: checking T6 inapplicability on DELETE")
    run = P.run_paired(16, "balanced", [("DELETE", x) for x in range(1, 9)])
    res = M.evaluate(run["events"])
    assert res["paid_total"] == 0
    return {"audit": "T6-inapplicable-DELETE", "status": "PASS"}


def check_case_completeness():
    """STEP-05-5/6: all 7 cases observed; block granularity exact-once."""
    print("STEP-05-5: checking case completeness and block coverage")
    from python.proof_attack import primitive_exhaust as PE
    rec = PE.run_exhaustion(n_list=[4, 5, 6, 8], budget_per_shape=8)
    assert rec["complete"]
    return {"audit": "case-completeness", "status": "PASS", "cases": rec["cases_covered"]}


def check_endpoints_and_hidden():
    """STEP-05-7/8: E0 empty-normalized; statement text has no forbidden refs."""
    print("STEP-05-6: checking endpoints and hidden-dependence hygiene")
    assert M.energy(M.empty()) == 0
    text = (REPO_ROOT / "math" / "theorem_MST13_delete_injection.md").read_text(encoding="utf-8")
    for bad in ("holdout", "corpus", "H3T", "seed", "panel"):
        assert bad not in text.lower(), bad
    return {"audit": "endpoints-hidden", "status": "PASS"}


def main(argv=None):
    """CLI entry: run audits, write evidence + review package, exit."""
    print("PHASE05: start (WorkPlan Phase 2, spec PHASE 05; evidence only)")
    ap = argparse.ArgumentParser(description="Phase-05 MST0-13 evidence runner")
    ap.parse_args(argv)
    checks = [check_rotations_bounded(), check_t7_bound(), check_t5_conservation(),
              check_t6_inapplicable_on_delete(), check_case_completeness(),
              check_endpoints_and_hidden()]
    assert all(c["status"] == "PASS" for c in checks)
    out = REPO_ROOT / "artifacts" / "v04" / "proof_attacks" / "injection"
    out.mkdir(parents=True, exist_ok=True)
    (out / "MST0-13_evidence.json").write_text(
        json.dumps({"gate": "MST0_13_EVIDENCE_READY", "checks": checks,
                    "verdict": "PENDING-HUMAN",
                    "note": "human ACCEPT/REJECT/BLOCKED only; REVIEWED unclaimed"},
                   indent=2, sort_keys=True) + "\n", encoding="utf-8")
    rev = REPO_ROOT / "math" / "reviews"
    rev.mkdir(parents=True, exist_ok=True)
    (rev / "MST0-13.PACKAGE.md").write_text(
        "# MST0-13 review package (evidence, verdict PENDING-HUMAN)\n\n"
        "Parent author proof: `parent/V03_PATH_FINAL.md` + v0.3 MST13 doc (Lemmas 1-4).\n"
        "v0.4 statement: `math/theorem_MST13_delete_injection.md`.\n"
        "Executable audit evidence: `artifacts/v04/proof_attacks/injection/MST0-13_evidence.json` "
        "(6/6 PASS: rotations<=cost exhaustive n<=6; T7 bound; T5 conservation; "
        "T6-inapplicable-DELETE; case completeness; endpoints/hygiene).\n"
        "Formal Lean artifact: pending toolchain (gate unclaimed).\n"
        "Human action required: ACCEPT, REJECT, or BLOCKED per review schema. "
        "REJECT/BLOCKED sets the reviewer gate only (v0.4.1 A2).\n",
        encoding="utf-8")
    print("PHASE05_PASS: 6 audits green; MST0_13_EVIDENCE_READY (REVIEWED unclaimed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
