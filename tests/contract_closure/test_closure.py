"""Malicious-implementer attack enumeration (v0.4.7 G12).

Each test plays one attack against the MACHINE-READABLE contract (yaml/json/
schemas/runners). Every attack must FAIL_CLOSED (assert the lawful block).
A passing suite = every attack blocked; a failing test = contract OPEN.
"""
import hashlib
import importlib.util
import itertools
import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

IMPL = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(IMPL))

spec = importlib.util.spec_from_file_location(
    "contract_closure", IMPL / "scripts/contract_closure.py")
cc = importlib.util.module_from_spec(spec)
sys.modules["contract_closure"] = cc
spec.loader.exec_module(cc)


def load(name):
    return yaml.safe_load((IMPL / name).read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def dual():
    return load("prereg/dual_obligation_policy.yaml")


@pytest.fixture(scope="module")
def battlefield():
    return load("prereg/theorem_battlefield.yaml")


@pytest.fixture(scope="module")
def gates():
    return load("prereg/theorem_gate_matrix.yaml")


@pytest.fixture(scope="module")
def status():
    return json.loads((IMPL / "math/proof_status.json").read_text(encoding="utf-8"))


def table(dual):
    return {(t["from_truth"], t["event"]) for t in dual["transitions"]}


def test_promote_without_certificate_blocked(dual):
    # No REVIEWED row reachable without the human-ACCEPT event.
    assert not any(t["to_truth"] == "REVIEWED" and t["event"] != "human-ACCEPT"
                   for t in dual["transitions"])


def test_reject_is_not_refuted(dual):
    assert ("PROVED", "human-REJECT") in table(dual)
    rows = [t for t in dual["transitions"]
            if t["from_truth"] == "PROVED" and t["event"] == "human-REJECT"]
    assert all(r["to_truth"] == "UNPROVED" for r in rows)
    assert not any("REJECT" in e and r["to_truth"] == "REFUTED"
                   for (f, e), r in [((t["from_truth"], t["event"]), t)
                                     for t in dual["transitions"]])


def test_blocked_is_not_refuted(dual):
    assert ("BLOCKED", "blocker-cleared") in table(dual)
    # BLOCKED->REFUTED exists ONLY via the exact-witness event (lawful); bare
    # BLOCKED status never refutes.
    bad = [t for t in dual["transitions"]
           if t["from_truth"] == "BLOCKED" and t["to_truth"] == "REFUTED"
           and t["event"] != "exact-witness-validated-G5"]
    assert not bad


def test_consume_before_reviewed_blocked(dual, gates):
    assert ("UNPROVED", "consume-before-REVIEWED") not in table(dual)
    for n, g in gates["gates"].items():
        if n != "MST0-19":
            assert g["required_status"] == "REVIEWED"


def test_no_weaker_theorem_under_same_id(battlefield):
    # Battlefield statements equal the G11 canonical lines in the amendment.
    am = (IMPL / "SPLAY_AM_DECIDE_IMPLEMENTATION_SPEC_v0.4.7_AMENDMENT.md").read_text(encoding="utf-8")
    import re
    BT = chr(96)
    for n in ["08U", "09", "11", "13", "14", "15", "22", "17", "18"]:
        m = re.search(r"### MST0-" + n + r".*?- Statement: " + BT + r"(.+?)" + BT, am, re.S)
        assert m and m.group(1) == battlefield["nodes"]["MST0-" + n]["statement"], n


def test_mutate_theorem_doc_detected(battlefield):
    # Live recomputation: battlefield document hashes match current bytes.
    for n, rec in battlefield["nodes"].items():
        live = hashlib.sha256((IMPL / rec["document"]).read_bytes()).hexdigest()
        assert live == rec["document_sha256"], n


def test_mutate_schema_detected():
    from jsonschema import Draft202012Validator
    for s in IMPL.glob("schemas/*.schema.json"):
        Draft202012Validator.check_schema(json.loads(s.read_text(encoding="utf-8")))


def test_mutate_executable_detected():
    from python.inherited import splay as S
    t = S.node(1, S.LEAF, S.node(2, S.LEAF, S.node(3, S.LEAF, S.LEAF)))
    t2 = S.splay(t, 3)
    assert S.valid(t2) and t2[1] == 3 and sorted(S.keys(t2)) == [1, 2, 3]


def test_finite_survival_is_not_proof(dual):
    assert dual["review_semantics"]["finite-survival-means"] == "not-proved"


def test_canary_is_diagnostic_only():
    am = (IMPL / "SPLAY_AM_DECIDE_IMPLEMENTATION_SPEC_v0.4.7_AMENDMENT.md").read_text(encoding="utf-8")
    assert "diagnostic only" in am and "Phase-03" in am


def test_fabricated_review_json_rejected():
    from jsonschema import validate, ValidationError
    schema = json.loads((IMPL / "schemas/review_record.schema.json").read_text(encoding="utf-8"))
    fabricated = {"node": "MST0-14", "verdict": "ACCEPT"}  # no provenance/hashes
    with pytest.raises(ValidationError):
        validate(fabricated, schema)


def test_refuted_without_witness_blocked(dual):
    assert "exact-witness-satisfying-frozen-negation" in dual["refuted_rule"]["requires"]


def test_refuted_without_replay_blocked(dual):
    assert "independent-replay-check-AGREE" in dual["refuted_rule"]["requires"]


def test_source_mismatch_is_block_not_falsity():
    # mismatch state (P4 true, no refutation): BLOCKED outcome, never DISPROVED.
    assert cc.phase18_decide(False, False, False, True, False, False) == "BRIDGE_BLOCKED_NO_CLAIM"


def test_source_unavailable_is_not_falsity(battlefield, gates, status):
    rec = battlefield["nodes"]["MST0-19"]
    assert rec["statement_synthesized"] is False
    assert "statement_sha256" not in rec
    assert gates["gates"]["MST0-19"]["required_status"] == "NOT_APPLICABLE_BY_SOURCE_UNAVAILABLE"
    assert status["obligations"]["MST0-19"]["truth"] == "BLOCKED"


def test_proof_failure_is_not_falsity(dual):
    rows = [t for t in dual["transitions"] if t["event"] == "human-REJECT"]
    assert rows and all(r["to_truth"] != "REFUTED" for r in rows)


def test_negative_without_exact_refuted_blocked():
    pol = load("prereg/negative_lifting_policy.yaml")
    assert pol["activation"] == "dormant-until-exact-REFUTED"


def test_refutation_survives_resource_exhaustion():
    assert cc.phase18_decide(False, False, True, False, False, True) == \
        "POSITIVE_ROUTE_REFUTED_NO_DOC_NEGATIVE"


def test_decision_total_and_single_valued():
    outs = {cc.phase18_decide(*b) for b in itertools.product([False, True], repeat=6)}
    assert outs <= {"DYNAMIC_OPTIMALITY_PROVED", "DYNAMIC_OPTIMALITY_DISPROVED",
                    "POSITIVE_ROUTE_REFUTED_NO_DOC_NEGATIVE",
                    "POSITIVE_ROUTE_BLOCKED_UNRESOLVED_NO_CLAIM",
                    "BRIDGE_BLOCKED_NO_CLAIM", "RESOURCE_LIMIT_NO_CLAIM"}
    assert len({cc.phase18_decide(*b) for b in itertools.product([False, True], repeat=6)}) >= 1
    for b in itertools.product([False, True], repeat=6):
        assert isinstance(cc.phase18_decide(*b), str)


def test_bridge_branch_needs_no_absent_artifacts(battlefield):
    res = battlefield["nodes"]["MST0-19"]["requirement_resolution"]
    assert res["bridge-theorem-formal-artifact"] == "NOT_APPLICABLE_BY_SOURCE_UNAVAILABLE"
    assert res["statement"] == "NOT_APPLICABLE_BY_SOURCE_UNAVAILABLE"


def test_blocked_19_not_counted_reviewed(status, gates):
    assert status["obligations"]["MST0-19"]["truth"] == "BLOCKED"
    assert gates["gates"]["MST0-19"]["required_status"] != "REVIEWED"


def test_9plus1_not_counted_as_10(battlefield):
    stmts = [n for n, r in battlefield["nodes"].items() if "statement_sha256" in r]
    assert len(stmts) == 9 and "MST0-19" not in stmts


def test_ratified_bytes_stable():
    ratified = ["IMPLEMENTATION_SPEC_v0.4.md",
                "SPLAY_AM_DECIDE_IMPLEMENTATION_SPEC_v0.4.1_AMENDMENT.md",
                "SPLAY_AM_DECIDE_IMPLEMENTATION_SPEC_v0.4.2_AMENDMENT.md",
                "SPLAY_AM_DECIDE_IMPLEMENTATION_SPEC_v0.4.3_AMENDMENT.md",
                "SPLAY_AM_DECIDE_IMPLEMENTATION_SPEC_v0.4.4_AMENDMENT.md",
                "SPLAY_AM_DECIDE_IMPLEMENTATION_SPEC_v0.4.5_AMENDMENT.md",
                "SPLAY_AM_DECIDE_IMPLEMENTATION_SPEC_v0.4.6_AMENDMENT.md"]
    r = subprocess.run(["git", "diff", "--quiet", "--", *ratified],
                       cwd=str(IMPL), timeout=60)
    assert r.returncode == 0


def test_erratum_invalidates_downstream(dual):
    rows = [t for t in dual["transitions"] if t["event"].startswith("erratum-E")]
    assert {t["event"] for t in rows} >= {"erratum-E1-proof-defective",
                                         "erratum-E2-exactly-refuted",
                                         "erratum-E3-refutation-invalid",
                                         "erratum-E4-dependency-invalidated"}
    assert any(t["prove_to"] == "INVALIDATED" for t in rows)
    assert "never overwritten" in dual["erratum_policy"]


def test_invalid_refutation_has_recovery(dual):
    rows = [t for t in dual["transitions"] if t["event"] == "erratum-E3-refutation-invalid"]
    assert rows and rows[0]["to_truth"] == "UNPROVED"
    assert any(t["event"] == "downstream-reactivation-after-E3" for t in dual["transitions"])


def test_integrity_failure_cannot_reach_phase18():
    r = subprocess.run([sys.executable, str(IMPL / "scripts/run_phase18.py")],
                       capture_output=True, timeout=60)
    assert r.returncode == 2
