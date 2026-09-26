# MST0-08U — universal reference locality (frozen Phase 1; theorem identity v0.4.7 G11)

- Parent status: UNPROVED.
- v0.4 owner phase: Phase 2.
- First consumer: MST0-17.
- Prerequisites: frozen definitions + MSTC-0002 binding; no upstream node.
- Child-lemma namespace: `MST0-08U/*` (registered, versioned, non-weakening).
- Banned weakening (v1.5, superseded): `forall L:Ledger, energy L >= 0`-style tautologies; single-operation cardinality without downstream-consumption uniformity.
- Falsity means: Downstream consumption unbounded -> positive route dies for the locality chain; MSTC-0002 refuted as formulated.
- Falsity does NOT mean: DOC false; any global claim; lift without exact-obstruction reduction (Phase 17).
- Statement: exists L : Nat, forall (A : BST) (x nkeys : Nat) (E : Engine) (ev : StepEv), ev in (splayTrace A x).2 -> (T7inject E true ev.lo ev.hi x nkeys K_frozen).ledger.length <= E.ledger.length + L
- Negation: forall L : Nat, exists (A : BST) (x nkeys : Nat) (E : Engine) (ev : StepEv), ev in (splayTrace A x).2 /\ (T7inject E true ev.lo ev.hi x nkeys K_frozen).ledger.length > E.ledger.length + L
- Proof artifact: `math/proofs/MST0-08U_proof.md` (PENDING owner phase).
- Formal artifact: `lean/Proofs/Locality.lean` (PENDING owner phase).
- Review artifact: `math/reviews/MST0-08U.PACKAGE.md` + `math/reviews/MST0-08U.review.json` (human verdict only).
- Refutation artifact: `artifacts/v04/proof_attacks/MST0-08U/` PSC-L record (PENDING owner phase).
