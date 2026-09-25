# SPLAY-AM-DECIDE v0.4.1 — Ratified Pre-Freeze Amendment / Normative Freeze Addendum

**Status:** `RATIFIED` — this amendment is issued before `FOUNDATION_FROZEN` and forms part of the normative v0.4 stack.
**Date ratified:** 2026-09-25 UTC
**Amends:** `IMPLEMENTATION_SPEC_v0.4.md` (byte-identity preserved — this file adds the amendment; it does not edit the v0.4 text).
**Authored because:** external review of `WorkPlan.md` v0.4-WP2 found three places where the repaired plan was scientifically preferable to a literal reading of the v0.4 text, plus one terminal-state hole. This amendment ratifies the repaired rules so “spec-compliant” and “scientifically correct” coincide. The WorkPlan was not reverted.

## A1. Parent pin (unchanged, restated for completeness)

The `PRE_FREEZE_PARENT_PIN_REQUIRED` condition is discharged only by the Phase-00 pin recorded in `WorkPlan.md` Phase 1 / `parent/README.md`: full sealed HEAD `353ee922b1cee0043afa46fe8929f42f7652e5bf` (short `353ee92`), terminal `TRANSFER_CALCULUS_SURVIVES_FINITE_TESTS`, ancestor chain `38c1be6afd2ab2420aa094c68ce45ee6a26b3628` / `6de1ca2a595e8895f54794f3a211fe6ee1a95a80`. Any `PARENT_SEAL_MISMATCH` against sealed bytes blocks execution.

## A2. MST0-13 REJECT != REFUTED (BLOCKER fix; overrides literal Phase-05 reading)

The v0.4 text Phase 05 can be read as routing reviewer outcome `MST0_13_REJECTED` into the positive-route-failure record and Phase-17 negative lifting. That reading is hereby narrowed:

- A human `REJECT` (or `BLOCKED`) on the MST0-13 review package sets only the reviewer gate (`MST0_13_REJECTED` / `MST0_13_BLOCKED`) and records a positive-route blockage.
- `proof_status.json` for `MST0-13` remains `UNPROVED` unless an exact negation witness independently justifies `REFUTED` under the §7 lifecycle. A bad or incomplete proof is not automatically a false theorem.
- A bare `REJECT`/`BLOCKED` without a preserved exact negation witness does NOT activate obstruction lifting. Phase 17 activates only on a preserved exact theorem obstruction/witness (or a proved-false Pair-Access/bridge theorem under frozen conventions).

## A3. New terminal level: POSITIVE_ROUTE_BLOCKED_UNRESOLVED_NO_CLAIM (BLOCKER fix; closes the terminal-state hole)

Phase 18 previously permitted exactly five theorem-facing outcomes, none of which truthfully described “a critical theorem remains unresolved (REJECT/BLOCKED/unproved) with no refutation and no resource failure.” Forcing such a stop into `POSITIVE_ROUTE_REFUTED_NO_DOC_NEGATIVE` would be false (nothing was refuted) and into `RESOURCE_LIMIT_NO_CLAIM` would be false (no exhaustion). The permitted set is therefore exactly six:

```text
DYNAMIC_OPTIMALITY_PROVED
DYNAMIC_OPTIMALITY_DISPROVED
POSITIVE_ROUTE_REFUTED_NO_DOC_NEGATIVE
POSITIVE_ROUTE_BLOCKED_UNRESOLVED_NO_CLAIM   (new)
BRIDGE_BLOCKED_NO_CLAIM
RESOURCE_LIMIT_NO_CLAIM
```

- Allowed claim for the new level: “The positive route is blocked at the named unresolved theorem(s) (reviewer REJECT/BLOCKED or UNPROVED with open proof obligations); no refutation and no resource failure is claimed; no YES/NO follows.”
- Forbidden: calling it a refutation, a DOC disproof, a bridge verdict, or a resource verdict; consuming the blocked theorem downstream; erasing the blockage record.
- YES (`DYNAMIC_OPTIMALITY_PROVED`) and NO (`DYNAMIC_OPTIMALITY_DISPROVED`) remain the only successful outcomes. The new level is an honest no-claim like the other three.

## A4. Bridge-source ordering ratification (MAJOR/FORMAL fix; deliberate deviation ratified)

The v0.4 text assigns L2/L3 acquisition to Phase 02. The ratified execution order is:

- Source acquisition (lawful exact L2/L3 bytes + manifest) is a Phase-00 foundation input completed BEFORE `FOUNDATION_FROZEN` and recorded immutably in `prereg/bridge_sources.yaml`.
- Spec Phase 02 then independently verifies the already-acquired bytes (second extraction, convention checklist) and writes only the separate certificate `artifacts/v04/freeze/PHASE02_BRIDGE_SOURCES_FREEZE.json` — never a prereg rewrite.
- This preserves “no prereg rewrite after `FOUNDATION_FROZEN`” with zero contradiction. Phase-00 text reading “source acquisition is a foundation input; Phase 02 verifies and freezes its theorem extraction” is normative under this amendment.

## A5. What is frozen by this amendment

The normative v0.4 stack is exactly:

1. `IMPLEMENTATION_SPEC_v0.4.md` (byte-identity),
2. this amendment (`SPLAY_AM_DECIDE_IMPLEMENTATION_SPEC_v0.4.1_AMENDMENT.md`),
3. `WorkPlan.md` v0.4-WP3 (which implements A2–A4),
4. `Path.md` (living tracker — versioned by commit history, not frozen text),
5. `prereg/` contents hashed in `prereg/prereg_sha256.txt` (which includes this amendment by reference once written at freeze).

## A6. Effect

With A2–A4 recorded, the three WP2-vs-spec divergences are compliant by amendment rather than by silent deviation. `FOUNDATION_FROZEN` may be claimed once the WorkPlan Phase-1 exit criteria (including pre-freeze bridge acquisition and this amendment’s inclusion in the prereg hash) are green. Any future normative change requires a new versioned amendment (`v0.4.2`, …); the v0.4 file itself is never edited in place.
