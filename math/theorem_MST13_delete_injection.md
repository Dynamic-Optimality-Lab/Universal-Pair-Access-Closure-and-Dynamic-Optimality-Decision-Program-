# MST0-13 — bounded DELETE injection (6.cost_A(D)) (frozen Phase 1; theorem identity v0.4.7 G11)

- Parent status: PROVED author claim, human review pending (truth UNPROVED until ACCEPT).
- v0.4 owner phase: Phase 2.
- First consumer: MST0-17 (BLOCKED on 13/14/15).
- Prerequisites: frozen definitions + MSTC-0002 binding + v0.3 author-proof transport.
- Child-lemma namespace: `MST0-13/*` (registered, versioned, non-weakening).
- Banned weakening (v1.5, superseded): Bound in injection-count variable k<=6 (v1.5) — NOT the cost-scaled theorem.
- Falsity means: Injection escapes 6.cost_A -> route dies. Bare REJECT never refutes (A2 gates).
- Falsity does NOT mean: DOC false; proof-failure-as-falsity.
- Statement: forall (E : Engine) (A : BST) (x nkeys : Nat), let (E2, _, a) := replayAccessA E A .DELETE x nkeys; energy E2.ledger <= energy E.ledger + 6 * a
- Negation: exists (E : Engine) (A : BST) (x nkeys : Nat), let (E2, _, a) := replayAccessA E A .DELETE x nkeys; energy E2.ledger > energy E.ledger + 6 * a
- Proof artifact: `math/proofs/MST0-13_proof.md` (PENDING owner phase).
- Formal artifact: `lean/Proofs/Injection.lean` (PENDING owner phase).
- Review artifact: `math/reviews/MST0-13.PACKAGE.md` + `math/reviews/MST0-13.review.json` (human verdict only).
- Refutation artifact: `artifacts/v04/proof_attacks/MST0-13/` hostile review + formal transport record (PENDING owner phase).
