# SPLAY-AM-DECIDE v0.4.4 — Ratified Pre-Freeze Amendment / Freeze-Authority Refinements

**Status:** `RATIFIED` — issued before `FOUNDATION_FROZEN`; part of the normative v0.4 stack.
**Date ratified:** 2026-09-25 UTC
**Amends:** v0.4.3 C1 (per-node readiness), WorkPlan freeze contract (bound set, snapshot semantics, verification chronology). v0.4–v0.4.3 bytes preserved.
**Authored because:** state-machine/freeze-authority exploits survive the v1.1 contract: flat Phase-5 readiness, mutable status under a byte-freeze, an unenmerated bound set, an acceptable-custom-axiom reading, verification-after-freeze wording, and an unrepresentable unavailable-source theorem.

## D1. Per-node PROVE_READY for Phase 5 (refines v0.4.3 C3)

```text
PROVE_READY(MST0-17) = REFUTE_READY(17) + 08U/09/11/13/14/15/22 all REVIEWED
PROVE_READY(MST0-18) = REFUTE_READY(18) + MST0-17 REVIEWED
PROVE_READY(MST0-19) = REFUTE_READY(19) + MST0-18 REVIEWED
  + BRIDGE_SOURCES_FROZEN + applicable frozen source/convention prerequisites
```

## D2. Living status vs frozen snapshot (immutable rule)

`math/proof_status.json` is the living derived ledger and may change ONLY through legal lifecycle transitions. The freeze binds exclusively the immutable snapshot `artifacts/v04/freeze/PROOF_STATUS_AT_FOUNDATION_FREEZE.json`. Every status mutation records previous_status_hash, new_status_hash, trigger_artifact_hashes, lifecycle_transition, and human_review_hash where required.

## D3. Exact FREEZE_BOUND_FILES set (normative enumeration)

```yaml
FREEZE_BOUND_FILES:
  - IMPLEMENTATION_SPEC_v0.4.md
  - SPLAY_AM_DECIDE_IMPLEMENTATION_SPEC_v0.4.1_AMENDMENT.md
  - SPLAY_AM_DECIDE_IMPLEMENTATION_SPEC_v0.4.2_AMENDMENT.md
  - SPLAY_AM_DECIDE_IMPLEMENTATION_SPEC_v0.4.3_AMENDMENT.md
  - SPLAY_AM_DECIDE_IMPLEMENTATION_SPEC_v0.4.4_AMENDMENT.md
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
```

Manifest rule: `manifestPaths = unique(PREREG_PAYLOAD_FILES ∪ FREEZE_BOUND_FILES)`; unexpected overlap fatal unless preregistered; v0.4.4 itself joins the bound set (self-inclusion across versions is by-version, never self-hash: each manifest hashes only files existing at its freeze).

## D4. Custom-axiom allowlist (closes the tracked-axiom exploit)

```text
CUSTOM_THEOREM_AXIOM_ALLOWLIST = empty set.
```

No custom axiom may assert or imply any Splay, MSTC-0002, locality, boundary, preservation, repayment, integrability, Pair-Access, telescope, bridge-consequence, or negative-family property. Every theorem-critical Lean declaration must report `#print axioms` / dependency closure. Any dependency on a custom theorem-bearing axiom invalidates Layer B. Only the trusted logical foundations of the pinned Lean/mathlib environment, as explicitly frozen, may be relied upon. “Declared custom axiom” never means “acceptable custom axiom.” Tracked axiom records are permitted solely for non-theorem-bearing operational identities (e.g., implementation-identity hooks discharged by canary agreement), each named and discharged before use.

## D5. Post-freeze verification chronology (no prereg mutation, ever)

BEFORE `FOUNDATION_FROZEN`: author/finalize all prereg payloads (PSC interfaces, mutants, seeds, minimization orders). `FOUNDATION_FROZEN` hashes those immutable bytes. Spec PHASE 02/04 AFTER foundation verify the already-frozen bytes, build conformance vectors/certificates, emit their gates, and MUST NOT modify prereg. Same principle for Phase 02 bridge verification.

## D6. MST0-19 representation under source unavailability (no invention rule)

If `BRIDGE_SOURCE_UNAVAILABLE`: MST0-19 carries `source_status = BLOCKED_SOURCE_UNAVAILABLE`; `PROVE_READY` and `REFUTE_READY` are false; no source-dependent canonical statement is synthesized and no theorem-facing source hypothesis is guessed. The battlefield preserves the node identity and blocked reason. No approximation of Levy–Tarjan from bibliography/prose may stand in for the frozen source.

## D7. Effect

D1–D6 bind Phases 1/5/6/7 execution. v0.4–v0.4.3 bytes preserved. Future changes need versioned amendments.
