# SPLAY-AM-DECIDE v0.4.3 — Ratified Pre-Freeze Amendment / Dual-Gate Execution Semantics

**Status:** `RATIFIED` — issued before `FOUNDATION_FROZEN`; part of the normative v0.4 stack.
**Date ratified:** 2026-09-25 UTC
**Amends:** `IMPLEMENTATION_SPEC_v0.4.md` §21 execution order (refines the single `ASSERT THEOREM GATES` line into two explicit gate asserts; adds no new theorems, alters no statement, constant, or calculus).
**Authored because:** a single phase-level `NOT_REACHED` gate contradicts the dual PROVE/REFUTE obligation: refutation needs only frozen inputs while proof needs reviewed prerequisites. Without separation, the plan both demands and prohibits the REFUTE track.

## C1. REFUTE_READY vs PROVE_READY (normative)

```text
REFUTE_READY(L) = frozen foundation + frozen exact statement/negation of L
  + survivor binding + exact executable semantics + PSC/interface conformance.

PROVE_READY(L) = REFUTE_READY(L)
  + every logical prerequisite required by PROVE(L) is REVIEWED.
```

- `REFUTE(L)` may execute whenever `REFUTE_READY(L)` holds.
- `PROVE(L)` may execute only whenever `PROVE_READY(L)` holds.
- `REFUTED(L)` freezes later POSITIVE-route consumption and, when the obstruction is eligible, activates negative lifting (Phase 6).
- Proof failure, human REJECT, or BLOCKED never equals `REFUTED` without an exact negation witness (v0.4.1 A2).

## C2. Bifurcated gate asserts in the §21 order

The single `ASSERT THEOREM GATES` step is executed as two explicit asserts:

```text
ASSERT FOUNDATION / REFUTATION GATES   (before LOAD THEOREM + NEGATION)
LOAD EXACT THEOREM + NEGATION
RUN REFUTATION ATTACK FIRST OR IN PARALLEL
ASSERT POSITIVE PROOF DEPENDENCY GATES (before DEVELOP / CHECK PROOF)
DEVELOP / CHECK PROOF
```

The remaining §21 steps are unchanged. `NOT_REACHED` is always per-track: a closed proof gate marks `PROVE(L)` not reached, never the phase's `REFUTE(L)`.

## C3. Phase-gate readings fixed by C1–C2

- Phase 3: `REFUTE(MST0-14)` (PHASE 10) runnable on `REFUTE_READY`; `PROVE(MST0-14)` (PHASE 11) only on all-five-upstream REVIEWED.
- Phase 4: `REFUTE(MST0-15)` (PHASE 12, Double-Spend Apocalypse) runnable on `REFUTE_READY`; `PROVE(MST0-15)` (PHASE 13) only on MST0-14 REVIEWED.
- Phase 5: `REFUTE(MST0-17)` runnable on `REFUTE_READY` with NO upstream-REVIEWED requirement (the endpoint-aware negation instantiates from the frozen statement + frozen semantics alone); `PROVE(MST0-17/18/19)` only on all-seven-upstream REVIEWED.
- “Later phases NOT_REACHED” always means later POSITIVE-route phases; exact refutation ACTIVATES Phase 6.

## C4. Effect

C1–C3 are the normative gate model; WorkPlan v1.1 implements them per-phase. v0.4/v0.4.1/v0.4.2 bytes preserved. Future changes need versioned amendments.
