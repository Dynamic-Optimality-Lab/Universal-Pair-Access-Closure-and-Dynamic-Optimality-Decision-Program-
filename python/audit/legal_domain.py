"""audit/legal_domain.py — LegalPairInstance executable mirror (MST0-14R repair track).

New file (repair track, not frozen): executablechecking mirror of the
minimal source-derived legal-domain predicate for paired executions.
Used by: domain-defect certification (negative cases), K6 rebinding
(positive cases), repaired-theorem test suites.

Normative sources (see LEGAL_DOMAIN_AUDIT below):
  C1 BST.Valid T0            <- IMPLEMENTATION_SPEC_v0.4.md s4/s5.2, MST0-11 obligations
  C2 tree keys within [n]    <- spec s4 key universe [n]={1,..,n} (SUBSET, not equality)
  C3 history modes legal     <- python/inherited/pair_access.py::validate_history
  C4 history keys within [n] <- spec s4 universe + validate_history
  C5 common initial tree     <- encoded structurally (execHist/execSuffices call shape T0 T0)

Deliberately NOT required (recorded, not silently resolved):
  - keys(T0) == [n] exactly (K6 uses exact trees, but splay handles misses
    gracefully; subset is the weaker sufficient guard)
  - history keys present in T0 (absent-key splay is a defined no-op;
    the model never requires presence)
  - Y-subsequence precondition (lives at MST0-17, not MST0-14)

Deterministic, no RNG, no I/O. Mirrors lean/Proofs/LegalDomain.lean.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from python.inherited import splay as S

LEGAL_MODES = ("KEEP", "DELETE")

# Conjunct identifiers (stable; used by violations() and audit records).
C_VALID = "C1-BST-Valid"
C_TREE_KEYS = "C2-tree-keys-in-universe"
C_MODES = "C3-history-modes-legal"
C_HIST_KEYS = "C4-history-keys-in-universe"
C_COMMON_TREE = "C5-common-initial-tree"


def tree_keys_ok(T0, n):
    """C2: every key of T0 lies in [n] (subset reading)."""
    return all(1 <= k <= n for k in S.keys(T0))


def history_ok(H, n):
    """C3+C4: every access has legal mode and key in [n]."""
    for m, x in H:
        if m not in LEGAL_MODES:
            return False
        if not (1 <= x <= n):
            return False
    return True


def violations(T0, H, n):
    """List violated conjunct ids (empty == LegalPairInstance holds).

    C5 is structural: callers pass the same T0 twice (execSuffices E T0 T0
    H n). A caller passing distinct A/B trees records C5 violation here
    via violations_split(); this function checks the shared-tree shape.
    """
    bad = []
    if not S.valid(T0):
        bad.append(C_VALID)
    if not tree_keys_ok(T0, n):
        bad.append(C_TREE_KEYS)
    modes_ok = all(m in LEGAL_MODES for m, _ in H)
    if not modes_ok:
        bad.append(C_MODES)
    if not all(1 <= x <= n for _, x in H):
        bad.append(C_HIST_KEYS)
    return bad


def legal_pair_instance(T0, H, n):
    """True iff (T0,H,n) lies in the intended paired-execution domain."""
    return violations(T0, H, n) == []


def violations_split(A, B, H, n):
    """Generalization used only for diagnostics: distinct A/B trees."""
    bad = []
    if not (S.valid(A) and S.valid(B)):
        bad.append(C_VALID)
    if not (tree_keys_ok(A, n) and tree_keys_ok(B, n)):
        bad.append(C_TREE_KEYS)
    if not all(m in LEGAL_MODES for m, _ in H):
        bad.append(C_MODES)
    if not all(1 <= x <= n for _, x in H):
        bad.append(C_HIST_KEYS)
    if A != B:
        bad.append(C_COMMON_TREE + "-caller-shape")
    return bad


LEGAL_DOMAIN_AUDIT = [
    {
        "conjunct": C_VALID,
        "normative_source": "IMPLEMENTATION_SPEC_v0.4.md s4/s5.2 (BST validity core object); MST0-11 preservation obligations include BST legality",
        "why_required": "splay rotation formulas assume BST ordering; all downstream consumption assumes valid trees",
        "malformed_excluded": "non-BST trees (inorder unsorted)",
        "k6_inputs_satisfy": True,
    },
    {
        "conjunct": C_TREE_KEYS,
        "normative_source": "IMPLEMENTATION_SPEC_v0.4.md s4: key universe [n]={1,..,n}; T7 sites filter 1<=i<nkeys binds n to the universe",
        "why_required": "rotation-event intervals derive from tree keys; sites supply exists only inside [1,nkeys); keys outside [n] starve T7 while costs stay large (the n=0 witness mechanism)",
        "malformed_excluded": "T0=vine{1,2,3} with n=0 (witness); any tree holding keys outside [n]",
        "k6_inputs_satisfy": True,
        "reading_note": "SUBSET (keys(T0) subset of [n]), NOT equality: splay on absent keys is a defined no-op and equality would over-restrict withoutFrozen-model mandate. K6 uses exact [n] trees; the theorem is stated for the weaker guard (stronger theorem).",
    },
    {
        "conjunct": C_MODES,
        "normative_source": "python/inherited/pair_access.py::validate_history (mode in {KEEP,DELETE}); Lean Mode inductive has exactly KEEP/DELETE constructors (well-typed by construction)",
        "why_required": "execLoop pattern-matches KEEP/DELETE only; unknown modes have no frozen semantics",
        "malformed_excluded": "histories with unknown mode tags (Python-level only; unrepresentable in Lean)",
        "k6_inputs_satisfy": True,
    },
    {
        "conjunct": C_HIST_KEYS,
        "normative_source": "IMPLEMENTATION_SPEC_v0.4.md s4 universe + validate_history 1<=x<=nkeys",
        "why_required": "accesses outside [n] address no universe key; combined with nkeys=n they reproduce the witness starvation shape",
        "malformed_excluded": "H=[(DELETE,3),(KEEP,3)] with n=0 (witness); any access outside [n]",
        "k6_inputs_satisfy": True,
        "reading_note": "Presence in T0 NOT required: absent-key splay is a defined no-op (tree unchanged, empty trace); the model never mandates presence.",
    },
    {
        "conjunct": C_COMMON_TREE,
        "normative_source": "MSTC0002Defs.execHist/execSuffices call shape (E T0 T0 H n); spec s4 Pair-Access precondition of a common initial tree",
        "why_required": "paired A/B divergence accounting starts from identical trees; distinct starts are a different (MST0-15-D5-style) question",
        "malformed_excluded": "split-start executions (not expressible in the repaired statement, which passes T0 twice)",
        "k6_inputs_satisfy": True,
        "reading_note": "Structural (call shape), not a runtime check; no Y-subsequence conjunct at MST0-14 level (that precondition lives at MST0-17).",
    },
]
