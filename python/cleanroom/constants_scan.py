"""Constant-dependence scanner (WorkPlan Phase 2, CONST-03..08 support).

Dependence-scoped (WP2 fix): flags assignments where a frozen constant or a
theorem-facing helper's VALUE derives from a forbidden parameter — not mere
occurrence of quantified variables (n, T, X, Y appear legitimately in
universal statements). Forbidden sources: names denoting n-derived
coefficients, sequence length, holdout/corpus/panel/seed identifiers,
cycle/state IDs, solver-chosen values, decomposition choices.
"""
from __future__ import annotations

import ast

FORBIDDEN_SOURCES = {"n_coeff", "seq_len", "holdout_id", "corpus_id", "panel",
                     "seed", "cycle_id", "state_id", "solver_choice",
                     "decomposition", "h3t", "bank_id"}


def scan_file(path):
    """Scan one file; return list of findings {line, target, source}."""
    print("CONST-SCAN: scanning %s" % path)
    tree = ast.parse(open(path, encoding="utf-8").read())
    findings = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = []
            if isinstance(node, ast.Assign):
                targets = [t.id for t in node.targets if isinstance(t, ast.Name)]
            value = node.value
            if value is None:
                continue
            bad = set()

            class W(ast.NodeVisitor):
                def visit_Name(self, n):
                    if n.id in FORBIDDEN_SOURCES:
                        bad.add(n.id)

            W().visit(value)
            for t in targets:
                if bad and (t in ("C", "k", "K_FROZEN", "C_FROZEN") or "const" in t.lower()):
                    findings.append({"line": node.lineno, "target": t,
                                     "source": sorted(bad)})
    print("CONST-SCAN: %s findings=%d" % (path, len(findings)))
    return findings


def scan_paths(paths):
    """Scan many files; return {path: findings}."""
    return {p: scan_file(p) for p in paths}
