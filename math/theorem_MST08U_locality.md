# MST0-08U — universal reference locality (frozen Phase 1; v0.4 §6, §9)

- Parent status: UNPROVED (universal form open).
- v0.4 owner phase: Phase 2 (WorkPlan §5; PSC-L Locality Explosion attack).
- First consumer: MST0-17 (Pair-Access composition; via the required-guard chain).
- Prerequisites: frozen SplayDefs/MSTC0002Defs + MSTC-0002 binding; no upstream node.
- Child-lemma namespace: `MST0-08U/*` (registered, versioned, non-weakening).
- Forbidden premises: parent holdout (H3T) reuse; finite-maximum survival as proof
  (LOC-07, STOP-30/31); un-frozen literature; any replacement calculus.
- Falsity consequence: positive route dies for the locality-dependent chain;
  MSTC-0002 refuted as currently formulated (no DOC-negative lift without an
  exact-obstruction reduction at Phase 17).
- Statement: forall (E : Engine) (isA : Bool) (lo hi x n k : Nat), k <= 6 -> (T7inject E isA lo hi x n k).ledger.length <= E.ledger.length + 6
- Negation: exists (E : Engine) (isA : Bool) (lo hi x n k : Nat), k <= 6 /\ (T7inject E isA lo hi x n k).ledger.length > E.ledger.length + 6
- Proof artifact: `math/proofs/MST0-08U_proof.md` (PENDING Phase 2).
- Formal artifact: `lean/Proofs/Locality.lean` (PENDING Phase 2).
- Review artifact: `math/reviews/MST0-08U.PACKAGE.md` + `math/reviews/MST0-08U.review.json` (human verdict only).
- Refutation artifact: `artifacts/v04/proof_attacks/MST0-08U/` PSC-L attack record (PENDING Phase 2).
