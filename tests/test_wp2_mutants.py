"""WP-2 mutant tests: every proof mutant must be rejected (T099/T100).

Sensitivity control (known-killed): weakened k=1 injection MUST expose
positive residual on burst histories. Structural mutants (dropped case,
T5-mints-SPENT) must fail their respective gates.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from python.audit import mutants as MU
from python.inherited import mstc0002 as M
from python.inherited import pair_access as P


BURDEN_HISTORY = [('KEEP', 5), ('KEEP', 16), ('KEEP', 3), ('KEEP', 16),
                    ('KEEP', 8), ('KEEP', 16), ('KEEP', 16), ('KEEP', 5),
                    ('KEEP', 5), ('DELETE', 13), ('DELETE', 3), ('KEEP', 2),
                    ('KEEP', 1), ('DELETE', 9), ('KEEP', 13), ('DELETE', 14),
                    ('KEEP', 15), ('DELETE', 5), ('DELETE', 4), ('KEEP', 16),
                    ('KEEP', 14), ('DELETE', 10), ('KEEP', 13), ('KEEP', 14)]


def _burst_events():
    """DELETE-burst-then-KEEP history stressing injection rate."""
    run = P.run_paired(16, "spine-left",
                       [("DELETE", x) for x in range(1, 9)] + [("KEEP", 9)] * 4)
    return run["events"]


def _burden_events():
    """Deterministic history with real repayment burden (base pays > 0)."""
    run = P.run_paired(16, "balanced", BURDEN_HISTORY)
    return run["events"]


K1_KILLER_HISTORY = ([("DELETE", x) for x in range(1, 33)] +
                     [("KEEP", 32 - (i % 16)) for i in range(32)])


def test_relax_k_to_1_killed():
    """Known-killed control: k=1 exposes residual where k=6 survives."""
    run = P.run_paired(32, "spine-right", K1_KILLER_HISTORY)
    assert M.evaluate(run["events"], k=6)["max_residual"] == 0
    assert MU.evaluate_relaxed_k(run["events"])["max_residual"] > 0


def test_t5_mints_spent_starves():
    """Mutant t5-mints-spent: repayment starves on real burden (residual > 0)."""
    evs = _burden_events()
    base = M.evaluate(evs)
    assert base["paid_total"] > 0 and base["max_residual"] == 0
    mut = MU.evaluate_t5_mints_spent(evs)
    assert mut["max_residual"] > 0


def test_drop_case_flagged():
    """Mutant drop-case: each dropped primitive is flagged missing."""
    covered = ["ROOT", "ZIG-left", "ZIG-right", "LL", "RR", "LR", "RL"]
    for drop in covered:
        assert drop in MU.check_coverage_with_drop(covered, drop)


def test_mutant_registry_complete():
    """Registry lists all six preregistered operators."""
    assert sorted(MU.MUTANTS) == sorted(["drop-ROOT", "drop-ZIG", "drop-LL",
                                         "t5-mints-spent", "support-no-validation",
                                         "relax-k-to-1"])
    assert MU.known_killed_control()["must_reject"] is True
