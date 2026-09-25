# SPLAY-AM-DECIDE v0.4.5 — Ratified Pre-Freeze Amendment / Unavailable-Source Branch Completion

**Status:** `RATIFIED` — issued before `FOUNDATION_FROZEN`; part of the normative v0.4 stack.
**Date ratified:** 2026-09-25 UTC
**Amends:** v0.4.4 D3/D6 and WorkPlan Phase-1/Phase-5 bridge wording (propagates the lawful unavailable branch through the freeze model; alters no theorem, constant, or calculus). v0.4–v0.4.4 bytes preserved.
**Authored because:** the freeze contract demanded both “never synthesize an MST0-19 source-dependent theorem” and “freeze 10 canonical Statements + Lean Props,” which cannot both hold when bridge bytes are lawfully unavailable — and the exact bound set named bytes that may not exist.

## E1. Two preregistered bound-set variants (replaces the single D3 set)

```yaml
FREEZE_BOUND_FILES_SOURCE_AVAILABLE:   # 26 members: D3 list as ratified
FREEZE_BOUND_FILES_SOURCE_UNAVAILABLE: # 25 members: D3 list minus bridge_sources/L3_1907.06310_v1.pdf
```

The unavailable variant binds the disposition record (`bridge_sources.yaml`, a payload file) instead of nonexistent source bytes. Variant selection follows the recorded acquisition outcome; the manifest rule `manifestPaths = unique(payload ∪ bound)` applies to the selected variant. Unexpected overlap remains fatal unless preregistered.

## E2. MST0-19 blocked-node representation (no-synthesis rule)

If `BRIDGE_SOURCE_UNAVAILABLE`, MST0-19 has NO canonical theorem Statement/Negation. Instead freeze exactly:

```text
theorem_id = MST0-19
source_status = BLOCKED_SOURCE_UNAVAILABLE
statement_status = UNINSTANTIATED_SOURCE_DEPENDENT
prove_ready = false
refute_ready = false
```

`math/theorem_MST19_bridge.md` contains only this blocked-node record, never a synthesized mathematical claim. `lean/Frozen/Statements.lean` contains no theorem-bearing MST0-19 Prop — only a blocked-source metadata representation. The “10 theorem docs / 10 Statement Props” requirements elsewhere read as 9 instantiated theorems + 1 frozen blocked-node representation in this branch. The battlefield preserves node identity and blocked reason.

## E3. Phase-02 wording (impossibility removed)

Phase 1 requires “exact L2/L3 bytes or the frozen unavailable disposition established before freeze” — never bare acquisition. Phase-02 execution verifies whichever branch was frozen.

## E4. Effect

E1–E3 complete the unavailable branch end to end. v0.4–v0.4.4 bytes preserved. Future changes need versioned amendments.
