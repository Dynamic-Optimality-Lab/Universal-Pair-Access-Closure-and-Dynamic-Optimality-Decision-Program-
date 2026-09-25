# SPLAY-AM-DECIDE v0.4.6 — Ratified Pre-Freeze Amendment / Stack Authority and Bound-Set Completion

**Status:** `RATIFIED` — issued before `FOUNDATION_FROZEN`; part of the normative v0.4 stack.
**Date ratified:** 2026-09-25 UTC
**Amends:** normative stack declarations (v0.4.5 authority) and v0.4.4 D3 / v0.4.5 E1 (bound-set supersession); adds battlefield-union (F2), kernel-hardening (F3), verification-chronology (F4) rules. v0.4–v0.4.5 bytes preserved.
**Authored because:** v0.4.5 existed, was ratified, and was cited by WorkPlan rules while missing from every stack declaration; and neither bound enumeration (D3's 26, E1's 26/25) can contain the amendment files that postdate it.

## F0. v0.4.5 authority completion

`SPLAY_AM_DECIDE_IMPLEMENTATION_SPEC_v0.4.5_AMENDMENT.md` (E1 bound variants, E2 blocked representation, E3 verification wording) is and was normative from its ratification. It joins the header normative line, the §0 amendment stack, the root-tree contract, and the bound set below. Its E-rules remain in force unmodified, except where explicitly superseded below.

## F1. Exact bound sets, versioned (supersede D3 and E1 enumerations)

```yaml
FREEZE_BOUND_FILES_SOURCE_AVAILABLE:   # 28 members
  - IMPLEMENTATION_SPEC_v0.4.md
  - SPLAY_AM_DECIDE_IMPLEMENTATION_SPEC_v0.4.1_AMENDMENT.md
  - SPLAY_AM_DECIDE_IMPLEMENTATION_SPEC_v0.4.2_AMENDMENT.md
  - SPLAY_AM_DECIDE_IMPLEMENTATION_SPEC_v0.4.3_AMENDMENT.md
  - SPLAY_AM_DECIDE_IMPLEMENTATION_SPEC_v0.4.4_AMENDMENT.md
  - SPLAY_AM_DECIDE_IMPLEMENTATION_SPEC_v0.4.5_AMENDMENT.md
  - SPLAY_AM_DECIDE_IMPLEMENTATION_SPEC_v0.4.6_AMENDMENT.md
  - WorkPlan.md
  - artifacts/v04/freeze/PATH_AT_FOUNDATION_FREEZE.md
  - artifacts/v04/freeze/PROOF_STATUS_AT_FOUNDATION_FREEZE.json
  - lean/Frozen/SplayDefs.lean
  - lean/Frozen/MSTC0002Defs.lean
  - lean/Frozen/Statements.lean
  - math/theorem_MST08U_locality.md
  - math/theorem_MST09_raw_boundary.md
  - math/theorem_MST11_preservation.md
  - math/theorem_MST13_delete_injection.md
  - math/theorem_MST14_keep_repayment.md
  - math/theorem_MST15_integrability.md
  - math/theorem_MST22_constant_independence.md
  - math/theorem_MST17_pair_access.md
  - math/theorem_MST18_telescoping.md
  - math/theorem_MST19_bridge.md
  - schemas/proof_attack.schema.json
  - schemas/pair_access_certificate.schema.json
  - prereg/proof_stress_corpus.yaml
  - bridge_sources/L3_1907.06310_v1.pdf
  - bridge_sources/README.md

FREEZE_BOUND_FILES_SOURCE_UNAVAILABLE: # 27 members: above minus the source PDF
```

Manifest rule: `manifestPaths = unique(payload ∪ bound(selected variant))`; unexpected overlap fatal unless preregistered; each manifest hashes only files existing at its freeze (by-version inclusion, never self-hash). Variant selection follows the recorded acquisition outcome.

## F2. Theorem-battlefield union (no silent pruning)

The frozen battlefield of exactly 10 nodes (spec §6: `08U/09/11/13/14/15/22/17/18/19`)
is the union bound by every freeze: no amendment, phase plan, or implementation step
may drop, merge, or replace a node. `prereg/theorem_battlefield.yaml` enumerates all 10
with statement/negation/document hashes, owner phases, first consumers, prerequisites,
child namespaces, forbidden premises, and the 4 artifacts each. Phase-1 execution
asserts `set(nodes)=={08U,09,11,13,14,15,22,17,18,19}` before any theorem-facing run.

## F3. Formal-kernel semantic hardening

`lean/Frozen/` contains ONLY actual total computable definitions over explicit state
(BST/splay/trace/cost/KEEP/DELETE, ledger/credit/T7/T5/T6/energy/discharge, paired
execution) plus `def ... : Prop` statement Props that name propositions without
asserting them. Rules: zero `sorry`/`admit`; zero `axiom` (the
`CUSTOM_THEOREM_AXIOM_ALLOWLIST` of v0.4.4 D4 is and stays empty — no custom axiom
may assert or imply any theorem-bearing property); `#print axioms` closure is
reported at Phase-1 execution; finite canary agreement against the Python executable
semantics is sanity-only and discharges nothing — Lean↔Python equivalence is PROVED
at Phase-03 execution, never assumed. The narrowed opaque class is empty: every
former opaque helper is either an actual definition or deleted.

## F4. Verification chronology

No theorem-facing execution before all foundation checks close in order: parent-seal
hashes → contract binding → Lean kernel policy (toolchain/manifest/allowlist/sorry
scan) → theorem+negation hash binding (whole-file, statement-line, negation-line) →
dual-gate readiness → only then PROVE/REFUTE tracks. `FOUNDATION_FROZEN` is claimed
exactly once, by the freeze script, after the chronology is green; `Path.md` entries
predate the commits they authorize and never post-claim work.

## F5. Effect

F0–F1 bind Phases 1/5/6/7 execution. v0.4–v0.4.5 bytes preserved. Future changes need versioned amendments.
