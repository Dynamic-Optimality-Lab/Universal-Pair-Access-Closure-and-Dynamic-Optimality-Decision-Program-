# MST0-22 — constant independence (uniformity law) (frozen Phase 1; theorem identity v0.4.7 G11)

- Parent status: UNPROVED.
- v0.4 owner phase: Phase 2.
- First consumer: MST0-17 (constants govern the composition bound).
- Prerequisites: frozen definitions + MSTC-0002 binding; no upstream node.
- Child-lemma namespace: `MST0-22/*` (registered, versioned, non-weakening).
- Banned weakening (v1.5, superseded): Bare `C_frozen = 2 /\ K_frozen = 6` literal equality (v1.5) — NOT independence from forbidden inputs.
- Falsity means: Constants depend on forbidden inputs or vary across inputs -> route dies.
- Falsity does NOT mean: Minimality claims; silent relaxation under v0.4 ID.
- Statement: (C_frozen = 2 /\ K_frozen = 6) /\ (forall y a : Nat, required y a = Int.toNat ((y : Int) - (C_frozen : Int) * (a : Int))) /\ (forall (E : Engine) (isA : Bool) (lo hi x nkeys k : Nat), k <= K_frozen -> (T7inject E isA lo hi x nkeys k).ledger.length <= E.ledger.length + K_frozen)
- Negation: ~(C_frozen = 2 /\ K_frozen = 6) \/ (exists y a : Nat, required y a != Int.toNat ((y : Int) - (C_frozen : Int) * (a : Int))) \/ (exists (E : Engine) (isA : Bool) (lo hi x nkeys k : Nat), k <= K_frozen /\ (T7inject E isA lo hi x nkeys k).ledger.length > E.ledger.length + K_frozen)
- Proof artifact: `math/proofs/MST0-22_proof.md` (PENDING owner phase).
- Formal artifact: `lean/Proofs/Constants.lean` (PENDING owner phase).
- Review artifact: `math/reviews/MST0-22.PACKAGE.md` + `math/reviews/MST0-22.review.json` (human verdict only).
- Refutation artifact: `artifacts/v04/proof_attacks/MST0-22/` constant-attack record (PENDING owner phase).
