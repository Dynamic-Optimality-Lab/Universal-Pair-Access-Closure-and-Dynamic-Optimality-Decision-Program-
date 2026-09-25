# MST0-11 — transfer preservation (v0.4 frozen statement)

**Parent provenance:** v0.3 `math/theorem_MST11_transfer_preservation.md` (SETUP, explicitly UNPROVED; statement/schema frozen, proof belonged to WP-6). v0.4 proves or refutes over the instantiated MSTC-0002 rules. All 7 Splay cases × every ledger rule, symbolic parameters.

## Frozen canonical statement (hashed)

```text
STATEMENT_MST0-11: Every legal primitive update of MSTC-0002 (ROOT, ZIG-left, ZIG-right, LL, RR, LR, RL, each under every applicable ledger rule with arbitrary legal subtree intervals/sizes/ranks/supports) maps a well-formed ledger to a well-formed ledger, preserving BST legality, support/mass/type/scale legality, ownership uniqueness where required, source/provenance validity, spent-credit non-resurrection, no forbidden future/history lookup, and the exact energy/flow identity required by the rule.
```

## Frozen canonical negation (hashed)

```text
NEGATION_MST0-11: There exists one legal primitive update violating at least one required downstream invariant.
```

## Metadata

- Owner phase: WorkPlan Phase 2 (spec PHASE 07). First consumers: MST0-14, MST0-15, MST0-17.
- Prerequisites: MSTC-0002 record. Required status: REVIEWED.
