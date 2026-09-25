# SPLAY-AM-DECIDE-v0.4 Path — implementation tracker

**Experiment:** `SPLAY-AM-DECIDE-v0.4`
**Normative spec:** `IMPLEMENTATION_SPEC_v0.4.md` (root, 85,888 bytes, copied verbatim) + ratified `SPLAY_AM_DECIDE_IMPLEMENTATION_SPEC_v0.4.1_AMENDMENT.md` (A2 REJECT!=REFUTED, A3 six outcomes, A4 bridge order) + ratified `SPLAY_AM_DECIDE_IMPLEMENTATION_SPEC_v0.4.2_AMENDMENT.md` (B1 living-revision binding, B2 witness-schema rule)
**Plan:** `WorkPlan.md` (current revision v0.4-WP6; revision history WP1→WP2→WP3→WP4→WP5 preserved below)
**Rule for this file:** Every implementation step is appended here contemporaneously with deep detail matching `WorkPlan.md` granularity — scope, files made, code produced and how it was coded, benchmarks (and their training-disjointness), anti-overfitting actions, gates — plus an explicit verdict: **FOLLOWS WorkPlan §X** or **DEVIATION from WorkPlan §X (justified)**. A phase gate without a Path entry is not closed (`INV-097`). No entry is ever rewritten; corrections are new entries (erratum-preserving).
**Current terminal status:** `PRE_FOUNDATION` (planning + skeleton done; `FOUNDATION_FROZEN` not yet claimed; no Phase 01+ theorem-facing execution has occurred — complies with `PRE_FREEZE_PARENT_PIN_REQUIRED`).
**Repo state at last entry:** `impl/` on `main`, clean skeleton + docs; `artifacts/v04/` empty by design (only new results after this plan are present — stale-clearance verified).

---

## Entry 001 — 2026-09-25 UTC — Deep doc study (WorkPlan §0) — FOLLOWS WorkPlan §0

**Scope.** Study-first: read the controlling v0.4 spec in full (via user-provided text, 3240 lines, §§0–38, PHASE 00–19, T001–T120, INV-001–100, STOP-01–70, full test matrix, Q01–Q60), plus lineage headers (`SPLAY_AM_MST_IMPLEMENTATION_SPEC_v0.3.md` 120,420 bytes, `SPLAY_AM_BD_IMPLEMENTATION_SPEC_v0.2.md` 100,175 bytes, `SPLAY_AM_PD_IMPLEMENTATION_SPEC_v0.1.md` 120,584 bytes — executive-purpose + pivot sections read), plus live parent/implementation repo pages (verified impl repo has 1 commit / LICENSE-only; parent repo has 18 commits / full v0.3 tree), plus unrelated `Downloads/WorkPlan.md` inspected and rejected as non-authoritative (MAVS Chapter 10B, different project — not used).
**Files made.** None (read-only study; no code).
**Code/how.** `Read` tool on `Downloads/SPLAY_AM_DECIDE_IMPLEMENTATION_SPEC_v0.4.md` (lines 1–100 verified byte-consistent with user text), `SPLAY_AM_MST…v0.3`/`…BD…v0.2`/`…PD…v0.1` (lines 1–120 each), `WebFetch` on both GitHub repos (markdown). Confirmed: 20 spec phases, 10 theorem nodes, 7 PSC families, Pair-Access form `Splay(Y,T) ≤ 2·Splay(X,T)+A(n)`, constants `C=2/k=6/P_all` frozen, YES/NO-only success, finite≠proof doctrine, dual prove/refute + 3-layer cert + human ACCEPT, negative dormant-until-REFUTED with `g/f→∞` requirement.
**Benchmarks.** None (study only; no measurement claimed).
**Anti-overfitting.** No finite result treated as theorem; lineage docs treated as evidence/context, never premises; web summaries never override frozen sources.
**Verdict.** FOLLOWS WorkPlan §0 (source authority). No deviation.

## Entry 002 — 2026-09-25 UTC — Clone implementation + parent repos, verify toolchain (WorkPlan §§0–1) — FOLLOWS WorkPlan §§0–1

**Scope.** Establish working copies and verify auth/toolchain before any file creation.
**Files made.** Local dirs `Dynamic-Optimality/impl/` (clone of implementation repo) and `Dynamic-Optimality/parent-ref/` (read-only reference clone of parent repo, never mutated).
**Code/how.** `git clone https://github.com/Dynamic-Optimality-Lab/Universal-Pair-Access-Closure-and-Dynamic-Optimality-Decision-Program- impl` → HEAD `b091dea Initial commit`, `LICENSE` only (1100 bytes), `git status` clean, `origin` https. `git clone …/splay-multiscale-transfer parent-ref` → HEAD `353ee922b1cee0043afa46fe8929f42f7652e5bf` (short `353ee92`, matches spec navigation commit), log shows WP-6 seal message with lifecycle `10/4/3/3/6`, `FINAL_RESULT` finite level, 424-file manifest, 16.9 MB archive, reproduce PASS. `gh auth status` → logged in as `InfernusReal` (repo/workflow scopes, push-capable). `python --version` → `3.13.7` (satisfies `3.12+`); `lean`/`lake` not on PATH (recorded as pending Phase-1 toolchain pin — no Lean claim made).
**Benchmarks.** None.
**Anti-overfitting.** Parent clone is reference-only; no parent artifact edited; no H3T touched; no theorem execution.
**Verdict.** FOLLOWS WorkPlan §0 (repo identities) and §3/Phase-1 setup. No deviation.

## Entry 003 — 2026-09-25 UTC — Parent seal inspection (WorkPlan Phase 1 scope) — FOLLOWS WorkPlan Phase 1

**Scope.** Read sealed parent evidence to bind exact identities for Phase-1 freeze (no execution, read-only).
**Files read (parent-ref, all read-only).**
- `TRANSFER_CALCULUS_LEDGER.md`: frozen set `MSTC-0001/0002/0003`, set hash `8FD3273143DEC3CA4611A1093F3521B8F22DE2BBD6A82715EE270412F65A2A00`, Branch-A unsigned ledger `E(L)=|LATENT|+|ACTIVE|`, T7 (≤k LATENT per A-rotation at cycling interior boundaries, LEFT iff `i+1≤x`), T5 (predicate-gated LATENT→ACTIVE), T6 (`w=y-2a`, `paid=min(pool,w)`, residual rejects at frozen C), WP-6 seal note (0002 stands 70k/70k + 54 large-n zero residuals; 0001 max_res 8 / 0003 max_res 23 killed fresh).
- `THEOREM_STATUS_REPORT.md`: lifecycle `UNPROVED→PROVED→REVIEWED`, table (REVIEWED 10 incl. 08-scoped-finite + 01/02/03/04/05/06/07/10/16; PROVED 4 incl. 13-author-claim + 23/24/26 pending review; NOT_APPLICABLE 3 (12/20/21); BLOCKED 3 (17/18/19); UNPROVED 6 (09/11/14/15/22/25)), gates 0–15 reached / 16 pending-review / 17–21 not reached, human actions (ACCEPT/REJECT/BLOCKED on 13/23/24/26; 13-ACCEPT permits re-seal at `BOUNDED_DELETE_INJECTION_PROVED` by amendment only).
- `artifacts/v03/seal/FINAL_RESULT.json`: terminal `TRANSFER_CALCULUS_SURVIVES_FINITE_TESTS`, `standing:[MSTC-0002]`, killed-fresh records (0001 n=32 idx=4406 res[2,1]/w[11,1] max[8,1]; 0003 n=16 idx=3610 res[1,1]/w[8,1] max[23,1]), hashes (candidate-set `8FD32731…`, H3T logical `CB37F3D9…`, per-size streams, reveal `FC916F06…`), firewalls (`H1 EMPTY/NOT_APPLICABLE, H2R BANK_COMMITTED/NOT_APPLICABLE, H3T UNLOCKED_ONCE/1, n8 CANARY_CONTAMINATED`), `parent_sealed_commit 38c1be6afd2ab2420aa094c68ce45ee6a26b3628`, `ancestor 6de1ca2a595e8895f54794f3a211fe6ee1a95a80`, `repo_head 94197b89…`.
- `artifacts/v03/holdouts/{candidate_set_commit,h3t_state,h3t_reveal}.json`: 3 candidates with SHAs (`0001 A8492C94…`, `0002 930EAD00…`, `0003 FE56D095…`), `UNLOCKED_ONCE/unlock_count=1`, reveal note “survival is finite-sample survival, never theorem status”.
- `SPLAY_AM_MST_IMPLEMENTATION_SPEC_v0.3.1_PIN.md`: ratified parent pin (`38c1be6afd…`, `FINITE_DEBT_LAW_MINING_RESULTS`, FINAL_RESULT SHA `C5B1C60A…`, manifest SHA `5C4BA61B…`, archive SHA `87AEA34C…`, spec SHA `462676E1…` 120,420 bytes), chain aides, freeze composition.
- `parent/import_ledger.json`, seal `MANIFEST.sha256` (head), `scripts/` (run_phase00–19 + reproduce), `python/` + `artifacts/v03/` layouts (used as interface reference for WorkPlan `python/inherited` wrappers).
**Code/how.** PowerShell `Get-Content`/`Get-ChildItem` only; no execution of parent scripts; no bank I/O.
**Benchmarks.** None (evidence inventory only).
**Anti-overfitting.** Finite seal explicitly recorded as non-theorem; H3T state verified `UNLOCKED_ONCE` without re-unlock; sibling kills preserved in plan.
**Verdict.** FOLLOWS WorkPlan §0 + Phase-1 spec coverage (PHASE 00–01 inputs). No deviation. Pending Phase-1 work (hash-recompute verifier, prereg freeze, bridge/Lean/PSC freeze) is explicitly not claimed as done.

## Entry 004 — 2026-09-25 UTC — Stale-results clearance (user instruction + WorkPlan §3) — FOLLOWS WorkPlan §3

**Scope.** Satisfy “when you clone the repo, the previous results are cleared and only the new results after the changes are present.”
**Finding.** `impl/` at clone contained only `LICENSE` (commit `b091dea`); `artifacts/v04/` did not exist. There were no previous results to clear — no deletion needed, no legacy output carried forward.
**Files made.** Created empty canonical `artifacts/v04/{freeze,formal,proof_attacks,counterexamples,proofs,negative,audits,logs,seal}/` (with `.gitkeep` placeholders added in Entry 006) so all future results are new-by-construction; `STALE_CLEARANCE.json` will be written at Phase-7 seal asserting this.
**Code/how.** `New-Item -ItemType Directory` for each `artifacts/v04/*` leaf; `Get-ChildItem impl` + `git log` verification.
**Benchmarks/anti-overfitting.** N/A (hygiene only; prevents stale-output contamination, `STOP-68/69`).
**Verdict.** FOLLOWS WorkPlan §3 (repo contract; `artifacts/v04` starts empty) + user clearance instruction. No deviation.

## Entry 005 — 2026-09-25 UTC — Repository skeleton + spec copy (WorkPlan §3) — FOLLOWS WorkPlan §3

**Scope.** Create the verbatim §18 directory skeleton so WorkPlan file references resolve; copy normative spec bytes.
**Files made.** `parent/`, `prereg/`, `math/negative/`, `math/reviews/`, `lean/{Splay,MSTC0002,PairAccess,Negative}/`, `python/{inherited,formal_bridge,proof_attack,negative,audit,seal,cleanroom}/`, `schemas/`, `tests/{parent,seal}/`, `artifacts/v04/{freeze,seal,logs}/`, `scripts/` (dirs only in this entry; file placeholders in Entry 006); `IMPLEMENTATION_SPEC_v0.4.md` copied verbatim from `Downloads/SPLAY_AM_DECIDE_IMPLEMENTATION_SPEC_v0.4.md` via `Copy-Item -Force` (85,888 bytes, length verified).
**Code/how.** PowerShell `New-Item -ItemType Directory -Force` per leaf (parent verified via `Test-Path impl\LICENSE`); `Copy-Item -LiteralPath …Downloads… -Destination impl\IMPLEMENTATION_SPEC_v0.4.md`. No semantic editing of spec bytes.
**Benchmarks.** None.
**Anti-overfitting.** Spec is reference copy, not premise mutation; skeleton dirs contain no scientific claims.
**Verdict.** FOLLOWS WorkPlan §3 (root tree). No deviation. Full file placeholders + docs follow in Entries 006–007.

## Entry 006 — 2026-09-25 UTC — WorkPlan.md creation (WorkPlan §§0–13) — FOLLOWS WorkPlan (self)

**Scope.** Write the normative implementation plan dividing all practical implications of the v0.4 documents into 7 phases (more than 5–6 because workload demands it), with nothing omitted and flawless division verified by coverage matrices.
**Files made.** `impl/WorkPlan.md` (v0.4-WP1): header (IDs, parent full SHA `353ee922…`, survivor/sibling/H3T hashes, core YES/NO rule) + §0 source authority (v0.4 full-spec study + lineage + parent-seal identities + literature L0–L4) + §1 mission/scope/non-goals + §2 no-training/brutal-benchmark/anti-overfitting policy (no ML training; PSC entirely disjoint from v0.3 banks; sensitivity/mutant/clean-room/independent/exact-arithmetic controls; finite≠proof at every gate) + §3 repo contract/tree + Phases 1–7 (each: scope, spec coverage PHASE 00–19, files, code + how-to-code with exact methods/determinism/canonical order/dual tracks/formal binding, brutal benchmarks with training-disjointness, anti-overfitting, exit gates) + §11 cross-cutting (prereg 13 files, 16+ schemas, §21 order, scaling/logging/deps/AI/decision-ladder/interpretation/allowed-forbidden/seal-checklist/success/Q01–Q60→reports/citations) + §12 verification appendix (matrices A–J: PHASE→WP, theorems→WP, PSC→WP, T001–T120→WP, tests→WP, INV-001–100→WP, STOP-01–70→WP, gates→WP, Q→reports, execution method) + §13 Path.md obligation.
**Code/how.** Authored via `Write` tool in one versioned file; structure mirrors spec §§0–38 so every spec section has an explicit WorkPlan owner (see appendix matrices). “Models to train” addressed head-on in §2.1–2.3 (none; PSC = brutal entirely-different benchmarks + 8 anti-overfitting actions). Per-phase “how will you code” gives concrete module/function/hash/gate detail (e.g., pure-function Splay core with trace, `Fraction` regret, JSON-schema survivor binding, seeded/sorted PSC, sympy/z3 hooks, share-nothing clean-room, AST quantifier scan, graph-based double-spend audit, 10-point bridge checklist, closed-form negative families, artifact-derived `FINAL_RESULT`).
**Benchmarks.** Plan-level: no benchmark executed in this entry; every future benchmark is specified as negation-derived + disjoint-seed/generator/objective/size/symbolic-axis from v0.3 banks, with replay/minimization/clean-room/mutant/formal/human controls.
**Anti-overfitting.** Plan forbids finite-as-proof, constant relaxation, calculus mutation, silent DAG edits, premature consumption/bridge/decision (mapped to STOPs/INVs/tests).
**Verification of “nothing omitted”.** Appendix A–J checked before writing: 20/20 spec phases owned, 10/10 theorems owned, 7/7 PSC owned, 120/120 threats owned (machine-checkable via `threat_control_matrix.yaml` in Phase 1), full test matrix owned, 100/100 invariants owned, 70/70 stops owned, 15/15 decision gates owned, 60/60 Qs mapped. `IMPLEMENTATION_SPEC_v0.4.md` byte length re-verified (85,888).
**Verdict.** FOLLOWS the user’s WorkPlan instructions (7 phases with scope/files/code/how/benchmarks/anti-overfitting; models addressed; flawless division verified) and WorkPlan §12 (self). No deviation. WorkPlan is versioned by git; after `FOUNDATION_FROZEN` it will never be silently edited.

## Entry 007 — 2026-09-25 UTC — Path.md creation + foundation scaffolding (this file; WorkPlan §13) — FOLLOWS WorkPlan §13

**Scope.** Create this tracker and the minimal committable foundation scaffold so every Path claim resolves to a real file. This entry itself is the contemporaneous Path update for Entries 001–007.
**Files made in this entry.**
- `impl/Path.md` (this file, Entries 001–007 + status + next steps).
- Foundation scaffold (all stubs explicitly marked `STUB — Phase-1 execution pending`, no scientific claims):
  - Docs: `README.md`, `CHANGELOG.md`, `CITATIONS.md`, `AI_USE.md`, `.gitignore`.
  - Build: `pyproject.toml`, `requirements-lock.txt`, `lean-toolchain`, `lakefile.lean`.
  - `parent/README.md` (pin record: navigation `353ee92`, full `353ee922b1cee0043afa46fe8929f42f7652e5bf`, ancestor/parent commits, terminal claim, `PARENT_SEAL_MISMATCH` rule).
  - `prereg/` 13 stubs (`experiment_v0.4.yaml`, `parent_contract.yaml`, `theorem_battlefield.yaml`, `theorem_gate_matrix.yaml`, `dual_obligation_policy.yaml`, `proof_kernel_policy.yaml`, `proof_stress_corpus.yaml`, `negative_lifting_policy.yaml`, `bridge_sources.yaml`, `threat_control_matrix.yaml`, `stop_control_matrix.yaml`, `allowed_claims.md`, `forbidden_claims.md`) — structure-only, hashes pending Phase-1 freeze (`prereg_sha256.txt` to be written at freeze).
  - `math/` stubs (`definitions_v0.4.md`, 10 `theorem_MST*.md` headers, `proof_status.json` with 10 nodes `UNPROVED` + 17/18/19 `BLOCKED`).
  - `lean/` stubs (12 `.lean` headers binding to frozen statements by hash placeholder).
  - `python/` stubs (`inherited/{splay.py,pair_access.py,mstc0002.py}`, `proof_attack/` 6 files, `negative/` 4 files, `audit/verify_parent.py`, `seal/final_result.py`, `cleanroom/README.md`) — exact-semantics TODOs pointing at parent interfaces, deterministic/exact-arithmetic notes.
  - `schemas/README.md` (16-schema list + canonical JSON rules).
  - `tests/test_foundation.py` (skeleton asserting parent full-SHA + survivor-tuple + battlefield-set placeholders — executable only after Phase-1 freeze; currently documents pending checks).
  - `scripts/{run_phase00..run_phase19,reproduce_all_v0.4}.py` (20 stubs, each printing its spec PHASE + WorkPlan-phase owner + `§21` order reminder; `run_phase00.py` additionally prints the three pin SHAs).
  - `.gitkeep` placeholders in all empty `artifacts/v04/*`, `tests/*`, `lean/*` leaves so the tree is committable without fake results.
**Code/how.** `Write` tool per file (absolute paths under `impl/`); Python stubs are import-safe (`if __name__ == "__main__"` guards, no network, no holdout I/O); scripts exit `2` with `NOT_FROZEN` message until Phase-1 freeze (fail-closed, prevents accidental theorem execution). No Lean toolchain invocation (not installed — recorded, not bypassed).
**Benchmarks.** None executed (scaffold only). Test skeleton lists `PARENT-01..10`/`FORM-01..12` placeholders as pending, never green-claimed.
**Anti-overfitting.** No finite evidence generated; no theorem status changed (all `UNPROVED`/`BLOCKED` as per mapped frontier); no bridge consumed; no H3T opened; AI assistance disclosed here + `AI_USE.md` (Muse Spark via OpenCode: plan/scaffold authorship; no human ACCEPT recorded; no theorem proof claimed).
**Verdict.** FOLLOWS WorkPlan §3 (tree), §11 (prereg/schemas/AI-use scaffolds), §13 (Path contemporaneous detail). Explicit non-deviation: scaffold stubs are narrower than WorkPlan Phase-1 deliverables (full verifier/binder/PSC/Lean implementations remain pending) — recorded here as pending, not silently omitted. Next blockers: (i) run Phase-1 freeze (hash-recompute verifier, survivor binder, L2/L3 source acquisition, Lean pin, PSC freeze) to claim `FOUNDATION_FROZEN`; (ii) no Phase-2+ work until then.

---

## Status table (mirrors WorkPlan phases; updated per entry)

| WorkPlan phase | Spec PHASEs | Status after Entry 007 | Follows WorkPlan? |
|---|---|---|---|
| Phase 1 — Foundation (parent/prereg/bridge/Lean/PSC) | 00,01,02,03,04 | STARTED (study+clone+seal-inventory+skeleton+plan done; verifier/binder/source-freeze/Lean-pin/PSC-freeze execution pending) | FOLLOWS (planning subset complete; execution explicitly pending, no premature gate claimed) |
| Phase 2 — Upstream blockers (13/08U/11/09/22) | 05,06,07,08,09 | PENDING (stubs only) | FOLLOWS (not started before `FOUNDATION_FROZEN`, per §21) |
| Phase 3 — KEEP repayment (10/11) | 10,11 | PENDING | FOLLOWS |
| Phase 4 — Integrability (12/13) | 12,13 | PENDING | FOLLOWS |
| Phase 5 — Composition (17/18/19) | 14,15,16 | PENDING (`BRIDGE_SOURCE_UNAVAILABLE` fail-closed armed) | FOLLOWS |
| Phase 6 — Negative + decision | 17,18 | PENDING (dormant, no speculative mining) | FOLLOWS |
| Phase 7 — Seal/reproduce/release | 19 | PENDING | FOLLOWS |

**Theorem ledger (frozen frontier, unchanged in Entries 001–007):** `08U UNPROVED`, `09 UNPROVED`, `11 UNPROVED`, `13 PROVED-author-claim/human-review-pending (treated as UNPROVED for consumption)`, `14 UNPROVED`, `15 UNPROVED`, `22 UNPROVED`, `17 BLOCKED`, `18 BLOCKED`, `19 BLOCKED/PENDING-source-freeze`. No lifecycle jump occurred (`INV-020`, lifecycle audit pending Phase 1).

---

## Next steps (committed)

1. Commit Entries 001–007 scaffold + docs and push to `main` (user ordered commit+push without prompting — executed next, with `git status/diff/log` inspection before commit, secrets never committed).
2. Execute WorkPlan Phase 1 for real: `python scripts/run_phase00.py` (hash-recompute vs `353ee922…`/manifest/archive/`FINAL_RESULT`/candidate-set/H3T-state/lifecycle/atlas), survivor field-by-field binder, `prereg/` freeze + `prereg_sha256.txt`, L2/L3 acquisition (or `BRIDGE_SOURCE_UNAVAILABLE`), Lean toolchain pin + equivalence canaries, PSC + dual-obligation freeze — each with its own Path entry — then claim `FOUNDATION_FROZEN` only when all Phase-1 exit criteria are green.
3. Phases 2–7 strictly in order with §21 discipline; first `REFUTED` (if any) freezes the positive route and activates Phase 6 per §31; `FINAL_RESULT` derived only in Phase 6/7 from artifacts.

## Entry 008 — 2026-09-25 UTC — Scaffold generation method clarification + pre-commit verification (WorkPlan §§3,12–13) — FOLLOWS WorkPlan (clarification, no scientific deviation)

**Scope.** Preserve audit honesty about Entry 007 tooling and verify nothing is omitted before commit+push.
**Clarification (erratum-preserving, Entry 007 not rewritten).** Entry 007 states “`Write` tool per file”. Implementation used one `Write` (`_scaffold_gen.py` bulk generator, since removed via `Remove-Item -Force`, verified absent) + one `python _scaffold_gen.py` execution producing the 80 stub files + `.gitkeep` leaves (164 total filesystem objects under `impl/`), then `python -m py_compile` + `python scripts/run_phase00.py` checks. File contents are byte-identical to the stub specifications in Entry 007; the difference is execution method only, not content or WorkPlan compliance (WorkPlan mandates file existence/content/phase ownership, not agent tool choice). Helper `_scaffold_gen.py` was deleted after use so the sealed tree contains only spec-layout files.
**Pre-commit verification (“verify if needed”, WorkPlan §12).**
- `Get-ChildItem -Recurse impl` → 164 objects; `scripts/` contains `run_phase00..19` + `reproduce_all_v0.4.py` (21 files); `lean/` 13 files; `math/` 10 theorem stubs + definitions + proof_status; `prereg/` 13 stubs + allowed/forbidden; `python/` 16 stubs + cleanroom README; `IMPLEMENTATION_SPEC_v0.4.md` 85,888 bytes; `WorkPlan.md` + `Path.md` present; `artifacts/v04/` leaves exist with only `.gitkeep` (no fake results — stale-clearance holds).
- `run_phase00.py` exits `2 NOT_FROZEN` (fail-closed, correct pre-freeze behavior); `py_compile` clean.
- Coverage re-asserted: 20/20 spec PHASEs owned (WorkPlan §12-A), 10/10 theorems (B), 7/7 PSC (C), T001–T120 matrix filed as `prereg/threat_control_matrix.yaml` stub for Phase-1 population (D), full test matrix stubbed (E), INV-001–100 (F), STOP-01–70 (G), gates (H), Q01–Q60→reports (I). No theorem status changed; no bridge consumed; H3T untouched; `FOUNDATION_FROZEN` not claimed.
- Secrets scan: no tokens/keys in tree (`gh` token lives in OS keyring only, never written to repo).
**Verdict.** FOLLOWS WorkPlan §§3 (tree), 12 (verification), 13 (contemporaneous Path). No deviation.

## Entry 009 — 2026-09-25 UTC — External review intake: 12 findings, architecture PASS / freeze-hygiene FAIL_REPAIRABLE (WorkPlan v0.4-WP1 → v0.4-WP2) — FOLLOWS WorkPlan §13 (repair before FOUNDATION_FROZEN)

**Scope.** Intake an external 12-finding review (2 BLOCKER, 4 MAJOR incl. count drift, 5 MEDIUM, 1 MINOR + negative-branch tightening note). Verdict quoted: architecture PASS; freeze hygiene FAIL_REPAIRABLE. All repairs applied to `WorkPlan.md` (now v0.4-WP2) plus scaffold corrections below, before any `FOUNDATION_FROZEN` claim. No theorem status changed; no Phase-1 execution advanced beyond planning.
**Files changed (deep detail).**
- `WorkPlan.md` → v0.4-WP2 (repair release line in header). (1) Bridge/prereg ordering BLOCKER: §3 + Phase-1 files/code rewritten — `prereg/bridge_sources.yaml` populated with final L2/L3 bytes BEFORE `FOUNDATION_FROZEN`; spec Phase 02 verifies bytes and writes separate `artifacts/v04/freeze/PHASE02_BRIDGE_SOURCES_FREEZE.json`, never a prereg rewrite. (2) MST0-13 status separation: Phase-2 scope/coverage/exit rewritten — human REJECT sets reviewer gate `MST0_13_REJECTED` only; `proof_status.json` stays `UNPROVED` absent an exact negation witness (`REFUTED` needs a witness); REJECT alone never activates Phase-17 lifting. (3) Fail-fast: hard entry gates added — Phase 3 needs `13/08U/11/09/22` REVIEWED, Phase 4 needs `MST0-14` REVIEWED, Phase 5 needs all seven upstream REVIEWED; exact `REFUTED` marks later positive phases `NOT_REACHED` + jumps to Phase-6 handling (§31, Phase-6/§11 ladder text updated). (4) Payment semantics: `k6_saturation.py` formula replaced — `required=max(w,0)`, `paid=imported_MSTC0002_payment(keep_event, ledger_state)` owned by `V03_MSTC_0002.json`; old `min(pool,w)` removed except as a post-binding proved lemma. (5) Mechanical counts (verified against spec bytes via Python regex/readback: 39 `^# \d+\.` sections; 14 prereg rows; 13 `lean/` rows; 17 schema rows; 14 `tests/` rows; 11 `§26.5` rows; 24 `§27` rows; 15 `§21` arrows): header/§0/§3/Phase-1/§11/§12/§13 corrected to 39 sections, 14 prereg, 13 Lean, 17 schemas, 14 test dirs, 11 resource fields, 24 logging fields, 15-step order; counts now derived from enumerated sets. (6) `tests/mutation/`: §3 tree + Phase-7 files + §12-E rewritten — authoritative cross-theorem suite for `T099/T100` (dir already existed with `.gitkeep`, verified). (7) Lean root: §3 tree + Phase-1 files/code — `lean-toolchain/lakefile.lean/lake-manifest.json` at root, only `.lean` under `lean/`. (8) 15-step order: §3/§11/§13 “13-step” → “15-step” (all 15 asserted incl. BUILD REVIEW PACKAGE, UPDATE-AFTER-VERDICT, APPEND Path). (9) Constant scan: Phase-2 code narrowed to dependence of constants/helpers on forbidden params (dataflow), not mere occurrence of `n,T,X,Y`. (10) Taxonomy: Phase-6 coverage/`run_phase18`/exit rewritten — exactly five outcomes, “other prereg no-claim” escape hatch removed. (11) Multi-owner: §12-D/F/G + Phase-6/7 — `T120→6+7`, `STOP-70→6+7`, `INV-100→6+7`, matrix from exact IDs. (12) Trailing hyphen: header annotated — remote `…Decision-Program-` verified via `remote -v` + GitHub page, pinned verbatim. Negative tightening: Phase-6 scope/coverage — lifting needs preserved exact obstruction/witness; bare REJECT → `NEGATIVE_BRANCH_NOT_ACTIVATED`.
- `schemas/README.md`: “16” → “17 required schemas” (list already enumerated 17).
- `lake-manifest.json` (new stub at root, STUB pending Phase-1 pin; `lean/` holds only `.lean` modules).
- `python/proof_attack/k6_saturation.py`: stub rebound to imported payment semantics (see (4)).
**Code/how.** `Read` (WorkPlan full) + `Bash` Python count-verification + `Edit` per fix + `Write` for `lake-manifest.json`; duplicate `**E. Tests**` header from overlapping edits deduped; grep re-checks: zero live wrong counts, `PHASE02_BRIDGE_SOURCES_FREEZE` ×4, `MST0_13_REJECTED` ×3, `NOT_REACHED` ×10, `tests/mutation` ×7.
**Benchmarks.** None executed (plan repair only).
**Anti-overfitting.** Count-drift guard added (counts derived from sets); no finite evidence; H3T untouched; `FOUNDATION_FROZEN` still unclaimed; AI work disclosed here.
**Verdict.** FOLLOWS WorkPlan v0.4-WP2 (§§3,11,12,13) + reviewer order (fix before freeze). No deviation; Entry 008’s “13 stubs” read as 13 present files of 14 planned entries (`prereg_sha256.txt` pending freeze).

## Entry 010 — 2026-09-25 UTC — Pre-commit re-verification for WP2 repairs — FOLLOWS WorkPlan §12-J

**Scope.** Verify WP2 tree before commit+push.
**Checks.** `tests/mutation/.gitkeep` present; `lake-manifest.json` present at root; `lean/` 13 `.lean` + root configs; `prereg/` 13 present files (14th `prereg_sha256.txt` pending freeze); `IMPLEMENTATION_SPEC_v0.4.md` 85,888 bytes; `run_phase00.py` still exits 2 `NOT_FROZEN`; WorkPlan grep clean (no live stale counts/taxonomy/formula); theorem ledger unchanged (all `UNPROVED`/`BLOCKED`, no lifecycle jump); no secrets in tree.
**Verdict.** FOLLOWS WorkPlan §12 (verification). Proceeding to commit+push (user ordered, no prompt).

## Entry 011 — 2026-09-25 UTC — Second review intake: WP2 structurally strong, DON'T freeze yet (4 items + 2 nits) — FOLLOWS WorkPlan §13

**Scope.** Intake follow-up review: document/spec-level recheck confirms WP2 repairs (39/14/17/13/14/11/24, 15-step, mutation ownership, dependence-scoped scan, fail-fast gates, imported payment, multi-owner endgame). Four pre-freeze items demanded: (1) BLOCKER — WP2 REJECT semantics now better than literal spec Phase-05 (which routes REJECT to failure record + lifting) → ratify via amendment, don’t revert plan; (2) BLOCKER — terminal hole (REJECT/BLOCKED/unproved with no witness and no exhaustion fits none of the five outcomes) → add `POSITIVE_ROUTE_BLOCKED_UNRESOLVED_NO_CLAIM`; (3) MAJOR/FORMAL — bridge-acquire-before-freeze is a deliberate deviation from literal Phase-02 assignment → ratify via same amendment; (4) MINOR — `prereg/ (14 entries + prereg_sha256.txt)` reads as 15 → fix wording. Nits: “five upstream … plus constant independence” miscounts (22 is one of the five); study-history timeline ambiguity (`b091dea` LICENSE-only vs skeleton/spec creation order).
**Disposition.** All accepted. Fix vehicle: new ratified file `SPLAY_AM_DECIDE_IMPLEMENTATION_SPEC_v0.4.1_AMENDMENT.md` (A2/A3/A4) + `WorkPlan.md` v0.4-WP2 → v0.4-WP3 + stub wording + `CHANGELOG.md`. No theorem work; `FOUNDATION_FROZEN` still unclaimed.
**Verdict.** FOLLOWS reviewer order + WorkPlan §13 (repair before freeze). No deviation.

## Entry 012 — 2026-09-25 UTC — WP3 repairs: amendment + six-outcome taxonomy + typo/nits (WorkPlan v0.4-WP3) — FOLLOWS WorkPlan v0.4-WP3

**Scope.** Implement Entry-011 dispositions with deep detail matching WorkPlan granularity.
**Files made/changed.**
- `SPLAY_AM_DECIDE_IMPLEMENTATION_SPEC_v0.4.1_AMENDMENT.md` (new, RATIFIED 2026-09-25): A1 pin restatement; A2 REJECT/BLOCKED sets reviewer gate only, status stays `UNPROVED` absent exact witness, bare REJECT/BLOCKED never lifts; A3 exactly-six outcomes with new-level allowed (“blocked at named unresolved theorem(s); no refutation, no exhaustion, no YES/NO”) / forbidden (never refutation/DOC/bridge/resource, never consume blocked theorem); A4 acquisition = Phase-00 input before freeze, Phase-02 verifies + writes `artifacts/v04/freeze/PHASE02_BRIDGE_SOURCES_FREEZE.json`; A5 stack (spec bytes + amendment + WP3 + Path + hashed prereg); A6 effect. V0.4 bytes untouched.
- `WorkPlan.md` → v0.4-WP3: header normative line + version line; core rule (+ new level); §0 timeline sentence (b091dea LICENSE-only; skeleton/spec uncommitted afterward) + new item 6 (amendment in stack); §3 tree (+ amendment file; prereg typo → “14 entries total, including prereg_sha256.txt”); Phase-2 scope (“five upstream nodes, including constant independence”); Phase-2 coverage/exit (+ `MST0_13_BLOCKED` gate, blockage → new no-claim routing); Phase-6 coverage/run_phase18/exit (five → six outcomes, unresolved-blockage routing, escape hatch stays removed); §11 allowed/forbidden (10 levels incl. new wording); `CHANGELOG.md` (WP3/WP2 lines).
- `prereg/allowed_claims.md` / `prereg/forbidden_claims.md`: new-level allowed/forbidden lines.
**Code/how.** `Write` (amendment) + `Edit` per item + `Select-String` re-grep: “exactly five” 0, “13-step” 0, “14 entries +” 0, “exactly six” live; §12-D/F/G multi-owner retained.
**Benchmarks.** None (plan + amendment only).
**Anti-overfitting.** Amendment prevents decision-machine lying about stop reason; bare REJECT still can’t lift; counts/meanings frozen before evidence; H3T untouched.
**Status table delta.** WorkPlan v0.4-WP3; theorem ledger unchanged (all `UNPROVED`/`BLOCKED`); Phase 1 still STARTED (planning), Phases 2–7 PENDING; `FOUNDATION_FROZEN` not claimed.
**Verdict.** FOLLOWS WorkPlan v0.4-WP3 (§§1,3,11,12,13) + v0.4.1 A2–A4. No deviation.

## Entry 013 — 2026-09-25 UTC — Third review intake: 2 pre-freeze blockers + 3 cleanups (WP3 → WP4) — FOLLOWS WorkPlan §13

**Scope.** Intake follow-up review: amendment issues resolved; remaining gates are (1) BLOCKER — `REFUTE(MST0-17)` lacks dedicated search/schema/replay/namespace precision; (2) BLOCKER — PSC “skeletons now, full implementations later” contradicts freeze-before-attacks; cleanups (a) MST0-19 BLOCKED-vs-REFUTED, (b) “disjoint by construction” overclaim, (c) “created verbatim” tree wording vs amendment file. All accepted; fix vehicle WP4 below. No theorem work; `FOUNDATION_FROZEN` unclaimed.
**Verdict.** FOLLOWS reviewer order (fix before freeze). No deviation.

## Entry 014 — 2026-09-25 UTC — WP4 repairs: REFUTE(MST0-17) + PSC spec-freeze + 3 cleanups (WorkPlan v0.4-WP4) — FOLLOWS WorkPlan v0.4-WP4

**Scope.** Implement Entry-013 dispositions.
**Files made/changed.**
- `WorkPlan.md` → v0.4-WP4: Phase-5 coverage (exact `REFUTE(MST0-17)` negation `∃T,X,Y≼X: Splay(Y,T) > 2·Splay(X,T)+A(n)`, MST0-19 BLOCKED-vs-REFUTED rule), files (`pair_access_search.py`, `cleanroom/pair_access_check.py`, `proof_attacks/{pair_access,telescope}/`, `counterexamples/pair_access/`, `PA-06` hardening on top of spec-minimum `PA-01..05`), code (`pair_access_search` evaluator + witness record + canonical minimization + inflation + clean-room agreement; bridge mismatch → BLOCKED never refutation), benchmarks (“independently generated” + hash-exclusion), exit (`MST0_17_REFUTED` routing, BLOCKED levels); Phase-1 PSC freezer (complete machine-readable specs normative, skeletons placeholder-only, conformance harness + `NOT_CONFORMED` guards, `STOP-17`); §2.1 generator list (+ `pair_access_search.py`, spec+conformance); §2.2 (§26.1 schedules under frozen spec) + Phases 2/3/4 (“disjoint…” → “independently generated” + hash-exclusion); §3 tree (“§18 layout implemented completely, plus explicit amendment artifact”); §11 prereg (battlefield incl. REFUTE-17 namespace, corpus spec+conformance, lifting witness-only, bridge pre-freeze).
- New stubs: `python/proof_attack/pair_access_search.py` (negation-bound evaluator spec), `python/cleanroom/pair_access_check.py`, `artifacts/v04/{counterexamples,proof_attacks}/pair_access/.gitkeep` (namespaces; no fake witnesses).
- `prereg/proof_stress_corpus.yaml`: spec-normative wording + conformance requirement. `CHANGELOG.md`: WP4 lines. No new schema file (witness reuses `proof_attack.schema.json` + `pair_access_certificate.schema.json` evaluation; 17-schema count preserved).
**Code/how.** `Read` (Phase-5/§11/§2) + `Edit` per item + `Write` ×2 stubs + `New-Item` namespaces + `py_compile` green; `Select-String` re-grep: “disjoint” 0 live overclaims, “created verbatim” 0, “exactly six” live, `pair_access_search` wired.
**Benchmarks.** None executed (plan + stubs only).
**Anti-overfitting.** REFUTE-17 survival never proof; PSC spec frozen before implementations; bare mismatch never refutation; overlap never claimed by prose; H3T untouched.
**Status table delta.** WorkPlan v0.4-WP4; ledger unchanged; Phase 1 STARTED, rest PENDING; `FOUNDATION_FROZEN` not claimed.
**Verdict.** FOLLOWS WorkPlan v0.4-WP4 + v0.4.1 A2–A4. No deviation.

## Entry 015 — 2026-09-25 UTC — Fixup: nested .gitkeep exclusion (WP4 follow-up) — FOLLOWS WorkPlan §3

**Scope.** Post-push check showed `artifacts/v04/{counterexamples,proof_attacks}/pair_access/.gitkeep` untracked: git cannot re-include a file inside an excluded parent dir, so the generic `!artifacts/v04/*/*/.gitkeep` line was insufficient while `artifacts/v04/counterexamples/*` excluded the `pair_access/` dir itself.
**Fix.** `.gitignore` now explicitly un-ignores both dirs and their `.gitkeep` files. Namespaces (`pair_access/` counterexamples + proof-attacks, empty by design — no fake witnesses) commit in this fixup.
**Verdict.** FOLLOWS WorkPlan §3 (empty-by-design namespaces). No deviation; Entry-014 claims now fully versioned.

## Entry 016 — 2026-09-25 UTC — Fourth review intake: 1 HARD blocker + 1 verification item + 2 header cleanups + 1 hardening (WP4 → WP5) — FOLLOWS WorkPlan §13

**Scope.** Intake follow-up review: (1) HARD — WP4 `REFUTE(MST0-17)` targeted the endpoint-free inequality, but frozen MST0-17 is the composition inequality with `E_m−E_0`; attacking the downstream form lets a negative endpoint term mask a missed violation. (2) Path header still says WP1 though plan is WP4. (3) Header omits normative v0.4.1 amendment. (4) Verify PSC specs are genuinely complete 12-field semantics, not conformance-declaring stubs. (5) Hardening: bind refutation executables to theorem/negation SHAs. All accepted; vehicle WP5 below. No theorem work; `FOUNDATION_FROZEN` unclaimed.
**Verdict.** FOLLOWS reviewer order (fix #1 before freeze; verify #4). No deviation.

## Entry 017 — 2026-09-25 UTC — WP5 repairs: endpoint-aware negation + living headers + complete PSC + SHA guard (WorkPlan v0.4-WP5) — FOLLOWS WorkPlan v0.4-WP5

**Scope.** Implement Entry-016 dispositions.
**Files made/changed.**
- `WorkPlan.md` → v0.4-WP5: Phase-5 coverage (exact negation `∃n,T,X,Y≼X,ledger: Splay(Y,T)+E_m−E_0 > 2·Splay(X,T)+A(n)` with `lhs/rhs` definitions + 15-field payload list + MST0-18 separation note); `pair_access_search` bullet (endpoint-aware evaluator, full payload, SHA-guard abort); new SHA-bind guard bullet (every refutation executable aborts unless loaded statement/negation SHAs equal `theorem_battlefield[ID]` SHAs; evaluator derived from versioned obligation; `STOP-15/16`); §12-C (exactly-7-families + interface note); version line.
- `python/proof_attack/pair_access_search.py`: stub rewritten to endpoint-aware negation + 15-field payload + SHA-guard (the prose drift that caused this blocker is now a startup failure by construction).
- `prereg/proof_stress_corpus.yaml`: REPLACED stub with complete machine-readable specs — YAML-validated: exactly 7 families (`PSC-L/P/B/K6/I/T/N`) + 1 `refutation_interfaces/REFUTE-MST0-17` entry (not an 8th family), all carrying the 12 required fields (domain, constructors, ranges, seeds, objectives, symbolic domains, minimization, canonical order, replay, independent-check, allowed freedom, forbidden changes); conformance harness section with `NOT_CONFORMED` guards + `STOP-17`. Verification: `yaml.safe_load` + field-presence check green (missing: NONE).
- `Path.md` headers: Plan → “current revision v0.4-WP5; history preserved below”; normative line + v0.4.1 amendment. Old entries untouched (provenance intact).
- `CHANGELOG.md`: WP5 lines.
**Code/how.** `Read` (Phase-5/Path headers/stubs) + `Edit` per item + `Write` (YAML) + `Bash` YAML validation (`safe_load`, family keys, 12-field presence); PSC-N mis-nesting under `refutation_interfaces` caught by validation and repaired (swap + duplicate removal, re-validated 7+1).
**Benchmarks.** None executed (plan + specs + stubs only).
**Anti-overfitting.** Endpoint omission class eliminated by SHA derivation; PSC behavior frozen before implementations; H3T untouched.
**Status table delta.** WorkPlan v0.4-WP5; ledger unchanged; Phase 1 STARTED, rest PENDING; `FOUNDATION_FROZEN` not claimed.
**Verdict.** FOLLOWS WorkPlan v0.4-WP5 + v0.4.1 A2–A4. No deviation.

## Entry 018 — 2026-09-25 UTC — Fifth review intake: 2 freeze-readiness verifications (WP5 → WP6) — FOLLOWS WorkPlan §13

**Scope.** Intake verification review: (1) v0.4.1 A5 literally binds WP3 while plan is WP5 — pre-freeze revision allowed, but stack must bind the living revision by rule or ratify WP5 at Phase 00. (2) WP5 reuses `proof_attack` + `pair_access_certificate` schemas for the endpoint-aware witness — verify they can actually encode `E_0/E_m`, ledger identity/trace, subsequence certificate, `lhs`/`rhs`, strict residual (restrictive `additionalProperties:false` on the payload path would break the contract). Both accepted as verification items (architecture not in dispute).
**Verdict.** FOLLOWS reviewer order (verify before freeze). No deviation.

## Entry 019 — 2026-09-25 UTC — WP6 repairs: v0.4.2 binding + authored schemas + green validation (WorkPlan v0.4-WP6) — FOLLOWS WorkPlan v0.4-WP6

**Scope.** Implement Entry-018 dispositions.
**Files made/changed.**
- `SPLAY_AM_DECIDE_IMPLEMENTATION_SPEC_v0.4.2_AMENDMENT.md` (new, RATIFIED 2026-09-25): B1 rebinds the stack to the final pre-freeze WorkPlan revision by rule (sealed by `prereg_sha256.txt` at freeze; no version-tag freeze — v0.4/v0.4.1 bytes untouched, A2–A4 in force); B2 requires the witness payload to validate under both schemas with no closed-world blockers, demonstrated by a validation record freeze artifact.
- `schemas/proof_attack.schema.json` (new): §8.4 envelope (12 required fields) + open-world `exact_witness` object with typed endpoint-aware payload properties (`E_0/E_m` rationals, `L_0/L_m` ledger refs with energy, `subsequence_certificate`, `paired_execution`, `block_decomposition`, costs, `lhs/rhs/residual`); envelope-level `additionalProperties:false` constrains only the 12-field record shell, never the payload path (B2-compliant).
- `schemas/pair_access_certificate.schema.json` (new): MST0-17 evaluation (`theorem_id` const, statement SHA, witness ref, `n`, ledger hashes, energies, costs, `A_n`, `lhs/rhs/residual`, strict-positive flag, subsequence certificate, block hash, replay/checker).
- Validation: sample endpoint-aware witness (lhs 26 > rhs 20, residual 6) validated green through both schemas with project-pinned jsonschema 4.25.1; record `artifacts/v04/freeze/WITNESS_SCHEMA_VALIDATION.json` (schema SHAs `97590c598934…` / `490ccf8aebc8…`, gitignored freeze artifact, SHA-logged here).
- `WorkPlan.md` → v0.4-WP6 (normative line, version, §0 stack item, §3 tree, §11 schemas note, Phase-5 validation parenthetical); `Path.md` headers (WP6, both amendments); `CHANGELOG.md` (WP6 lines).
**Code/how.** `Write` (amendment + 2 schemas) + `Bash` validation (`jsonschema.validate` ×2 green) + record writer (SHA-256) + `Edit` per item.
**Benchmarks.** None (schemas + validation only; sample is a shape check, not evidence).
**Anti-overfitting.** Payload fields optional at the witness-object level by design (attack-survived `null` + other theorems unaffected); closed-world risk eliminated on the payload path; H3T untouched.
**Status table delta.** WorkPlan v0.4-WP6, inside its own stack by B1 rule; ledger unchanged; Phase 1 STARTED, rest PENDING; `FOUNDATION_FROZEN` not claimed.
**Verdict.** FOLLOWS WorkPlan v0.4-WP6 + v0.4.1 A2–A4 + v0.4.2 B1–B2. No deviation.

**End of Path entries so far (append-only below this line).**
