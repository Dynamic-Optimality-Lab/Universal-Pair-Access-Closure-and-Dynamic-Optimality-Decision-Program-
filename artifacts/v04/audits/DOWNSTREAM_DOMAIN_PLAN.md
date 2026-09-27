# Downstream domain dispositions after MST0-14R refutation (append-only plan note)

No frozen theorem doc, battlefield entry, gate-matrix row, Lean Frozen
module, or proof_status.json node was modified. This note is the minimum
dependency/domain plumbing (task Sec 30).

## MST0-15 — preserved TOTAL (no guard added)

D1-D4 quantify over arbitrary `Ledger/need` (pure discharge algebra; no
tree/history/universe quantifiers — nothing to guard). D5 (history-partition
consistency over `execTrees/execLoop`) was re-executed on the malformed
n=0 witness: both sides equal (determinism holds regardless of legality).
Per the strongest-true-theorem rule, NO legal-domain premise is added to
MST0-15. Its owner-phase proof work (WP-4) is unaffected by the MST0-14R
refutation except that MST0-15 can no longer feed a live Pair-Access
composition through the repayment node.

## MST0-17 / MST0-18 — raw-domain hygiene issue confirmed, NOT refuted

Both state `exists A : Nat -> Nat, forall E0/T0/H/n ...` with the inner
universal ranging over illegal instances (keys outside `[n]`, trees outside
the universe). The current witnesses do NOT refute them (witness checks
satisfy with `A(0)=0`; an `exists`-statement needs a uniform family to
refute). Lawful repair is a versioned successor with a LegalPairInstance-
style guard, owned by the WP-5 phase — NOT performed here (out of scope;
no WP-4/WP-5 mathematics attempted).

## Consumption guard (dependency plumbing)

MST0-17 PROVE requires MST0-08U/09/11/13/14/15/22 REVIEWED. The MST0-14
slot can never be filled: the frozen identity is doubly falsified
(malformed-domain witness + legal witness) and its repaired successor
MST0-14R is mathematically refuted (lifecycle: UNPROVED pending human G5
validation in both ledgers). Downstream phases must not consume any
repayment premise. If WP-5 ever proceeds, it must route around the
repayment node (new calculus = new experiment ID) or activate Phase-6
negative lifting from the preserved closed-form obstruction family
(`artifacts/v04/counterexamples/MST0-14R/MST0-14R_LEGAL_WITNESS.json`,
residual ~ -n/4 unbounded).
