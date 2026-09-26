# MST0-08U — Layer-A proof: universal reference locality (WP-2 PROVE track)

Status: PROVED (human Layer-A argument complete; Lean formalization + human
ACCEPT pending — truth stays UNPROVED per lifecycle). Frozen statement:
`math/theorem_MST08U_locality.md` (G11 identity).

## Definitions invoked (frozen only)

`T7inject E isA lo hi x nkeys k`, `sites`, `K_frozen = 6`, `splayTrace`.

## Proof

Take L = 6. Fix arbitrary `E`, `isA`, `lo`, `hi`, `x`, `nkeys`, and a real
rotation event `ev ∈ (splayTrace A x).2` for arbitrary `A`.
`T7inject E true ev.lo ev.hi x nkeys K_frozen` computes `ss = sites ...` and
`picks` by filtering over `List.range K_frozen`; hence `|picks| ≤ K_frozen = 6`
for every input (a filter cannot lengthen a length-6 list). The new ledger is
`E.ledger ++ new-credits`, so it grows by exactly `|picks| ≤ 6 = L`.
For `isA = false` the engine is unchanged (growth 0 ≤ L).
The bound uses nothing about `A`, `x`, `ev`, or `nkeys` beyond the event
interval — one constant for all inputs (uniformity = locality).

## Scope notes

This proves the per-event downstream-consumption bound. No finite maxima are premises (the argument is uniform, LOC-07 clean).
Matching Lean theorem: `lean/Proofs/Locality.lean` (pending build-green).
Attack evidence: PSC-L campaign (NO_WITNESS, checker AGREE).
