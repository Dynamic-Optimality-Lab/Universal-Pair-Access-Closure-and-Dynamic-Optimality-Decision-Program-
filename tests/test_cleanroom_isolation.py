"""Clean-room isolation enforcement (INV-037, STOP-19).

Fails closed if any import edge exists between the two theorem-critical
implementation trees: python/cleanroom/* must never import
python.inherited or python.proof_attack, and vice versa. Shared surface is
recorded programs (plain data) only.
"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

CLEANROOM_FILES = [
    "python/cleanroom/core.py",
    "python/cleanroom/locality_check.py",
    "python/cleanroom/preservation_check.py",
    "python/cleanroom/boundary_check.py",
    "python/cleanroom/pair_access_check.py",
    "python/cleanroom/constants_scan.py",
]
INHERITED_FILES = [
    "python/inherited/splay.py",
    "python/inherited/pair_access.py",
    "python/inherited/mstc0002.py",
]
ATTACK_FILES = [
    "python/proof_attack/locality_explosion.py",
    "python/proof_attack/primitive_exhaust.py",
    "python/proof_attack/boundary_torture.py",
    "python/proof_attack/k6_saturation.py",
    "python/proof_attack/double_spend.py",
    "python/proof_attack/telescope_torture.py",
    "python/proof_attack/pair_access_search.py",
]


def _tree_refs(path):
    """Return which FOREIGN theorem-critical trees a file imports.

    Intra-tree imports (cleanroom->cleanroom, inherited->inherited,
    attack->attack) are legitimate structure, not boundary violations.
    """
    own = path.split("/")[1]
    text = (REPO_ROOT / path).read_text(encoding="utf-8")
    refs = set()
    for tok in ("inherited", "proof_attack", "cleanroom"):
        if tok == own:
            continue
        if ("from python.%s" % tok) in text or ("import python.%s" % tok) in text:
            refs.add(tok)
    return refs


def test_cleanroom_imports_nothing_theorem_critical():
    """Clean-room files import stdlib only (no inherited/proof_attack edge)."""
    for path in CLEANROOM_FILES:
        if not (REPO_ROOT / path).exists():
            continue
        assert _tree_refs(path) == set(), path


def test_inherited_imports_no_cleanroom_or_attack():
    """Inherited core never imports cleanroom or attack trees."""
    for path in INHERITED_FILES:
        assert _tree_refs(path) == set(), path


def test_attack_imports_inherited_only():
    """Attack batteries may use inherited core but never cleanroom."""
    for path in ATTACK_FILES:
        if not (REPO_ROOT / path).exists():
            continue
        got = _tree_refs(path)
        assert "cleanroom" not in got, path
