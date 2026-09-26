"""audit/mutants.py — mutation-runner utility (WP-2, T099/T100 support).

Applies a named semantic-fault operator to a scratch copy of the executable
core, runs a detector callable against the mutant, and reports killed/survived.
Operators mirror the preregistered set (dual_obligation_policy.yaml).
"""
import shutil
import sys
from pathlib import Path

IMPL = Path(__file__).resolve().parents[2]

OPERATORS = ["constant-swap-C-k", "predicate-weakening-P_all", "support-shift",
             "injection-count-off-by-one", "discharge-sign-flip",
             "cost-convention-plus-one", "endpoint-term-drop"]


def run_mutant(operator, mutate_fn, detector_fn, workdir):
    """Copy core to workdir, apply mutate_fn(core_dir), run detector_fn(core_dir).

    detector_fn(core_dir) returns True iff it DETECTS the mutant (bad case
    caught). Returns True iff the mutant was KILLED. Raises on harness error.
    Callers must separately assert detector_fn(unmutated core) is False
    (no false positives on the frozen core).
    """
    core = workdir / "core"
    if core.exists():
        shutil.rmtree(core)
    shutil.copytree(IMPL / "python/inherited", core)
    mutate_fn(core)
    sys.path.insert(0, str(workdir))
    try:
        for mod in [m for m in list(sys.modules) if m == "core" or m.startswith("core.")]:
            del sys.modules[mod]
        killed = bool(detector_fn(core))
    finally:
        try:
            sys.path.remove(str(workdir))
        except ValueError:
            pass
        for mod in [m for m in list(sys.modules) if m == "core" or m.startswith("core.")]:
            del sys.modules[mod]
    if operator not in OPERATORS and not operator.startswith("WP2-"):
        raise ValueError(f"unregistered operator {operator}")
    return killed
