# MST0-09 — Layer-A proof: raw boundary cost-bearing-source law (WP-2 PROVE track)

Status: PROVED (human Layer-A argument complete; Lean formalization + human
ACCEPT pending — truth stays UNPROVED per lifecycle). Frozen statement:
`math/theorem_MST09_raw_boundary.md` (G11 identity).

## Definitions invoked (frozen only)

`replayAccessA`, `splayTrace`, `replayStep = T5 ∘ T7`, `energy`, 08U/11-C1
lemmas (proved above, same track — consumed only if REVIEWED; cited as
sibling argument here, dependency recorded).

## Proof

Take C9 = 6. Fix arbitrary `A, x, nkeys, E`. `replayAccessA E A KEEP x nkeys`
folds `replayStep` over `evs = (splayTrace A x).2`. Per step: T7 adds at most
6 LATENT credits (08U argument with k = 6), and T5 preserves energy (11-C1
shape), so each step grows energy by at most 6. By induction over the fold,
after all `|evs|` steps `energy(E2) ≤ energy(E) + 6·|evs|`.
Cost-bearing-source reading: every unit of growth is created by the T7
injection of exactly one rotation event — the event IS the source, identified
by its trace interval. The 12 boundary classes (nested/alternating/
creation-rate/rank-gap/span/burden/burst/lifetime/reactivation/asymmetry/
mirror/scale) are all trace-event families over legal BSTs, hence covered by
the uniform per-event bound; no class needs a separate constant.

## Scope notes

No finite enumeration as premise (bound uniform over all inputs). Matching
Lean theorem: `lean/Proofs/Boundary.lean` (build-green: `MST0_09_proved`). Attack
evidence: PSC-B campaign (NO_WITNESS, 12 classes, checker AGREE).
