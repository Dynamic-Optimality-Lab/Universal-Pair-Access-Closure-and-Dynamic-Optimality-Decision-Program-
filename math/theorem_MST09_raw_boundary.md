# MST0-09 — raw boundary cost-bearing-source law (frozen Phase 1; theorem identity v0.4.7 G11)

- Parent status: UNPROVED.
- v0.4 owner phase: Phase 2.
- First consumer: MST0-17 (via repayment/integrability consumption).
- Prerequisites: frozen definitions + MSTC-0002 binding; no upstream node.
- Child-lemma namespace: `MST0-09/*` (registered, versioned, non-weakening).
- Banned weakening (v1.5, superseded): `forall L:Ledger, energy L >= 0` (Nat tautology) frozen in v1.5 — NOT this theorem.
- Falsity means: Boundary costs escape universal bound -> route dies for the boundary chain.
- Falsity does NOT mean: Any finite maximum observed is the law (finite!=proof); DOC false.
- Statement: exists C9 : Nat, forall (A : BST) (x nkeys : Nat) (E : Engine), energy (replayAccessA E A .KEEP x nkeys).1.ledger <= energy E.ledger + C9 * (splayTrace A x).2.length
- Negation: forall C9 : Nat, exists (A : BST) (x nkeys : Nat) (E : Engine), energy (replayAccessA E A .KEEP x nkeys).1.ledger > energy E.ledger + C9 * (splayTrace A x).2.length
- Proof artifact: `math/proofs/MST0-09_proof.md` (PENDING owner phase).
- Formal artifact: `lean/Proofs/Boundary.lean` (PENDING owner phase).
- Review artifact: `math/reviews/MST0-09.PACKAGE.md` + `math/reviews/MST0-09.review.json` (human verdict only).
- Refutation artifact: `artifacts/v04/proof_attacks/MST0-09/` PSC-B record (PENDING owner phase).
