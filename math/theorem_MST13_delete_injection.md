# MST0-13 — bounded DELETE injection (frozen Phase 1; v0.4 §6, §12)

- Parent status: PROVED author claim, human review pending (NOT REVIEWED; consumes nothing until REVIEWED).
- v0.4 owner phase: Phase 2 (WorkPlan §5; hostile review + formal transport of the v0.3 author proof).
- First consumer: MST0-17 (BLOCKED on 13/14/15).
- Prerequisites: frozen SplayDefs/MSTC0002Defs + MSTC-0002 binding + v0.3 author-proof transport record.
- Child-lemma namespace: `MST0-13/*` (registered, versioned, non-weakening).
- Forbidden premises: parent holdout (H3T) reuse; bare REJECT as refutation (v0.4.1 A2:
  only the `MST0_13_REJECTED`/`MST0_13_BLOCKED` reviewer gates route status);
  K6 demand read as six slots (T043, INV-053, STOP-38).
- Falsity consequence: positive route dies; MSTC-0002 refuted as currently formulated
  (no DOC-negative lift without an exact-obstruction reduction at Phase 17).
- Statement: forall (E : Engine) (isA : Bool) (lo hi x n k : Nat), k <= 6 -> energy (T7inject E isA lo hi x n k).ledger <= energy E.ledger + 6 * k
- Negation: exists (E : Engine) (isA : Bool) (lo hi x n k : Nat), k <= 6 /\ energy (T7inject E isA lo hi x n k).ledger > energy E.ledger + 6 * k
- Proof artifact: `math/proofs/MST0-13_proof.md` (PENDING Phase 2; hostile review of the transported author claim).
- Formal artifact: `lean/Proofs/Injection.lean` (PENDING Phase 2).
- Review artifact: `math/reviews/MST0-13.PACKAGE.md` + `math/reviews/MST0-13.review.json` (human verdict only; routes PROVED->REVIEWED or the A2 gates).
- Refutation artifact: `artifacts/v04/proof_attacks/MST0-13/` attack record (PENDING Phase 2).
