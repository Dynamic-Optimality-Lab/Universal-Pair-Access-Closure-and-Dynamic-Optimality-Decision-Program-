# MST0-11 — transfer preservation (six-clause rotation-case law) (frozen Phase 1; theorem identity v0.4.7 G11)

- Parent status: UNPROVED.
- v0.4 owner phase: Phase 2.
- First consumer: MST0-17 (required-guard chain).
- Prerequisites: frozen definitions + MSTC-0002 binding; no upstream node.
- Child-lemma namespace: `MST0-11/*` (registered, versioned, non-weakening).
- Banned weakening (v1.5, superseded): Lone energy equality (v1.5 C1-shape) — NOT the ten preservation obligations.
- Falsity means: A rotation case breaks accounting identity -> route dies for the preservation chain.
- Falsity does NOT mean: DOC/global inference; finite case sampling as premise (all cases symbolic).
- Statement: forall (E : Engine) (isA : Bool) (m : Mode) (ev : StepEv) (x nkeys : Nat), let E1 := T7inject E isA ev.lo ev.hi x nkeys K_frozen; let E2 := T5activate E1 m; energy E2.ledger = energy E.ledger + (E1.ledger.length - E.ledger.length) /\ (forall c in E2.ledger.drop E.ledger.length, c.ctype = .LATENT \/ c.ctype = .ACTIVE) /\ (forall c in E2.ledger, c.ctype = .SPENT -> c in E.ledger) /\ (forall c in E2.ledger.drop E.ledger.length, ev.lo <= c.sup.lo /\ c.sup.hi <= ev.hi) /\ (forall c in E2.ledger, c.ctype = .ACTIVE -> c in E1.ledger \/ (exists c0, c0 in E1.ledger /\ c0.ctype = .LATENT /\ c.sup = c0.sup)) /\ (forall c in E2.ledger.drop E.ledger.length, (c.sup.leftOriented = true -> c.sup.hi <= x) /\ (c.sup.leftOriented = false -> x < c.sup.hi))
- Negation: exists (E : Engine) (isA : Bool) (m : Mode) (ev : StepEv) (x nkeys : Nat), let E1 := T7inject E isA ev.lo ev.hi x nkeys K_frozen; let E2 := T5activate E1 m; ~(energy E2.ledger = energy E.ledger + (E1.ledger.length - E.ledger.length) /\ (forall c in E2.ledger.drop E.ledger.length, c.ctype = .LATENT \/ c.ctype = .ACTIVE) /\ (forall c in E2.ledger, c.ctype = .SPENT -> c in E.ledger) /\ (forall c in E2.ledger.drop E.ledger.length, ev.lo <= c.sup.lo /\ c.sup.hi <= ev.hi) /\ (forall c in E2.ledger, c.ctype = .ACTIVE -> c in E1.ledger \/ (exists c0, c0 in E1.ledger /\ c0.ctype = .LATENT /\ c.sup = c0.sup)) /\ (forall c in E2.ledger.drop E.ledger.length, (c.sup.leftOriented = true -> c.sup.hi <= x) /\ (c.sup.leftOriented = false -> x < c.sup.hi)))
- Proof artifact: `math/proofs/MST0-11_proof.md` (PENDING owner phase).
- Formal artifact: `lean/Proofs/Preservation.lean` (PENDING owner phase).
- Review artifact: `math/reviews/MST0-11.PACKAGE.md` + `math/reviews/MST0-11.review.json` (human verdict only).
- Refutation artifact: `artifacts/v04/proof_attacks/MST0-11/` PSC-P record (PENDING owner phase).
