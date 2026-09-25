# CHANGELOG — SPLAY-AM-DECIDE-v0.4

All notable decisions are recorded here. Tracker detail lives in `Path.md` (append-only).

## [Unreleased] — 2026-09-25
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
