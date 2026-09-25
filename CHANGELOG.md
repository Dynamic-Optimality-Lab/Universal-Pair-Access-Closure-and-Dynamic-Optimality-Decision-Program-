# CHANGELOG — SPLAY-AM-DECIDE-v0.4

All notable decisions are recorded here. Tracker detail lives in `Path.md` (append-only).

## [Unreleased] — 2026-09-25
- Added (WP-0): full `scripts/run_phase00.py` (13 STEP checks, fail-closed, `PHASE00_PASS`), `tests/test_phase00_stress.py` (repeatability/tamper/missing/wrong-commit); `tests/test_foundation.py` now 8 real tests; `artifacts/v04/freeze/PHASE00_PARENT_PIN.json` + `logs/phase00.log`; Path Entries 024–026 (spec PHASE 00 COMPLETE; Phase 1 otherwise STARTED; `FOUNDATION_FROZEN` not claimed).
- Changed (WP8): manifest contract fixed — `PREREG_PAYLOAD_FILES ∪ FREEZE_BOUND_FILES` (manifest never self-hashes) + `PATH_AT_FOUNDATION_FREEZE.md` snapshot pinned instead of living Path (append-only preserved).
- Changed (WP7): explicit `prereg_sha256.txt` manifest contract (pinned lines for WorkPlan/Path/spec/amendments/toolchain/schemas/PSC — B1 loophole closed without a new amendment); triple-artifact `MST0_17_REFUTED` gate (attack record AND PA certificate AND interface conformance); Path header artifacts truthfulness.
- Added (WP6): `SPLAY_AM_DECIDE_IMPLEMENTATION_SPEC_v0.4.2_AMENDMENT.md` (B1 living-revision binding, B2 witness-schema rule); `schemas/{proof_attack,pair_access_certificate}.schema.json` authored + sample endpoint-aware witness validated green (`artifacts/v04/freeze/WITNESS_SCHEMA_VALIDATION.json`).
- Changed (WP6): `WorkPlan.md` v0.4-WP5 → v0.4-WP6 (amendment refs, stack wording, schema-validation notes).
- Changed (WP5): `REFUTE(MST0-17)` negation now endpoint-aware (`lhs = Splay(Y,T)+E_m−E_0 > rhs = 2·Splay(X,T)+A(n)`, 15-field witness) + executable SHA-bind guard; `prereg/proof_stress_corpus.yaml` now complete (12-field specs × 7 PSC families + `REFUTE-MST0-17` interface, YAML-validated); Path headers carry living revision + amendment.
- Changed (WP4): `WorkPlan.md` v0.4-WP3 → v0.4-WP4 (explicit `REFUTE(MST0-17)` machinery, PSC spec-freeze + conformance harness, MST0-19 BLOCKED-vs-REFUTED, “independently generated” wording, §18-plus-amendment tree).
- Added (WP4): `python/proof_attack/pair_access_search.py`, `python/cleanroom/pair_access_check.py`, `artifacts/v04/{counterexamples,proof_attacks}/pair_access/` namespaces, `PA-06` hardening test.
- Added (WP3): `SPLAY_AM_DECIDE_IMPLEMENTATION_SPEC_v0.4.1_AMENDMENT.md` (ratified pre-freeze: A2 REJECT!=REFUTED, A3 `POSITIVE_ROUTE_BLOCKED_UNRESOLVED_NO_CLAIM` → exactly-six Phase-18 taxonomy, A4 bridge-acquire-before-freeze; v0.4 bytes preserved).
- Changed (WP3): `WorkPlan.md` v0.4-WP2 → v0.4-WP3 (amendment refs, BLOCKED gate, prereg-count typo → “14 entries total, including prereg_sha256.txt”, upstream-count + timeline nits, allowed/forbidden +10th level).
- Changed (WP3): `prereg/allowed_claims.md`, `prereg/forbidden_claims.md` (new no-claim level wording).
- Added (WP2): repairs for 12 findings — bridge-before-freeze + PHASE02 freeze file, gate-vs-status separation, fail-fast gates + NOT_REACHED, imported payment semantics, counts 39/14/13/17/14/11/24 + 15-step, `tests/mutation/` authority, Lean root paths, dependence-scoped scan, multi-owner T120/STOP-70/INV-100; `lake-manifest.json` stub; `Path.md` Entries 008–010.
- Added (WP1): `WorkPlan.md` v0.4-WP1 (7 phases covering spec PHASE 00–19, verification appendix A–J).
- Added: `Path.md` Entries 001–007 (study, clone, seal inventory, stale clearance, skeleton, plan).
- Added: `IMPLEMENTATION_SPEC_v0.4.md` verbatim copy (85,888 bytes).
- Added: foundation skeleton (`parent/`, `prereg/`, `math/`, `lean/`, `python/`, `schemas/`, `tests/`, `artifacts/v04/`, `scripts/`).
- Verified: implementation repo started clean (`b091dea`, LICENSE-only); `artifacts/v04/` empty by design (only new results present).
- Pinned (to be hash-verified in Phase 1 execution): parent full SHA `353ee922b1cee0043afa46fe8929f42f7652e5bf`, ancestor `6de1ca2a595e8895f54794f3a211fe6ee1a95a80`, v0.3 parent `38c1be6afd2ab2420aa094c68ce45ee6a26b3628`, terminal `TRANSFER_CALCULUS_SURVIVES_FINITE_TESTS`, survivor `MSTC-0002=(P_all,k=6,C=2)`.
- Not claimed: `FOUNDATION_FROZEN` (pending Phase-1 execution); no theorem status changed; no bridge consumed; H3T never re-unlocked.
