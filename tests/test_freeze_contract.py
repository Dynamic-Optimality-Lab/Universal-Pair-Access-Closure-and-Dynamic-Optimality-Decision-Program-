"""Regression tests for the freeze-contract repair (v1 freeze defects).

Manifest tests prove the exact-set contract; ordering tests prove foundation
emission causally precedes any authoritative Phase-1 rerun. All 21 prior
tests are retained unweakened. Fail-closed drills use real functions on
temporary fixture copies and restore clean state via tmp_path.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import freeze_foundation
import run_phase01

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_overlap_detected_and_preregistered():
    """1: raw lists contain the known intentional overlap and it is detected."""
    raw = freeze_foundation.PREREG_PAYLOAD_FILES + freeze_foundation.FREEZE_BOUND_FILES
    dupes = {p for p in raw if raw.count(p) > 1}
    assert dupes == set(freeze_foundation.EXPECTED_OVERLAP)
    assert dupes == {"prereg/proof_stress_corpus.yaml"}


def test_union_unique_and_derived():
    """2+9: canonical union has unique paths; count derived, never hard-coded."""
    members = freeze_foundation.freeze_members()
    assert len(members) == len(set(members))
    assert len(members) == len(set(freeze_foundation.PREREG_PAYLOAD_FILES)
                               | set(freeze_foundation.FREEZE_BOUND_FILES))
    assert "prereg/prereg_sha256.txt" not in members


def test_corpus_exactly_once():
    """3: proof_stress_corpus.yaml appears exactly once."""
    members = freeze_foundation.freeze_members()
    assert members.count("prereg/proof_stress_corpus.yaml") == 1


def test_undeclared_overlap_fails(tmp_path, monkeypatch):
    """Fail-closed: undeclared duplicate declarations raise, never masked."""
    monkeypatch.setattr(freeze_foundation, "EXPECTED_OVERLAP", frozenset())
    with pytest.raises(freeze_foundation.FreezeError):
        freeze_foundation.freeze_members()


def _tmp_repo_with_members(tmp_path):
    """Create empty files for every freeze member; return (repo, hashes)."""
    members = freeze_foundation.freeze_members()
    hashes = {}
    for m in members:
        p = tmp_path / m
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b"")
        hashes[m] = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    return members, hashes


def _run_verify_with_manifest(tmp_path, monkeypatch, manifest_text):
    """Point REPO_ROOT at tmp_path, write manifest, run real verify_manifest."""
    monkeypatch.setattr(freeze_foundation, "REPO_ROOT", tmp_path)
    (tmp_path / "prereg").mkdir(parents=True, exist_ok=True)
    (tmp_path / "prereg" / "prereg_sha256.txt").write_text(manifest_text, encoding="utf-8")
    freeze_foundation.verify_manifest([])


def test_duplicate_line_fails(tmp_path, monkeypatch):
    """4 (drill): duplicated path rejected even with identical hashes (46 lines)."""
    members = freeze_foundation.freeze_members()
    for m in members:
        p = tmp_path / m
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b"")
    h = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    dup_text = "\n".join("%s  %s" % (h, m) for m in members + [members[0]]) + "\n"
    with pytest.raises(freeze_foundation.FreezeError):
        _run_verify_with_manifest(tmp_path, monkeypatch, dup_text)


def test_duplicate_masked_by_drop_fails(tmp_path, monkeypatch):
    """4b (drill): duplicate+drop keeps 44 lines but set check still rejects."""
    members = freeze_foundation.freeze_members()
    for m in members:
        p = tmp_path / m
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b"")
    h = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    masked = [m for m in members if m != members[0]] + [members[1]]
    text = "\n".join("%s  %s" % (h, m) for m in masked) + "\n"
    with pytest.raises(freeze_foundation.FreezeError):
        _run_verify_with_manifest(tmp_path, monkeypatch, text)


def test_missing_member_fails(tmp_path, monkeypatch):
    """5 (drill): manifest missing one member rejected."""
    members = freeze_foundation.freeze_members()
    for m in members:
        p = tmp_path / m
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b"")
    h = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    short = "\n".join("%s  %s" % (h, m) for m in members[1:]) + "\n"
    with pytest.raises(freeze_foundation.FreezeError):
        _run_verify_with_manifest(tmp_path, monkeypatch, short)


def test_extra_member_fails(tmp_path, monkeypatch):
    """6 (drill): unexpected extra path rejected."""
    members = freeze_foundation.freeze_members()
    for m in members:
        p = tmp_path / m
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b"")
    evil = tmp_path / "evil" / "extra.md"
    evil.parent.mkdir(parents=True, exist_ok=True)
    evil.write_bytes(b"")
    h = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    text = "\n".join("%s  %s" % (h, m) for m in members + ["evil/extra.md"]) + "\n"
    with pytest.raises(freeze_foundation.FreezeError):
        _run_verify_with_manifest(tmp_path, monkeypatch, text)


def test_wrong_sha_fails(tmp_path, monkeypatch):
    """7 (drill): one altered byte (wrong SHA) rejected."""
    members = freeze_foundation.freeze_members()
    for m in members:
        p = tmp_path / m
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b"")
    h = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    bad = ["0" * 64 if m == members[0] else h for m in members]
    text = "\n".join("%s  %s" % (x, m) for x, m in zip(bad, members)) + "\n"
    with pytest.raises(freeze_foundation.FreezeError):
        _run_verify_with_manifest(tmp_path, monkeypatch, text)


def test_self_reference_fails(tmp_path, monkeypatch):
    """8 (drill): manifest referencing itself rejected."""
    members = freeze_foundation.freeze_members()
    for m in members:
        p = tmp_path / m
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b"")
    h = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    text = "\n".join("%s  %s" % (h, m) for m in members) + "\n"
    text += "%s  prereg/prereg_sha256.txt\n" % h
    with pytest.raises(freeze_foundation.FreezeError):
        _run_verify_with_manifest(tmp_path, monkeypatch, text)


def test_valid_manifest_passes(tmp_path, monkeypatch):
    """Control: exact manifest over empty-byte members verifies green."""
    members = freeze_foundation.freeze_members()
    for m in members:
        p = tmp_path / m
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b"")
    h = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    text = "\n".join("%s  %s" % (h, m) for m in members) + "\n"
    log = []
    monkeypatch.setattr(freeze_foundation, "REPO_ROOT", tmp_path)
    (tmp_path / "prereg").mkdir(parents=True, exist_ok=True)
    (tmp_path / "prereg" / "prereg_sha256.txt").write_text(text, encoding="utf-8")
    freeze_foundation.verify_manifest(log)
    assert log[0]["status"] == "PASS"


def _ordered_harness(tmp_path, monkeypatch, emit=None, phase1=None):
    """Run the REAL run_freeze with stubbed steps; return the call record."""
    import run_phase00
    import run_phase01
    calls = []
    monkeypatch.setattr(freeze_foundation, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(run_phase00, "run_phase00",
                        lambda *a, **k: calls.append("p00") or {"checks": []})
    for name in ("freeze_parent_package", "verify_downstream_identities",
                 "verify_lifecycle_legality", "verify_bridge_manifest",
                 "verify_prereg_content", "write_snapshot", "write_manifest",
                 "verify_manifest", "verify_prefix"):
        monkeypatch.setattr(freeze_foundation, name,
                            lambda log, _n=name: calls.append(_n) or None)
    parent = tmp_path / "parent"
    parent.mkdir(parents=True, exist_ok=True)
    (tmp_path / "artifacts" / "v04" / "freeze").mkdir(parents=True, exist_ok=True)
    (tmp_path / "artifacts" / "v04" / "logs").mkdir(parents=True, exist_ok=True)
    real_emit = freeze_foundation.emit_foundation
    monkeypatch.setattr(freeze_foundation, "emit_foundation",
                        lambda log: calls.append("emit") or real_emit(log))
    if emit == "raise":
        def boom(log):
            calls.append("emit")
            raise freeze_foundation.FreezeError("forced emission failure")
        monkeypatch.setattr(freeze_foundation, "emit_foundation", boom)
    if phase1 == "raise":
        def fail(*a, **k):
            calls.append("phase1")
            raise run_phase01.Phase01Error("forced phase1 failure")
        monkeypatch.setattr(run_phase01, "run_phase01", fail)
    else:
        monkeypatch.setattr(run_phase01, "run_phase01",
                            lambda *a, **k: calls.append("phase1") or {"checks": []})
    monkeypatch.setattr(freeze_foundation, "write_superseded_v1",
                        lambda *a, **k: calls.append("supersede") or {})
    return calls, parent


def test_emit_before_phase1(tmp_path, monkeypatch):
    """10: REAL run_freeze emits foundation before authoritative Phase-1 rerun."""
    calls, parent = _ordered_harness(tmp_path, monkeypatch)
    freeze_foundation.run_freeze(str(parent))
    assert calls.index("emit") < calls.index("phase1") < calls.index("supersede")
    assert (tmp_path / "artifacts" / "v04" / "freeze" / "FOUNDATION_FROZEN.json").exists()


def test_emit_failure_blocks_phase1(tmp_path, monkeypatch):
    """11 (drill): if emission fails, Phase 1 never runs."""
    calls, parent = _ordered_harness(tmp_path, monkeypatch, emit="raise")
    with pytest.raises(freeze_foundation.FreezeError):
        freeze_foundation.run_freeze(str(parent))
    assert "phase1" not in calls
    assert "supersede" not in calls


def test_phase1_failure_blocks_authority(tmp_path, monkeypatch):
    """12 (drill): Phase-1 failure after valid freeze propagates; no authority."""
    calls, parent = _ordered_harness(tmp_path, monkeypatch, phase1="raise")
    with pytest.raises(freeze_foundation.FreezeError):
        freeze_foundation.run_freeze(str(parent))
    assert "supersede" not in calls
    assert not (tmp_path / "artifacts" / "v04" / "freeze" / "SUPERSEDED_V1_FREEZE.json").exists()


def test_supersede_requires_post_freeze_order():
    """13: supersession record schema demands both foundation and phase1 SHAs."""
    import inspect
    src = inspect.getsource(freeze_foundation.write_superseded_v1)
    assert "new_foundation_sha" in src
    assert "new_phase1_sha" in src
    assert "old_foundation_sha" in src
    assert "divergent" in src
