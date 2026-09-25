# MST0-17 — universal Pair-Access composition (frozen Phase 1; v0.4 §6, Phase-14 contract)

- Parent status: BLOCKED on 13/14/15 (+ required guards).
- v0.4 owner phase: Phase 5 (WorkPlan §8; PSC pair-access search, spec PHASE 14).
- First consumer: MST0-18 (telescoping / approximate monotonicity).
- Prerequisites: MST0-08U/09/11/13/14/15/22 REVIEWED (PROVE track; REFUTE track runs on
  REFUTE_READY with no upstream-REVIEWED requirement per v0.4.3 C1).
- Child-lemma namespace: `MST0-17/*` (registered, versioned, non-weakening).
- Forbidden premises: parent holdout (H3T) reuse or re-unlock; status-toggling instead of
  reconstruction from scratch; the endpoint-free form attacked as 17 (negative E_m - E_0
  must not escape; endpoint elimination belongs to MST0-18); consumed holdout citation.
- Falsity consequence: exact legal witness/family REFUTES (after independent replay,
  canonical minimization, certificate validation) and ACTIVATES Phase 6 negative lifting
  candidacy; local residual without reduction never lifts (T079-T081, STOP-60).
- Statement: exists A : Nat -> Nat, forall (T0 : BST) (H : List (Mode * Nat)) (n : Nat), let (E, sA, sB) := execHist {ledger := [], cursor := 0} T0 H n in sB + energy E.ledger <= 2 * sA + A n
- Negation: forall A : Nat -> Nat, exists (T0 : BST) (H : List (Mode * Nat)) (n : Nat), let (E, sA, sB) := execHist {ledger := [], cursor := 0} T0 H n in sB + energy E.ledger > 2 * sA + A n
- Proof artifact: `math/proofs/MST0-17_proof.md` (PENDING Phase 5; independently written proof that block/local inequalities imply the composition bound with exact block coverage).
- Formal artifact: `lean/Proofs/Composition.lean` (PENDING Phase 5).
- Review artifact: `math/reviews/MST0-17.PACKAGE.md` + `math/reviews/MST0-17.review.json` (human verdict only).
- Refutation artifact: `artifacts/v04/proof_attacks/MST0-17/` pair-access search record with full reconstruction payload witness (PENDING Phase 5).
