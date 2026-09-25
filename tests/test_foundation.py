"""Foundation tests for spec PHASE 00-01 (WorkPlan Phase 1).

Functional layer: each test mirrors one run_phaseXX STEP by calling the same
check functions, so a green suite means the scripts and the suite agree.
Stress layers live in test_phase00_stress.py and test_phase01_stress.py.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import run_phase00
import run_phase01

PARENT = Path(__file__).resolve().parent.parent.parent / "parent-ref"


def test_parent_head_and_clean():
    """PARENT-01: full sealed commit exact; working tree clean."""
    log = []
    run_phase00.check_parent_head(PARENT, log)
    assert log[0]["status"] == "PASS"


def test_final_result_terminal():
    """PARENT-02/05/06/07: terminal claim, survivor, sibling kills, firewalls."""
    log = []
    run_phase00.check_final_result(PARENT, log)
    assert log[0]["status"] == "PASS"


def test_candidate_set_binds_survivor():
    """PARENT-05/06: MSTC-0002 = (P_all, k=6, C=2) bound to set hash."""
    log = []
    run_phase00.check_candidate_set(PARENT, log)
    assert log[0]["status"] == "PASS"


def test_h3t_state_once():
    """PARENT-08: H3T UNLOCKED_ONCE/1 without reread."""
    log = []
    run_phase00.check_h3t_state(PARENT, log)
    assert log[0]["status"] == "PASS"


def test_lifecycle_counts():
    """PARENT-09 (part): lifecycle 10/4/3/3/6 over 26 obligations."""
    log = []
    run_phase00.check_obligation_status(PARENT, log)
    assert log[0]["status"] == "PASS"


def test_seal_byte_identity():
    """PARENT-03: 424-file manifest shape + archive byte identity."""
    log = []
    run_phase00.check_seal_files(PARENT, log)
    assert log[0]["status"] == "PASS"


def test_spec_and_ledger_frozen():
    """Spec bytes preserved; v0.4 ledger matches the mapped frontier."""
    log = []
    run_phase00.check_spec_freeze(log)
    run_phase00.check_prereg_inventory(log)
    run_phase00.check_theorem_ledger(log)
    assert all(c["status"] == "PASS" for c in log)


def test_downstream_docs_present():
    """Atlas + downstream theorem docs/reviews recorded by hash."""
    log = []
    run_phase00.check_downstream_docs(PARENT, log)
    assert log[0]["status"] == "PASS"


def test_survivor_binding():
    """PHASE 01.1: MSTC-0002 fields bound across 3 sealed records."""
    log = []
    run_phase01.check_survivor_binding(PARENT, log)
    assert log[0]["status"] == "PASS"


def test_set_hash_agreement():
    """PHASE 01.1: one set hash in FINAL_RESULT, h3t_state, candidate-set."""
    log = []
    run_phase01.check_set_hash_agreement(PARENT, log)
    assert log[0]["status"] == "PASS"


def test_fresh_history():
    """PHASE 01.2: reveal verdicts match kills; commitment intact; no unlock."""
    log = []
    run_phase01.check_fresh_history(PARENT, log)
    run_phase01.check_no_reunlock(log)
    assert all(c["status"] == "PASS" for c in log)


def test_blocker_dag():
    """PHASE 01.3: 10-node critical set re-derived; ledger agrees."""
    log = []
    run_phase01.check_blocker_dag(PARENT, log)
    assert log[0]["status"] == "PASS"
