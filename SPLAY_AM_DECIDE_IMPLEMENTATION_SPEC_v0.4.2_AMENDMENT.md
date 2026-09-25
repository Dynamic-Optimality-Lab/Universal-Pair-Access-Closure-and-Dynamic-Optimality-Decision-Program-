# SPLAY-AM-DECIDE v0.4.2 — Ratified Pre-Freeze Amendment / Stack-Binding Fix

**Status:** `RATIFIED` — issued before `FOUNDATION_FROZEN`; forms part of the normative v0.4 stack.
**Date ratified:** 2026-09-25 UTC
**Amends:** `SPLAY_AM_DECIDE_IMPLEMENTATION_SPEC_v0.4.1_AMENDMENT.md` §A5 only (v0.4 and v0.4.1 bytes preserved — this file adds the fix; it neither edits nor supersedes A2–A4, which remain in force).
**Authored because:** verification review found that v0.4.1 §A5 literally binds `WorkPlan.md` v0.4-WP3 by version tag, while the living plan has since advanced (WP4 → WP5 → WP6). Since the project is still `PRE_FOUNDATION`, plan revision is allowed — but a correct plan sitting outside its own normative stack would be a provenance defect. This amendment rebinds the stack to the living revision.

## B1. Living-revision stack binding (supersedes the version tag in A5, not its substance)

The normative v0.4 stack is exactly:

1. `IMPLEMENTATION_SPEC_v0.4.md` (byte-identity),
2. this amendment series (`..._v0.4.1_AMENDMENT.md` A2–A4/A6 + `..._v0.4.2_AMENDMENT.md` B1–B3),
3. `WorkPlan.md` **at its final pre-`FOUNDATION_FROZEN` revision, whatever its version tag** (at issuance: v0.4-WP6) — the binding is sealed at freeze by `prereg/prereg_sha256.txt`, which hashes the exact bytes,
4. `Path.md` (living tracker — versioned by commit history, not frozen text),
5. `prereg/` contents hashed in `prereg/prereg_sha256.txt` (which includes both amendments by reference once written at freeze).

Any future WorkPlan change after `FOUNDATION_FROZEN` requires a new versioned amendment; any pre-freeze revision is covered by B1 automatically, with the frozen bytes pinned by the prereg hash.

## B2. Schema-compatibility rule for endpoint-aware witnesses (normative clarification, no new machinery)

The `REFUTE(MST0-17)` witness payload (endpoint terms, ledger identity/trace, subsequence certificate, exact `lhs`/`rhs`, strict residual) must validate under the frozen `proof_attack.schema.json` (+ `pair_access_certificate.schema.json` evaluation). Neither schema may use a restrictive `additionalProperties: false` (or any equivalent closed-world constraint) that rejects a required payload field. Conformance is demonstrated before `FOUNDATION_FROZEN` by validating a sample witness through both schemas with the project-pinned `jsonschema` version; the validation record is a freeze artifact.

## B3. Effect

With B1 recorded, the WP5/WP6 plan is inside its own normative stack by rule rather than by tag coincidence, and no further amendment is needed for pre-freeze plan revisions. B2 makes the WP5 “reuse existing schemas” claim checkable instead of declarative. `FOUNDATION_FROZEN` additionally requires the B2 sample-witness validation record. The v0.4 and v0.4.1 files themselves are never edited in place.
