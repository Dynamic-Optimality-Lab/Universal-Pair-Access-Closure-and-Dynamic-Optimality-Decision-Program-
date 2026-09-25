# MST0-17 — universal Pair-Access composition (v0.4 frozen statement)

**Parent provenance:** v0.3 `math/theorem_MST17_pair_access.md` (BLOCKED; requires REVIEWED 13/14/15 then block-composition proof of the endpoint inequality with A(n) = 0 preferred). v0.4 independent reconstruction (no status-toggling shortcut) + dedicated `REFUTE(MST0-17)` battery with endpoint-aware negation (v0.4-WP5 HARD fix).

## Frozen canonical statement (hashed)

```text
STATEMENT_MST0-17: For every legal paired execution (n, T, X, Y << X) with canonical block decomposition and ledgers L_0, L_m under MSTC-0002, Splay(Y,T) + E_m - E_0 <= 2 * Splay(X,T) + A(n).
```

## Frozen canonical negation (hashed)

```text
NEGATION_MST0-17: There exist n, T, X, Y << X with certificate, paired execution, canonical block decomposition, and ledgers L_0, L_m such that lhs > rhs with lhs = Splay(Y,T) + E_m - E_0 and rhs = 2 * Splay(X,T) + A(n) (strict positive residual lhs - rhs).
```

## Metadata

- Owner phase: WorkPlan Phase 5 (spec PHASE 14). First consumer: MST0-18.
- Prerequisites: MST0-08U, MST0-09, MST0-11, MST0-13, MST0-14, MST0-15, MST0-22 (all REVIEWED; hard entry gate) + inherited structural prerequisites. Required status: REVIEWED.
- Refutation witness: 15-field endpoint-aware payload (`proof_attack.schema.json` + `pair_access_certificate.schema.json` + interface conformance); triple-artifact gate for REFUTED.
