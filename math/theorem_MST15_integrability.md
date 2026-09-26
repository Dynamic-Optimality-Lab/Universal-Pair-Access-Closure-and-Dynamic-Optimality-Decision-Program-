# MST0-15 — global integrability (five-clause law) (frozen Phase 1; theorem identity v0.4.7 G11)

- Parent status: UNPROVED.
- v0.4 owner phase: Phase 4.
- First consumer: MST0-17 (BLOCKED on 13/14/15).
- Prerequisites: frozen definitions + MSTC-0002 binding (Phase-4 proves global reading).
- Child-lemma namespace: `MST0-15/*` (registered, versioned, non-weakening).
- Banned weakening (v1.5, superseded): One-step conservation identity alone (v1.5) — NOT no-double-spend/lifecycle/splitting/partition law.
- Falsity means: Double spend, lifecycle violation, decomposition dependence, or partition inconsistency -> route dies.
- Falsity does NOT mean: DOC false; local-to-global inference without D5.
- Statement: (forall (L : Ledger) (need : Nat) (c : Credit), c in L -> c.ctype = .SPENT -> c in (discharge L need).1) /\ (forall (L : Ledger) (need : Nat) (c : Credit), c in (discharge L need).1 -> c.ctype = .SPENT -> c in L \/ (exists c0, c0 in L /\ c0.ctype = .ACTIVE /\ c.sup = c0.sup)) /\ (forall (L : Ledger) (n1 n2 : Nat), (discharge L (n1 + n2)).2 = (discharge L n1).2 + (discharge (discharge L n1).1 n2).2 /\ (discharge (discharge L n1).1 n2).1 = (discharge L (n1 + n2)).1) /\ (forall (L : Ledger) (need : Nat), activePool (discharge L need).1 + (discharge L need).2 = activePool L) /\ (forall (E0 : Engine) (T0 : BST) (H1 H2 : List (Mode * Nat)) (n : Nat), let (E1, A1, B1, sA1, sB1) := execTrees E0 T0 T0 H1 n; execLoop E1 A1 B1 n H2 sA1 sB1 = execLoop E0 T0 T0 n (H1 ++ H2) 0 0)
- Negation: (exists (L : Ledger) (need : Nat) (c : Credit), ~((forall (L : Ledger) (need : Nat) (c : Credit), c in L -> c.ctype = .SPENT -> c in (discharge L need).1) /\ (forall (L : Ledger) (need : Nat) (c : Credit), c in (discharge L need).1 -> c.ctype = .SPENT -> c in L \/ (exists c0, c0 in L /\ c0.ctype = .ACTIVE /\ c.sup = c0.sup)))) \/ (exists (L : Ledger) (n1 n2 : Nat), ~(forall (L : Ledger) (n1 n2 : Nat), (discharge L (n1 + n2)).2 = (discharge L n1).2 + (discharge (discharge L n1).1 n2).2 /\ (discharge (discharge L n1).1 n2).1 = (discharge L (n1 + n2)).1)) \/ (exists (L : Ledger) (need : Nat), activePool (discharge L need).1 + (discharge L need).2 != activePool L) \/ (exists (E0 : Engine) (T0 : BST) (H1 H2 : List (Mode * Nat)) (n : Nat), let (E1, A1, B1, sA1, sB1) := execTrees E0 T0 T0 H1 n; execLoop E1 A1 B1 n H2 sA1 sB1 != execLoop E0 T0 T0 n (H1 ++ H2) 0 0)
- Proof artifact: `math/proofs/MST0-15_proof.md` (PENDING owner phase).
- Formal artifact: `lean/Proofs/Integrability.lean` (PENDING owner phase).
- Review artifact: `math/reviews/MST0-15.PACKAGE.md` + `math/reviews/MST0-15.review.json` (human verdict only).
- Refutation artifact: `artifacts/v04/proof_attacks/MST0-15/` PSC-I record (PENDING owner phase).
