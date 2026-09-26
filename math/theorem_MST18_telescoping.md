# MST0-18 — telescoping / approximate monotonicity (frozen Phase 1; theorem identity v0.4.7 G11)

- Parent status: BLOCKED on 17.
- v0.4 owner phase: Phase 5.
- First consumer: MST0-19.
- Prerequisites: MST0-17 REVIEWED (PROVE track; REFUTE needs REFUTE_READY only).
- Child-lemma namespace: `MST0-18/*` (registered, versioned, non-weakening).
- Banned weakening (v1.5, superseded): Assumed endpoint bounds (T066); length-dependent additive (T067/STOP-53-54).
- Falsity means: Exact endpoint witness/family may REFUTE (endpoint-aware schema validation).
- Falsity does NOT mean: DOC false; direction-unchecked claims.
- Statement: exists A : Nat -> Nat, forall (T0 : BST) (H : List (Mode * Nat)) (n : Nat), let (_, sA, sB) := execHist { ledger := [], cursor := 0 } T0 H n; sB <= 2 * sA + A n
- Negation: forall A : Nat -> Nat, exists (T0 : BST) (H : List (Mode * Nat)) (n : Nat), let (_, sA, sB) := execHist { ledger := [], cursor := 0 } T0 H n; sB > 2 * sA + A n
- Proof artifact: `math/proofs/MST0-18_proof.md` (PENDING owner phase).
- Formal artifact: `lean/Proofs/Telescope.lean` (PENDING owner phase).
- Review artifact: `math/reviews/MST0-18.PACKAGE.md` + `math/reviews/MST0-18.review.json` (human verdict only).
- Refutation artifact: `artifacts/v04/proof_attacks/MST0-18/` PSC-T + direct symbolic endpoint search record (PENDING owner phase).
