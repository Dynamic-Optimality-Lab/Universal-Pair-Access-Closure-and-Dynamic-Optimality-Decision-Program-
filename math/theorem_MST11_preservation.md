# MST0-11 — transfer preservation (frozen Phase 1; v0.4 §6, §10)

- Parent status: UNPROVED.
- v0.4 owner phase: Phase 2 (WorkPlan §5; symbolic primitive-exhaustion attack).
- First consumer: MST0-17 (Pair-Access composition; via the required-guard chain).
- Prerequisites: frozen SplayDefs/MSTC0002Defs + MSTC-0002 binding; no upstream node.
- Child-lemma namespace: `MST0-11/*` (registered, versioned, non-weakening).
- Forbidden premises: parent holdout (H3T) reuse; finite enumeration as premise
  (all 10 preservation obligations discharged symbolically); un-frozen literature.
- Falsity consequence: positive route dies for the preservation-dependent chain;
  MSTC-0002 refuted as currently formulated (no DOC-negative lift without an
  exact-obstruction reduction at Phase 17).
- Statement: forall (E : Engine) (m : Mode), energy (T5activate E m).ledger = energy E.ledger
- Negation: exists (E : Engine) (m : Mode), energy (T5activate E m).ledger != energy E.ledger
- Proof artifact: `math/proofs/MST0-11_proof.md` (PENDING Phase 2; ROOT/ZIG-left/ZIG-right/LL/RR/LR/RL x every T5/T6/T7 branch, arbitrary intervals/sizes/ranks/supports/provenance).
- Formal artifact: `lean/Proofs/Preservation.lean` (PENDING Phase 2).
- Review artifact: `math/reviews/MST0-11.PACKAGE.md` + `math/reviews/MST0-11.review.json` (human verdict only).
- Refutation artifact: `artifacts/v04/proof_attacks/MST0-11/` PSC-P attack record (PENDING Phase 2).
