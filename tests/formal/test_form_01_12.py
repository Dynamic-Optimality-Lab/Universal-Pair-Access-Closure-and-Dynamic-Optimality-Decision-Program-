"""FORM-01..FORM-12 named tests (exact normative meanings, v0.4 spec s5/WorkPlan s4).

FORM-01 Lean toolchain exact | FORM-02 no sorry/admit | FORM-03 undeclared axiom
scan clean | FORM-04 Splay case semantics agreement | FORM-05 cost depth+1 binding |
FORM-06 Pair-Access KEEP binding | FORM-07 Pair-Access DELETE binding |
FORM-08 MSTC-0002 field-by-field binding | FORM-09 theorem statement hash binding |
FORM-10 dependency hash binding | FORM-11 formal mutant rejected |
FORM-12 markdown/formal statement equivalence audit.
Fail-closed: missing pinned toolchain fails FORM-01 (and dependent tests).
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

IMPL = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(IMPL))
LEAN_HOME = Path(os.environ.get("LEAN_HOME",
    r"C:\Users\SAIFMA~1\AppData\Local\Temp\opencode\lean-4.21.0\lean-4.21.0-windows"))
LAKE = str(LEAN_HOME / "bin" / "lake.exe")
LEAN = str(LEAN_HOME / "bin" / "lean.exe")
PIN = "leanprover/lean4:v4.21.0"


def run(cmd, cwd=IMPL, timeout=600):
    env = dict(os.environ)
    env["Path"] = str(LEAN_HOME / "bin") + ";" + env.get("Path", "")
    return subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True,
                          timeout=timeout, env=env)


def test_FORM_01_toolchain_exact():
    assert Path(LAKE).exists(), "pinned toolchain absent"
    r = run([LEAN, "--version"])
    assert "4.21.0" in r.stdout, r.stdout
    assert (IMPL / "lean-toolchain").read_text(encoding="utf-8").splitlines()[0] == PIN


def test_FORM_02_no_sorry_admit():
    r = run([LAKE, "build"])
    assert r.returncode == 0, r.stderr[-2000:]
    hits = []
    for f in list((IMPL / "lean").rglob("*.lean")):
        for i, ln in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            s = ln.strip()
            if s.startswith("sorry") or s.startswith("admit") or ":= sorry" in s:
                hits.append(f"{f.name}:{i}")
    assert not hits, hits


def test_FORM_03_axiom_scan_clean():
    ax = (IMPL / "artifacts/v04/formal/AXIOMS_CLOSURE.txt").read_text(encoding="utf-8")
    assert "sorryAx" not in ax
    assert ax.count("does not depend on any axioms") == 14, ax
    for f in list((IMPL / "lean").rglob("*.lean")):
        assert not re.search(r"^\s*(opaque|axiom)\b", f.read_text(encoding="utf-8"), re.M), f


def _agree_outputs():
    agree = IMPL / ".lake/build/bin/agree.exe"
    assert agree.exists(), "agree exe not built"
    env = dict(os.environ)
    env["Path"] = str(LEAN_HOME / "bin") + ";" + env.get("Path", "")
    r = subprocess.run([str(agree)], capture_output=True, timeout=300, env=env, cwd=str(IMPL))
    assert r.returncode == 0
    lean_lines = r.stdout.decode("utf-8").splitlines()
    p = subprocess.run([sys.executable, str(IMPL / "tests/formal/agree_py.py")],
                       capture_output=True, timeout=300, cwd=str(IMPL))
    assert p.returncode == 0
    py_lines = p.stdout.decode("utf-8").splitlines()
    return lean_lines, py_lines


def test_FORM_04_splay_case_agreement():
    lean_lines, py_lines = _agree_outputs()
    lt = [l for l in lean_lines if l.startswith("TRACE ")]
    pt = [l for l in py_lines if l.startswith("TRACE ")]
    assert lt and lt == pt


def test_FORM_05_cost_binding():
    lean_lines, py_lines = _agree_outputs()
    lc = [l for l in lean_lines if l.startswith("COST ") or l.startswith("PATH ")]
    pc = [l for l in py_lines if l.startswith("COST ") or l.startswith("PATH ")]
    assert lc and lc == pc


def test_FORM_06_keep_binding():
    lean_lines, py_lines = _agree_outputs()
    assert [l for l in lean_lines if l.startswith("LEDGER ")] == \
           [l for l in py_lines if l.startswith("LEDGER ")]


def test_FORM_07_delete_binding():
    from python.inherited import mstc0002 as M
    from python.inherited import splay as S
    t = S.node(1, S.LEAF, S.node(2, S.LEAF, S.node(3, S.LEAF, S.LEAF)))
    E = ([], 0)
    E2, _A2, a = M.replay_access_A(E, t, "DELETE", 3, 3)
    assert a == S.splay_cost(t, 3)
    assert M.energy(E2[0]) - M.energy(E[0]) <= 6 * a


def test_FORM_08_mstc0002_binding():
    m = json.loads((IMPL / "parent/V03_MSTC_0002.json").read_text(encoding="utf-8"))
    from python.inherited import mstc0002 as M
    lean = (IMPL / "lean/Frozen/MSTC0002Defs.lean").read_text(encoding="utf-8")
    assert m["calculus_id"] == "MSTC-0002" and m["injection_rules"][0]["k"] == M.K_FROZEN == 6
    assert m["universal_constant_C"] == M.C_FROZEN == 2
    assert "def C_frozen : Nat := 2" in lean and "def K_frozen : Nat := 6" in lean


def test_FORM_09_statement_hash_binding():
    bf = yaml.safe_load((IMPL / "prereg/theorem_battlefield.yaml").read_text(encoding="utf-8"))
    for n, rec in bf["nodes"].items():
        if n == "MST0-19":
            continue
        live = hashlib.sha256((IMPL / rec["document"]).read_bytes()).hexdigest()
        assert live == rec["document_sha256"], n
        st = next(l[len("- Statement: "):]
                  for l in (IMPL / rec["document"]).read_text(encoding="utf-8").splitlines()
                  if l.startswith("- Statement: "))
        assert hashlib.sha256(st.encode()).hexdigest() == rec["statement_sha256"], n


def test_FORM_10_dependency_binding():
    bf = yaml.safe_load((IMPL / "prereg/theorem_battlefield.yaml").read_text(encoding="utf-8"))
    gm = yaml.safe_load((IMPL / "prereg/theorem_gate_matrix.yaml").read_text(encoding="utf-8"))
    for n in [k for k in bf["nodes"] if k != "MST0-19"]:
        assert bf["nodes"][n].get("prerequisites"), n
        assert gm["gates"][n].get("controls"), n
    lean = (IMPL / "lean/Frozen/Statements.lean").read_text(encoding="utf-8")
    assert "import Frozen.SplayDefs" in lean and "import Frozen.MSTC0002Defs" in lean


def test_FORM_11_formal_mutant_rejected(tmp_path):
    # Mutate K_frozen 6->7 in a scratch copy; agreement must DIVERGE (caught).
    scratch = tmp_path / "mut"
    (scratch / "lean").mkdir(parents=True)
    for f in ["lakefile.lean", "lean-toolchain", "lake-manifest.json"]:
        shutil.copy(IMPL / f, scratch / f)
    shutil.copytree(IMPL / "lean", scratch / "lean", dirs_exist_ok=True)
    src = scratch / "lean/Frozen/MSTC0002Defs.lean"
    t = src.read_text(encoding="utf-8")
    assert "def K_frozen : Nat := 6" in t
    src.write_text(t.replace("def K_frozen : Nat := 6", "def K_frozen : Nat := 7"), encoding="utf-8")
    env = dict(os.environ)
    env["Path"] = str(LEAN_HOME / "bin") + ";" + env.get("Path", "")
    b = subprocess.run([LAKE, "build", "agree"], cwd=str(scratch),
                       capture_output=True, text=True, timeout=600, env=env)
    assert b.returncode == 0, "mutant must stay well-typed (rejection via agreement, not compile)"
    exe = scratch / ".lake/build/bin/agree.exe"
    r = subprocess.run([str(exe)], capture_output=True, timeout=300, env=env, cwd=str(scratch))
    mutant_lines = r.stdout.decode("utf-8").splitlines()
    p = subprocess.run([sys.executable, str(IMPL / "tests/formal/agree_py.py")],
                       capture_output=True, timeout=300, cwd=str(IMPL))
    assert mutant_lines != p.stdout.decode("utf-8").splitlines(), \
        "FORM-11 FAIL: formal mutant NOT caught by agreement"


def test_FORM_12_markdown_formal_equivalence():
    bf = yaml.safe_load((IMPL / "prereg/theorem_battlefield.yaml").read_text(encoding="utf-8"))
    lean = (IMPL / "lean/Frozen/Statements.lean").read_text(encoding="utf-8")
    bodies = dict(re.findall(r"def (MST0_\w+) : Prop :=\n((?:  .*\n)+)", lean))
    TOK = [("∀", "forall"), ("∃", "exists"), ("≤", "<="), ("≥", ">="),
           ("→", "->"), ("∧", "/\\"), ("∨", "\\/"), ("¬", "~"),
           ("∈", "in"), ("≠", "!="), ("×", "*")]

    def norm(s):
        s = re.sub(r"\s+", " ", s).strip()
        for a, b in TOK:
            s = s.replace(a, b)
        return s

    for n, rec in bf["nodes"].items():
        if n == "MST0-19":
            continue
        assert norm(bodies["MST0_" + n.replace("MST0-", "")]) == rec["statement"], n
