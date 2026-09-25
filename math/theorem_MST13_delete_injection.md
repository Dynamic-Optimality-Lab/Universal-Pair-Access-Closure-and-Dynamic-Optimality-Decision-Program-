# MST0-13 — bounded DELETE injection (v0.4 frozen statement)

**Parent provenance:** v0.3 `math/theorem_MST13_delete_injection.md` (author proof claim, Lemmas 1–4: rotations≤cost, T7 bound k=6/rotation, T5 conservation, T6 inapplicability on DELETE; human review pending; `artifacts/v03/proofs/MST13_injection_bound.json` supporting only). v0.4 hostile review + formalization; human ACCEPT/REJECT/BLOCKED per v0.4.1 A2 (REJECT/BLOCKED = reviewer gate only, never automatic REFUTED).

## Frozen canonical statement (hashed)

```text
STATEMENT_MST0-13: For every A-only DELETE block D under MSTC-0002, E_after - E_before <= 6 * cost_A(D), with E(L) = count(BOUNDARY_LATENT) + count(BOUNDARY_ACTIVE) and E(empty) = 0.
```

## Frozen canonical negation (hashed)

```text
NEGATION_MST0-13: There exists a legal A-only DELETE block D with E_after - E_before > 6 * cost_A(D) (strict positive injection residual).
```

## Metadata

- Owner phase: WorkPlan Phase 2 (spec PHASE 05). First consumer: MST0-17.
- Prerequisites: parent import + MSTC-0002 record. Required status: REVIEWED (ACCEPT + formal green).
