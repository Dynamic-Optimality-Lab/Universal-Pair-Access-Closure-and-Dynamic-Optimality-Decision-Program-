# MST0-09 — raw boundary law (frozen Phase 1; v0.4 §6, §11)

- Parent status: UNPROVED.
- v0.4 owner phase: Phase 2 (WorkPlan §5; PSC-B Boundary Torture attack).
- First consumer: MST0-17 (via repayment/integrability consumption of the boundary theorem).
- Prerequisites: frozen SplayDefs/MSTC0002Defs + MSTC-0002 binding; no upstream node.
- Child-lemma namespace: `MST0-09/*` (registered, versioned, non-weakening).
- Forbidden premises: parent holdout (H3T) reuse; finite enumeration as premise for the
  arbitrary-n law; un-frozen literature; cost-bearing-source claims without the
  Phase-2 case analysis (nested/alternating/creation-rate/rank-gap/span/burden/
  burst/lifetime/reactivation/asymmetry/mirror/scale).
- Falsity consequence: positive route dies for the boundary-dependent chain;
  MSTC-0002 refuted as currently formulated (no DOC-negative lift without an
  exact-obstruction reduction at Phase 17).
- Statement: forall L : Ledger, energy L >= 0
- Negation: exists L : Ledger, energy L < 0
- Proof artifact: `math/proofs/MST0-09_proof.md` (PENDING Phase 2; must identify the exact cost-bearing source of every harmful boundary contribution with the universal bound).
- Formal artifact: `lean/Proofs/Boundary.lean` (PENDING Phase 2).
- Review artifact: `math/reviews/MST0-09.PACKAGE.md` + `math/reviews/MST0-09.review.json` (human verdict only).
- Refutation artifact: `artifacts/v04/proof_attacks/MST0-09/` PSC-B attack record (PENDING Phase 2).
