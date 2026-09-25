# SPLAY-AM-DECIDE v0.4.1 — Ratified Pre-Freeze Amendment / Normative Freeze Addendum

**Status:** `RATIFIED` — issued before `FOUNDATION_FROZEN`; part of the normative v0.4 stack.
**Date ratified:** 2026-09-25 UTC
**Amends:** `IMPLEMENTATION_SPEC_v0.4.md` (byte-identity preserved — adds, never edits, the v0.4 text).
**Authored because:** review found three places where the repaired plan is scientifically preferable to a literal reading of the v0.4 text, plus one terminal-state hole. This amendment ratifies the repaired rules so “spec-compliant” and “scientifically correct” coincide.

## A1. Parent pin (restated)

`PRE_FREEZE_PARENT_PIN_REQUIRED` is discharged only by the Phase-00 pin: full sealed HEAD `353ee922b1cee0043afa46fe8929f42f7652e5bf` (short `353ee92`), terminal `TRANSFER_CALCULUS_SURVIVES_FINITE_TESTS`, ancestor chain `38c1be6afd2ab2420aa094c68ce45ee6a26b3628` / `6de1ca2a595e8895f54794f3a211fe6ee1a95a80`. Any `PARENT_SEAL_MISMATCH` blocks execution.

## A2. MST0-13 REJECT != REFUTED (overrides literal Phase-05 reading)

A human `REJECT` (or `BLOCKED`) sets only the reviewer gate (`MST0_13_REJECTED` / `MST0_13_BLOCKED`) and records a positive-route blockage. `proof_status.json` stays `UNPROVED` unless an exact negation witness independently justifies `REFUTED`. A bare `REJECT`/`BLOCKED` without a preserved exact negation witness does NOT activate obstruction lifting. Phase 17 activates only on a preserved exact theorem obstruction/witness (or proved-false Pair-Access/bridge under frozen conventions).

## A3. New terminal level: POSITIVE_ROUTE_BLOCKED_UNRESOLVED_NO_CLAIM

Phase 18 previously permitted exactly five outcomes, none truthfully describing “a critical theorem remains unresolved (REJECT/BLOCKED/unproved) with no refutation and no resource failure.” The permitted set is exactly six:

```text
DYNAMIC_OPTIMALITY_PROVED
DYNAMIC_OPTIMALITY_DISPROVED
POSITIVE_ROUTE_REFUTED_NO_DOC_NEGATIVE
POSITIVE_ROUTE_BLOCKED_UNRESOLVED_NO_CLAIM   (new)
BRIDGE_BLOCKED_NO_CLAIM
RESOURCE_LIMIT_NO_CLAIM
```

Allowed: “positive route blocked at named unresolved theorem(s); no refutation, no resource failure, no YES/NO.” Forbidden: calling it refutation/DOC-disproof/bridge/resource verdict; consuming the blocked theorem; erasing the blockage. YES/NO remain the only successes.

## A4. Bridge-source ordering ratification

L2/L3 acquisition is a Phase-00 foundation input completed BEFORE `FOUNDATION_FROZEN` in `prereg/bridge_sources.yaml`. Spec Phase 02 verifies those bytes and writes only `artifacts/v04/freeze/PHASE02_BRIDGE_SOURCES_FREEZE.json` — never a prereg rewrite, preserving “no prereg rewrite after `FOUNDATION_FROZEN`.”

## A5. Frozen stack

1. `IMPLEMENTATION_SPEC_v0.4.md` (byte-identity), 2. this amendment, 3. `WorkPlan.md` final pre-freeze revision, 4. `Path.md` (living, versioned by history), 5. `prereg/` hashed in `prereg_sha256.txt` (includes this amendment by reference at freeze).

## A6. Effect

Divergences are compliant by amendment, not silent deviation. `FOUNDATION_FROZEN` requires Phase-1 exit criteria green. Future changes need versioned amendments; v0.4 never edited in place.
