# MST0-11 — Layer-A proof: transfer preservation, six clauses (WP-2 PROVE track)

Status: PROVED (human Layer-A argument complete; Lean formalization + human
ACCEPT pending — truth stays UNPROVED per lifecycle). Frozen statement:
`math/theorem_MST11_preservation.md` (G11 identity).

## Definitions invoked (frozen only)

`T7inject`, `T5activate`, `activateFirst`, `energy`, `sites`, `StepEv`
(case + interval). All ten obligations (ROOT/ZIG×2/LL/RR/LR/RL × T5/T6/T7
branches per §5) reduce below to interval-parametric facts: every rotation
case emits a `StepEv` with the rotated interval, and every clause depends only
on the interval plus the T7/T5 laws — so one symbolic argument covers all
cases (never finite enumeration as premise). ROOT emits no event (vacuous).

## Proof

Fix arbitrary `E, isA, m, ev, x, nkeys`. Let `E1 = T7inject ...`,
`E2 = T5activate E1 m`.
- C1 (flow identity): T7 appends exactly `|picks|` LATENT credits, so
  `energy` rises by `|picks| = |E1| − |E|`; T5 flips at most one LATENT to
  ACTIVE (both count 1) or nothing, preserving energy. Hence
  `energy(E2) = energy(E) + (|E1| − |E|)`.
- C2 (ownership): positions ≥ |E| in E2 hold appended credits — LATENT, except
  possibly the single flipped position (ACTIVE). Both permitted.
- C3 (non-resurrection): T7 appends LATENT only; T5 changes LATENT→ACTIVE
  only. Every SPENT in E2 occupies a position that was SPENT in E.
- C4 (support containment): appended supports come from
  `sites(lo,hi,x,nkeys)`: each is `(i,i+1)` with `lo ≤ i` (range start) and
  `i+1 ≤ hi` (filter condition). Hence `ev.lo ≤ sup.lo ∧ sup.hi ≤ ev.hi`.
- C5 (no-future-lookup): T5 flips at most the FIRST LATENT, in place (support
  preserved). Every ACTIVE in E2 was ACTIVE in E1 or is that flipped credit
  (LATENT with identical support in E1). No credit is conjured or looked up
  from future state.
- C6 (orientation): `sites` sets `leftOriented = decide (i+1 ≤ x)` with
  `sup.hi = i+1`; hence oriented-true credits end at/below `x`, others start
  above `x`.

## Scope notes

Symbolic over all intervals/sizes/ranks/supports/provenance. Matching Lean
theorem: `lean/Proofs/Preservation.lean` (build-green: helpers + `MST0_11_flow_identity` + full `MST0_11_proved`). Attack
evidence: PSC-P campaign (NO_WITNESS, all 24 case/mode/side combos covered,
checker AGREE).
