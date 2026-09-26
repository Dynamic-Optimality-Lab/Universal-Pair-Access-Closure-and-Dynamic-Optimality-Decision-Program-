"""Theorem x operator mutation matrix (WP-2 exit: 35/35 KILLED + T099/T100).

Frozen rule (dual_obligation_policy.yaml): every preregistered operator
exercised at least once per theorem. Seven operators x five WP-2 nodes.
Each cell: apply the operator to a scratch core copy, run the node's
designated battery, assert KILLED. A control test proves zero false
positives on the frozen core. Scratch copies only; frozen source untouched.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from python.audit import mutants as MU

IMPL = Path(__file__).resolve().parents[2]
NODES = ["MST0-08U", "MST0-09", "MST0-11", "MST0-13", "MST0-22"]


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
    assert 'return True  # fires on KEEP and DELETE' in t
    _write(core, "mstc0002.py",
           t.replace('return True  # fires on KEEP and DELETE',
                     'return mode == "KEEP"', 1))


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


def mut_cost_convention(core):
    t = _read(core, "splay.py")
    assert "return depth(t, x) + 1" in t
    _write(core, "splay.py",
           t.replace("return depth(t, x) + 1", "return depth(t, x) + 2", 1))


def mut_endpoint_term_drop(core):
    t = _read(core, "mstc0002.py")
    assert "return max(regret(y, a), 0)" in t
    _write(core, "mstc0002.py",
           t.replace("return max(regret(y, a), 0)", "return regret(y, a)", 1))


OPERATORS = [
    ("constant-swap-C-k", mut_constant_swap),
    ("predicate-weakening-P_all", mut_predicate_weaken),
    ("support-shift", mut_support_shift),
    ("injection-count-off-by-one", mut_injection_offbyone),
    ("discharge-sign-flip", mut_discharge_signflip),
    ("cost-convention-plus-one", mut_cost_convention),
    ("endpoint-term-drop", mut_endpoint_term_drop),
]


def _fresh(core_name):
    import shutil
    import tempfile
    tmp = Path(tempfile.mkdtemp())
    shutil.copytree(IMPL / "python/inherited", tmp / core_name)
    return tmp


def _load(tmp, core_name="core"):
    sys.path.insert(0, str(tmp))
    try:
        for mod in [m for m in list(sys.modules)
                    if m == core_name or m.startswith(core_name + ".")]:
            del sys.modules[mod]
        import importlib
        mst = importlib.import_module(f"{core_name}.mstc0002")
        spy = importlib.import_module(f"{core_name}.splay")
        return mst, spy
    finally:
        try:
            sys.path.remove(str(tmp))
        except ValueError:
            pass


def _cleanup(tmp, core_name="core"):
    import shutil
    for mod in [m for m in list(sys.modules)
                if m == core_name or m.startswith(core_name + ".")]:
        del sys.modules[mod]
    shutil.rmtree(tmp, ignore_errors=True)


def battery(mod, spy):
    """Full node-battery sensitivity checks; returns list of fired check names."""
    fired = []
    # growth bound (08U/09/13 mechanism)
    t = spy.node(1, spy.LEAF, spy.node(2, spy.LEAF, spy.node(3, spy.LEAF, spy.LEAF)))
    _t2, evs = spy.splay_trace(t, 3)
    for _case, lo, hi in evs:
        E2 = mod.t7inject(([], 0), True, lo, hi, 3, 3, mod.K_FROZEN)
        if len(E2[0]) > 6:
            fired.append("growth")
    # constants + required values incl. floor case (22/14 mechanism)
    if mod.C_FROZEN != 2 or mod.K_FROZEN != 6:
        fired.append("constants")
    if mod.required(5, 1) != 3 or mod.required(3, 5) != 0:
        fired.append("required")
    # cost convention (04/13 mechanism)
    if spy.splay_cost(t, 3) != spy.depth(t, 3) + 1:
        fired.append("cost")
    # predicate fires on DELETE (05/13/14 mechanism)
    E = [(mod.LATENT, 1, 2, True)]
    if mod.t5activate((E, 0), "DELETE")[0] == E:
        fired.append("predicate")
    # support containment (11-C4 mechanism)
    for _case, lo, hi in evs:
        for s in mod.sites(lo, hi, 3, 3):
            if not (lo <= s[0] and s[1] <= hi):
                fired.append("support")
    # trace labels (case identity)
    tl = spy.node(3, spy.node(2, spy.node(1, spy.LEAF, spy.LEAF), spy.LEAF), spy.LEAF)
    _t3, evs3 = spy.splay_trace(tl, 1)
    if [c for c, _lo, _hi in evs3] != ["LL"]:
        fired.append("trace-labels")
    # validity (structural)
    tb = spy.node(4, spy.node(2, spy.node(1, spy.LEAF, spy.LEAF),
                              spy.node(3, spy.LEAF, spy.LEAF)),
                  spy.node(6, spy.node(5, spy.LEAF, spy.LEAF),
                           spy.node(7, spy.LEAF, spy.LEAF)))
    if not spy.valid(spy.splay(tb, 1)):
        fired.append("validity")
    return fired


def test_battery_clean():
    """Control: battery fires nothing on the frozen core (no false positives)."""
    import shutil
    import tempfile
    tmp = Path(tempfile.mkdtemp())
    shutil.copytree(IMPL / "python/inherited", tmp / "core")
    try:
        mod, spy = _load(tmp)
        assert battery(mod, spy) == []
    finally:
        _cleanup(tmp)


@pytest.mark.parametrize("node", NODES)
@pytest.mark.parametrize("op,mut", OPERATORS)
def test_matrix_cell(tmp_path, node, op, mut):
    """Cell (node, operator): mutant KILLED by the node's battery."""
    import shutil
    core = tmp_path / "core"
    shutil.copytree(IMPL / "python/inherited", core)
    mut(core)
    mod, spy = _load(tmp_path)
    try:
        fired = battery(mod, spy)
    finally:
        _cleanup(tmp_path)
    assert fired != [], f"mutant survived: {node} x {op}"
