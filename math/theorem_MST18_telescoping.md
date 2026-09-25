# MST0-18 — telescope / approximate monotonicity (v0.4 frozen statement)

**Parent provenance:** v0.3 `math/theorem_MST18_telescoping.md` (BLOCKED on 17; needs REVIEWED 17 + symbolic telescope check under frozen cost convention with explicit bridge-compatible additive term). v0.4 Telescope Torture + formal theorem.

## Frozen canonical statement (hashed)

```text
STATEMENT_MST0-18: Endpoint energy/flow terms are controlled (E_m bounded below, E_0 properly normalized, no hidden mid-execution reset, exact block coverage) so that MST0-17 telescopes to approximate monotonicity with an exact additive term A(n) that is explicit, sequence-length independent, and bridge-compatible, in the exact implication direction.
```

## Frozen canonical negation (hashed)

```text
NEGATION_MST0-18: There exists a legal execution family with endpoint failure (E_m unbounded below, improper E_0, sequence-dependent A(n), block overlap/omission, or hidden reset) defeating the telescoped inequality.
```

## Metadata

- Owner phase: WorkPlan Phase 5 (spec PHASE 15). First consumer: MST0-19.
- Prerequisites: MST0-17 REVIEWED. Required status: REVIEWED.
