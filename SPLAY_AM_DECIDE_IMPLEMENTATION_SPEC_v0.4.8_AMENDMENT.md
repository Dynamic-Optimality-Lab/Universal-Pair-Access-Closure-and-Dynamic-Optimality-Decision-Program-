# SPLAY-AM-DECIDE v0.4.8 — Foundation Placeholder-Completion Supersession

**Status:** `RATIFIED` — issued after `FOUNDATION_FROZEN` under the versioned-supersession
rule (WorkPlan `SUPERSEDED_*.json` mechanism; v0.4.7 G12 "future changes need
versioned amendments"). Narrow scope: foundation-owned prereg placeholders only.
**Date ratified:** 2026-09-26 UTC
**Amends:** completes `prereg/parent_contract.yaml` + `prereg/bridge_sources.yaml`
placeholder fields; supersedes the affected freeze artifacts (below). v0.4–v0.4.7 bytes
preserved. No theorem science, PSC, review, or downstream-phase content touched.

## H1. Placeholder completion authorization

The eleven `PENDING-Phase-1-*` fields frozen as markers are replaced with verified values:
(1) `parent_contract.yaml` ten hashes := exact SHA-256 of the corresponding already-verified
`parent/` artifacts (`V03_SEAL/FINAL_RESULT/MANIFEST/ARCHIVE/PATH_FINAL/WORKPLAN_FINAL/
MSTC_0002/THEOREM_STATUS/COUNTEREXAMPLE_INDEX` + `BOOTSTRAP_MANIFEST`); the section key
is renamed `pending_Phase-1-hashes` → `verified_Phase-1-hashes` (no mechanical consumers).
(2) `bridge_sources.yaml` L0 `hash:` := disposition `NOT_APPLICABLE_BY_PARENT_BOUND`
(no authority issues a SHA-256 of the release as one blob; the release is identified by
`parent_full_sha 353ee922b1cee0043afa46fe8929f42f7652e5bf` (HEAD verified) and its bytes
by the nine `parent/V03_*` hashes in `BOOTSTRAP_MANIFEST.sha256`; inventing a hash is
forbidden). The F1 variant label `SOURCE_AVAILABLE-28` is retained verbatim (frozen in
`PHASE02_BRIDGE_SOURCES_FREEZE.json`); set membership is governed by the G1 rule as
restated in H2.

## H2. Supersession mechanics + materialization

Old freeze preserved: `artifacts/v04/freeze/SUPERSEDED_prereg_sha256_<old8>.txt`
(old manifest bytes) + `SUPERSEDED_PATH_AT_FOUNDATION_FREEZE_<old8>.md`
(old Path snapshot bytes) + `artifacts/v04/freeze/SUPERSEDED_PREREG_PLACEHOLDER_REPAIR.json`
(reason, old/new manifest hashes, files changed, this amendment as authority).
Regenerated: `prereg/prereg_sha256.txt` (payload UNION bound, never itself) and
`artifacts/v04/freeze/FOUNDATION_FROZEN.json` (new manifest hash/member count +
supersession pointer). Normative-stack declarations wire v0.4.8 (WorkPlan header/§0/tree,
v1.6→v1.7); v1.6 bytes stay pinned by the superseded manifest + git history. PATH snapshot
regenerated to living Path bytes through the repair record (future entries append
below the end-marker, preserving the prefix invariant); PROOF_STATUS snapshot
untouched (ledger bytes unchanged). Byte-stability rule: `.gitattributes * -text`
(no ending conversion; manifest hashes over working-tree bytes are stable across
clone/commit).
Materialization restated (derived, asserted by verifier): 45 available /
44 unavailable members at freeze (prior 44/43 plus this amendment file); 43 on-disk
working members pre-freeze.

## H3. Effect

H1–H2 bind seal/reproduction reads of the repaired fields. Zero foundation-owned
prereg fields may contain `PENDING-Phase-1-*` after this supersession (asserted by
`scripts/contract_closure.py`; legitimate `PENDING-owner-phase-execution` /
`PENDING-HUMAN` downstream states unaffected). Future changes need versioned amendments.
