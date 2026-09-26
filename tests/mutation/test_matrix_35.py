"""Theorem x operator mutation matrix (WP-2 exit: 35/35 KILLED + T099/T100).

Frozen rule (dual_obligation_policy.yaml): every preregistered operator
exercised at least once per theorem. Seven operators x five WP-2 nodes.
Each cell applies the operator to a scratch core copy and runs that NODE's
own battery (BATTERIES[node]): mechanism checks exact to the frozen theorem
plus frozen-core/binding/integrity checks for orthogonal faults. A control
test proves zero false positives on the frozen core. Scratch copies only;
frozen source untouched.
"""
import sys
from collections import Counter
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


def _vine(spy, n, left=False):
    t = spy.LEAF
    for k in (range(n, 0, -1) if left else range(1, n + 1)):
        t = _ins(spy, t, k)
    return t


def _ins(spy, t, k):
    if t[0] == "leaf":
        return spy.node(k, spy.LEAF, spy.LEAF)
    _, kk, l, r = t
    if k < kk:
        return spy.node(kk, _ins(spy, l, k), r)
    return spy.node(kk, l, _ins(spy, r, k))


def _check_growth(mod, spy):
    """MST0-08U mechanism: per-event T7 growth <= 6."""
    t = spy.node(1, spy.LEAF, spy.node(2, spy.LEAF, spy.node(3, spy.LEAF, spy.LEAF)))
    _t2, evs = spy.splay_trace(t, 3)
    for _case, lo, hi in evs:
        E2 = mod.t7inject(([], 0), True, lo, hi, 3, 3, mod.K_FROZEN)
        if len(E2[0]) > 6:
            return True
    return False


def _check_fold_bound(mod, spy):
    """MST0-09 mechanism: per-access growth <= 6 * event count."""
    t = _vine(spy, 7)
    for x in (1, 4, 7):
        E = ([], 0)
        E2, _A2, _a = mod.replay_access_A(E, t, "KEEP", x, 7)
        _t2, evs = spy.splay_trace(t, x)
        if M_energy(E2) - M_energy(E) > 6 * len(evs):
            return True
    return False


def M_energy(E):
    return sum(1 for c in E[0] if c[0] in ("LATENT", "ACTIVE"))


def _check_clauses(mod, spy):
    """MST0-11 mechanism: six preservation clauses on sampled replay steps."""
    E = ([(mod.LATENT, 1, 2, True), (mod.SPENT, 3, 4, False)], 0)
    trees = [(7, _vine(spy, 7), [1, 4, 7]),
             (7, spy.node(4, spy.node(2, spy.node(1, spy.LEAF, spy.LEAF),
                                     spy.node(3, spy.LEAF, spy.LEAF)),
                          spy.node(6, spy.node(5, spy.LEAF, spy.LEAF),
                                   spy.node(7, spy.LEAF, spy.LEAF))), [4]),
             (3, _vine(spy, 3), [3])]
    for n, t, xs in trees:
        for x in xs:
            _t2, evs = spy.splay_trace(t, x)
            for _case, lo, hi in evs:
                E1 = mod.t7inject(E, True, lo, hi, x, n, mod.K_FROZEN)
                E2 = mod.t5activate(E1, "KEEP")
                L, L1, L2 = E[0], E1[0], E2[0]
                if M_energy((L2, 0)) != M_energy((L, 0)) + (len(L1) - len(L)):
                    return True
                new = L2[len(L):]
                if any(c[0] not in (mod.LATENT, mod.ACTIVE) for c in new):
                    return True
                if Counter([c for c in L2 if c[0] == mod.SPENT]) - Counter(
                        [c for c in L if c[0] == mod.SPENT]):
                    return True
                if any(not (lo <= c[1] and c[2] <= hi) for c in new):
                    return True
                E = E2
    return False


def _check_residual(mod, spy):
    """MST0-13 mechanism: growth - 6*cost_A <= 0 on samples."""
    for n, xs in ((7, [1, 4, 7]), (3, [1, 3])):
        t = _vine(spy, n)
        for x in xs:
            E = ([], 0)
            E2, _A2, a = mod.replay_access_A(E, t, "DELETE", x, n)
            growth = M_energy(E2) - M_energy(E)
            if growth - 6 * a > 0:
                return True
    return False


def _check_nospent_A(mod, spy):
    """MST0-13 integrity: DELETE-side replay never creates SPENT."""
    t = _vine(spy, 7)
    for x in (1, 4, 7):
        E = ([], 0)
        E2, _A2, _a = mod.replay_access_A(E, t, "DELETE", x, 7)
        if any(c[0] == mod.SPENT for c in E2[0]):
            return True
    return False


def _check_literals(mod, spy):
    """MST0-22 mechanism: C=2/K=6 literals + regret linkage + uniformity."""
    _ = spy
    if mod.C_FROZEN != 2 or mod.K_FROZEN != 6:
        return True
    if mod.required(5, 1) != 3 or mod.required(3, 5) != 0:
        return True
    E = ([], 0)
    E2 = mod.t7inject(E, True, 1, 4, 2, 9, mod.K_FROZEN)
    if len(E2[0]) - len(E[0]) > mod.K_FROZEN:
        return True
    return False


def _check_binding(mod, spy):
    """Frozen-core/binding/integrity requirements shared by all nodes:
    cost convention, predicate firing both modes, trace labels, support shape,
    K literal binding, required() values incl. the zero floor. Orthogonal
    faults die here; mechanism faults die in the node batteries above."""
    t = spy.node(1, spy.LEAF, spy.node(2, spy.LEAF, spy.node(3, spy.LEAF, spy.LEAF)))
    if spy.splay_cost(t, 3) != spy.depth(t, 3) + 1:
        return True
    E = [(mod.LATENT, 1, 2, True)]
    if mod.t5activate((E, 0), "DELETE")[0] == E:
        return True
    if mod.t5activate((E, 0), "KEEP")[0] == E:
        return True
    tl = spy.node(3, spy.node(2, spy.node(1, spy.LEAF, spy.LEAF), spy.LEAF), spy.LEAF)
    _t3, evs3 = spy.splay_trace(tl, 1)
    if [c for c, _lo, _hi in evs3] != ["LL"]:
        return True
    _t2, evs = spy.splay_trace(t, 3)
    for _case, lo, hi in evs:
        for s in mod.sites(lo, hi, 3, 3):
            if not (lo <= s[0] and s[1] <= hi):
                return True
    if mod.K_FROZEN != 6 or mod.C_FROZEN != 2:
        return True
    if mod.required(5, 1) != 3 or mod.required(3, 5) != 0:
        return True
    return False


def _check_event_growth(mod, spy, trees_xs):
    """Supporting injection integrity for 11/13 (their bounds need per-event ≤ 6)."""
    for t, xs, nkeys in trees_xs:
        for x in xs:
            _t2, evs = spy.splay_trace(t, x)
            for _case, lo, hi in evs:
                E2 = mod.t7inject(([], 0), True, lo, hi, x, nkeys, mod.K_FROZEN)
                if len(E2[0]) > 6:
                    return True
    return False


def battery_08u(mod, spy):
    """MST0-08U: per-event growth bound + K binding + replay composition."""
    if _check_growth(mod, spy):
        return True
    if mod.K_FROZEN != 6:
        return True
    E = ([], 0)
    t = _vine(spy, 7)
    _t2, evs = spy.splay_trace(t, 4)
    E2 = E
    for ev in evs:
        E2 = mod.replay_step(E2, True, "KEEP", ev, 4, 7)
    if M_energy(E2) - M_energy(E) > 6 * len(evs):
        return True
    return _check_binding(mod, spy)


def battery_09(mod, spy):
    """MST0-09: per-access fold bound + support containment + energy form."""
    if _check_fold_bound(mod, spy):
        return True
    if M_energy(([], 0)) != 0:
        return True
    t = _vine(spy, 7)
    _t2, evs = spy.splay_trace(t, 7)
    for _case, lo, hi in evs:
        for s in mod.sites(lo, hi, 7, 7):
            if not (lo <= s[0] and s[1] <= hi):
                return True
    return _check_binding(mod, spy)


def battery_11(mod, spy):
    """MST0-11: six-clause preservation + T5 energy conservation + injection
    integrity (per-event growth, which C1/C4 accounting needs)."""
    if _check_clauses(mod, spy):
        return True
    E = ([(mod.LATENT, 1, 2, True)], 5)
    E2 = mod.t5activate(E, "KEEP")
    if M_energy(E2) != M_energy(E):
        return True
    if _check_event_growth(mod, spy, [(_vine(spy, 7), [1, 4, 7], 7)]):
        return True
    return _check_binding(mod, spy)


def battery_13(mod, spy):
    """MST0-13: residual bound + cost convention + DELETE-side T6 absence +
    injection integrity (per-event growth feeds the 6*cost argument)."""
    if _check_residual(mod, spy):
        return True
    if _check_nospent_A(mod, spy):
        return True
    t = _vine(spy, 7)
    if spy.splay_cost(t, 1) != spy.depth(t, 1) + 1:
        return True
    if _check_event_growth(mod, spy, [(t, [1, 4, 7], 7)]):
        return True
    return _check_binding(mod, spy)


def battery_22(mod, spy):
    """MST0-22: literals + regret linkage + uniformity + predicate."""
    if _check_literals(mod, spy):
        return True
    E = ([(mod.LATENT, 1, 2, True)], 0)
    if mod.t5activate(E, "KEEP")[0] == E[0] or mod.t5activate(E, "DELETE")[0] == E[0]:
        return True
    return _check_binding(mod, spy)


BATTERIES = {
    "MST0-08U": battery_08u,
    "MST0-09": battery_09,
    "MST0-11": battery_11,
    "MST0-13": battery_13,
    "MST0-22": battery_22,
}


def test_battery_clean():
    """Control: all five batteries silent on the frozen core."""
    import shutil
    import tempfile
    tmp = Path(tempfile.mkdtemp())
    shutil.copytree(IMPL / "python/inherited", tmp / "core")
    try:
        mod, spy = _load(tmp)
        for node, bat in BATTERIES.items():
            assert bat(mod, spy) is False, f"false positive: {node}"
    finally:
        _cleanup(tmp)


@pytest.mark.parametrize("node", NODES)
@pytest.mark.parametrize("op,mut", OPERATORS)
def test_matrix_cell(tmp_path, node, op, mut):
    """Cell (node, operator): mutant KILLED by that node's own battery."""
    import shutil
    core = tmp_path / "core"
    shutil.copytree(IMPL / "python/inherited", core)
    mut(core)
    mod, spy = _load(tmp_path)
    try:
        fired = BATTERIES[node](mod, spy)
    finally:
        _cleanup(tmp_path)
    assert fired is True, f"mutant survived: {node} x {op}"
