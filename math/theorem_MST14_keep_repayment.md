# MST0-14 — synchronous KEEP repayment (frozen Phase 1; v0.4 §6, §14)

- Parent status: UNPROVED.
- v0.4 owner phase: Phase 3 (WorkPlan §6; PSC-K6 K6 Saturation War, spec PHASE 10-11).
- First consumer: MST0-17 (BLOCKED on 13/14/15).
- Prerequisites: frozen SplayDefs/MSTC0002Defs + MSTC-0002 binding; no upstream node
  (Phase-3 proves pool sufficiency along paired executions at C = 2).
- Child-lemma namespace: `MST0-14/*` (registered, versioned, non-weakening).
- Forbidden premises: parent holdout (H3T) reuse; K6 demand read as six slots
  (T043, INV-053, STOP-38); `min(pool,w)`-form reduction assumed before binding
  (recorded as proved binding lemma after binding, never assumed); payment from
  anything but legally available ACTIVE pool.
- Falsity consequence: positive route dies; MSTC-0002 refuted as currently formulated
  (no DOC-negative lift without an exact-obstruction reduction at Phase 17).
- Statement: forall (L : Ledger) (y a : Nat), (discharge L (required y a)).2 = min (activePool L) (required y a)
- Negation: exists (L : Ledger) (y a : Nat), (discharge L (required y a)).2 != min (activePool L) (required y a)
- Proof artifact: `math/proofs/MST0-14_proof.md` (PENDING Phase 3; human case-complete proof + matching theorem).
- Formal artifact: `lean/Proofs/Repayment.lean` (PENDING Phase 3).
- Review artifact: `math/reviews/MST0-14.PACKAGE.md` + `math/reviews/MST0-14.review.json` (human verdict only).
- Refutation artifact: `artifacts/v04/proof_attacks/MST0-14/` PSC-K6 attack record (PENDING Phase 3).
