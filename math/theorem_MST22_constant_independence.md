# MST0-22 — constant independence (v0.4 frozen statement)

**Parent provenance:** v0.3 WP-5 setup record (UNPROVED). v0.4 quantifier audit + proof. Static scans support only; hidden dependence refutes.

## Frozen canonical statement (hashed)

```text
STATEMENT_MST0-22: There exist frozen constants C = 2 and k = 6 such that for all n, all initial trees T, all sequences X, and all subsequences Y << X, the MSTC-0002 theorem statements hold with these constants, whose definitions depend on none of: n, sequence length, initial tree, subsequence choice, proof decomposition, finite corpus, holdout bank, search generator, solver state, holdout/cycle/state identifiers.
```

## Frozen canonical negation (hashed)

```text
NEGATION_MST0-22: Some theorem-facing constant or helper definition depends on at least one forbidden parameter above.
```

## Metadata

- Owner phase: WorkPlan Phase 2 (spec PHASE 09). First consumer: MST0-17 (guards all).
- Prerequisites: MSTC-0002 record. Required status: REVIEWED.
