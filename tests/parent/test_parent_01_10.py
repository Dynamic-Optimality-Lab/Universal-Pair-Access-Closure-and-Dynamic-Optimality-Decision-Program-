"""PARENT-01..PARENT-10 named tests (exact normative meanings, v0.4 spec s2/WorkPlan s4).

PARENT-01 full sealed commit exact | PARENT-02 FINAL_RESULT exact |
PARENT-03 manifest/archive exact | PARENT-04 Path/WorkPlan exact |
PARENT-05 MSTC-0002 record exact | PARENT-06 candidate-set binds MSTC-0002 |
PARENT-07 sibling H3T failures preserved | PARENT-08 H3T UNLOCKED_ONCE, no reread |
PARENT-09 blocker DAG matches sealed matrix | PARENT-10 no pre-prereg v0.4 science.
All evidence from parent/V03_* bootstrap (hash-verified copies + provenance records).
"""
import hashlib
import json
import subprocess
from pathlib import Path

IMPL = Path(__file__).resolve().parents[2]
PREF = IMPL / ".." / "parent-ref"
PIN = "353ee922b1cee0043afa46fe8929f42f7652e5bf"
SET_HASH = "8FD3273143DEC3CA4611A1093F3521B8F22DE2BBD6A82715EE270412F65A2A00"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def test_PARENT_01_sealed_commit_exact():
    r = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(PREF),
                       capture_output=True, text=True, timeout=60)
    assert r.stdout.strip() == PIN


def test_PARENT_02_final_result_exact():
    assert sha(IMPL / "parent/V03_FINAL_RESULT.json") == \
        sha(PREF / "artifacts/v03/seal/FINAL_RESULT.json")


def test_PARENT_03_manifest_archive_exact():
    assert sha(IMPL / "parent/V03_MANIFEST.sha256") == \
        sha(PREF / "artifacts/v03/seal/MANIFEST.sha256")
    assert sha(IMPL / "parent/V03_ARCHIVE.sha256") == \
        sha(PREF / "artifacts/v03/seal/ARCHIVE.sha256")


def test_PARENT_04_path_workplan_exact():
    assert sha(IMPL / "parent/V03_PATH_FINAL.md") == sha(PREF / "Path.md")
    assert sha(IMPL / "parent/V03_WORKPLAN_FINAL.md") == sha(PREF / "WorkPlan.md")


def test_PARENT_05_mstc0002_exact():
    assert sha(IMPL / "parent/V03_MSTC_0002.json") == \
        sha(PREF / "artifacts/v03/hypotheses/MSTC-0002.json")


def test_PARENT_06_candidate_set_binds_survivor():
    fr = json.loads((IMPL / "parent/V03_FINAL_RESULT.json").read_text(encoding="utf-8"))
    assert fr["hashes"]["candidate_set"] == SET_HASH
    assert fr["standing"] == ["MSTC-0002"]
    m = json.loads((IMPL / "parent/V03_MSTC_0002.json").read_text(encoding="utf-8"))
    assert m["calculus_id"] == "MSTC-0002"


def test_PARENT_07_sibling_failures_preserved():
    fr = json.loads((IMPL / "parent/V03_FINAL_RESULT.json").read_text(encoding="utf-8"))
    killed = {k["calculus_id"]: k["verdict"] for k in fr["killed_fresh"]}
    assert killed.get("MSTC-0001") == "FRESH_H3T_FAIL"
    assert killed.get("MSTC-0003") == "FRESH_H3T_FAIL"


def test_PARENT_08_h3t_unlocked_once_no_reread():
    fr = json.loads((IMPL / "parent/V03_FINAL_RESULT.json").read_text(encoding="utf-8"))
    assert fr["firewalls"]["H3T"] == "UNLOCKED_ONCE/unlocks=1"
    assert not list(IMPL.rglob("*h3t*")) and not list(IMPL.rglob("*H3T*"))
    assert not list(IMPL.glob("holdout*"))


def test_PARENT_09_blocker_dag_matches():
    st = json.loads((IMPL / "parent/V03_THEOREM_STATUS.json").read_text(encoding="utf-8"))
    obs = st["obligations"]
    get = lambda oid: next(v for k, v in obs.items() if k.startswith(oid))
    assert get("MST0-13")["status"] == "PROVED"
    assert get("MST0-14")["status"] == "UNPROVED"
    assert "finite" in get("MST0-08")["evidence"].lower()
    assert st["final_obligations_map"] == {"BLOCKED": 3, "NOT_APPLICABLE": 3,
                                           "PROVED": 4, "REVIEWED": 10, "UNPROVED": 6}


def test_PARENT_10_no_preprereg_science():
    for d in ["proofs", "counterexamples", "seal", "negative"]:
        files = [p for p in (IMPL / "artifacts/v04" / d).iterdir() if p.name != ".gitkeep"]
        assert not files, (d, files)
    assert not (IMPL / "artifacts/v04/seal/FINAL_RESULT.json").exists()
