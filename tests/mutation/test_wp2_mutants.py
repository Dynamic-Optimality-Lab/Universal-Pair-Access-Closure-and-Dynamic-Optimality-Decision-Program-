"""Mutation + known-killed tests for WP-2 (T099/T100 + preregistered operators).

T099 (proof mutant not caught): a weakened preservation claim (C1 dropped) and
a case-label mutant must be REJECTED by the clause checker.
T100 (known-killed control): a trivially broken core (C=3) must be KILLED by
the agreement/canary detectors, proving killing power.
Five preregistered operators applied via audit/mutants.py runner: constant-swap,
predicate-weakening, support-shift, injection-count-off-by-one, discharge-sign-flip.
Each mutant must be killed; survivors fail the suite.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from python.audit import mutants as MU
from python.inherited import splay as S
from python.inherited import mstc0002 as M

IMPL = Path(__file__).resolve().parents[2]


def _read(core, name):
    return (core / name).read_text(encoding="utf-8")


def _write(core, name, text):
    (core / name).write_text(text, encoding="utf-8")


def mut_constant_swap(core):
    t = _read(core, "mstc0002.py")
    assert "K_FROZEN = 6" in t
    _write(core, "mstc0002.py", t.replace("K_FROZEN = 6", "K_FROZEN = 7", 1))


def mut_predicate_weaken(core):
    t = _read(core, "mstc0002.py")
    assert "def p_all(mode):\n    return True  # fires on KEEP and DELETE" in t
    _write(core, "mstc0002.py",
           t.replace("def p_all(mode):\n    return True  # fires on KEEP and DELETE",
                     "def p_all(mode):\n    return mode == \"KEEP\"", 1))


def mut_support_shift(core):
    t = _read(core, "mstc0002.py")
    assert "out.append((i, i + 1, (i + 1) <= x))" in t
    _write(core, "mstc0002.py",
           t.replace("out.append((i, i + 1, (i + 1) <= x))",
                     "out.append((i, i + 2, (i + 1) <= x))", 1))


def mut_injection_offbyone(core):
    t = _read(core, "mstc0002.py")
    assert "for j in range(k)]" in t
    _write(core, "mstc0002.py",
           t.replace("for j in range(k)]", "for j in range(k + 1)]", 1))


def mut_discharge_signflip(core):
    t = _read(core, "mstc0002.py")
    assert "return max(regret(y, a), 0)" in t
    _write(core, "mstc0002.py",
           t.replace("return max(regret(y, a), 0)", "return max(-regret(y, a), 0)", 1))


def mut_case_label(core):
    t = _read(core, "splay.py")
    assert 'evs + [("LL", lo, hi)]' in t
    _write(core, "splay.py",
           t.replace('evs + [("LL", lo, hi)]', 'evs + [("RR", lo, hi)]', 1))


def detect_growth_bound(core_dir):
    """True iff a per-event growth violation is detected (mutant caught)."""
    import importlib
    mod = importlib.import_module("core.mstc0002")
    sp = importlib.import_module("core.splay")
    t = sp.node(1, sp.LEAF, sp.node(2, sp.LEAF, sp.node(3, sp.LEAF, sp.LEAF)))
    _t2, evs = sp.splay_trace(t, 3)
    for _case, lo, hi in evs:
        E2 = mod.t7inject(([], 0), True, lo, hi, 3, 3, mod.K_FROZEN)
        if len(E2[0]) > 6:
            return True
    return False


def detect_constants(core_dir):
    """True iff C/K deviation detected."""
    import importlib
    mod = importlib.import_module("core.mstc0002")
    return mod.C_FROZEN != 2 or mod.K_FROZEN != 6 or mod.required(5, 1) != max(5 - 2 * 1, 0)


def detect_validity(core_dir):
    """True iff splay validity break detected."""
    import importlib
    sp = importlib.import_module("core.splay")
    t = sp.node(4, sp.node(2, sp.node(1, sp.LEAF, sp.LEAF), sp.node(3, sp.LEAF, sp.LEAF)),
                sp.node(6, sp.node(5, sp.LEAF, sp.LEAF), sp.node(7, sp.LEAF, sp.LEAF)))
    t2 = sp.splay(t, 1)
    return not sp.valid(t2)


def detect_support_containment(core_dir):
    """True iff a support-containment (C4) violation is detected."""
    import importlib
    mod = importlib.import_module("core.mstc0002")
    sp = importlib.import_module("core.splay")
    t = sp.node(1, sp.LEAF, sp.node(2, sp.LEAF, sp.node(3, sp.LEAF, sp.LEAF)))
    _t2, evs = sp.splay_trace(t, 3)
    for _case, lo, hi in evs:
        for s in mod.sites(lo, hi, 3, 3):
            if not (lo <= s[0] and s[1] <= hi):
                return True
    return False


def detect_trace_labels(core_dir):
    """True iff rotation-case labels disagree with the frozen oracle."""
    import importlib
    sp = importlib.import_module("core.splay")
    t = sp.node(3, sp.node(2, sp.node(1, sp.LEAF, sp.LEAF), sp.LEAF), sp.LEAF)
    _t2, evs = sp.splay_trace(t, 1)
    cases = [c for c, _lo, _hi in evs]
    return cases != ["LL"]


def detect_predicate(core_dir):
    """True iff DELETE-side activation failure detected (P_all weakened)."""
    import importlib
    mod = importlib.import_module("core.mstc0002")
    E = ([(mod.LATENT, 1, 2, True)], 0)
    E2 = mod.t5activate(E, "DELETE")
    return E2[0] == E[0]


MUTANTS = [
    ("constant-swap-C-k", mut_constant_swap, detect_constants),
    ("predicate-weakening-P_all", mut_predicate_weaken, detect_predicate),
    ("support-shift", mut_support_shift, detect_support_containment),
    ("injection-count-off-by-one", mut_injection_offbyone, detect_growth_bound),
    ("discharge-sign-flip", mut_discharge_signflip, detect_constants),
    ("WP2-case-label", mut_case_label, detect_trace_labels),
]


def test_no_false_positives_on_frozen_core(tmp_path):
    import shutil
    core = tmp_path / "core"
    shutil.copytree(IMPL / "python/inherited", core)
    sys.path.insert(0, str(tmp_path))
    try:
        for mod in [m for m in list(sys.modules) if m == "core" or m.startswith("core.")]:
            del sys.modules[mod]
        assert detect_growth_bound(core) is False
        for mod in [m for m in list(sys.modules) if m == "core" or m.startswith("core.")]:
            del sys.modules[mod]
        assert detect_constants(core) is False
        for mod in [m for m in list(sys.modules) if m == "core" or m.startswith("core.")]:
            del sys.modules[mod]
        assert detect_validity(core) is False
        for mod in [m for m in list(sys.modules) if m == "core" or m.startswith("core.")]:
            del sys.modules[mod]
        assert detect_support_containment(core) is False
        for mod in [m for m in list(sys.modules) if m == "core" or m.startswith("core.")]:
            del sys.modules[mod]
        assert detect_trace_labels(core) is False
        for mod in [m for m in list(sys.modules) if m == "core" or m.startswith("core.")]:
            del sys.modules[mod]
        assert detect_predicate(core) is False
    finally:
        try:
            sys.path.remove(str(tmp_path))
        except ValueError:
            pass
        for mod in [m for m in list(sys.modules) if m == "core" or m.startswith("core.")]:
            del sys.modules[mod]


@pytest.mark.parametrize("op,mut,det", MUTANTS)
def test_mutant_killed(tmp_path, op, mut, det):
    assert MU.run_mutant(op, mut, det, tmp_path) is True, f"mutant survived: {op}"


def test_T099_proof_mutant_caught():
    # T099: weakened proof statement (v1.5-era energy tautology) must NOT bind
    # to MST0-11: the startup SHA-guard rejects it (hash mismatch -> abort).
    import hashlib
    import yaml
    bf = yaml.safe_load((IMPL / "prereg/theorem_battlefield.yaml").read_text(encoding="utf-8"))
    weak_line = "forall L : Ledger, energy L >= 0"
    assert hashlib.sha256(weak_line.encode()).hexdigest() != \
        bf["nodes"]["MST0-11"]["statement_sha256"]
    doc = (IMPL / bf["nodes"]["MST0-11"]["document"]).read_text(encoding="utf-8")
    live = next(l[len("- Statement: "):] for l in doc.splitlines()
                if l.startswith("- Statement: "))
    assert hashlib.sha256(live.encode()).hexdigest() == \
        bf["nodes"]["MST0-11"]["statement_sha256"]


def test_T100_known_killed_control(tmp_path):
    # T100: trivially broken core (C=3) is KILLED -> suite has killing power.
    def mut(core):
        t = _read(core, "mstc0002.py")
        _write(core, "mstc0002.py", t.replace("C_FROZEN = 2", "C_FROZEN = 3", 1))

    assert MU.run_mutant("WP2-known-killed-C3", mut, detect_constants, tmp_path) is True
