"""Stress tests for spec PHASE 00 (WorkPlan Phase 1).

Proves the gate is deterministic, tamper-evident, and fail-closed:
repeatability (idempotent green), tamper detection (mutated seal fails),
missing-input handling (absent parent fails). No holdout is touched.
"""

import json
import shutil
import sys
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import run_phase00

PARENT = Path(__file__).resolve().parent.parent.parent / "parent-ref"
REPO_ROOT = Path(__file__).resolve().parent.parent


def _minimal_parent_copy(tmp, mutate_final=False):
    """Build a slim parent tree with the seal files the gate reads."""
    src_seal = PARENT / "artifacts" / "v03" / "seal"
    dst = Path(tmp) / "parent"
    (dst / "artifacts" / "v03" / "seal").mkdir(parents=True)
    (dst / "artifacts" / "v03" / "holdouts").mkdir(parents=True)
    (dst / "artifacts" / "v03" / "proofs").mkdir(parents=True)
    for name in ("FINAL_RESULT.json", "MANIFEST.sha256", "ARCHIVE.sha256",
                 "SPLAY-AM-MST-v0.3.tar.zst"):
        shutil.copy2(src_seal / name, dst / "artifacts" / "v03" / "seal" / name)
    for name in ("candidate_set_commit.json", "h3t_state.json"):
        shutil.copy2(PARENT / "artifacts" / "v03" / "holdouts" / name,
                     dst / "artifacts" / "v03" / "holdouts" / name)
    shutil.copy2(PARENT / "artifacts" / "v03" / "proofs" / "obligation_status.json",
                 dst / "artifacts" / "v03" / "proofs" / "obligation_status.json")
    for name in ("TRANSFER_CALCULUS_LEDGER.md", "Path.md", "WorkPlan.md",
                 "SPLAY_AM_MST_IMPLEMENTATION_SPEC_v0.3.1_PIN.md"):
        shutil.copy2(PARENT / name, dst / name)
    if mutate_final:
        p = dst / "artifacts" / "v03" / "seal" / "FINAL_RESULT.json"
        fr = json.loads(p.read_text(encoding="utf-8"))
        fr["terminal_claim"] = "TAMPERED_CLAIM"
        p.write_text(json.dumps(fr), encoding="utf-8")
    return dst


def _init_git_repo(path):
    """Init a git repo at path with everything committed; return Nothing."""
    import subprocess
    subprocess.run(["git", "init", "-q", str(path)], check=True, timeout=60)
    subprocess.run(["git", "-C", str(path), "config", "user.email", "t@t"],
                   check=True, timeout=60)
    subprocess.run(["git", "-C", str(path), "config", "user.name", "t"],
                   check=True, timeout=60)
    subprocess.run(["git", "-C", str(path), "add", "-A"], check=True, timeout=60)
    subprocess.run(["git", "-C", str(path), "commit", "-qm", "t"], check=True, timeout=60)


def test_repeatability_same_certificate():
    """Two consecutive full runs produce byte-identical check sequences."""
    cert1 = run_phase00.run_phase00(str(PARENT))
    cert2 = run_phase00.run_phase00(str(PARENT))
    seq1 = [(c["step"], c["name"], c["status"]) for c in cert1["checks"]]
    seq2 = [(c["step"], c["name"], c["status"]) for c in cert2["checks"]]
    assert seq1 == seq2
    assert len(seq1) == 13


def test_missing_parent_fails_closed():
    """Absent parent directory raises instead of passing vacuously."""
    with pytest.raises(run_phase00.Phase00Error):
        run_phase00.run_phase00(str(REPO_ROOT / "no-such-parent"))


def test_tampered_terminal_fails():
    """Mutated FINAL_RESULT is rejected (tamper-evident gate)."""
    with tempfile.TemporaryDirectory() as tmp:
        dst = _minimal_parent_copy(tmp, mutate_final=True)
        _init_git_repo(dst)
        log = []
        with pytest.raises(run_phase00.Phase00Error):
            run_phase00.check_final_result(dst, log)


def test_wrong_head_fails():
    """A clone at any other commit is rejected (full-SHA binding)."""
    with tempfile.TemporaryDirectory() as tmp:
        dst = _minimal_parent_copy(tmp)
        _init_git_repo(dst)
        log = []
        with pytest.raises(run_phase00.Phase00Error):
            run_phase00.check_parent_head(dst, log)
