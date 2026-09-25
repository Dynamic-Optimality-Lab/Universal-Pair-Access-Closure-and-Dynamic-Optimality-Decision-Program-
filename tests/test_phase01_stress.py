"""Stress tests for spec PHASE 01 (WorkPlan Phase 1).

Proves the gates are deterministic, tamper-evident, and fail-closed:
repeatability, mutated-survivor rejection, mutated-reveal rejection,
missing-input handling. No holdout content is read by any test.
"""

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import run_phase01

PARENT = Path(__file__).resolve().parent.parent.parent / "parent-ref"
REPO_ROOT = Path(__file__).resolve().parent.parent


def _slim_parent_copy(tmp):
    """Copy only the seal files the PHASE-01 gate reads (no bank content)."""
    dst = Path(tmp) / "parent"
    for rel in ("artifacts/v03/seal/FINAL_RESULT.json",
                "artifacts/v03/seal/MANIFEST.sha256",
                "artifacts/v03/seal/ARCHIVE.sha256",
                "artifacts/v03/seal/SPLAY-AM-MST-v0.3.tar.zst",
                "artifacts/v03/holdouts/candidate_set_commit.json",
                "artifacts/v03/holdouts/h3t_state.json",
                "artifacts/v03/holdouts/h3t_reveal.json",
                "artifacts/v03/holdouts/h3t_commitment.json",
                "artifacts/v03/proofs/obligation_status.json",
                "TRANSFER_CALCULUS_LEDGER.md",
                "Path.md", "WorkPlan.md",
                "SPLAY_AM_MST_IMPLEMENTATION_SPEC_v0.3.1_PIN.md",
                "COUNTEREXAMPLE_ATLAS.md",
                "math/theorem_MST13_delete_injection.md",
                "artifacts/v03/proofs/MST13_injection_bound.json"):
        src = PARENT / rel
        tgt = dst / rel
        tgt.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, tgt)
    (dst / "math" / "reviews").mkdir(parents=True, exist_ok=True)
    return dst


def _init_git_repo(path):
    """Init a git repo at path with everything committed; return Nothing."""
    subprocess.run(["git", "init", "-q", str(path)], check=True, timeout=60)
    subprocess.run(["git", "-C", str(path), "config", "user.email", "t@t"],
                   check=True, timeout=60)
    subprocess.run(["git", "-C", str(path), "config", "user.name", "t"],
                   check=True, timeout=60)
    subprocess.run(["git", "-C", str(path), "add", "-A"], check=True, timeout=60)
    subprocess.run(["git", "-C", str(path), "commit", "-qm", "t"], check=True, timeout=60)


def test_repeatability_same_certificate():
    """Two full runs produce identical 6-check PASS sequences."""
    cert1 = run_phase01.run_phase01(str(PARENT))
    cert2 = run_phase01.run_phase01(str(PARENT))
    seq1 = [(c["step"], c["name"], c["status"]) for c in cert1["checks"]]
    seq2 = [(c["step"], c["name"], c["status"]) for c in cert2["checks"]]
    assert seq1 == seq2
    assert len(seq1) == 6
    assert cert1["gates"] == ["SURVIVOR_IDENTITY_VERIFIED", "BATTLEFIELD_VERIFIED"]


def test_missing_parent_fails_closed():
    """Absent parent directory raises instead of passing vacuously."""
    with pytest.raises(run_phase01.Phase01Error):
        run_phase01.run_phase01(str(REPO_ROOT / "no-such-parent"))


def test_mutated_k_rejected():
    """k=6 -> k=5 in the candidate-set copy is rejected (field binding)."""
    with tempfile.TemporaryDirectory() as tmp:
        dst = _slim_parent_copy(tmp)
        _init_git_repo(dst)
        p = dst / "artifacts" / "v03" / "holdouts" / "candidate_set_commit.json"
        cs = json.loads(p.read_text(encoding="utf-8"))
        for c in cs["candidates"]:
            if c["calculus_id"] == "MSTC-0002":
                c["k"] = 5
        p.write_text(json.dumps(cs), encoding="utf-8")
        log = []
        with pytest.raises(run_phase01.Phase01Error):
            run_phase01.check_survivor_binding(dst, log)


def test_mutated_reveal_verdict_rejected():
    """Flipped sibling verdict in the reveal copy is rejected (history check)."""
    with tempfile.TemporaryDirectory() as tmp:
        dst = _slim_parent_copy(tmp)
        _init_git_repo(dst)
        p = dst / "artifacts" / "v03" / "holdouts" / "h3t_reveal.json"
        rv = json.loads(p.read_text(encoding="utf-8"))
        for r in rv["results"]:
            if r["calculus_id"] == "MSTC-0001":
                r["verdict"] = "FRESH_H3T_PASS"
        p.write_text(json.dumps(rv), encoding="utf-8")
        log = []
        with pytest.raises(run_phase01.Phase01Error):
            run_phase01.check_fresh_history(dst, log)


def test_wrong_head_fails():
    """A clone at any other commit is rejected (full-SHA binding)."""
    with tempfile.TemporaryDirectory() as tmp:
        dst = _slim_parent_copy(tmp)
        _init_git_repo(dst)
        log = []
        with pytest.raises(run_phase01.Phase01Error):
            run_phase01.check_parent_head(dst, log)
