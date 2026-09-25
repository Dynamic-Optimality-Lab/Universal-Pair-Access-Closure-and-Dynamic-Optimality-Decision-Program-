# MST0-08U — universal reference locality (v0.4 frozen statement)

**Parent provenance:** `parent/V03_PATH_FINAL.md` + v0.3 `math/theorem_MST08_reference_rotation_locality.md` (finite bounds PROVED for n≤6: ≤2 heavy flips, ≤3 interval creations; arbitrary-n O(1) modification claim UNPROVED with explicit ancestor-chain gap). v0.4 must prove or refute the universal form. No finite maximum is a premise.

## Frozen canonical statement (hashed)

```text
STATEMENT_MST0-08U: There exists a universal constant L, independent of n, sequence length, initial tree, and proof decomposition, such that every legal single A-side rotation changes at most L translated primitives of the MSTC-0002 reference/support representation consumed by MST0-14/15.
```

## Frozen canonical negation (hashed)

```text
NEGATION_MST0-08U: For every bound B there exists a legal single A-side rotation (at some n) changing more than B translated primitives of the consumed representation.
```

## Metadata

- Owner phase: WorkPlan Phase 2 (spec PHASE 06). First consumers: MST0-14, MST0-15.
- Prerequisites: frozen Splay/Pair-Access semantics + imported MSTC-0002 record. Required status: REVIEWED.
- Refutation kills the positive route at this ID unless a preregistered sufficient child lemma is proved.
