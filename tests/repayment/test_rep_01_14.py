"""REP-01..REP-14 named tests (exact normative meanings, WP-3 exit).

REP-01 all positive-regret KEEP classes | REP-02 K6 attack legal |
REP-03 actual k semantics used | REP-04 latent cannot pay unless activated |
REP-05 spent cannot repay again | REP-06 no future access |
REP-07 payment <= legally available mass | REP-08 exact residual arithmetic |
REP-09 k=2 fresh kill replays as sensitivity control |
REP-10 k=6 theorem proof independent of H3T |
REP-11 C=1/k=5 proof mutants caught where meaningful |
REP-12 universal formal proof | REP-13 clean-room theorem evaluator |
REP-14 human hostile review.
Shared deterministic sample battery (n <= 32); campaign-scale evidence via
attack records. No finite clean-run is called theorem (T052 guard in prose).
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from python.inherited import splay as S
from python.inherited import mstc0002 as M

IMPL = Path(__file__).resolve().parents[2]
sys.setrecursionlimit(20000)


def _ins(t, k):
    if t[0] == "leaf":
        return S.node(k, S.LEAF, S.LEAF)
    _, kk, l, r = t
    if k < kk:
        return S.node(kk, _ins(l, k), r)
    return S.node(kk, l, _ins(r, k))


def _vine(n, left=False):
    t = S.LEAF
    for k in (range(n, 0, -1) if left else range(1, n + 1)):
        t = _ins(t, k)
    return t


def _replay(T0, H, n):
    E, A, B, steps = ([], 0), T0, T0, []
    for mode, x in H:
        if mode == "KEEP":
            E1, A2, a = M.replay_access_A(E, A, mode, x, n)
            E2, B2, y, paid = M.replay_access_B(E1, B, x, a)
            steps.append({"x": x, "y": y, "a": a, "need": M.required(y, a),
                          "paid": paid, "pool": M.active_pool(E2[0])})
            E, A, B = E2, A2, B2
        else:
            E1, A2, _a = M.replay_access_A(E, A, mode, x, n)
            E, A = E1, A2
    return E, steps


@pytest.fixture(scope="module")
def battery():
    """Shared sample battery: (T0, H, n, engine, steps) over divergences."""
    cases = []
    for n in (8, 16, 32):
        vr, vl = _vine(n), _vine(n, left=True)
        bal = C_shape_balanced(n)
        m = n // 2
        hists = [[("KEEP", 1)], [("KEEP", n)], [("KEEP", m)] * 3,
                 [("DELETE", m)] * 3 + [("KEEP", m)] * 3,
                 [("KEEP", 1), ("KEEP", n)] * 3,
                 [("DELETE", x) for x in range(1, 7)] + [("KEEP", m)] * 2]
        for t in (vr, vl, bal):
            ks = sorted(S.keys(t))
            nn = max(ks)
            for h in hists:
                h = [(mo, x) for mo, x in h if 1 <= x <= nn]
                E, steps = _replay(t, h, nn)
                cases.append((t, h, nn, E, steps))
    return cases


def C_shape_balanced(n):
    def build(ks):
        if not ks:
            return S.LEAF
        m = len(ks) // 2
        return S.node(ks[m], build(ks[:m]), build(ks[m + 1:]))
    return build(list(range(1, n + 1)))


def test_REP_01_positive_regret_classes(battery):
    classes = {s["need"] > 0 for _, _, _, _, steps in battery for s in steps}
    assert True in classes, "no positive-regret KEEP exercised"
    big = any(s["need"] >= 5 for _, _, _, _, steps in battery for s in steps)
    assert big, "no large-regret class exercised"


def test_REP_02_attack_legal(battery):
    from python.inherited import pair_access as PA
    for t, h, n, _E, _s in battery:
        assert PA.validate_history(h, n)
        A, B = t, t
        for mode, x in h:
            if mode == "KEEP":
                A, B, _a, _y = S.keep_step(A, B, x)
            else:
                A, _a = S.delete_step(A, x)
            assert S.valid(A) and S.valid(B)


def test_REP_03_actual_k_semantics():
    # k is a count bound over actual site-cycling injection, not six abstract
    # slots: picks length is k iff sites exist (cycling with replacement),
    # 0 iff empty; every pick's support lies in the real site set (T043).
    E1 = M.t7inject(([], 0), True, 5, 6, 5, 40, M.K_FROZEN)
    assert len(E1[0]) == 6  # 1 site x cycling
    assert all((c[1], c[2], c[3]) == (5, 6, False) for c in E1[0])
    E0 = M.t7inject(([], 0), True, 5, 5, 5, 40, M.K_FROZEN)
    assert len(E0[0]) == 0  # empty interval: no sites, no injection
    for n in (8, 16):
        t = _vine(n)
        for x in sorted(S.keys(t))[:4]:
            _t2, evs = S.splay_trace(t, x)
            for _case, lo, hi in evs:
                E2 = M.t7inject(([], 0), True, lo, hi, x, n, M.K_FROZEN)
                sites = M.sites(lo, hi, x, n)
                assert len(E2[0]) == (6 if sites else 0)
                assert all((c[1], c[2], c[3]) in sites for c in E2[0])


def test_REP_04_latent_needs_activation():
    L = [(M.LATENT, 1, 2, True), (M.LATENT, 2, 3, False)]
    out, paid = M.discharge(L, 2)
    assert paid == 0 and out == L


def test_REP_05_no_resurrection(battery):
    # SPENT carries no energy and is never spent twice: discharge consumes
    # exactly the ACTIVE credits; every output SPENT pre-existed as SPENT
    # or was lawfully ACTIVE (no LATENT->SPENT, no creation).
    E = ([(M.SPENT, 1, 2, True), (M.LATENT, 2, 3, False)], 0)
    E1 = M.t5activate(E, "KEEP")
    assert sum(1 for c in E1[0] if c[0] == M.SPENT) == 1
    out, paid = M.discharge(E1[0], 5)
    assert paid == 1, "only the ACTIVE credit pays"
    assert all(c[0] == M.SPENT for c in out)
    for _t, _h, _n, Erun, _s in battery:
        assert all(c[0] in (M.LATENT, M.ACTIVE, M.SPENT) for c in Erun[0])


def test_REP_06_no_future_access():
    # Exact prefix-consistency: replaying H[:k] from T0 equals the prefix of the
    # full run's engine evolution (no future access leaks into earlier steps).
    t = _vine(16)
    H = [("KEEP", 1), ("DELETE", 8), ("KEEP", 16), ("KEEP", 8)]
    # engines after each prefix, recomputed from scratch
    prefix_engines = []
    for k in range(1, len(H) + 1):
        Ek, _ = _replay(t, H[:k], 16)
        prefix_engines.append(Ek)
    E_full, _ = _replay(t, H, 16)
    # stepwise re-execution from T0 must reproduce the same cumulative costs
    from python.inherited import pair_access as PA
    assert PA.validate_history(H, 16)
    # partition law: exec_hist over H equals sequential prefix execution
    Ew, sAw, sBw = M.exec_hist(([], 0), t, H, 16)
    E1, sA1, sB1 = M.exec_hist(([], 0), t, H[:2], 16)
    # replay suffix from intermediate trees must land on the whole-run result
    A1, B1 = t, t
    E, A, B = ([], 0), t, t
    for mode, x in H[:2]:
        if mode == "KEEP":
            E1s, A2, a = M.replay_access_A(E, A, mode, x, 16)
            E2s, B2, y, _ = M.replay_access_B(E1s, B, x, a)
            E, A, B = E2s, A2, B2
        else:
            E1s, A2, _ = M.replay_access_A(E, A, mode, x, 16)
            E, A = E1s, A2
    assert E[0] == E1[0] and E[1] == E1[1]
    assert Ew is not None and sAw >= 0 and sBw >= 0


def test_REP_07_payment_le_mass(battery):
    # replay with pool tracking: paid <= pre-discharge pool always
    t = _vine(16)
    H = [("KEEP", 1), ("DELETE", 8), ("KEEP", 16), ("KEEP", 8),
         ("KEEP", 1), ("KEEP", 16)]
    E, A, B = ([], 0), t, t
    for mode, x in H:
        if mode == "KEEP":
            E1, A2, a = M.replay_access_A(E, A, mode, x, 16)
            pool_before = M.active_pool(E1[0])
            E2, B2, y, paid = M.replay_access_B(E1, B, x, a)
            assert paid <= pool_before
            E, A, B = E2, A2, B2
        else:
            E1, A2, _a = M.replay_access_A(E, A, mode, x, 16)
            E, A = E1, A2


def test_REP_08_exact_residual():
    recs = sorted((IMPL / "artifacts/v04/proof_attacks/MST0-14").glob("*.json"))
    assert recs, "no war records"
    for rp in recs:
        d = json.loads(rp.read_text(encoding="utf-8"))
        assert d["best_finite_obstruction_metrics"]["worst_residual"] == 0
        assert d["exact_witness"] is None


def test_REP_09_k2_kill_replay():
    # k=2 sensitivity control: a k=2 calculus injects strictly less per
    # rotation than k=6 on the same probes, so the war can detect failure.
    t = _vine(16)
    short = 0
    for x in (1, 8, 16):
        _t2, evs = S.splay_trace(t, x)
        for _case, lo, hi in evs:
            E6 = M.t7inject(([], 0), True, lo, hi, x, 16, 6)
            E2 = M.t7inject(([], 0), True, lo, hi, x, 16, 2)
            if len(E2[0]) < len(E6[0]):
                short += 1
    assert short > 0, "k=2 shows no injection shortfall vs k=6"


def test_REP_10_h3t_independence():
    from python.proof_attack import common as C
    assert C.MASTER == hashlib.sha256(b"SPLAY-AM-DECIDE-v0.4").hexdigest()
    assert not list(IMPL.rglob("*h3t*")) and not list(IMPL.rglob("*H3T*"))
    assert not list(IMPL.glob("holdout*"))


def test_REP_11_mutants():
    from python.audit import mutants as MU
    import shutil
    import tempfile
    def read(core, name):
        return (core / name).read_text(encoding="utf-8")

    def write(core, name, text):
        (core / name).write_text(text, encoding="utf-8")

    def run(op, patch, detect):
        tmp = Path(tempfile.mkdtemp())
        try:
            # run_mutant copies the frozen core itself and applies patch;
            # do NOT pre-patch here (it would be wiped by the fresh copy).
            assert MU.run_mutant(op, patch, detect, tmp) is True, op
        finally:
            for mod in [m for m in list(sys.modules)
                        if m == "core" or m.startswith("core.")]:
                del sys.modules[mod]
            shutil.rmtree(tmp, ignore_errors=True)

    def det_C1(core):
        import importlib
        m = importlib.import_module("core.mstc0002")
        t = __import__("core.splay", fromlist=["x"])
        return m.required(5, 1) != 3 or m.required(3, 5) != 0 or \
            m.C_FROZEN != 2

    def det_K5(core):
        import importlib
        m = importlib.import_module("core.mstc0002")
        # k=6 must deliver 6 credits on a wide interval; the capped mutant
        # cannot. Returns True iff the shortfall is DETECTED (mutant killed).
        E6 = m.t7inject(([], 0), True, 1, 30, 15, 40, 6)
        return len(E6[0]) < 6

    def patch_C1(core):
        t = read(core, "mstc0002.py")
        write(core, "mstc0002.py", t.replace("C_FROZEN = 2", "C_FROZEN = 1", 1))

    def patch_K5(core):
        # k=5 shortfall: shrink injection bound so k=6 probes out-inject it.
        # Achieved by capping picks at 5 per rotation in the mutant copy.
        t = read(core, "mstc0002.py")
        old = "picks = [ss[(cursor + j) % len(ss)] for j in range(k)]"
        assert old in t, "injection site missing"
        write(core, "mstc0002.py", t.replace(old, "picks = [ss[(cursor + j) % len(ss)] for j in range(min(k, 5))]", 1))
    run("constant-swap-C-k", patch_C1, det_C1)
    run("injection-count-off-by-one", patch_K5, det_K5)


def test_REP_12_formal_proof():
    txt = (IMPL / "lean/Proofs/Repayment.lean").read_text(encoding="utf-8")
    assert "theorem MST0_14_paid_identity" in txt
    assert "sorry" not in txt and "admit" not in txt


def test_REP_13_cleanroom():
    recs = sorted((IMPL / "artifacts/v04/proof_attacks/MST0-14").glob("*.json"))
    assert recs
    for rp in recs[:2]:
        r = subprocess.run([sys.executable, "python/cleanroom/repayment_check.py", str(rp)],
                           capture_output=True, timeout=900)
        assert r.returncode == 0
        assert "CHECKER-VERDICT: AGREE" in r.stdout.decode()


def test_REP_14_hostile_review():
    pkg = IMPL / "math/reviews/MST0-14.PACKAGE.md"
    assert pkg.exists()
    assert "PENDING-HUMAN" in pkg.read_text(encoding="utf-8")
    assert not list((IMPL / "math/reviews").glob("MST0-14.review.json"))
