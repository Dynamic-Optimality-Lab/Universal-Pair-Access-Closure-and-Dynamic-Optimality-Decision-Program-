/-
Frozen theorem statements for SPLAY-AM-DECIDE-v0.4 (normative, hash-frozen).

9 instantiated statement Props at full intended strength (v0.4.7 G11:
THEOREM_IDENTITY — Markdown = battlefield = Lean; no weakened substitutions)
plus the MST0-19 blocked-source metadata representation (v0.4.5 E2, v0.4.7 G8:
never a theorem-bearing Prop while L2 premise bytes are absent).
A `def ... : Prop` NAMES the proposition; it asserts nothing and proves
nothing — proofs belong in `lean/Proofs/`. Canonical ASCII lines in
`math/theorem_MST*.md` and `prereg/theorem_battlefield.yaml` are
whitespace-normalized identical to these bodies (ASCII tokens `forall`,
`exists`, `<=`, `>=`, `->`, `/\`, `\/`, `~`, `in`, `!=` map to Lean
`∀`, `∃`, `≤`, `≥`, `→`, `∧`, `∨`, `¬`, `∈`, `≠`).
Zero proofs here; zero sorry/admit; zero opaque/axiom (the
CUSTOM_THEOREM_AXIOM_ALLOWLIST of v0.4.4 D4 is empty). Finite canary
agreement against the Python executable semantics is sanity-only;
Lean↔Python equivalence is PROVED at Phase-03 execution.
-/
import Frozen.SplayDefs
import Frozen.MSTC0002Defs

/-- MST0-08U: universal reference locality — one universal constant bounds
    downstream-consumed modifications per A-side rotation event, uniformly
    over all trees, accesses, and real rotation events. -/
def MST0_08U : Prop :=
  ∃ L : Nat, ∀ (A : BST) (x nkeys : Nat) (E : Engine) (ev : StepEv),
    ev ∈ (splayTrace A x).2 →
    (T7inject E true ev.lo ev.hi x nkeys K_frozen).ledger.length ≤ E.ledger.length + L

/-- MST0-09: raw boundary cost-bearing-source law — per-access energy growth
    is universally bounded by rotation-event count; every boundary class is a
    trace event. (A bare `energy ≥ 0` Nat fact is NOT this theorem.) -/
def MST0_09 : Prop :=
  ∃ C9 : Nat, ∀ (A : BST) (x nkeys : Nat) (E : Engine),
    energy (replayAccessA E A .KEEP x nkeys).1.ledger ≤
      energy E.ledger + C9 * (splayTrace A x).2.length

/-- MST0-11: transfer preservation — six-clause rotation-case law: flow
    identity, ownership, non-resurrection, support containment,
    no-future-lookup, orientation; all cases incl. ROOT-vacuous. -/
def MST0_11 : Prop :=
  ∀ (E : Engine) (isA : Bool) (m : Mode) (ev : StepEv) (x nkeys : Nat),
    let E1 := T7inject E isA ev.lo ev.hi x nkeys K_frozen;
    let E2 := T5activate E1 m;
    energy E2.ledger = energy E.ledger + (E1.ledger.length - E.ledger.length)
    ∧ (∀ c ∈ E2.ledger.drop E.ledger.length,
        c.ctype = .LATENT ∨ c.ctype = .ACTIVE)
    ∧ (∀ c ∈ E2.ledger, c.ctype = .SPENT → c ∈ E.ledger)
    ∧ (∀ c ∈ E2.ledger.drop E.ledger.length,
        ev.lo ≤ c.sup.lo ∧ c.sup.hi ≤ ev.hi)
    ∧ (∀ c ∈ E2.ledger, c.ctype = .ACTIVE →
        c ∈ E1.ledger ∨ (∃ c0, c0 ∈ E1.ledger ∧ c0.ctype = .LATENT ∧ c.sup = c0.sup))
    ∧ (∀ c ∈ E2.ledger.drop E.ledger.length,
        (c.sup.leftOriented = true → c.sup.hi ≤ x) ∧
        (c.sup.leftOriented = false → x < c.sup.hi))

/-- MST0-13: bounded DELETE injection — E_after − E_before ≤ 6·cost_A(D)
    with the EXECUTED A-side cost, not an injection-count variable. -/
def MST0_13 : Prop :=
  ∀ (E : Engine) (A : BST) (x nkeys : Nat),
    let (E2, _, a) := replayAccessA E A .DELETE x nkeys;
    energy E2.ledger ≤ energy E.ledger + 6 * a

/-- MST0-14: universal synchronous KEEP repayment — mechanism identity as
    lemma-conjunct PLUS sufficiency along all paired executions from the
    empty ledger (the `min` identity alone is NOT the theorem). -/
def MST0_14 : Prop :=
  (∀ (L : Ledger) (y a : Nat),
    (discharge L (required y a)).2 = Nat.min (activePool L) (required y a))
  ∧ (∀ (T0 : BST) (H : List (Mode × Nat)) (n : Nat),
    execSuffices { ledger := [], cursor := 0 } T0 T0 H n = true)

/-- MST0-15: global integrability — SPENT-monotone + flip-legality (no double
    spend, unique lifecycle), discharge splitting invariance (decomposition
    independence), pool conservation, history-partition consistency. -/
def MST0_15 : Prop :=
  (∀ (L : Ledger) (need : Nat) (c : Credit),
    c ∈ L → c.ctype = .SPENT → c ∈ (discharge L need).1)
  ∧ (∀ (L : Ledger) (need : Nat) (c : Credit),
    c ∈ (discharge L need).1 → c.ctype = .SPENT →
      c ∈ L ∨ (∃ c0, c0 ∈ L ∧ c0.ctype = .ACTIVE ∧ c.sup = c0.sup))
  ∧ (∀ (L : Ledger) (n1 n2 : Nat),
    (discharge L (n1 + n2)).2 =
      (discharge L n1).2 + (discharge (discharge L n1).1 n2).2
    ∧ (discharge (discharge L n1).1 n2).1 = (discharge L (n1 + n2)).1)
  ∧ (∀ (L : Ledger) (need : Nat),
    activePool (discharge L need).1 + (discharge L need).2 = activePool L)
  ∧ (∀ (E0 : Engine) (T0 : BST) (H1 H2 : List (Mode × Nat)) (n : Nat),
    let (E1, A1, B1, sA1, sB1) := execTrees E0 T0 T0 H1 n;
    execLoop E1 A1 B1 n H2 sA1 sB1 = execLoop E0 T0 T0 n (H1 ++ H2) 0 0)

/-- MST0-22: constant independence — literals PLUS regret C-linkage PLUS
    K-uniformity across all inputs (bare literal equality is NOT this). -/
def MST0_22 : Prop :=
  (C_frozen = 2 ∧ K_frozen = 6)
  ∧ (∀ y a : Nat, required y a = Int.toNat ((y : Int) - (C_frozen : Int) * (a : Int)))
  ∧ (∀ (E : Engine) (isA : Bool) (lo hi x nkeys k : Nat), k ≤ K_frozen →
      (T7inject E isA lo hi x nkeys k).ledger.length ≤ E.ledger.length + K_frozen)

/-- MST0-17: universal Pair-Access composition, E_0-generalized —
    Splay(Y,T) + E_m − E_0 ≤ 2·Splay(X,T) + A(n) from arbitrary ledgers. -/
def MST0_17 : Prop :=
  ∃ A : Nat → Nat, ∀ (E0 : Engine) (T0 : BST) (H : List (Mode × Nat)) (n : Nat),
    let (E, sA, sB) := execHist E0 T0 H n;
    sB + energy E.ledger ≤ 2 * sA + A n + energy E0.ledger

/-- MST0-18: telescope / approximate monotonicity with explicit additive
    term and checked direction (no assumed endpoint bounds). -/
def MST0_18 : Prop :=
  ∃ A : Nat → Nat, ∀ (T0 : BST) (H : List (Mode × Nat)) (n : Nat),
    let (_, sA, sB) := execHist { ledger := [], cursor := 0 } T0 H n;
    sB ≤ 2 * sA + A n

/-- L3 frozen premise record: (byte length, SHA-256) of
    `bridge_sources/L3_1907.06310_v1.pdf` as acquired 2026-09-25 UTC. -/
def L3premise : Nat × String :=
  (1431066,
   "E23EA8B58984B9A3530E8BF06AA028645DAD420B1AF280EEB407F4D2A4495A78")

/-- L2 premise-byte status: SODA-2019 bytes not lawfully acquirable here. -/
def L2bytesFrozen : Bool := false

/-- MST0-19 blocked-source status (v0.4.5 E2, v0.4.7 G8): L3 premise record
    frozen, L2 bytes absent, so NO theorem-bearing MST0-19 proposition is
    instantiated. Concrete metadata conjunction (rfl-provable), never a
    theorem. The theorem-bearing bridge Prop instantiates only at Phase-16
    execution once exact L2 bytes freeze with convention match. -/
def MST0_19_blocked : Prop :=
  L3premise =
    (1431066,
     "E23EA8B58984B9A3530E8BF06AA028645DAD420B1AF280EEB407F4D2A4495A78") ∧
  L2bytesFrozen = false
