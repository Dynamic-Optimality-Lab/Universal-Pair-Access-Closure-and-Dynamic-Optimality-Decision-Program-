# SPLAY-AM-DECIDE v0.4.2 — Ratified Pre-Freeze Amendment / Stack-Binding Fix

**Status:** `RATIFIED` — issued before `FOUNDATION_FROZEN`; part of the normative v0.4 stack.
**Date ratified:** 2026-09-25 UTC
**Amends:** v0.4.1 §A5 only (v0.4 and v0.4.1 bytes preserved — adds, never edits; A2–A4 remain in force).
**Authored because:** A5 bound `WorkPlan.md` by version tag, but the plan is living pre-freeze — a correct later revision would sit outside its own stack. This rebinds by rule.

## B1. Living-revision stack binding

The normative stack is: 1. `IMPLEMENTATION_SPEC_v0.4.md`, 2. amendments (v0.4.1 A2–A4/A6 + v0.4.2 B1–B3), 3. `WorkPlan.md` **at its final pre-`FOUNDATION_FROZEN` revision, whatever its tag** (binding sealed at freeze by `prereg/prereg_sha256.txt`), 4. `Path.md` (living, history-versioned), 5. `prereg/` contents hashed in `prereg_sha256.txt`. Post-freeze WorkPlan changes need new amendments; pre-freeze revisions are covered automatically with bytes pinned by the prereg hash.

## B2. Schema-compatibility rule for endpoint-aware witnesses

The `REFUTE(MST0-17)` witness payload (endpoint terms, ledger identity/trace, subsequence certificate, exact `lhs`/`rhs`, strict residual) must validate under frozen `proof_attack.schema.json` (+ `pair_access_certificate.schema.json` evaluation). Neither schema may use restrictive `additionalProperties: false` (or equivalent closed-world constraint) rejecting a required payload field. Conformance is demonstrated before `FOUNDATION_FROZEN` by validating a sample witness through both schemas with the pinned `jsonschema` version; the validation record is a freeze artifact.

## B3. Effect

WP revisions need no further amendment pre-freeze; B2 makes schema-reuse checkable, not declarative. `FOUNDATION_FROZEN` additionally requires the B2 validation record. v0.4/v0.4.1 never edited in place.
