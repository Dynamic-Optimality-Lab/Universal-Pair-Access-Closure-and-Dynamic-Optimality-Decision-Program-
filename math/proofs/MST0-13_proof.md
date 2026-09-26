# MST0-13 — hostile-review transport analysis (WP-2, Phase 05)

Status: PROVED author claim TRANSPORTED (v0.3) + hostile analysis complete;
human review pending — truth UNPROVED until human ACCEPT (reviewer gates
`MST0_13_REJECTED`/`MST0_13_BLOCKED` per A2 on REJECT/BLOCKED). Frozen
statement: `math/theorem_MST13_delete_injection.md` (G11 identity:
E_after − E_before ≤ 6·cost_A(D) with executed cost).

## Transported formalization under review

`replayAccessA E A DELETE x nkeys = (E2, _, a)` with `a = splayCost A x`
(depth+1, executed). Per-step growth ≤ 6 (09 argument) gives
`energy(E2) ≤ energy(E) + 6·|evs|`. Key lemma (review focus): `|evs| ≤ a`.
Proof of lemma: the descend context at focus has length exactly `depth(x)`
(one frame per level); `splayWithT` consumes ≥1 frame per emitted event
(zig 1, doubles 2); events partition the frame list; hence
`|evs| ≤ depth ≤ depth+1 = a`. Therefore growth ≤ 6·a. Absent-x paths:
descend fails → empty trace → growth 0 ≤ 6·a (endpoint covered).

## Hostile checklist (for the human reviewer)

- Rotation-count≤cost: lemma above (all cases; ROOT/ZIG/LL/RR/LR/RL emit).
- T7-bound: 08U per-event ≤ 6 with k = 6.
- T5-conservation: 11-C1 (activation preserves energy).
- T6-inapplicability: DELETE side performs no discharge (replayStep = T7+T5 only).
- Case completeness: every splay case emits StepEv (Lean match total, compiler-checked).
- Granularity: per-event accounting, never per-access assumed.
- Endpoints: absent-x and empty-history cases exact.
- K6-as-slots: not used (T043/INV-053/STOP-38 clean).
- v0.3 author-claim mapping: bounded-DELETE-injection claim restated over frozen
  defs above; no content added or relaxed in transport.

## Scope notes

ACCEPT requires human verification of the lemma + formal green; bare REJECT
never refutes. Matching Lean development: `lean/Proofs/Injection.lean` (build-green: `MST0_13_proved` + descend/loop/cost lemmas).
Evidence package: `math/reviews/MST0-13.PACKAGE.md` (verdict PENDING-HUMAN).
