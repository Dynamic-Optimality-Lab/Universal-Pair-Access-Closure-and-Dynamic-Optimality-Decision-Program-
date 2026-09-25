# MST0-15 — global integrability (frozen Phase 1; v0.4 §6, §15)

- Parent status: UNPROVED.
- v0.4 owner phase: Phase 4 (WorkPlan §7; PSC-I Double-Spend Apocalypse, spec PHASE 12-13).
- First consumer: MST0-17 (BLOCKED on 13/14/15).
- Prerequisites: frozen SplayDefs/MSTC0002Defs + MSTC-0002 binding; no upstream node
  (Phase-4 proves global coexistence: no decomposition dependence, no duplicate consumption).
- Child-lemma namespace: `MST0-15/*` (registered, versioned, non-weakening).
- Forbidden premises: parent holdout (H3T) reuse; local-to-global inference without the
  global proof; double consumption; un-frozen literature.
- Falsity consequence: positive route dies; MSTC-0002 refuted as currently formulated
  (no DOC-negative lift without an exact-obstruction reduction at Phase 17).
- Statement: forall (L : Ledger) (need : Nat), activePool (discharge L need).1 + (discharge L need).2 = activePool L
- Negation: exists (L : Ledger) (need : Nat), activePool (discharge L need).1 + (discharge L need).2 != activePool L
- Proof artifact: `math/proofs/MST0-15_proof.md` (PENDING Phase 4; human global + endpoint theorems).
- Formal artifact: `lean/Proofs/Integrability.lean` (PENDING Phase 4).
- Review artifact: `math/reviews/MST0-15.PACKAGE.md` + `math/reviews/MST0-15.review.json` (human verdict only).
- Refutation artifact: `artifacts/v04/proof_attacks/MST0-15/` PSC-I attack record (PENDING Phase 4).
