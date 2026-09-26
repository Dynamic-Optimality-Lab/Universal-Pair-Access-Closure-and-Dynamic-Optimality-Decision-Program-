# MST0-14 — universal synchronous KEEP repayment (sufficiency) (frozen Phase 1; theorem identity v0.4.7 G11)

- Parent status: UNPROVED.
- v0.4 owner phase: Phase 3.
- First consumer: MST0-17 (BLOCKED on 13/14/15).
- Prerequisites: frozen definitions + MSTC-0002 binding (Phase-3 proves sufficiency at C=2).
- Child-lemma namespace: `MST0-14/*` (registered, versioned, non-weakening).
- Banned weakening (v1.5, superseded): Bare `paid = min(pool, required)` mechanism identity (v1.5 whole statement) — a lemma-conjunct here, NOT sufficiency.
- Falsity means: A legal KEEP in some paired execution lacks full legal payment -> route dies.
- Falsity does NOT mean: DOC false; min-form reductions assumed before binding; K6-as-six-slots.
- Statement: (forall (L : Ledger) (y a : Nat), (discharge L (required y a)).2 = Nat.min (activePool L) (required y a)) /\ (forall (T0 : BST) (H : List (Mode * Nat)) (n : Nat), execSuffices { ledger := [], cursor := 0 } T0 T0 H n = true)
- Negation: ~(forall (L : Ledger) (y a : Nat), (discharge L (required y a)).2 = Nat.min (activePool L) (required y a)) \/ (exists (T0 : BST) (H : List (Mode * Nat)) (n : Nat), execSuffices { ledger := [], cursor := 0 } T0 T0 H n = false)
- Proof artifact: `math/proofs/MST0-14_proof.md` (PENDING owner phase).
- Formal artifact: `lean/Proofs/Repayment.lean` (PENDING owner phase).
- Review artifact: `math/reviews/MST0-14.PACKAGE.md` + `math/reviews/MST0-14.review.json` (human verdict only).
- Refutation artifact: `artifacts/v04/proof_attacks/MST0-14/` PSC-K6 record (PENDING owner phase).
