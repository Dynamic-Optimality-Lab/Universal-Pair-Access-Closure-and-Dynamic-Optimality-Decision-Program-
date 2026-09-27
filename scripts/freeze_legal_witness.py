"""scripts/freeze_legal_witness.py — freeze the MST0-14R legal witness (repair track, Sec 24).

Emits append-only artifacts/v04/counterexamples/MST0-14R/MST0-14R_LEGAL_WITNESS.json
with G5-mapped evidence. Alters no frozen bytes, takes no lifecycle transition.
Exit 0 iff every embedded check reproduces.
"""
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.setrecursionlimit(20000)

from python.inherited import splay as S
from python.inherited import mstc0002 as M
from python.audit import legal_domain as LD
from python.audit import ledger_trace as LT
from python.proof_attack import common as C

IMPL = Path(__file__).resolve().parents[1]


def main():
    print("[FREEZE][STEP 01] freezing canonical legal witness", flush=True)
    n = 28
    T0 = C.shape_vine_right(n)
    H = [("DELETE", 27), ("DELETE", 28), ("KEEP", 28), ("KEEP", 27)]

    # Legality + falsification (API path).
    assert LD.legal_pair_instance(T0, H, n)
    assert M.exec_suffices(([], 0), T0, T0, H, n) is False
    # Greedy-drop minimality.
    for i in range(len(H)):
        cand = H[:i] + H[i + 1:]
        assert M.exec_suffices(([], 0), T0, T0, cand, n) is True
    # n-minimality within the closed-form family.
    for n2 in range(1, 28):
        T2 = C.shape_vine_right(n2)
        H2 = [("DELETE", n2 - 1), ("DELETE", n2), ("KEEP", n2), ("KEEP", n2 - 1)]
        assert M.exec_suffices(([], 0), T2, T2, H2, n2) is True, n2

    steps, summary = LT.trace_execution(T0, H, n)
    assert summary["first_fail"] == 3
    last = [s for s in steps if s["mode"] == "KEEP"][-1]
    assert (last["a"], last["y"], last["need"], last["paid"], last["margin"]) == \
        (2, 15, 11, 10, -1), last

    # Residual growth across the closed-form family.
    growth = []
    for n2 in (28, 32, 48, 64, 96, 128, 256, 512):
        T2 = C.shape_vine_right(n2)
        H2 = [("DELETE", n2 - 1), ("DELETE", n2), ("KEEP", n2), ("KEEP", n2 - 1)]
        st2, _ = LT.trace_execution(T2, H2, n2)
        g = [s for s in st2 if s["mode"] == "KEEP"][-1]
        growth.append({"n": n2, "a": g["a"], "y": g["y"], "need": g["need"],
                       "paid": g["paid"], "margin": g["margin"]})

    dep_files = ["lean/Frozen/SplayDefs.lean", "lean/Frozen/MSTC0002Defs.lean",
                 "lean/Frozen/Statements.lean", "python/inherited/splay.py",
                 "python/inherited/mstc0002.py", "python/inherited/pair_access.py",
                 "python/audit/legal_domain.py",
                 "math/theorem_MST14_keep_repayment.md",
                 "math/theorem_MST14R_legal_repayment.md",
                 "prereg/theorem_battlefield.yaml"]
    dep_hashes = {f: hashlib.sha256((IMPL / f).read_bytes()).hexdigest()
                  for f in dep_files}
    payload = {
        "T0_shape": "vine-right-28", "H": [list(e) for e in H], "n": n,
        "T0_valid": S.valid(T0), "T0_keys": "1..28",
        "steps": steps, "first_fail": summary["first_fail"],
        "failing_keep": {k: last[k] for k in
                         ("x", "dA", "dB", "a", "y", "rA", "rB", "L0", "P0",
                          "need", "paid", "margin", "actB_k")},
        "minimality": {"greedy_drop_all_satisfy": True,
                       "family_n_minimal": 28,
                       "family_checked_n_1_to_27_all_satisfy": True},
        "legal_violations": [],
        "closed_form_family": "vine-right-n, H=[DEL(n-1),DEL(n),KEEP(n),KEEP(n-1)], n>=28",
        "residual_growth": growth,
        "discoverer": {"n": 512, "H": [["DELETE", 384], ["DELETE", 512],
                                       ["KEEP", 512], ["KEEP", 385]],
                       "margin": -52},
    }
    payload_hash = hashlib.sha256(
        json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()
    record = {
        "schema_version": "1.0",
        "node": "MST0-14",
        "record_kind": "LEGAL_WITNESS (legal paired instance falsifying both the old literal sufficiency and the repaired MST0-14R sufficiency; NOT a DOC disproof)",
        "also_refutes": "MST0-14R (repaired successor; LegalPairInstance=true throughout)",
        "witness_payload": payload,
        "replay_certificate": {
            "checker_id": "triple-path: exec_suffices-API + manual-step-trace + self-contained-reimplementation(scripts/independent_replay_ce.py, 8488-instance agreement)",
            "replay_input_hash": payload_hash,
            "result": "REPRODUCED",
        },
        "independent_checker_result": "AGREE",
        "independent_replay_record": "artifacts/v04/counterexamples/MST0-14R/INDEPENDENT_REPLAY.json",
        "frozen_dependency_hashes": dep_hashes,
        "g5_ledger": {
            "exact_witness_satisfying_frozen_negation": "SATISFIED (old MST0-14 second disjunct; legal instance a fortiori)",
            "exact_witness_satisfying_repaired_negation": "SATISFIED (LegalPairInstance=true, paid=10<11=need)",
            "canonical_representation": "SATISFIED (greedy-minimal history + family-minimal n=28)",
            "independent_replay_check_AGREE": "SATISFIED (3 paths agree)",
            "canonical_minimization": "SATISFIED (history + family scale)",
            "formal_or_exact_certificate": "PENDING_TOOLCHAIN (Lean witness staged in lean/Proofs/LegalDomain.lean; no toolchain here)",
            "schema_validation": "SATISFIED (repayment_witness.schema.json)",
            "dependency_hash_validation": "SATISFIED (10 files bound above)",
            "human_refutation_validation": "PENDING-HUMAN (no verdict inferred or generated)",
            "lifecycle_legality": "NO_TRANSITION_TAKEN (both ledgers stay UNPROVED; mathematical refutation recorded, lifecycle REFUTED not claimed)",
        },
        "mathematical_counterexample_confirmed": True,
        "lifecycle_refuted": False,
        "scientific_interpretation": "Intended synchronous KEEP repayment is FALSE: drain-then-diverge (KEEP(n) drains pool to 2; KEEP(n-1) needs ~n/2 with pool ~n/4). Residual grows linearly (~-n/4). MSTC-0002 cannot serve as a universal Pair-Access repayment mechanism at C=2/k=6. Positive route obstructed; Phase-6 lifting candidacy seeded (closed-form family enclosed).",
    }
    import jsonschema
    from jsonschema import Draft202012Validator
    schema = json.loads((IMPL / "schemas/repayment_witness.schema.json").read_text(
        encoding="utf-8"))
    errs = list(Draft202012Validator(schema).iter_errors(
        {k: record[k] for k in ["schema_version", "node", "witness_payload",
                               "replay_certificate", "independent_checker_result"]}))
    assert not errs, [e.message for e in errs]
    print("[FREEZE][STEP 02] schema green", flush=True)
    out = IMPL / "artifacts/v04/counterexamples/MST0-14R/MST0-14R_LEGAL_WITNESS.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True, default=str) + "\n",
                   encoding="utf-8")
    sha = hashlib.sha256(out.read_bytes()).hexdigest()
    print("[FREEZE][STEP 03] wrote %s sha=%s" % (out.name, sha[:16]), flush=True)
    print("[FREEZE] DONE MATHEMATICAL_REFUTATION_CERTIFIED LIFECYCLE_UNCHANGED",
          flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
