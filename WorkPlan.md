# SPLAY-AM-DECIDE-v0.4 WorkPlan

**Experiment:** `SPLAY-AM-DECIDE-v0.4` — Universal Pair-Access Closure and Dynamic-Optimality Decision Program
**Normative spec:** `IMPLEMENTATION_SPEC_v0.4.md` (frozen v0.4 spec, 39 numbered sections 0–38, PHASE 00–19, this repo root) + ratified pre-freeze amendments `SPLAY_AM_DECIDE_IMPLEMENTATION_SPEC_v0.4.1_AMENDMENT.md` (A2 REJECT!=REFUTED, A3 `POSITIVE_ROUTE_BLOCKED_UNRESOLVED_NO_CLAIM` → six outcomes, A4 bridge-acquire-before-freeze) + `SPLAY_AM_DECIDE_IMPLEMENTATION_SPEC_v0.4.2_AMENDMENT.md` (B1 living-revision stack binding sealed by manifest, B2 witness-schema compatibility rule; v0.4/v0.4.1 bytes preserved)
**Spec authoring status:** `PRE_FREEZE_PARENT_PIN_REQUIRED` — no Phase 01+ theorem-facing execution before `FOUNDATION_FROZEN`.
**Target problem:** Is ordinary bottom-up Splay dynamically optimal? (Sleator–Tarjan Dynamic Optimality Conjecture)
**Primary positive route:** sealed v0.3 survivor `MSTC-0002 = (P_all, k=6, C=2)` → `MST0-08U/09/11/13/14/15/22 REVIEWED` → `MST0-17 REVIEWED` → `MST0-18 REVIEWED` → `MST0-19 REVIEWED` → Universal Pair Access → Approximate Monotonicity → Dynamic Optimality.
**Primary negative route:** exact universal obstruction → closed-form obstruction family → legal real-Splay `(T_m, X_m)` with `Splay(X_m,T_m) >= g(m)` + explicit legal BST competitor `<= f(m)` with `g(m)/f(m) -> infinity` → Dynamic Optimality disproved.
**Plan version:** v1.0 (clean-rebuild release: all freeze-hygiene repairs from the prior history cycle folded in from the start; versioned by git history, never silently edited after `FOUNDATION_FROZEN`)
**WorkPlan phases:** 7 (Phase 1–7) covering all 20 spec phases (PHASE 00–19). 7 is used instead of 5–6 because the workload is large (10 theorem nodes, 7 PSC families, Lean kernel, 120 threats, 100 invariants, 70 stops, decision + seal). Nothing is omitted; see §12 Verification Appendix for exhaustive coverage matrices.
**Implementation repo:** `Dynamic-Optimality-Lab/Universal-Pair-Access-Closure-and-Dynamic-Optimality-Decision-Program-` (trailing hyphen verified as the actual remote name, not a typo — `git remote -v` + GitHub page; pinned verbatim in artifacts)
**Parent repo:** `Dynamic-Optimality-Lab/splay-multiscale-transfer` (`SPLAY-AM-MST-v0.3`)
**Parent navigation commit (short):** `353ee92`
**Parent full sealed HEAD (verify at Phase 1 from clone):** `353ee922b1cee0043afa46fe8929f42f7652e5bf`
**Parent terminal claim (expected, hash-verify in Phase 1):** `TRANSFER_CALCULUS_SURVIVES_FINITE_TESTS`
**Parent chain aides:** v0.3 parent `38c1be6afd2ab2420aa094c68ce45ee6a26b3628` (`SPLAY-AM-BD-v0.2`, `FINITE_DEBT_LAW_MINING_RESULTS`), ancestor `6de1ca2a595e8895f54794f3a211fe6ee1a95a80` (`SPLAY-AM-PD-v0.1`, `FINITE_EXACT_BN_RESULTS`).
**Survivor (immutable input):** `MSTC-0002 = (P_all, k=6, C=2)`, unique v0.3 fresh-H3T + clean-room + large-n survivor. Siblings killed fresh: `MSTC-0001 (P_all,k=2,C=2)` max residual 8 (first witness n=32 idx=4406), `MSTC-0003 (P_keep,k=1,C=6)` max residual 23 (first witness n=16 idx=3610). Survivor fresh pass: 70,000/70,000 max residual 0. Candidate-set hash `8FD3273143DEC3CA4611A1093F3521B8F22DE2BBD6A82715EE270412F65A2A00`. H3T state `UNLOCKED_ONCE/unlocks=1`, never to be re-unlocked.
**Core rule:** YES (`DYNAMIC_OPTIMALITY_PROVED`) or NO (`DYNAMIC_OPTIMALITY_DISPROVED`) are the only successful terminal outcomes. Honest no-claim levels (`RESOURCE_LIMIT_NO_CLAIM`, `POSITIVE_ROUTE_REFUTED_NO_DOC_NEGATIVE`, `POSITIVE_ROUTE_BLOCKED_UNRESOLVED_NO_CLAIM` per v0.4.1 A3, `BRIDGE_BLOCKED_NO_CLAIM`) are allowed and preferred over an invalid binary claim. No finite-survival result is ever a theorem premise.

---

## 0. Source authority (study-first record)

This plan was built only after deep study of the controlling v0.4 spec in full (3240 lines, 39 numbered sections 0–38, PHASE 00–19, T001–T120, INV-001–100, STOP-01–70, full test matrix, Q01–Q60), the lineage headers (v0.3 transfer-ledger pivot, v0.2 Bellman-debt pivot, v0.1 pair-dynamics), the parent seal artifacts (ledger, theorem status, FINAL_RESULT, holdout commitments, v0.3.1 pin), and both GitHub repos. Timeline: the implementation repo at reset held only `LICENSE`; the skeleton and verbatim spec copy below were created afterward, in that order.

1. **Controlling document — v0.4 spec (39 numbered sections 0–38):** §§0–1 (survivor table, blocker DAG `08U/09/11/13/14/15/22/17/18/19`, positive/negative chains, no-calculus-discovery, finite≠proof doctrine, Pair-Access form `Splay(Y,T) ≤ 2·Splay(X,T)+A(n)`, constant policy `C=2/k=6/P_all` frozen, YES/NO-only rule, 17 non-goals); §2 (parent lineage, read-only evidence, `PARENT_SEAL_MISMATCH` fail-closed, parent `Path.md` as audit inheritance); §3 (L0–L4 literature; `MST0-19` never leaves PENDING without exact bytes; per-source record schema); §4 (Splay/Pair-Access/survivor contract: cost `depth+1`, KEEP/DELETE, `w=y−2a`, wrap-never-mutate); §5 (Lean 4 kernel: frozen toolchain, core objects, 3-layer certificate, `FORMALIZATION_MISMATCH`); §6 (exactly 10 nodes; child-lemma registration rule); §7 (dual PROVE/REFUTE; lifecycle `UNPROVED→PROVED→REVIEWED`, `UNPROVED→REFUTED`, erratum rule); §8 (PSC: 7 families `PSC-L/P/B/K6/I/T/N`, never proof, attack-record schema); §§9–15 (per-theorem attack/proof contracts for 08U/11/09/13/22/14/15); §16 (negative lifting: dormant-until-REFUTED, `g/f→∞` with explicit competitor, ledger independence); §17 (outcome taxonomy); §18 (repository layout); §19 (14 prereg entries: 13 source files + freeze manifest `prereg_sha256.txt`, which hashes those 13 + bound files and never itself); §20 (17 schemas, canonical JSON rules); §21 (deterministic 15-step order: VERIFY hashes → LOAD contract → ASSERT gates → ASSERT binding → ASSERT kernel → LOAD theorem+negation → REFUTE-first/parallel → PROOF → append-only raw → formal cert → independent check → mutants → BUILD HUMAN REVIEW PACKAGE → UPDATE STATUS ONLY AFTER HUMAN VERDICT → APPEND Path.md; no prereg rewrite after `FOUNDATION_FROZEN`); §22 (PHASE 00–19); §23 (threats `T001–T120`); §24 (test matrix over 14 directories: `parent/`, `formal/`, `locality/`, `preservation/`, `boundary/`, `injection/`, `repayment/`, `integrability/`, `constants/`, `pair_access/`, `bridge/`, `negative/`, `mutation/`, `seal/`); §25 (invariants `INV-001–100`); §26 (scaling, symbolic-before-brute, 11-field resource-failure record); §27 (24-field append-only run records); §28 (deps); §29 (AI policy, mandatory `AI_USE.md`); §30 (stops `STOP-01–70`); §31 (decision ladder `DEC-GATE-00..14`, `NEG-GATE-00..06`; first refutation freezes the route); §32 (8 interpretation rules); §33 (allowed/forbidden claims); §34 (seal checklist); §35 (S1/S2 success only); §36 (Q01–Q60); §37 (citations); §38 (intent).
2. **Lineage documents (evidence, never premises):** v0.3/v0.2/v0.1 spec headers and pivots (understand the frozen search stop; never theorem premises).
3. **Parent repository (read-only reference clone):** ledger (frozen set, set hash, T7/T5/T6 semantics), theorem-status report (10/4/3/3/6), FINAL_RESULT (terminal, kills, firewalls, hashes), holdout commitments (`UNLOCKED_ONCE`), v0.3.1 pin (parent/ancestor commits, spec SHA), parent `Path.md` (audit inheritance, never premise).
4. **Implementation repository:** reset to `LICENSE`-only (commit `543ca6f`); `artifacts/v04/` starts empty by design (only new results present; stale files trigger `STALE_CLEARANCE.json` + `STOP-68/69`).
5. **Frozen literature (hash-freeze in Phase 1, never consume before):** L1 context, L2/L3 bridge premises only after source freeze + convention audit, L4 context-only. No web summary overrides frozen bytes (`INV-099`).
6. **Ratified pre-freeze amendments (normative):** v0.4.1 (A2 REJECT!=REFUTED with `MST0_13_REJECTED`/`MST0_13_BLOCKED` reviewer gates, A3 six-outcome taxonomy, A4 bridge-acquire-before-freeze with separate `PHASE02_BRIDGE_SOURCES_FREEZE.json`) + v0.4.2 (B1 living-revision binding sealed by manifest, B2 witness-schema compatibility rule). Normative stack: spec + amendments + final pre-freeze WorkPlan + `Path.md` + hashed `prereg/`.

---

## 1. Mission and scope boundary

**Mission.** Execute the frozen decision program exactly as specified and emit the strongest mathematically justified terminal level — `DYNAMIC_OPTIMALITY_PROVED`, `DYNAMIC_OPTIMALITY_DISPROVED`, or an exact honest no-claim level — deterministically, exactly, certificate-first, dual prove/refute, formal-kernel checked, hostile-review gated, obstruction-preserving, fail-closed, reproducible from fresh checkout.

**Central questions (frozen).** Is ordinary bottom-up Splay dynamically optimal? Positive: does frozen `MSTC-0002=(P_all,k=6,C=2)` satisfy the complete arbitrary-n Pair-Access chain? Negative: if that chain fails, can the exact obstruction be lifted to a closed-form real-Splay family with unbounded Splay/OPT?

**Positive chain (frozen, DEC-GATE-00..14).** Sealed MSTC-0002 → 08U/09/11/13/14/15/22 REVIEWED → 17 REVIEWED → 18 REVIEWED → 19 REVIEWED → UNIVERSAL PAIR ACCESS → APPROXIMATE MONOTONICITY → DYNAMIC OPTIMALITY. Pair-Access form `Splay(Y,T) ≤ 2·Splay(X,T) + A(n)` (`A(n)=0` preferred; nonzero only if exact, length-independent, explicit, bridge-accepted, deficit-free).

**Negative chain (frozen, NEG-GATE-00..06, dormant until exact REFUTED).** Exact obstruction → closed-form family → legal `(T_m,X_m)` → Splay ≥ g(m) + explicit competitor ≤ f(m) → g/f → ∞ → DISPROVED. Local residual / Pair-Access counterexample without reduction is never a DOC disproof (`T079–T081`, `STOP-60`).

**In scope.** All §§2–22 divided into Phases 1–7 below, with threats/tests/invariants/stops/logging/AI-use throughout.

**Out of scope / non-goals (spec §1.7, `STOP-05/25/26`, `INV-008/014/017`).** No calculus discovery (no new P/k/C/support/injection/transfer/scale/mapping/energy under v0.4 ID); no silent constant relaxation; no minimality claims; no local→global or failure→DOC-false inferences; no assistant/review/formal substitution fallacies; no bridge before source+convention freeze; no literature-driven DAG edits; no resource-exhaustion-as-evidence. Mutations need a new experiment ID.

---

## 2. No-model-training, brutal-benchmark, and anti-overfitting policy

There are **no ML models to train** in v0.4. The user-requested training/benchmark/overfitting policy is instantiated for this theorem-decision program:

**2.1 No training.** `MSTC-0002` is immutable input. No fitting, hyperparameter search, constant ladder, grammar search, or threshold tuning on the theorem path. Attack generators are deterministic exact falsification instruments with parameters preregistered in `proof_stress_corpus.yaml` before attacks and frozen (`STOP-17`, `INV-034`). Statistical conjecture tools, if any, are quarantined as theorem-mining only with `AI_USE.md` disclosure.

**2.2 Brutal benchmarks entirely separate from any training-adjacent data.** The sealed v0.3 corpus (dev + consumed `HOLDOUT-H3T-v0.3`, 70,000 episodes + large-n sweep) is NEVER reused as a benchmark: H3T stays `UNLOCKED_ONCE/1` (`STOP-08/09`, `INV-012`, `T007`); finite survival is never a premise (`INV-014`, `T008/09`). Every attack uses fresh negation-derived families (deterministic schedules `16..1024+` plus symbolic parameters plus SMT where applicable), independently generated from v0.3 banks — canonical episode hashes compared to exclude reuse where bank bytes are available, otherwise stated as independently generated (zero overlap never claimed by prose alone). Controls: `k=2` kill replay as must-fail control, `C=1/k=5` mutants, formal mutants, missing-case mutants, known-killed control (`T100`). Independence: generators know negations only (`INV-036`, `STOP-18`); clean-room shares no helpers (`INV-037`, `STOP-19`); independent bridge reconstruction (`BR-09`); finite-canary agreement plus symbolic proof, never finite-maximum premises. Exactness: integer/rational arithmetic only (`INV-093`, `STOP-20`); SAT with exact replay / UNSAT with certificate (`STOP-21/22`); frozen canonical witness order with deterministic post-sort (`INV-039/091/092`, `STOP-23`). Survival is recorded as attack-survived, never proof (`INV-035`); refutations append-only with replay (`INV-040`, `STOP-24`); failed attempts and mutants retained (`INV-089/090`, `STOP-67`).

**2.3 Anti-overfitting (= anti finite-premise upgrade).** Universal statements quantify arbitrary `n` explicitly (`MST0-22`: `∃C=2,k=6 ∀n,T,X,Y`); locality/preservation/repayment/integrability proofs are symbolic, not empirical maxima; constants proved uniform (no n/length/tree/subsequence/decomposition/corpus/holdout/seed/panel dependence, `CONST-01..08` — static scans support only); credit-use graph proves lifecycle/conservation/acyclicity/independence/endpoint bounds; telescope controls `E_m/E_0/A(n)` with bridge-compatible term; bridge consumes exact frozen bytes with 9-point convention match; decision recomputed from artifact hashes; seal regenerates `FINAL_RESULT` solely from statuses/certificates/reviews/counterexamples/bridge audit (`SEAL-11`, `INV-096`).

---

## 3. Repository contract and layout

Deterministic Python (semantics, falsification, certificates, audits, reproduction) + Lean 4 (formalization); Rust only behind exact-agreement gates. Every phase follows the §21 15-step order. Prereg freeze ordering: `prereg/bridge_sources.yaml` is populated with final L2/L3 bytes BEFORE `FOUNDATION_FROZEN`; spec Phase 02 verifies those bytes and writes only the separate `artifacts/v04/freeze/PHASE02_BRIDGE_SOURCES_FREEZE.json` — never a post-freeze prereg rewrite. Freeze-integrity contract: `prereg_sha256.txt` hashes exactly `PREREG_PAYLOAD_FILES` (13 source files) ∪ `FREEZE_BOUND_FILES`, where the manifest never hashes itself (no `H(manifest containing H(manifest))`), and the living `Path.md` is bound via the immutable snapshot `artifacts/v04/freeze/PATH_AT_FOUNDATION_FREEZE.md` (living Path stays append-only; freeze script verifies it still opens with the snapshot bytes; missing/mismatching lines fail closed as `STOP-06`).

**Root tree (§18 layout implemented completely, plus explicit amendment artifacts; `artifacts/v04/` starts empty):** this repo root: `README.md`, `IMPLEMENTATION_SPEC_v0.4.md`, `SPLAY_AM_DECIDE_IMPLEMENTATION_SPEC_v0.4.1_AMENDMENT.md`, `SPLAY_AM_DECIDE_IMPLEMENTATION_SPEC_v0.4.2_AMENDMENT.md`, `WorkPlan.md`, `Path.md`, `CHANGELOG.md`, `CITATIONS.md`, `AI_USE.md`, `LICENSE`, `pyproject.toml`, `requirements-lock.txt`, `lean-toolchain`, `lakefile.lean`, `lake-manifest.json` (all three Lean configs at root — only `.lean` modules under `lean/`), `bridge_sources/` (L2/L3 byte store; manifest remains `prereg/bridge_sources.yaml`), `parent/` (10 hash-verified V03 files + `BOOTSTRAP_MANIFEST.sha256`), `prereg/` (14 entries total, including `prereg_sha256.txt`: 13 contract files + manifest), `math/` (10 theorem docs + `negative/` + `reviews/` + `proof_status.json` + `definitions_v0.4.md`), `lean/` (13 files: `Splay/Core.lean`, `Splay/PairAccess.lean`, `MSTC0002/{Ledger,Locality,Preservation,Boundary,Injection,Repayment,Integrability,Constants}.lean` (8), `PairAccess/{Composition,Telescope}.lean` (2), `Negative/Family.lean` (1)), `python/` (`inherited/`, `formal_bridge/`, `proof_attack/{locality_explosion,primitive_exhaust,boundary_torture,k6_saturation,double_spend,telescope_torture,pair_access_search}.py`, `negative/{lift_obstruction,splay_lower,competitor_upper,family_replay}.py`, `audit/`, `seal/`, `cleanroom/`), `schemas/` (17 schemas), `tests/` (14 directories: `parent/`, `formal/`, `locality/`, `preservation/`, `boundary/`, `injection/`, `repayment/`, `integrability/`, `constants/`, `pair_access/`, `bridge/`, `negative/`, `mutation/`, `seal/` — `tests/mutation/` authoritative for `T099/T100`), `artifacts/v04/{freeze,formal,proof_attacks,counterexamples,proofs,negative,audits,logs,seal}/`, `scripts/{run_phase00..run_phase19,reproduce_all_v0.4}.py` (+ `freeze_foundation.py` repair orchestrator).
Git hygiene: generated datasets/traces/heavy outputs ignored; small verification reports, manifests, and freeze evidence tracked; archive canonical-ordered rebuild-identical.

---

## 4. Phase 1 — Foundation freeze: parent pin, prereg, bridge sources, formal kernel, PSC (spec PHASE 00–04)

**Scope.** Create the immutable battlefield before any proof search or refutation attack. Gates: `FOUNDATION_FROZEN`, `SURVIVOR_IDENTITY_VERIFIED`, `BATTLEFIELD_VERIFIED`, `BRIDGE_SOURCES_FROZEN` (or fail-closed `BRIDGE_SOURCE_UNAVAILABLE`), `FORMAL_KERNEL_FROZEN`, `PSC_FROZEN`, `DUAL_OBLIGATIONS_FROZEN` (DEC-GATE-00..03).

**Spec coverage.** PHASE 00 (pin seal: FINAL_RESULT/MANIFEST/archive/Path/WorkPlan/MSTC-0002/candidate-set/H3T/lifecycle/atlas/theorem docs + freeze spec/prereg/battlefield/ledger); PHASE 01 (survivor binding field-by-field + fresh-history integrity without re-unlock + blocker-DAG re-derivation `08U/09/11/13/14/15/22/17/18/19`); PHASE 02 (L2/L3 exact bytes acquired BEFORE freeze + convention checklist + independent extraction; Phase-02 script verifies and writes only the separate freeze file); PHASE 03 (Splay ROOT/ZIG/LL/RR/LR/RL + cost + KEEP/DELETE/subsequence + MSTC-0002 field binding; finite-canary agreement, symbolic proof reserved); PHASE 04 (PSC-L/P/B/K6/I/T/N as complete machine-readable specs + exact statement/negation/attack-interface/mutant freeze; later implementations need conformance-harness green, `STOP-17`).

**Files to be made.** `parent/{V03_SEAL.json,V03_FINAL_RESULT.json,V03_MANIFEST.sha256,V03_ARCHIVE.sha256,V03_PATH_FINAL.md,V03_WORKPLAN_FINAL.md,V03_MSTC_0002.json,V03_THEOREM_STATUS.json,V03_COUNTEREXAMPLE_INDEX.json,BOOTSTRAP_MANIFEST.sha256}` (hash-verified copies + provenance-built records, read-only) + `bridge_sources/` (L2/L3 bytes + README; manifest `prereg/bridge_sources.yaml`) + `prereg/` (14 entries; `bridge_sources.yaml` populated before freeze) + `artifacts/v04/freeze/{PHASE02_BRIDGE_SOURCES_FREEZE.json,PATH_AT_FOUNDATION_FREEZE.md,SUPERSEDED_*.json,FOUNDATION_FROZEN.json,WITNESS_SCHEMA_VALIDATION.json}` (separate verification records, snapshot, supersession records, validation record) + `prereg_sha256.txt` (freeze manifest over exactly payload ∪ bound, never itself) + root Lean configs (`lean-toolchain`, `lakefile.lean`, `lake-manifest.json`; only `.lean` modules under `lean/`) + `lean/{Splay/Core,Splay/PairAccess,MSTC0002/Ledger}.lean` (kernel subset; full 13 bound by hash) + `python/inherited/{splay,pair_access,mstc0002}.py` (exact core) + `math/{definitions_v0.4.md,10 theorem docs with hashed canonical Statement/Negation lines,proof_status.json at mapped frontier}` + `schemas/` (17: authored `proof_attack` with open-world witness payload + `pair_access_certificate` with mandatory load-bearing fields, sample-validated) + `tests/{parent/,formal/,mutation/}` + `scripts/{run_phase00..run_phase04,freeze_foundation,reproduce_all_v0.4}.py`.

**Files to be made.** `parent/` (10 hash-verified files, read-only) + `bridge_sources/` (L2/L3 bytes + README; manifest `prereg/bridge_sources.yaml`) + `prereg/` (14 entries; `bridge_sources.yaml` populated before freeze) + `artifacts/v04/freeze/PHASE02_BRIDGE_SOURCES_FREEZE.json` (separate verification record) + root Lean configs + `lean/` modules + `python/inherited/` exact core + `math/` (definitions, 10 theorem docs with hashed canonical Statement/Negation lines, `proof_status.json` at mapped frontier) + `schemas/` (17, incl. authored `proof_attack` + `pair_access_certificate` with sample-validated endpoint payload) + `tests/{parent/,formal/}` (+ `tests/mutation/` skeleton) + `scripts/{run_phase00..run_phase04,freeze_foundation,reproduce_all_v0.4}.py`.

**Code to produce and how to code.** Exact BST/Splay core (immutable structures, `depth+1` cost, bottom-up cases as pure functions returning traces; port parent interfaces read-only, wrap without semantic change); survivor binder (dataclass loading sealed record by SHA-256, field-by-field asserts); parent verifier (full-SHA check never short hash, terminal/standing/kills/firewalls/DAG derivation, read-only clone); bridge freezer (lawful acquisition option A/B else `BRIDGE_SOURCE_UNAVAILABLE` fail-closed; verbatim capture; hypothesis checklist; independent second extraction); Lean kernel (frozen toolchain + manifest hash, declared axioms only, `sorry/admit` CI scan, markdown↔Lean equivalence audit); PSC freezer (negation-predicate interfaces, seeded deterministic RNG + sorted outputs, sympy/z3 hooks). Payment-semantics binding: evaluator calls imported payment (`required=max(w,0)`, `paid=imported_MSTC0002_payment(...)`); any `min(pool,w)`-form reduction recorded as proved binding lemma after binding, never assumed. K6 demand never interpreted as six slots (`T043`, `INV-053`, `STOP-38`).

**Benchmarks (independently generated, entirely separate from v0.3 banks).** Only finite-canary equivalence (explicitly non-theorem-facing) in Phase 1. PSC definitions audited for legal-BST generation, witness-replay compatibility, actual-k targeting, clean-room share-nothing, canonical order. No PSC survival claim until Phases 2–4.

**Anti-overfitting.** H3T never re-unlocked; finite survival never premise; prereg frozen before attacks; formal/executable binding audited; AI disclosed.

**Exit criteria.** All seven gates; `PARENT-01..10`, `FORM-01..12` green; threats `T001–T007,T012–T026,T069` controlled; stops `STOP-01..19` armed; invariants `INV-001..039` holding. `prereg_sha256.txt` over the exact unique union (mechanically derived count, zero self-reference) with living-Path prefix verified.

---

## 5. Phase 2 — Upstream blockers: DELETE injection review, locality, preservation, boundary, constants (spec PHASE 05–09)

**Scope.** Close or exactly refute the five upstream nodes `MST0-13/08U/11/09/22` (22 guards all), each with simultaneous PROVE + REFUTE tracks and 3-layer certificates. Exact `REFUTED` freezes the positive route at that ID (later phases `NOT_REACHED`) and permits Phase-6 lifting; never implies DOC false. Human REJECT/BLOCKED sets only the reviewer gate (`MST0_13_REJECTED`/`MST0_13_BLOCKED`); `proof_status.json` stays `UNPROVED` absent an exact negation witness (v0.4.1 A2). Corresponds to `DEC-GATE-04..08`.

**Spec coverage.** PHASE 05 (MST0-13: formalize `E_after−E_before ≤ 6·cost_A(D)`; attack rotations/T5-T7/block granularity/hidden-n/finite-evidence; human ACCEPT/REJECT/BLOCKED → reviewer gate; `BOUNDED_DELETE_INJECTION_PROVED` only on ACCEPT+formal green); PHASE 06 (08U: PSC-L 7 objectives; universal-constant bound on downstream-consumed modifications; no finite-maximum premise → REVIEWED/REFUTED); PHASE 07 (11: symbolic 7 cases × every rule on arbitrary intervals/sizes/ranks/supports; 9 preservation obligations; mutants → REVIEWED/REFUTED); PHASE 08 (09: PSC-B 11 dimensions; exact cost-bearing source law; smallest-counterexample + inflation append-only → REVIEWED/REFUTED); PHASE 09 (22: literal `∃C=2,k=6 ∀…` order; dependence-scoped static scan as support-only; hidden dependence refutes → REVIEWED/REFUTED).

**Files to be made.** `math/` theorem docs (exact Statement/Negation lines) + `math/reviews/*.review.json` (human verdicts only) + versioned `proof_status.json`; `lean/MSTC0002/{Injection,Locality,Preservation,Boundary,Constants}.lean` + formal certs; `python/proof_attack/{locality_explosion,primitive_exhaust,boundary_torture}.py` + `python/cleanroom/{locality_check,preservation_check,boundary_check,constants_scan}.py` (share-nothing; dependence — not occurrence — scanning for constants) + `python/audit/{review_package,mutants}.py`; `artifacts/v04/` attack/counterexample/proof/audit dirs + `tests/{injection,locality,preservation,boundary,constants,mutation}/` + `scripts/run_phase05..09.py`.

**Code to produce and how to code.** Locality engine (7 objectives on the actual frozen model; symbolic + brute `16..1024`; canonical minimization + replay + agreement); primitive splitter (7 cases × rules, arbitrary symbolic parameters; 9 obligations; missing-case detector fail-closed `STOP-28/29`); boundary chamber (11 dimensions; immutable damage definition; source-cost identification); constants scanner (AST dataflow from forbidden parameters into constant/helper outputs — never mere mention of `n,T,X,Y` — plus formal quantifier check); MST0-13 formalization (rotation-count≤cost, T7-bound, T5-conservation, T6-inapplicability, case completeness, granularity, endpoints) + hostile package → human verdict only. Mutants (delete-case/mutate-rule/alter-support/weaken-quantifier/relax-C-k) must all be rejected.

**Benchmarks (independently generated).** PSC-L/P/B negation-derived, disjoint generators/seeds/objectives/sizes from v0.3 banks; k=2 kill replay as sensitivity control; clean-room share-nothing; deterministic post-sort. Survival = attack-survived, never theorem.

**Anti-overfitting.** No finite maximum premise (`LOC-07`, `STOP-30/31`); n-independence proved mathematically; damage immutable (`STOP-32/33`); no weakening under same ID (`STOP-25`); no consumption before REVIEWED (`STOP-27`).

**Exit criteria.** 08U/11/09/22 REVIEWED-or-REFUTED with formal + review + replay + mutants; 13 at a reviewer gate (`REVIEWED` → injection terminal allowed; `REJECTED`/`BLOCKED` → blockage record, status stays UNPROVED absent witness); `INJ/LOC/PRES/BND/CONST` green; threats `T008–T011,T015–T042` controlled; first exact REFUTED freezes the route per §31.

---

## 6. Phase 3 — KEEP repayment war: K6 saturation attack + MST0-14 proof (spec PHASE 10–11)

**Scope.** Hard entry gate: starts only if 13/08U/11/09/22 are all REVIEWED, else `NOT_REACHED` (attack track needs no prerequisites and may still falsify). Destroy-or-prove synchronous repayment for every legal KEEP at C=2 (DEC-GATE-09; success → `SYNCHRONOUS_KEEP_TRANSFER_PROVED`, still not global).

**Spec coverage.** PHASE 10 (`K6_SATURATION_ATTACK` 13 dimensions on actual calculus semantics; lemma mining without promotion; `KEEP_REPAYMENT_EXACT_COUNTEREXAMPLE` or `KEEP_REPAYMENT_ATTACK_SURVIVED` — survival is not theorem); PHASE 11 (case-complete proof + injection-to-payment matching + versioned child lemmas + formal + hostile review → REVIEWED/`SYNCHRONOUS_KEEP_TRANSFER_PROVED` or REFUTED/`MSTC0002_UNIVERSAL_COUNTEREXAMPLE` with replay + canonical minimization).

**Files to be made.** `python/proof_attack/k6_saturation.py` + `python/cleanroom/repayment_check.py` + `lean/MSTC0002/Repayment.lean` + `math/theorem_MST14_keep_repayment.md` (+ child lemmas) + `math/reviews/MST0-14.review.json`; `artifacts/v04/` k6/counterexample/proof/audit dirs + `tests/repayment/` (`REP-01..14`) + `scripts/run_phase10.py`, `run_phase11.py`.

**Code to produce and how to code.** Saturation evaluator (`residual = required − paid`, `required=max(w,0)`, `paid=imported_MSTC0002_payment(...)`; no future info, no illegal latent/spent use, no double-spend, payment ≤ legal mass); demand maximizers over 13 dimensions (generated + symbolic + spliced + nested-scale + recurrent + mirror; deterministic sharding + post-sort; z3 hooks); any res>0 → independent replay + canonical minimization. Matching theorem (whatever exact sufficient structure holds — overlap/multiplicity/merge-cancellation/bend/laminar — not required to say “six claims”). Clean-room share-nothing agreement. Controls: k=2 kill replay, H3T-independence, C=1/k=5 mutants, formal proof, hostile review.

**Benchmarks (independently generated).** Fresh repayment-objective families disjoint from v0.3 and Phase-2 banks; large-n stress only; recurrent/burst/latent/activation tortures; decomposition-varied replays; all witnesses minimized + replayed + checked. No finite clean-run called theorem (`T052`).

**Anti-overfitting.** All positive-regret classes included; causal legal payment sources; local repayment never integrability (`STOP-44`); finite ≠ proof; no silent weakening.

**Exit criteria.** Entry gate satisfied or `NOT_REACHED`. REVIEWED + terminal or REFUTED + counterexample (+ Phase-6 activation, later phases `NOT_REACHED`); `REP-01..14` green; threats `T043–T052` controlled.

---

## 7. Phase 4 — Global integrability: Double-Spend Apocalypse + MST0-15 proof (spec PHASE 12–13)

**Scope.** Hard entry gate: starts only if MST0-14 REVIEWED, else `NOT_REACHED`. Prove global coexistence (no double spend, decomposition independence, controlled endpoints) or exactly refute (DEC-GATE-10; success → `GLOBAL_INTEGRABILITY_PROVED`).

**Spec coverage.** PHASE 12 (credit-use graph: creation/ownership/transfer/split-merge/activation/consumption/cancellation/migration; 8 `DOUBLE_SPEND_APOCALYPSE` objectives; independent checker; counterexample-or-survived gate); PHASE 13 (unique lifecycle + conservation + acyclicity/independence + scalar-energy lower bound or flow telescope; endpoint theorems; formal + hostile review, no finite-enumeration premise → REVIEWED/`GLOBAL_INTEGRABILITY_PROVED` or REFUTED).

**Files to be made.** `python/proof_attack/double_spend.py` + `python/cleanroom/integrability_check.py` + `lean/MSTC0002/Integrability.lean` + `math/theorem_MST15_integrability.md` + `math/reviews/MST0-15.review.json`; `artifacts/v04/` integrability/counterexample/proof/graph dirs + `tests/integrability/` (`INT-01..14`) + `scripts/run_phase12.py`, `run_phase13.py`.

**Code to produce and how to code.** Exact directed credit-use graphs (immutable adjacency, exact Fractions, cycle detection, decomposition-mutant harness, deterministic sharding + post-sort); tortures (long histories, recurrent KEEPs, nested/crossing intervals, cyclic-transfer attempts, terminal drift); Lean proof of whichever sufficient structure holds (laminar/unique-ownership/acyclic/conservation/independence/energy-bound/flow-telescope); endpoints independent of sequence length; exact-once block partition. Clean-room independent builder + auditor.

**Benchmarks (independently generated).** Global-lifecycle objectives disjoint from K6/locality banks; nested/crossing/recurrent/cyclic families; decomposition mutants; long-history tortures with 11-field resource-failure records on limit-hit (never evidence).

**Anti-overfitting.** Local ≠ global (`T053`, `STOP-44`); graph completeness (`STOP-45`); double-spend/split/decomposition/endpoint blocks (`STOP-46..49`); no finite enumeration premise.

**Exit criteria.** Entry gate satisfied or `NOT_REACHED`. REVIEWED + terminal or REFUTED (+ Phase-6 activation); `INT-01..14` green; threats `T053–T063` controlled.

---

## 8. Phase 5 — Composition endgame: Pair Access + telescope + Levy–Tarjan bridge (spec PHASE 14–16)

**Scope.** Hard entry gate: all seven upstream REVIEWED, else `NOT_REACHED`. Reconstruct Pair Access from scratch (no status-toggling), control endpoints to approximate monotonicity, audit the exact bridge (DEC-GATE-11..13 → `BRIDGE_READY_FOR_DECISION`).

**Spec coverage.** PHASE 14 (MST0-17: independently written proof that block/local inequalities imply `Splay(Y,T)+E_m−E_0 ≤ 2·Splay(X,T)+A(n)`; exact block coverage → REVIEWED/`UNIVERSAL_PAIR_ACCESS_LEMMA_PROVED`). Dual `REFUTE(MST0-17)` with endpoint-aware negation `∃n,T,X,Y≼X: lhs>rhs`, `lhs=Splay(Y,T)+E_m−E_0`, `rhs=2·Splay(X,T)+A(n)` (the endpoint-free form belongs downstream; attacking it as 17 would let negative `E_m−E_0` escape); full reconstruction payload witness; MST0-18 decides endpoint elimination. PHASE 15 (MST0-18: PSC-T endpoint tortures; exact additive term + direction → REVIEWED/`APPROXIMATE_MONOTONICITY_PROVED`). PHASE 16 (10-point convention checklist + independent reconstruction → REVIEWED/`BRIDGE_READY_FOR_DECISION`, or BLOCKED + `BRIDGE_BLOCKED_NO_CLAIM` on mismatch — mismatch blocks, never refutes; REFUTED only on exact negation witness).

**Files to be made.** `lean/PairAccess/{Composition,Telescope}.lean` + `python/proof_attack/{pair_access_search,telescope_torture}.py` + `python/cleanroom/pair_access_check.py` + `python/formal_bridge/{bridge_audit,independent_bridge}.py` + `math/` 17/18/19 docs + reviews + `artifacts/v04/` proofs/attacks/counterexamples/audits + `tests/{pair_access,bridge}/` (`PA-01..05` + `PA-06` hardening, `TEL-01..04`, `BR-01..09`) + `scripts/run_phase14..16.py`.

**Code to produce and how to code.** Pair-access search over legal executions with exact Fraction costs, seeded deterministic families, canonical minimization + inflation + independent replay; startup SHA-guard (`sha256(statement)==battlefield` and `sha256(negation)==battlefield`, else abort — prose drift becomes startup failure); clean-room agreement; composition from hash-bound reviewed lemmas (exact-once partition, no holdout citation); telescope endpoint audit (no assumed `E_m≥0`, length-independent additive, direction check); 10-point bridge match with dual reconstruction (mismatches block per `STOP-55..59`; unavailable source → `BRIDGE_BLOCKED_NO_CLAIM`, never consume).

**Benchmarks (independently generated).** Triple-focused counterexample battery; endpoint-focused telescope battery; source-text bridge audit; all with replay + minimization + agreement + formal + review.

**Anti-overfitting.** No assumed endpoint bounds (`T066`); length-independent additive (`T067`, `STOP-53/54`); exact source bytes (`T069`); frozen sources immutable (`T078`, `INV-099`).

**Exit criteria.** 17+18+19 REVIEWED (→ ready), or 17 REFUTED only on the triple-artifact gate (valid attack record AND valid pair-access certificate with all load-bearing fields AND interface conformance — generic pass never refutes), or BLOCKED levels with first-wall localization; `PA/TEL/BR` green; threats `T062–T078` controlled.

---

## 9. Phase 6 — Negative lifting + decision gate (spec PHASE 17–18)

**Scope.** Dormant until exact REFUTED (bare REJECT/BLOCKED without witness routes to `POSITIVE_ROUTE_BLOCKED_UNRESOLVED_NO_CLAIM`, never lifting). On exact obstruction, lift to genuine DOC disproof; otherwise record `NEGATIVE_BRANCH_NOT_ACTIVATED` with no speculative mining. Then emit exactly one recomputed terminal level (DEC-GATE-14; exactly six permitted outcomes, no escape hatch).

**Spec coverage.** PHASE 17 (closed-form families, legality, symbolic Splay lower, explicit legal competitor upper, ratio divergence, finite-prefix replay, formal + review → `NEGATIVE_BRANCH_NOT_ACTIVATED` / `NEGATIVE_REAL_SPLAY_FAMILY_PROVED` / `POSITIVE_ROUTE_REFUTED_NO_DOC_NEGATIVE` / `POSITIVE_ROUTE_BLOCKED_UNRESOLVED_NO_CLAIM` / `RESOURCE_LIMIT_NO_CLAIM`); PHASE 18 (YES only if all 10 REVIEWED + hashes match with full DAG regeneration; NO only on REVIEWED divergence theorem; unresolved-blockage → blocked-unresolved; mutual exclusivity).

**Files to be made.** `python/negative/{lift_obstruction,splay_lower,competitor_upper,family_replay}.py` + `lean/Negative/Family.lean` + `math/negative/` + reviews + `artifacts/v04/negative/` + `proofs/decision.json` + `tests/negative/` (`NEG-01..12`) + `scripts/run_phase17.py`, `run_phase18.py`.

**Code to produce and how to code.** Closed-form (never solver-enumerated) families with legality proofs; symbolic (never empirical) bounds; divergence proof; independent finite-prefix replay; ledger-independent formal proof; hostile review. Decision recomputed solely from statuses/certs/reviews/counterexamples/bridge/negative certs (never hardcoded); exactly-one-branch; YES-needs-10 / NO-needs-theorem; no-claim never success; resource-limit never YES/NO (`STOP-70`, multi-owned).

**Benchmarks.** Confirmatory replays only; authority is symbolic proof + formal + review. No residual-as-lower-bound (`T080`); no reduction-free counterexample use (`T081`).

**Anti-overfitting.** Local failure never DOC disproof (`STOP-60`, `INV-078`); closed-form/legality/divergence proved (`STOP-61..64`); resource failure → no-claim with full 11-field record.

**Exit criteria.** Exactly one of the six outcomes, recomputed and hash-bound; `NEG-*`, `DEC-*` green.

---

## 10. Phase 7 — Seal, reproduce, package, release (spec PHASE 19 + cross-cutting closeout)

**Scope.** Seal from artifacts only: regenerate `FINAL_RESULT`, fresh-checkout reproduction, deterministic archive, 12 reports + ledger updates, AI disclosure, release tag. Closes all cross-cutting obligations.

**Spec coverage.** PHASE 19 (`FINAL_RESULT` regeneration; 9 fresh-checkout checks; `SPLAY-AM-DECIDE-v0.4.tar.zst` canonical rebuild-identical; 12 reports: `DECISION_REPORT.md` (Q01–Q60 each), `THEOREM_BATTLEFIELD_REPORT.md`, `MSTC0002_PROOF_LEDGER.md`, `LOCALITY_REPORT.md`, `KEEP_REPAYMENT_REPORT.md`, `INTEGRABILITY_REPORT.md`, `PAIR_ACCESS_REPORT.md`, `BRIDGE_AUDIT.md`, `NEGATIVE_OBSTRUCTION_REPORT.md`, `COUNTEREXAMPLE_ATLAS.md`, `REPRODUCIBILITY.md`, `AI_USE.md`); §§23–30 closeout (T001–T120 each ≥1 control; STOP-01–70 owned; INV-001–100 holding; full matrix + mutants green; derived manifest/archive/`FINAL_RESULT`).

**Files to be made.** `artifacts/v04/seal/{FINAL_RESULT.json,MANIFEST.sha256,ARCHIVE.sha256,STALE_CLEARANCE.json}` + archive (+ rebuild proof) + `scripts/{run_phase19,reproduce_all_v0.4}.py`; 12 root reports; `python/{audit/{lifecycle,log,status},seal/{manifest,archive,final_result}}.py` + `tests/seal/` (`SEAL-01..12`) + `tests/mutation/` (T099/T100 + known-killed) + `schemas/final_result_v0.4.schema.json`.

**Code to produce and how to code.** Artifact-derived `FINAL_RESULT` (mutual exclusivity + YES/NO preconditions; never hardcoded); canonical JSON + sorted order + zstandard + rebuild-identity check; fresh-checkout runner (parent/MSTC-0002/prereg/Lean/proofs/reviews/counterexamples/PSC/bridge/negative/Phase-18 order; no H3T re-unlock; 24-field append-only logs); Q01–Q60 answered one-by-one with hashes; failed attempts/counterexamples/negative evidence retained; AI edits disclosed.

**Benchmarks.** Determinism/identity benchmarks (byte-identical archive, hash-exact manifest, fresh-checkout regeneration), not theorem evidence; proof-mutation suite (≥1 mutant per theorem + known-killed) green.

**Anti-overfitting.** Artifact-derived result; both-branches-active blocked; no-claim never success (`T117`); resource record complete; Phase-18-before-gates blocked (`T120`, `STOP-66`).

**Exit criteria.** `SEAL-01..12` green; threat/stop/invariant sets exact; archive rebuild-identical; fresh checkout reproduces claim; 12 reports + `AI_USE.md`; release tagged.

---

## 11. Cross-cutting obligations (owned across phases; verified in Phase 7)

**Prereg (§19, 14 entries total including manifest).** `experiment_v0.4.yaml`, `parent_contract.yaml`, `theorem_battlefield.yaml` (10 nodes × hashes/statuses/owners/consumers/prerequisites/namespaces/premises/artifacts/lifting-eligibility), `theorem_gate_matrix.yaml`, `dual_obligation_policy.yaml` (simultaneous tracks, canonical order, mutation policy incl. preregistered operators, review schema, erratum, no-consumption-before-REVIEWED), `proof_kernel_policy.yaml` (toolchain/manifest/axioms, 3-layer cert, mismatch rule), `proof_stress_corpus.yaml` (7 families as complete machine-readable specs + `REFUTE-MST0-17` attack interface — not an 8th family; later implementations need conformance green, `STOP-17`), `negative_lifting_policy.yaml` (witness-only activation + DISPROVED requirements), `bridge_sources.yaml` (L2/L3 acquired before freeze), `theorem_gate_matrix.yaml`, `threat_control_matrix.yaml` (`T001–T120`), `stop_control_matrix.yaml` (`STOP-01..70`), `allowed_claims.md`/`forbidden_claims.md` (§33 + A3 10 levels), `prereg_sha256.txt` (freeze manifest over exactly payload ∪ bound, never itself; living Path bound via snapshot). Frozen in Phase 1; never rewritten after (§21).

**Schemas (§20, 17, counts derived).** `parent_import`, `survivor_binding`, `theorem_obligation`, `proof_certificate`, `formal_certificate`, `review_record`, `proof_attack` (open-world witness payload per B2), `locality_witness`, `preservation_case`, `boundary_witness`, `repayment_witness`, `credit_use_graph`, `integrability_witness`, `pair_access_certificate` (mandatory load-bearing fields), `bridge_audit`, `negative_family`, `final_result_v0.4`. `jsonschema`-validated writers.

**Deterministic order (§21, 15 steps).** Every phase script asserts all 15; violations fail closed. Parallelism only for independent searches/cases/replays/mutations/modules/prefixes with deterministic post-sort.

**Scaling (§26).** Sizes `16..1024+`; symbolic-before-brute; sharding/compression with logical-stream hashes; 11-field resource-failure records.

**Logging (§27).** 24-field append-only run records.

**Deps (§28).** Python 3.12+, sympy, zstandard, jsonschema, z3-solver if SMT, Lean 4 pinned + mathlib pin, Rust optional behind agreement gates. Solvers propose only.

**AI policy (§29).** Allowed: code/formalization scaffolding, proof search, counterexample generation, mutant design, audited extraction, brainstorming, checklists, prose, audits. Silently forbidden: MSTC-0002 change, post-failure statement change, human ACCEPT, negation weakening, counterexample suppression, finite-as-proof, failure-as-DOC-false, OPT invention, bridge replacement, axiom/sorry hiding, premature Phase-18. `AI_USE.md` mandatory.

**Decision ladder (§31).** `DEC-GATE-00..14` with fail-fast entry gates (Phase 3 needs upstream REVIEWED; Phase 4 needs MST0-14; Phase 5 needs all seven; first refutation → later phases `NOT_REACHED`); `NEG-GATE-00..06` on preserved exact witness only.

**Interpretation (§32).** 8 rules enforced in checklists and reports.

**Allowed/forbidden claims (§33 + A3, 10 levels).** Exact wording per level; enforced by claims files + decision runner + human review.

**Seal checklist (§34).** 10 groups, all required pre-release.

**Success (§35).** S1/S2 only; otherwise exact no-claim.

**Q01–Q60 (§36) → reports.** Parent/survivor → decision/ledger; bridge Q05/Q38–43 → bridge audit; kernel Q06–07 → reproducibility; locality Q08–16, preservation/boundary Q11–16, injection Q17–18, constants Q19–20, repayment Q21–26, integrability Q27–32, composition Q33–37, decision Q44–45, negative Q46–53, decision Q54–55, mutants/reviews Q56–58, checkout Q59, paper claims Q60. Template enforces one subsection per Q.

**Citations (§37).** Exact L0–L4 metadata from frozen manifest; ST85 context, L2/L3 premise-only-after-freeze+audit, Chmel context-only, v0.3 sealed source.

---

## 12. Verification appendix — proof that nothing is omitted

**A. Spec PHASE 00–19 → WorkPlan phases.** 00→1, 01→1, 02→1, 03→1, 04→1, 05→2, 06→2, 07→2, 08→2, 09→2, 10→3, 11→3, 12→4, 13→4, 14→5, 15→5, 16→5, 17→6, 18→6, 19→7. All 20 covered.
**B. Theorem nodes → phases.** 08U→2, 09→2, 11→2, 13→2, 14→3, 15→4, 22→2, 17→5, 18→5, 19→5. All 10 with dual tracks + 3-layer certs.
**C. PSC families → phases.** L→1/2, P→1/2, B→1/2, K6→1/3, I→1/4, T→1/5, N→1/6. All 7 frozen before attacks (no 8th family; REFUTE-17 interface separate).
**D. Threats T001–T120 → phases (multi-owner, from exact IDs).** Parent/survivor/finite 001–011→1/2; DAG/insertion/weakening 012–014→1; negation/witness/canonical 015–020→1–5; formal binding 021–025→1–5; Splay/locality 026–033→1/2; boundary 034–037→2; constants 038–042→2; K6 043–052→3; integrability 053–063→4; composition/telescope 064–068→5; bridge/literature 069–078→1/5; negative 079–089→6; review/lifecycle 090–098→2–6; mutants/determinism/solver 099–110→1–6 + `tests/mutation/`; reports/manifest/FINAL/AI 111–119→7; T120→6+7. Machine-checkable matrix in Phase 1; exact set asserted at seal.
**E. Tests → phases.** PARENT→1, FORM→1+, LOC/PRES/BND/INJ/CONST→2, REP→3, INT→4, PA/TEL/BR→1/5, NEG/DEC→6, SEAL→7, mutation suite cross-phase for T099/T100.
**F. Invariants INV-001–100 → phases.** 001–013→1; 014→1–6; 015–040→1/6; 041–051→2; 052–057→3; 058–065→4; 066–075→5; 076–088→6; 089–093→7; 094–099→7; INV-100→6+7 (Phase-18-only claim at decision + Phase-7 re-audit, multi-owned). Machine-checked at seal from exact IDs.
**G. Stops STOP-01–70 → phases.** 01–10→1; 11–19→1/5; 20–24→1–4; 25–27→2–5; 28–37→2/3; 38–43→3; 44–49→4; 50–59→5; 60–66→6; 67–69→7; STOP-70→6+7 (resource-exhaustion guard at decision + seal, multi-owned). Exact set asserted at seal.
**H. Decision gates → phases.** DEC-GATE-00..03→1, 04..08→2, 09→3, 10→4, 11..13→5, 14→6; NEG-GATE-00..06→6.
**I. Q01–Q60 → Phase-7 reports** per §11 mapping.
**J. Verification execution.** Phase-1 audit modules + foundation tests assert A–C; `reproduce_all_v0.4.py` + seal tests assert D–I pre-release. Any gap fails closed and is recorded in `Path.md`.

---

## 13. Execution order and Path.md obligation

WorkPlan phases execute 1→7 (spec PHASE order preserved inside each phase). Within every phase the §21 15-step order is mandatory. `Path.md` is appended contemporaneously after every phase-step with: implementation, WorkPlan section followed (or justified deviation), scope/files/code/how/benchmarks/anti-overfitting/gates detail, verification evidence (tests/hashes/review IDs), and next blockers. A gate without a `Path.md` entry is not closed (`INV-097`).

**End of WorkPlan.**
