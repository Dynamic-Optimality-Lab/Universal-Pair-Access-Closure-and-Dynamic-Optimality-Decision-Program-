"""cleanroom/constants_scan.py — dependence/dataflow support scan (WP-2, MST0-22).

Support-only scan (never the proof): backward program slicing from the return
values of the constant/helper outputs (C_FROZEN, K_FROZEN, required,
active_pool, discharge, energy) over python/inherited/mstc0002.py, plus Lean
definition-body dependency check. Flags a forbidden identifier ONLY if it
flows into an output (never mere mention). Writes
artifacts/v04/formal/MST0-22.scan.json and a 24-field run record.
Exit 0 with SCAN-VERDICT line; exit 2 on I/O failure.
"""
import ast
import hashlib
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

IMPL = Path(__file__).resolve().parents[2]
FORBIDDEN = {"n", "sequence_length", "initial_tree", "subsequence_choice",
             "proof_decomposition", "corpus_or_holdout_identity",
             "search_generator_or_seed", "solver_state_or_selected_panel",
             "finite_state_id", "cycle_id"}
ALLOW = {"len", "range", "max", "min", "sum", "sorted", "True", "False", "None",
         "C_FROZEN", "K_FROZEN", "P_all", "LATENT", "ACTIVE", "SPENT",
         "int", "str", "bool", "isinstance", "enumerate", "zip", "abs"}
TARGETS = ["required", "active_pool", "discharge", "energy"]
SCAN_ARTIFACT = IMPL / "artifacts/v04/formal/MST0-22.scan.json"


class Slicer(ast.NodeVisitor):
    """Collect assignment map + return expressions + call graph per function."""

    def __init__(self, tree):
        self.funcs = {}
        self.visit(tree)

    def visit_FunctionDef(self, node):
        params = {a.arg for a in node.args.args} | \
                 {a.arg for a in node.args.kwonlyargs}
        assigns, returns, calls = {}, [], set()
        for sub in ast.walk(node):
            if isinstance(sub, (ast.Assign, ast.AnnAssign)):
                tgt = sub.targets[0] if isinstance(sub, ast.Assign) else sub.target
                for t in ast.walk(tgt):
                    if isinstance(t, ast.Name) and isinstance(t.ctx, ast.Store):
                        assigns.setdefault(t.id, set())
                        for u in ast.walk(sub.value):
                            if isinstance(u, ast.Name) and isinstance(u.ctx, ast.Load):
                                assigns[t.id].add(u.id)
            elif isinstance(sub, ast.For):
                for t in ast.walk(sub.target):
                    if isinstance(t, ast.Name) and isinstance(t.ctx, ast.Store):
                        assigns.setdefault(t.id, set())
                        for u in ast.walk(sub.iter):
                            if isinstance(u, ast.Name) and isinstance(u.ctx, ast.Load):
                                assigns[t.id].add(u.id)
            elif isinstance(sub, ast.Return) and sub.value is not None:
                returns.append(sub.value)
            elif isinstance(sub, ast.Call) and isinstance(sub.func, ast.Name):
                calls.add(sub.func.id)
        self.funcs[node.name] = {"params": params, "assigns": assigns,
                                 "returns": returns, "calls": calls}


def names_of(expr):
    return {u.id for u in ast.walk(expr)
            if isinstance(u, ast.Name) and isinstance(u.ctx, ast.Load)}


def slice_deps(slicer, target, seen=None):
    """Names flowing into target's return values (transitive, over-approx)."""
    seen = seen or set()
    if target in seen or target not in slicer.funcs:
        return set()
    seen.add(target)
    fn = slicer.funcs[target]
    deps = set()
    work = list(fn["params"])
    frontier = set()
    for r in fn["returns"]:
        frontier |= names_of(r)
    while frontier:
        x = frontier.pop()
        if x in deps or x in ALLOW:
            continue
        deps.add(x)
        if x in fn["params"]:
            continue
        if x in fn["assigns"]:
            frontier |= fn["assigns"][x]
        elif x in slicer.funcs:
            deps |= slice_deps(slicer, x, seen)
    return deps


def python_dataflow():
    """Return {target: sorted-dep-list} + forbidden hits."""
    from python.inherited import mstc0002 as _M  # noqa: F401 (pins module identity)
    tree = ast.parse((IMPL / "python/inherited/mstc0002.py").read_text(encoding="utf-8"))
    slicer = Slicer(tree)
    consts = {}
    for name, want in (("C_FROZEN", 2), ("K_FROZEN", 6)):
        assign = next(n for n in ast.walk(tree)
                      if isinstance(n, ast.Assign)
                      and any(isinstance(t, ast.Name) and t.id == name for t in n.targets))
        consts[name] = {"literal": assign.value.value
                        if isinstance(assign.value, ast.Constant) else None,
                        "expected": want}
    out, hits = {"constants": consts}, []
    for t in TARGETS + ["regret", "p_all", "t7inject", "t5activate"]:
        deps = sorted(slice_deps(slicer, t))
        entry = {"deps": deps,
                 "forbidden_inflow": sorted(set(deps) & FORBIDDEN)}
        out[t] = entry
        if t in TARGETS and entry["forbidden_inflow"]:
            hits.append(f"{t}:{entry['forbidden_inflow']}")
    for name, want in (("C_FROZEN", 2), ("K_FROZEN", 6)):
        if out["constants"][name]["literal"] != want:
            hits.append(f"{name}-not-literal-{want}")
    return out, hits


def lean_dependencies():
    """Lean-side dependency check: C/K literal bodies; helper bodies free of
    forbidden identifiers; MST0_22 quantifier order."""
    import re
    frozen = (IMPL / "lean/Frozen/MSTC0002Defs.lean").read_text(encoding="utf-8")
    stmts = (IMPL / "lean/Frozen/Statements.lean").read_text(encoding="utf-8")
    hits, info = [], {}
    for name, want in (("C_frozen", "2"), ("K_frozen", "6")):
        m = re.search(rf"def {name} : Nat := (\S+)", frozen)
        lit = m.group(1) if m else None
        info[name] = {"body": lit}
        if lit != want:
            hits.append(f"{name}-not-literal")
    for name in ["required", "activePool", "discharge", "energy", "T7inject",
                 "T5activate", "sites"]:
        m = re.search(rf"(?:def|abbrev) {name}.*?:=\n((?:  .*\n)+)", frozen)
        body = m.group(1) if m else ""
        toks = set(re.findall(r"[A-Za-z_][\w]*", body))
        bad = sorted(t for t in toks if t in FORBIDDEN and t != "n")
        bare_n = bool(re.search(r"(?<![\w])n(?![\w])", body))
        info[name] = {"forbidden_tokens": bad, "bare_n_present": bare_n}
        if bad:
            hits.append(f"{name}:{bad}")
    m22 = re.search(r"def MST0_22 : Prop :=\n((?:  .*\n)+)", stmts)
    body22 = m22.group(1) if m22 else ""
    order_ok = body22.lstrip().startswith("(C_frozen = 2") \
        and "∀ y a : Nat" in body22 and "∀ (E : Engine)" in body22
    info["MST0_22_order_ok"] = order_ok
    if not order_ok:
        hits.append("MST0_22-order")
    return info, hits


def main():
    # WP-2 STEP CS-01: dependence/dataflow scan over frozen sources.
    print("[WP-2][STEP CS-01] constants dataflow scan running", flush=True)
    try:
        from python.audit import log as LOG
        with LOG.Timer() as tm:
            py, py_hits = python_dataflow()
            ln, ln_hits = lean_dependencies()
        hits = py_hits + ln_hits
        verdict = "CLEAN" if not hits else "DIRTY"
        artifact = {"findings": {"python_dataflow": py, "lean_dependencies": ln},
                    "hits": hits, "verdict": verdict}
        SCAN_ARTIFACT.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n",
                                 encoding="utf-8")
        import hashlib as _h
        sha = _h.sha256(SCAN_ARTIFACT.read_bytes()).hexdigest()
        record = LOG.base_record("MST0-22", "PROVE",
                                 "python/cleanroom/constants_scan.py")
        record.update({"input hashes": [
            _h.sha256((IMPL / f).read_bytes()).hexdigest()
            for f in ["python/inherited/mstc0002.py", "lean/Frozen/MSTC0002Defs.lean",
                      "lean/Frozen/Statements.lean"]],
            "output hashes": [sha], "stdout/stderr hashes": [],
            "wall time": tm.wall, "peak memory": tm.peak,
            "exit code": 0, "scientific status": "SCAN-" + verdict})
        LOG.emit_run_record(record)
    except OSError:
        print("[WP-2][STEP CS-01] source unreadable", flush=True)
        return 2
    # WP-2 STEP CS-02: scan verdict emitted.
    print(f"[WP-2][STEP CS-02] SCAN-VERDICT: {verdict} "
          f"(hits={hits} artifact={SCAN_ARTIFACT.name})", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
