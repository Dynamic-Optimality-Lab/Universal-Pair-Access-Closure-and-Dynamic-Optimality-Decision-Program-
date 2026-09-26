# SPLAY-AM-DECIDE v0.4.7 — Contract-Closure Amendment (finite-state + theorem-identity)

**Status:** `RATIFIED` — issued before `FOUNDATION_FROZEN`; part of the normative v0.4 stack.
**Date ratified:** 2026-09-26 UTC
**Amends:** refines v0.4.6 F2 (ten-node hash language); supersedes v0.4.6 F1 fixed-count
materialization with the invariant bound rule (G1); extends the lifecycle (§7, v0.4.1 A2,
v0.4.3 C1, v0.4.4 D1/D5) with total transition semantics; extends the checkpoint order
(v0.4.3 C2) with branch-safe automaton semantics; freezes the exact REFUTED rule and the
Phase-18 total precedence function. v0.4–v0.4.6 bytes preserved.

## G1. Normative-authority invariant rule (supersedes fixed-count maintenance)

`FREEZE_BOUND_FILES` is not a hand-maintained integer. It is the mechanical derivation:

```text
FREEZE_BOUND_FILES(variant) =
  {IMPLEMENTATION_SPEC_v0.4.md}
  ∪ ALL_RATIFIED_PRE_FREEZE_AMENDMENTS
  ∪ {WorkPlan.md, PATH_AT_FOUNDATION_FREEZE.md, PROOF_STATUS_AT_FOUNDATION_FREEZE.json}
  ∪ {lean/Frozen/SplayDefs.lean, lean/Frozen/MSTC0002Defs.lean, lean/Frozen/Statements.lean}
  ∪ {10 theorem docs}
  ∪ {all schemas/*.schema.json present at freeze}
  ∪ {prereg/proof_stress_corpus.yaml}
  ∪ {bridge_sources/L3_1907.06310_v1.pdf (available variant only), bridge_sources/README.md}
```

`scripts/contract_closure.py` derives this set from the rule at runtime and asserts
exact set equality with the committed file list (CLOSURE-08). Current materialization:
44 members available (1 + 7 amendments + 1 + 2 + 3 + 10 + 17 schemas + 1 + 2),
43 unavailable (minus the source PDF). No future amendment may hand-edit a count;
counts are derived and asserted, never typed.

## G2. Closed theorem lifecycle (truth status × track readiness)

Truth status and execution readiness were conflated. They are now orthogonal dimensions:

```text
truth_status: UNPROVED | PROVED | REVIEWED | REFUTED | BLOCKED
prove_track:  NOT_READY | READY | RUNNING | PROVED_PENDING_REVIEW | REVIEW_REJECTED
            | REVIEW_BLOCKED | REVIEWED | NOT_REACHED | INVALIDATED
refute_track: NOT_READY | READY | RUNNING | NO_WITNESS | WITNESS_PENDING_VALIDATION
            | REFUTED | BLOCKED | NOT_REACHED | INVALIDATED
```

`BLOCKED` (truth) means "verdict unreachable in the current branch"; it is not a truth
value and never implies falsity. Full transition table (event → new truth/track state,
all-nodes general) is frozen in `prereg/dual_obligation_policy.yaml` and includes:

```text
BLOCKED -> UNPROVED on blocker-cleared (unblocks 17/18/19 downstream only via gates)
PROVED_PENDING_REVIEW + ACCEPT -> REVIEWED (truth REVIEWED, prove REVIEWED)
PROVED_PENDING_REVIEW + REJECT -> UNPROVED (truth UNPROVED, prove REVIEW_REJECTED; theorem open, proof failed)
PROVED_PENDING_REVIEW + BLOCKED -> BLOCKED (truth BLOCKED, prove REVIEW_BLOCKED; re-review when cleared)
```

General review semantics (all nodes, superseding the 13-only special case):

```text
human REJECT != REFUTED | human BLOCKED != REFUTED | proof failure != REFUTED
timeout != REFUTED | finite attack survival != PROVED
```

Exact refutation requires the exact frozen negation (G5), never a broken proof.
`math/proof_status.json` records per-node truth + both tracks; 17/18/19 initialize
truth BLOCKED with tracks lawful (prove NOT_REACHED, refute BLOCKED/NOT_READY per G8).

## G3. Erratum and invalidation transitions (history-preserving)

Four disjoint erratum cases; history is never overwritten (old status/review/hashes +
erratum record + trigger evidence + new status + invalidated downstream hashes):

```text
E1 reviewed-proof-defective (theorem not disproved): REVIEWED -> UNPROVED, downstream REVIEWED-as-premise invalidated by dependency hash
E2 reviewed-theorem-exactly-refuted: REVIEWED -> REFUTED (via G5), downstream invalidated
E3 refutation-certificate-invalid: REFUTED -> UNPROVED (witness retained as failed attempt), downstream reactivated only via gates
E4 dependency-invalidated: any downstream of E1/E2 becomes UNPROVED-or-BLOCKED with INVALIDATED tracks until re-derived
```

## G4. Branch-safe 16-checkpoint automaton (extends v0.4.3 C2)

The ordered checkpoints are explicitly (03 and 08 split, never compressed):

```text
01 VERIFY-HASHES 02 LOAD-CONTRACT 03 ASSERT/COMPUTE-REFUTE_READY
04 LOAD-SEMANTICS 05 ASSERT-BINDING 06 ASSERT-KERNEL
07 LOAD-THEOREM-PLUS-NEGATION 08 ASSERT/COMPUTE-PROVE_READY
09 REFUTE-FIRST-OR-PARALLEL 10 PROOF 11 APPEND-ONLY-RAW 12 FORMAL-CERT
13 INDEPENDENT-CHECK 14 MUTANTS 15 BUILD-HUMAN-REVIEW-PACKAGE
16 UPDATE-STATUS-ONLY-AFTER-HUMAN-VERDICT-THEN-APPEND-PATH
```

Branch law (frozen in `prereg/dual_obligation_policy.yaml`): if REFUTE_READY run
refutation; exact refutation obtained → validate/referee → REFUTED, skip the now-false
positive proof; else compute PROVE_READY → proof track or lawful NOT_REACHED/NOT_READY.
Lawful branch `MST0-19 + BRIDGE_SOURCE_UNAVAILABLE` routes to the frozen
blocked-source disposition and never fails on false READY predicates. Runners must
distinguish corrupt-contract assertion failure (ABORT, G7) from legitimately-false
predicates in a lawful branch (record reason, continue). Pre-freeze runner stubs
fail-closed (exit 2) and therefore cannot misinterpret the automaton.

## G5. Exact REFUTED rule (frozen, all nodes)

`REFUTED(L)` requires all of: exact witness satisfying frozen Negation(L);
independent replay/check AGREE; canonical minimization where applicable;
formal/kernel-checkable witness or theorem-specific exact certificate; schema
validation (proof_attack + pair_access_certificate where applicable); dependency/hash
validation; human refutation validation bound to reviewer provenance/attestation and
exact theorem+witness hashes (`refutation_review` in the attack record). It must NOT
require constructing Layers A+B proving the false positive proposition.

## G6. Phase-18 total precedence function (frozen)

Predicates evaluated in fixed order; first true wins (exactly one outcome always):

```text
P1 negative divergence theorem REVIEWED -> DYNAMIC_OPTIMALITY_DISPROVED
P2 all ten positive nodes REVIEWED + bridge regenerated -> DYNAMIC_OPTIMALITY_PROVED
P3 exact positive refutation exists (lifting failed/absent) -> POSITIVE_ROUTE_REFUTED_NO_DOC_NEGATIVE
P4 bridge blocked/mismatched (and P3 false) -> BRIDGE_BLOCKED_NO_CLAIM
P5 unresolved blockage, bridge sound (and P3/P4 false) -> POSITIVE_ROUTE_BLOCKED_UNRESOLVED_NO_CLAIM
P6 otherwise-at-termination -> RESOURCE_LIMIT_NO_CLAIM
```

Justification: proved exact mathematics dominates; exact refutation is never erased by
later resource failure (P3 before P6); bridge blockage never overrides an exact
refutation (P3 before P4) and never refutes (mismatch → P4, never DISPROVED);
review blockage + independent exact refutation → P3. Totality: a terminated campaign
with none of P1–P5 true has no refutation, no block, full resources, but an unproved
node — contradiction with termination, so P6 covers exactly the resource-exhausted
remainder. `run_phase18.py` remains a fail-closed stub; the function is frozen here,
in WorkPlan Phase 6, in `schemas/final_result_v0.4.schema.json`, and executable in
`scripts/contract_closure.py` (enumerated over all 64 abstract predicate states).

## G7. Outer execution state (RUN_VALID)

```text
PRE_FOUNDATION -> RUN_VALID (freeze script, chronology green)
PRE_FOUNDATION -> ABORTED_PRE_FOUNDATION (integrity failure; no theorem outcome emittable)
RUN_VALID -> INVALIDATED_POST_FREEZE (post-freeze integrity failure; prior evidence quarantined, no outcome emittable)
RUN_VALID -> SEALED (Phase-19 seal on a G6 outcome)
```

Integrity failure must not masquerade as a scientific outcome: no transition from any
ABORTED/INVALIDATED state reaches Phase 18. Frozen in `prereg/dual_obligation_policy.yaml`.

## G8. Source-unavailable N/A propagation (refines v0.4.6 F2)

F2's "all ten nodes have statement/negation/document hashes" is refined: all ten nodes
are bound; nine carry statement/negation/document hashes; MST0-19 carries the document
hash plus the blocked-record hash and NO statement/negation hash (nothing synthesized).
Every requirement on 19 resolves explicitly as REQUIRED / SATISFIED /
NOT_APPLICABLE_BY_SOURCE_UNAVAILABLE (table in `prereg/theorem_battlefield.yaml`,
gate matrix, proof_status tracks). No empty artifacts fabricated; nothing silently
omitted. Consistency required across WorkPlan, battlefield, gate matrix, schemas,
reports, test matrix, seal, checkout reproduction (asserted by the verifier).

## G9. Freeze-all-theorem-critical-interfaces rule

Every theorem-critical mutable interface is frozen directly by hash or by an exact
manifest whose contents are immutable and hash-bound: all ratified amendments; final
pre-freeze WorkPlan; frozen Path snapshot; prereg payloads; all 17 schemas; theorem
identity records (G11, inside this amendment); all theorem docs; Lean frozen
semantics/statements; exact executable Python core (`python/inherited/`,
`python/formal_bridge/`, interface-frozen now, bytes hash-bound at Phase 1);
bridge-source identities/disposition; PSC specifications; review/proof/refutation/
decision/negative-family schemas. Acceptance criteria are immutable after evidence
generation. The verifier asserts zero theorem-critical mutable interfaces outside
the freeze (CLOSURE-09).

## G10. Semantic-equivalence rule

Finite canary agreement is diagnostic only and never establishes universal equivalence
between Python executable semantics, Lean formal semantics, and intended mathematical
semantics. Theorem-facing operations require actual definitions plus Phase-03 formal
equivalence proofs/certificates. No theorem-bearing semantics hides behind opaque,
axiom, trusted implementation identity, canary agreement, or tested equivalence
unless the equivalence itself is formally justified.

## G11. THEOREM_IDENTITY table (authoritative; Markdown = battlefield = Lean)

Conventions: canonical Statement/Negation lines are ASCII-identical across
`math/theorem_MST*.md` and `prereg/theorem_battlefield.yaml`, and whitespace-normalized
identical to the `def MST0_* : Prop` bodies in `lean/Frozen/Statements.lean`
(token map: forall/∀, exists/∃, <=/≤, ->/→, /\//∧, \//∨, ~/¬, in/∈).
Multi-clause negations use the exact `~(C1 /\ ... /\ Cn)` form; a REFUTE witness
satisfies any falsified clause. `scripts/contract_closure.py` asserts string equality
(doc = battlefield), Lean containment (normalized), and identifier resolution
(every non-core name used in Statements resolves to a Frozen definition).

### MST0-08U — universal reference locality
- Role: a universal constant bounds the primitive modifications consumed downstream
  per A-side rotation event, uniformly over all trees, accesses, and events.
- Quantifiers/domains: `exists L:Nat, forall A:BST, x nkeys:Nat, E:Engine, ev:StepEv`
  with legality `ev ∈ (splayTrace A x).2` (real rotation events only); uniformity is
  the point (one L for all inputs).
- Statement: `exists L : Nat, forall (A : BST) (x nkeys : Nat) (E : Engine) (ev : StepEv), ev in (splayTrace A x).2 -> (T7inject E true ev.lo ev.hi x nkeys K_frozen).ledger.length <= E.ledger.length + L`
- Negation: `forall L : Nat, exists (A : BST) (x nkeys : Nat) (E : Engine) (ev : StepEv), ev in (splayTrace A x).2 /\ (T7inject E true ev.lo ev.hi x nkeys K_frozen).ledger.length > E.ledger.length + L`
- Dependency role: guard consumed by MST0-17; no upstream node.
- Falsity means: downstream consumption unbounded → positive route dies for the
  locality chain; MSTC-0002 refuted as formulated. Falsity does NOT mean: DOC false;
  any global claim; lift without exact-obstruction reduction (Phase 17).
- Representations: doc `math/theorem_MST08U_locality.md`; battlefield `MST0-08U`;
  formal `MST0_08U`; executable `python/inherited/mstc0002.py::t7inject` uniformity probe;
  refutation interface PSC-L.

### MST0-09 — raw boundary cost-bearing-source law
- Role: every boundary contribution's cost source is a rotation event; per-access
  energy growth is universally bounded by event count; all boundary classes
  (nested/alternating/creation-rate/rank-gap/span/burden/burst/lifetime/
  reactivation/asymmetry/mirror/scale) are events of the trace.
- Quantifiers/domains: `exists C9:Nat, forall A:BST, x nkeys:Nat, E:Engine`
  (arbitrary legal inputs; uniformity over classes via trace exhaustiveness).
- Statement: `exists C9 : Nat, forall (A : BST) (x nkeys : Nat) (E : Engine), energy (replayAccessA E A .KEEP x nkeys).1.ledger <= energy E.ledger + C9 * (splayTrace A x).2.length`
- Negation: `forall C9 : Nat, exists (A : BST) (x nkeys : Nat) (E : Engine), energy (replayAccessA E A .KEEP x nkeys).1.ledger > energy E.ledger + C9 * (splayTrace A x).2.length`
- Dependency role: consumed by repayment/integrability; guard for MST0-17.
- Falsity means: boundary costs escape universal bound → route dies for the
  boundary chain. Falsity does NOT mean: any finite maximum observed is the law
  (finite≠proof); DOC false.
- Representations: doc `math/theorem_MST09_raw_boundary.md`; battlefield `MST0-09`;
  formal `MST0_09`; executable boundary-growth probe; refutation interface PSC-B.
- Forbidden weakening (was frozen in v1.5): `forall L, energy L >= 0` is a Nat
  tautology, NOT this theorem.

### MST0-11 — transfer preservation (six-clause rotation-case law)
- Role: every rotation case (ROOT-vacuous, ZIG-left/right, LL, RR, LR, RL) replayed
  through T7+T5 preserves: (C1) flow identity — energy growth equals injected count;
  (C2) ownership — new credits are LATENT or lawfully activated; (C3)
  non-resurrection — SPENT in output pre-existed; (C4) support containment — new
  supports lie inside the rotated interval; (C5) no-future-lookup — every ACTIVE
  was ACTIVE or is a flipped LATENT with identical support; (C6) orientation —
  left-oriented supports end at/below x, others start above x.
- Quantifiers/domains: `forall E:Engine, isA:Bool, m:Mode, ev:StepEv, x nkeys:Nat`
  (all rotations, both sides, both modes; ROOT covered vacuously via empty trace).
- Statement: `forall (E : Engine) (isA : Bool) (m : Mode) (ev : StepEv) (x nkeys : Nat), let E1 := T7inject E isA ev.lo ev.hi x nkeys K_frozen; let E2 := T5activate E1 m; energy E2.ledger = energy E.ledger + (E1.ledger.length - E.ledger.length) /\ (forall c in E2.ledger.drop E.ledger.length, c.ctype = .LATENT \/ c.ctype = .ACTIVE) /\ (forall c in E2.ledger, c.ctype = .SPENT -> c in E.ledger) /\ (forall c in E2.ledger.drop E.ledger.length, ev.lo <= c.sup.lo /\ c.sup.hi <= ev.hi) /\ (forall c in E2.ledger, c.ctype = .ACTIVE -> c in E1.ledger \/ (exists c0, c0 in E1.ledger /\ c0.ctype = .LATENT /\ c.sup = c0.sup)) /\ (forall c in E2.ledger.drop E.ledger.length, (c.sup.leftOriented = true -> c.sup.hi <= x) /\ (c.sup.leftOriented = false -> x < c.sup.hi))`
- Negation: `exists (E : Engine) (isA : Bool) (m : Mode) (ev : StepEv) (x nkeys : Nat), let E1 := T7inject E isA ev.lo ev.hi x nkeys K_frozen; let E2 := T5activate E1 m; ~(energy E2.ledger = energy E.ledger + (E1.ledger.length - E.ledger.length) /\ (forall c in E2.ledger.drop E.ledger.length, c.ctype = .LATENT \/ c.ctype = .ACTIVE) /\ (forall c in E2.ledger, c.ctype = .SPENT -> c in E.ledger) /\ (forall c in E2.ledger.drop E.ledger.length, ev.lo <= c.sup.lo /\ c.sup.hi <= ev.hi) /\ (forall c in E2.ledger, c.ctype = .ACTIVE -> c in E1.ledger \/ (exists c0, c0 in E1.ledger /\ c0.ctype = .LATENT /\ c.sup = c0.sup)) /\ (forall c in E2.ledger.drop E.ledger.length, (c.sup.leftOriented = true -> c.sup.hi <= x) /\ (c.sup.leftOriented = false -> x < c.sup.hi)))`
- Dependency role: guard for MST0-17 (all 10 obligations discharged symbolically,
  never finite enumeration as premise).
- Falsity means/does-NOT-mean: as 08U (route dies for preservation chain; no
  DOC/global inference).
- Representations: doc `math/theorem_MST11_preservation.md`; battlefield `MST0-11`;
  formal `MST0_11`; executable case-matrix probe; refutation interface PSC-P.
- Forbidden weakening (was frozen in v1.5): lone energy equality is one component (C1 shape), NOT the ten obligations.

### MST0-13 — bounded DELETE injection (6·cost_A(D))
- Role: E_after − E_before ≤ 6·cost_A(D), where cost_A(D) is the executed A-side
  splay cost (depth+1), not an unrelated injection-count variable.
- Quantifiers/domains: `forall E:Engine, A:BST, x nkeys:Nat` (arbitrary trees incl.
  absent-x paths; cost is executed, never assumed).
- Statement: `forall (E : Engine) (A : BST) (x nkeys : Nat), let (E2, _, a) := replayAccessA E A .DELETE x nkeys; energy E2.ledger <= energy E.ledger + 6 * a`
- Negation: `exists (E : Engine) (A : BST) (x nkeys : Nat), let (E2, _, a) := replayAccessA E A .DELETE x nkeys; energy E2.ledger > energy E.ledger + 6 * a`
- Dependency role: BLOCKED-gate input to MST0-17; v0.3 author proof transported,
  hostile review pending (truth UNPROVED until human ACCEPT).
- Falsity means/does-NOT-mean: as 08U; bare REJECT never refutes (v0.4.1 A2 gates).
- Representations: doc `math/theorem_MST13_delete_injection.md`; battlefield `MST0-13`;
  formal `MST0_13`; executable injection-bound probe; hostile review + formal transport.
- Forbidden weakening (was frozen in v1.5): bound in an injection-count variable
  k≤6 is NOT the cost-scaled theorem.

### MST0-14 — universal synchronous KEEP repayment (sufficiency)
- Role: every legal KEEP, in every legal paired execution from the empty ledger,
  holds enough legally available ACTIVE payment to cover its positive regret at
  C=2 (mechanism identity `paid = min(pool, required)` is a lemma-conjunct, not
  the theorem).
- Quantifiers/domains: mechanism `forall L:Ledger, y a:Nat`; sufficiency
  `forall T0:BST, H:List (Mode * Nat), n:Nat` over `execSuffices` from empty engine.
- Statement: `(forall (L : Ledger) (y a : Nat), (discharge L (required y a)).2 = Nat.min (activePool L) (required y a)) /\ (forall (T0 : BST) (H : List (Mode * Nat)) (n : Nat), execSuffices { ledger := [], cursor := 0 } T0 T0 H n = true)`
- Negation: `~(forall (L : Ledger) (y a : Nat), (discharge L (required y a)).2 = Nat.min (activePool L) (required y a)) \/ (exists (T0 : BST) (H : List (Mode * Nat)) (n : Nat), execSuffices { ledger := [], cursor := 0 } T0 T0 H n = false)`
- Dependency role: BLOCKED-gate input to MST0-17; K6 demand never read as six slots.
- Falsity means/does-NOT-mean: as 08U; `min(pool,w)` reductions only as proved
  binding lemmas, never assumed.
- Representations: doc `math/theorem_MST14_keep_repayment.md`; battlefield `MST0-14`;
  formal `MST0_14`; executable sufficiency replay; refutation interface PSC-K6.
- Forbidden weakening (was frozen in v1.5): the `min` mechanism identity alone
  does NOT prove pool sufficiency.

### MST0-15 — global integrability (five-clause law)
- Role: (D1) SPENT-monotone + flip-legality — no double spend, unique lifecycle
  direction; (D2) discharge splitting invariance — decomposition independence of
  payment; (D3) LATENT conservation — lifecycle order; (D4) pool conservation;
  (D5) history-partition consistency — sequential replay equals whole replay
  (globally consistent histories, acyclic accounting).
- Quantifiers/domains: D1–D4 `forall L:Ledger, need/n1/n2:Nat, c:Credit`; D5
  `forall E0:Engine, T0:BST, H1 H2:List (Mode * Nat), n:Nat`.
- Statement: `(forall (L : Ledger) (need : Nat) (c : Credit), c in L -> c.ctype = .SPENT -> c in (discharge L need).1) /\ (forall (L : Ledger) (need : Nat) (c : Credit), c in (discharge L need).1 -> c.ctype = .SPENT -> c in L \/ (exists c0, c0 in L /\ c0.ctype = .ACTIVE /\ c.sup = c0.sup)) /\ (forall (L : Ledger) (n1 n2 : Nat), (discharge L (n1 + n2)).2 = (discharge L n1).2 + (discharge (discharge L n1).1 n2).2 /\ (discharge (discharge L n1).1 n2).1 = (discharge L (n1 + n2)).1) /\ (forall (L : Ledger) (need : Nat), activePool (discharge L need).1 + (discharge L need).2 = activePool L) /\ (forall (E0 : Engine) (T0 : BST) (H1 H2 : List (Mode * Nat)) (n : Nat), let (E1, A1, B1, sA1, sB1) := execTrees E0 T0 T0 H1 n; execLoop E1 A1 B1 n H2 sA1 sB1 = execLoop E0 T0 T0 n (H1 ++ H2) 0 0)`
- Negation: `exists (L : Ledger) (need : Nat) (c : Credit), ~((c in L -> c.ctype = .SPENT -> c in (discharge L need).1) /\ (c in (discharge L need).1 -> c.ctype = .SPENT -> c in L \/ (exists c0, c0 in L /\ c0.ctype = .ACTIVE /\ c.sup = c0.sup))) \/ (exists (L : Ledger) (n1 n2 : Nat), ~((discharge L (n1 + n2)).2 = (discharge L n1).2 + (discharge (discharge L n1).1 n2).2 /\ (discharge (discharge L n1).1 n2).1 = (discharge L (n1 + n2)).1)) \/ (exists (L : Ledger) (need : Nat), activePool (discharge L need).1 + (discharge L need).2 != activePool L) \/ (exists (E0 : Engine) (T0 : BST) (H1 H2 : List (Mode * Nat)) (n : Nat), let (E1, A1, B1, sA1, sB1) := execTrees E0 T0 T0 H1 n; execLoop E1 A1 B1 n H2 sA1 sB1 != execLoop E0 T0 T0 n (H1 ++ H2) 0 0)`
- Dependency role: BLOCKED-gate input to MST0-17.
- Falsity means/does-NOT-mean: as 08U; no local→global inference without D5.
- Representations: doc `math/theorem_MST15_integrability.md`; battlefield `MST0-15`;
  formal `MST0_15`; executable double-spend/partition probes; refutation interface PSC-I.
- Forbidden weakening (was frozen in v1.5): one-step conservation (old D4 alone)
  is NOT global integrability.

### MST0-22 — constant independence (uniformity law)
- Role: C=2/k=6 literals PLUS regret's C-linkage PLUS K-uniformity of injection
  across all inputs — independence from every forbidden input (no calculus
  discovery, no silent relaxation, no input-dependent constants).
- Quantifiers/domains: literals closed; linkage `forall y a:Nat`; uniformity
  `forall E:Engine, isA:Bool, lo hi x nkeys k:Nat` with `k ≤ K_frozen`.
- Statement: `(C_frozen = 2 /\ K_frozen = 6) /\ (forall y a : Nat, required y a = Int.toNat ((y : Int) - (C_frozen : Int) * (a : Int))) /\ (forall (E : Engine) (isA : Bool) (lo hi x nkeys k : Nat), k <= K_frozen -> (T7inject E isA lo hi x nkeys k).ledger.length <= E.ledger.length + K_frozen)`
- Negation: `~(C_frozen = 2 /\ K_frozen = 6) \/ (exists y a : Nat, required y a != Int.toNat ((y : Int) - (C_frozen : Int) * (a : Int))) \/ (exists (E : Engine) (isA : Bool) (lo hi x nkeys k : Nat), k <= K_frozen /\ (T7inject E isA lo hi x nkeys k).ledger.length > E.ledger.length + K_frozen)`
- Dependency role: guard for MST0-17 (constants govern the composition bound).
- Falsity means/does-NOT-mean: as 08U; minimality never claimed.
- Representations: doc `math/theorem_MST22_constant_independence.md`;
  battlefield `MST0-22`; formal `MST0_22`; executable uniformity probe.
- Forbidden weakening (was frozen in v1.5): bare literal equality is NOT
  independence from forbidden inputs.

### MST0-17 — universal Pair-Access composition (E_0-generalized)
- Role: `Splay(Y,T) + E_m − E_0 ≤ 2·Splay(X,T) + A(n)` for arbitrary initial
  ledgers (E_0 explicit, not zero-assumed); A(n)=0 preferred, nonzero only if
  exact, length-independent, explicit, bridge-accepted, deficit-free.
- Quantifiers/domains: `exists A:Nat->Nat, forall E0:Engine, T0:BST,
  H:List (Mode * Nat), n:Nat` (exact-once block partition underneath).
- Statement: `exists A : Nat -> Nat, forall (E0 : Engine) (T0 : BST) (H : List (Mode * Nat)) (n : Nat), let (E, sA, sB) := execHist E0 T0 H n; sB + energy E.ledger <= 2 * sA + A n + energy E0.ledger`
- Negation: `forall A : Nat -> Nat, exists (E0 : Engine) (T0 : BST) (H : List (Mode * Nat)) (n : Nat), let (E, sA, sB) := execHist E0 T0 H n; sB + energy E.ledger > 2 * sA + A n + energy E0.ledger`
- Dependency role: consumes 08U/09/11/13/14/15/22 REVIEWED (PROVE) ; feeds MST0-18.
- Falsity means: exact legal witness/family REFUTES (replay+minimization+certificate)
  and activates Phase-6 candidacy. Falsity does NOT mean: DOC false; residual without
  reduction lifts (T079–T081, STOP-60).
- Representations: doc `math/theorem_MST17_pair_access.md`; battlefield `MST0-17`;
  formal `MST0_17`; executable pair-access search; endpoint-aware negation.

### MST0-18 — telescoping / approximate monotonicity
- Role: endpoint-controlled approximate monotonicity with explicit additive term
  and checked direction; decides endpoint elimination for 17.
- Quantifiers/domains: `exists A:Nat->Nat, forall T0:BST, H:List (Mode * Nat), n:Nat`
  from the empty ledger (endpoint terms explicit, none assumed).
- Statement: `exists A : Nat -> Nat, forall (T0 : BST) (H : List (Mode * Nat)) (n : Nat), let (_, sA, sB) := execHist { ledger := [], cursor := 0 } T0 H n; sB <= 2 * sA + A n`
- Negation: `forall A : Nat -> Nat, exists (T0 : BST) (H : List (Mode * Nat)) (n : Nat), let (_, sA, sB) := execHist { ledger := [], cursor := 0 } T0 H n; sB > 2 * sA + A n`
- Falsity means/does-NOT-mean: as 17 (endpoint witness may REFUTE; assumed
  endpoint bounds forbidden, T066; length-dependence forbidden, T067/STOP-53-54).

### MST0-19 — Levy-Tarjan bridge (blocked-source representation, unchanged)
- No theorem-bearing proposition while L2 bytes are absent (G8). Document hash +
  blocked-record hash bound; zero statement/negation hashes. Theorem-bearing bridge
  Prop instantiates only at Phase-16 execution on exact L2+L3 bytes + convention
  match. Mismatch → BLOCKED (never REFUTED); unavailable → BRIDGE_BLOCKED_NO_CLAIM.

## G12. Effect

G1–G11 bind Phases 1/5/6/7 execution. v0.4–v0.4.6 bytes preserved. Future changes
need versioned amendments. `scripts/contract_closure.py` + `tests/contract_closure/`
mechanically assert G1–G11 closure before `FOUNDATION_FROZEN` (CLOSURE-01..20);
any nonzero field keeps `CONTRACT_CLOSURE = OPEN`.
