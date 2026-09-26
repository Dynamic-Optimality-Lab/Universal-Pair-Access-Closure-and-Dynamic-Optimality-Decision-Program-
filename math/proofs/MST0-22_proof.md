# MST0-22 — Layer-A proof: constant independence, uniformity law (WP-2 PROVE track)

Status: PROVED (human Layer-A argument complete; Lean formalization + human
ACCEPT pending — truth stays UNPROVED per lifecycle). Frozen statement:
`math/theorem_MST22_constant_independence.md` (G11 identity).

## Definitions invoked (frozen only)

`C_frozen`, `K_frozen`, `required`, `regret`, `T7inject`.

## Proof

Three conjuncts. (1) Literals: `C_frozen = 2 ∧ K_frozen = 6` by definition.
(2) C-linkage: unfolding gives `required y a = Int.toNat (y − 2·a)` for all
`y, a`; with (1) this is `Int.toNat (y − C_frozen·a)` — regret is computed
with the frozen constant, not a parameter. (3) K-uniformity: for all inputs
with `k ≤ K_frozen`, T7 picks over `List.range k`, so growth ≤ k ≤ 6 =
K_frozen — the 08U argument with general k. Supports/orientation affect
credit identity only, never the count. Hence one constant pair governs all
inputs; no forbidden input (n, history, seed, decomposition, holdout)
enters any constant. Support-only scan (`constants_scan.py` CLEAN) attached;
scanner output is support, never the proof.

## Scope notes

No minimality claimed; no silent relaxation (new constants need a new
experiment ID). Matching Lean theorem: `lean/Proofs/Constants.lean` (build-green: `MST0_22_proved`).
Hidden-dependence attack surface: none found by scan.
