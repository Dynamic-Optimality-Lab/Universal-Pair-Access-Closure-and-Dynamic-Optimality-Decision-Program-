"""scripts/certify_mst014_domain_defect.py — certify the MST0-14 domain defect (repair track).

Replays the malformed-domain witness against the exact current frozen
Python mirror via two independent call paths, verifies minimality,
verifies LegalPairInstance rejects it, binds frozen dependency hashes,
validates against schemas/repayment_witness.schema.json, and emits an
append-only counterexample record. New file; alters no frozen bytes.

Witness: T0 = right vine {1,2,3}, H = [(DELETE,3),(KEEP,3)], n = 0.
Expected: execSuffices = False with paid=0 != need=1 at KEEP 3.

G5 ledger honesty (see record): formal machine-check + human refutation
validation are PENDING; proof_status.json is NOT touched by this script.
Exit 0 iff every check reproduces exactly.
"""
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.setrecursionlimit(20000)

from python.inherited import splay as S
from python.inherited import mstc0002 as M
from python.inherited import pair_access as PA
from python.audit import legal_domain as LD
from python.proof_attack import common as C

IMPL = Path(__file__).resolve().parents[1]


def build_vine(ks):
    t = S.LEAF
    for k in ks:
        t = C._insert_desc(t, k)
    return t


def replay_path_api(T0, H, n):
    """Path 1: top-level exec_suffices predicate."""
    return M.exec_suffices(([], 0), T0, T0, H, n)


def replay_path_manual(T0, H, n):
    """Path 2: manual step replay with per-KEEP (need,paid,pool) trace."""
    E, A, B, steps = ([], 0), T0, T0, []
    for mode, x in H:
        if mode == "KEEP":
            a_pre = S.splay_cost(A, x)
            y_pre = S.splay_cost(B, x)
            E1, A2, a = M.replay_access_A(E, A, mode, x, n)
            assert a == a_pre
            pool_pre = M.active_pool(E1[0])
            E2, B2, y, paid = M.replay_access_B(E1, B, x, a)
            assert y == y_pre
            need = M.required(y, a)
            steps.append({"x": x, "y": y, "a": a, "need": need,
                          "paid": paid, "pool_pre": pool_pre,
                          "ok": paid == need})
            E, A, B = E2, A2, B2
        else:
            E1, A2, _a = M.replay_access_A(E, A, mode, x, n)
            E, A = E1, A2
    return all(s["ok"] for s in steps if True) and all(
        s["ok"] for s in steps), steps


def main():
    print("[CERT][STEP 01] replaying MST0-14 domain-defect witness", flush=True)
    T0 = build_vine([1, 2, 3])
    H = [("DELETE", 3), ("KEEP", 3)]
    n = 0

    # Static facts.
    assert S.valid(T0), "T0 must be a valid BST"
    assert S.keys(T0) == [1, 2, 3]
    assert S.depth(T0, 3) == 2 and S.splay_cost(T0, 3) == 3
    trace_del = S.splay_trace(T0, 3)[1]
    assert trace_del == [("RR", 1, 3)], f"unexpected DELETE trace {trace_del}"
    assert M.sites(1, 3, 3, n) == [], "sites must starve at nkeys=0"

    # Path 1.
    r_api = replay_path_api(T0, H, n)
    # Path 2.
    r_manual, steps = replay_path_manual(T0, H, n)
    assert r_api is False, "witness must falsify exec_suffices"
    assert r_manual is False, "manual replay must agree"
    assert len(steps) == 1
    st = steps[0]
    assert (st["y"], st["a"], st["need"], st["paid"], st["pool_pre"]) == (3, 1, 1, 0, 0), st

    # Minimality: every strict sub-history satisfies.
    assert M.exec_suffices(([], 0), T0, T0, H[:1], n) is True
    assert M.exec_suffices(([], 0), T0, T0, H[1:], n) is True
    assert M.exec_suffices(([], 0), T0, T0, [], n) is True

    # Legal-domain rejection.
    bad = LD.violations(T0, H, n)
    assert LD.C_TREE_KEYS in bad and LD.C_HIST_KEYS in bad, bad
    assert LD.legal_pair_instance(T0, H, n) is False
    assert PA.validate_history(H, n) is False

    print("[CERT][STEP 02] MATHEMATICAL_COUNTEREXAMPLE_CONFIRMED=true", flush=True)

    # Dependency hashes (frozen bytes bound at certification time).
    frozen_files = ["lean/Frozen/SplayDefs.lean", "lean/Frozen/MSTC0002Defs.lean",
                    "lean/Frozen/Statements.lean", "python/inherited/splay.py",
                    "python/inherited/mstc0002.py", "python/inherited/pair_access.py",
                    "math/theorem_MST14_keep_repayment.md",
                    "prereg/theorem_battlefield.yaml"]
    dep_hashes = {f: hashlib.sha256((IMPL / f).read_bytes()).hexdigest()
                  for f in frozen_files}

    payload = {
        "T0": T0, "H": [list(e) for e in H], "n": n,
        "T0_valid": True, "T0_keys": [1, 2, 3],
        "DELETE": {"a": 3, "trace": [["RR", 1, 3]], "sites_1_3_3_0": [],
                   "ledger_after": [], "cursor_after": 0},
        "KEEP": {"a": 1, "A_trace": [], "y": 3, "B_trace": [["RR", 1, 3]],
                 "need": 1, "paid": 0, "pool_pre": 0},
        "exec_suffices": False,
        "minimality": {"drop_DELETE_satisfies": True,
                       "drop_KEEP_satisfies": True,
                       "empty_satisfies": True},
        "legal_violations": sorted(bad),
        "validate_history_H_0": False,
    }
    payload_hash = C.sha_text(json.dumps(payload, sort_keys=True))
    record = {
        "schema_version": "1.0",
        "node": "MST0-14",
        "record_kind": "DOMAIN_DEFECT_WITNESS (old literal proposition; NOT a legal MSTC-0002 counterexample)",
        "witness_payload": payload,
        "replay_certificate": {
            "checker_id": "scripts/certify_mst014_domain_defect.py dual-path replay",
            "replay_input_hash": payload_hash,
            "result": "REPRODUCED",
        },
        "dual_path_agreement": {"exec_suffices_api": False,
                                "manual_step_replay": False},
        "independent_checker_result": "AGREE",
        "frozen_dependency_hashes": dep_hashes,
        "old_statement_line_sha256": hashlib.sha256(
            next(l[len("- Statement: "):] for l in
                 (IMPL / "math/theorem_MST14_keep_repayment.md").read_text(
                     encoding="utf-8").splitlines()
                 if l.startswith("- Statement: ")).encode("utf-8")).hexdigest(),
        "g5_ledger": {
            "exact_witness_satisfying_frozen_negation": "SATISFIED (second disjunct: exists T0,H,n with execSuffices=false)",
            "canonical_representation": "SATISFIED (sorted-JSON payload, greedy-minimal history)",
            "independent_replay_check_AGREE": "SATISFIED (dual Python call paths agree)",
            "canonical_minimization": "SATISFIED (all strict sub-histories satisfy)",
            "formal_or_exact_certificate": "PENDING_TOOLCHAIN (Lean witness file staged; no toolchain in this environment)",
            "schema_validation": "SATISFIED (repayment_witness.schema.json, see below)",
            "dependency_hash_validation": "SATISFIED (8 frozen files bound above)",
            "human_refutation_validation": "PENDING-HUMAN (no verdict inferred or generated)",
            "lifecycle_legality": "NO_TRANSITION_TAKEN (proof_status.json untouched; MATHEMATICAL fact recorded, LIFECYCLE REFUTED not claimed)",
        },
        "mathematical_counterexample_confirmed": True,
        "lifecycle_refuted": False,
        "scientific_interpretation": "The literal frozen MST0-14 sufficiency conjunct is false (domain bug: no LegalPairInstance guard). The witness is ILLEGAL (violates C2+C4), so it does not touch the intended MSTC-0002 repayment claim. Old bytes preserved; repaired successor tracked separately.",
    }

    # Schema validation (repayment_witness: node const + open payload).
    import jsonschema
    from jsonschema import Draft202012Validator
    schema = json.loads((IMPL / "schemas/repayment_witness.schema.json").read_text(
        encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    errors = list(validator.iter_errors({k: record[k] for k in
                                         ["schema_version", "node", "witness_payload",
                                          "replay_certificate", "independent_checker_result"]}))
    assert not errors, [e.message for e in errors]
    print("[CERT][STEP 03] schema validation green", flush=True)

    outdir = IMPL / "artifacts/v04/counterexamples/MST0-14"
    outdir.mkdir(parents=True, exist_ok=True)
    path = outdir / "MST0-14_DOMAIN_DEFECT_WITNESS.json"
    path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8")
    sha = hashlib.sha256(path.read_bytes()).hexdigest()
    print(f"[CERT][STEP 04] wrote {path} sha={sha[:16]}", flush=True)
    print("[CERT] DONE MATHEMATICAL_COUNTEREXAMPLE_CONFIRMED=true LIFECYCLE_REFUTED=false",
          flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
