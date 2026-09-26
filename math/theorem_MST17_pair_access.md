# MST0-17 — universal Pair-Access composition (E_0-generalized) (frozen Phase 1; theorem identity v0.4.7 G11)

- Parent status: BLOCKED on 13/14/15 (+ required guards).
- v0.4 owner phase: Phase 5.
- First consumer: MST0-18.
- Prerequisites: MST0-08U/09/11/13/14/15/22 REVIEWED (PROVE track; REFUTE needs REFUTE_READY only).
- Child-lemma namespace: `MST0-17/*` (registered, versioned, non-weakening).
- Banned weakening (v1.5, superseded): Endpoint-free form attacked as 17 (negative E_m-E_0 escape).
- Falsity means: Exact legal witness/family REFUTES (replay+minimization+certificate) and activates Phase-6 candidacy.
- Falsity does NOT mean: DOC false; residual-without-reduction lifts (T079-T081, STOP-60).
- Statement: exists A : Nat -> Nat, forall (E0 : Engine) (T0 : BST) (H : List (Mode * Nat)) (n : Nat), let (E, sA, sB) := execHist E0 T0 H n; sB + energy E.ledger <= 2 * sA + A n + energy E0.ledger
- Negation: forall A : Nat -> Nat, exists (E0 : Engine) (T0 : BST) (H : List (Mode * Nat)) (n : Nat), let (E, sA, sB) := execHist E0 T0 H n; sB + energy E.ledger > 2 * sA + A n + energy E0.ledger
- Proof artifact: `math/proofs/MST0-17_proof.md` (PENDING owner phase).
- Formal artifact: `lean/Proofs/Composition.lean` (PENDING owner phase).
- Review artifact: `math/reviews/MST0-17.PACKAGE.md` + `math/reviews/MST0-17.review.json` (human verdict only).
- Refutation artifact: `artifacts/v04/proof_attacks/MST0-17/` pair-access search (endpoint-aware negation) record (PENDING owner phase).
