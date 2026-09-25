# MST0-14 — synchronous KEEP repayment (v0.4 frozen statement)

**Parent provenance:** v0.3 `math/theorem_MST14_keep_repayment.md` (UNPROVED status record; finite survival only; sibling fresh kills; needs 08U-universal + 15). v0.4 K6 Saturation War + proof. Payment semantics owned by the imported MSTC-0002 record (parent ledger/T6 describes discharge of legally active credit against positive regret; any `min(pool,w)`-form reduction is recorded as a proved binding lemma, never assumed).

## Frozen canonical statement (hashed)

```text
STATEMENT_MST0-14: For every legal KEEP event/block under MSTC-0002 at C=2, with edge regret w = y - 2a and required = max(w, 0), the legally available payment under the imported payment semantics covers required in full (paid = imported_MSTC0002_payment(...)), with no future information, no latent-without-activation use, no spent resurrection, and no double use within or across KEEP events.
```

## Frozen canonical negation (hashed)

```text
NEGATION_MST0-14: There exists a legal KEEP event/block with strict positive residual required - paid > 0 under the frozen theorem semantics.
```

## Metadata

- Owner phase: WorkPlan Phase 3 (spec PHASE 10–11). First consumers: MST0-15, MST0-17.
- Prerequisites: MST0-08U, MST0-09, MST0-11, MST0-13, MST0-22 (all REVIEWED; hard entry gate). Required status: REVIEWED.
