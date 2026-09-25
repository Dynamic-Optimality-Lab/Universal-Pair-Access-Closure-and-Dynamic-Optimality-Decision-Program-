# MST0-22 — constant independence (frozen Phase 1; v0.4 §6, §13)

- Parent status: UNPROVED.
- v0.4 owner phase: Phase 2 (WorkPlan §5).
- First consumer: MST0-17 (Pair-Access composition; C = 2 and k = 6 govern the composition bound).
- Prerequisites: frozen SplayDefs/MSTC0002Defs + MSTC-0002 binding; no upstream node.
- Child-lemma namespace: `MST0-22/*` (registered, versioned, non-weakening).
- Forbidden premises: silent constant relaxation under the v0.4 ID (new constants need a new
  experiment ID); minimality claims; finite evidence for n-independence.
- Falsity consequence: positive route dies; MSTC-0002 refuted as currently formulated
  (no DOC-negative lift without an exact-obstruction reduction at Phase 17).
- Statement: C_frozen = 2 /\ K_frozen = 6
- Negation: C_frozen != 2 \/ K_frozen != 6
- Proof artifact: `math/proofs/MST0-22_proof.md` (PENDING Phase 2).
- Formal artifact: `lean/Proofs/Constants.lean` (PENDING Phase 2).
- Review artifact: `math/reviews/MST0-22.PACKAGE.md` + `math/reviews/MST0-22.review.json` (human verdict only).
- Refutation artifact: `artifacts/v04/proof_attacks/MST0-22/` attack record (PENDING Phase 2).
