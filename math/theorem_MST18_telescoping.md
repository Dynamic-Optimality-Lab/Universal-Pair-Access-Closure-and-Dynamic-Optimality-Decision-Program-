# MST0-18 — telescoping / approximate monotonicity (frozen Phase 1; v0.4 §6, Phase-15 contract)

- Parent status: BLOCKED on 17.
- v0.4 owner phase: Phase 5 (WorkPlan §8; PSC-T telescope endpoint torture, spec PHASE 15).
- First consumer: MST0-19 (Levy-Tarjan bridge; 18 supplies the exact approximate-monotonicity statement the bridge consumes).
- Prerequisites: MST0-17 REVIEWED (PROVE track; REFUTE track runs on REFUTE_READY per v0.4.3 C1).
- Child-lemma namespace: `MST0-18/*` (registered, versioned, non-weakening).
- Forbidden premises: parent holdout (H3T) reuse; assumed endpoint bounds (no assumed E_m >= 0;
  T066); length-dependent additive (T067, STOP-53/54); direction unchecked.
- Falsity consequence: exact legal witness/family violating the endpoint theorem may REFUTE
  (independent replay, canonical minimization, endpoint-aware witness-schema validation) and
  ACTIVATES Phase 6 negative lifting candidacy.
- Statement: exists A : Nat -> Nat, forall (T0 : BST) (H : List (Mode * Nat)) (n : Nat), let (E, sA, sB) := execHist {ledger := [], cursor := 0} T0 H n in sB <= 2 * sA + A n
- Negation: forall A : Nat -> Nat, exists (T0 : BST) (H : List (Mode * Nat)) (n : Nat), let (E, sA, sB) := execHist {ledger := [], cursor := 0} T0 H n in sB > 2 * sA + A n
- Proof artifact: `math/proofs/MST0-18_proof.md` (PENDING Phase 5; exact additive term + direction).
- Formal artifact: `lean/Proofs/Telescope.lean` (PENDING Phase 5).
- Review artifact: `math/reviews/MST0-18.PACKAGE.md` + `math/reviews/MST0-18.review.json` (human verdict only).
- Refutation artifact: `artifacts/v04/proof_attacks/MST0-18/` PSC-T + direct symbolic endpoint search record (PENDING Phase 5).
