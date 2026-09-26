"""PSC implementation conformance tests (STOP-17, WP-2).

Each generator must satisfy the frozen corpus spec: exact interface signature,
corpus seed-derivation formula, canonical sorted outputs, declared size
coverage. Failures block attack execution (run_phase gates on the same checks).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from python.audit import conformance as CF


def test_conformance_locality():
    assert CF.check_module("python.proof_attack.locality_explosion") == []


def test_conformance_preservation():
    assert CF.check_module("python.proof_attack.primitive_exhaust") == []


def test_conformance_boundary():
    assert CF.check_module("python.proof_attack.boundary_torture") == []


def test_conformance_rejects_unknown():
    assert CF.check_module("python.proof_attack.no_such_module") != []
