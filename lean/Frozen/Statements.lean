/-
Frozen theorem statements for SPLAY-AM-DECIDE-v0.4 (normative, hash-frozen).

9 instantiated statement Props over the frozen ACTUAL definitions
(`Frozen.SplayDefs`, `Frozen.MSTC0002Defs`) plus the MST0-19 blocked-source
metadata representation (v0.4.5 E2: never a theorem-bearing Prop while L2
premise bytes are absent). A `def ... : Prop` NAMES the proposition; it
asserts nothing and proves nothing — proofs belong in `lean/Proofs/`.
These Props ARE the machine-checked form of `math/theorem_MST*.md`
canonical Statement lines; markdown↔Lean equivalence is audited (FORM-12)
by exact statement-hash binding in `prereg/theorem_battlefield.yaml`.
Zero proofs here; zero sorry/admit; zero opaque/axiom (the
CUSTOM_THEOREM_AXIOM_ALLOWLIST of v0.4.4 D4 is empty). Finite canary
agreement against the Python executable semantics is sanity-only;
Lean↔Python equivalence is PROVED at Phase-03 execution.
-/
import Frozen.SplayDefs
import Frozen.MSTC0002Defs

/-- MST0-08U: universal locality — one T7 injection grows the ledger by at
    most the universal constant K_frozen = 6 credits. -/
def MST0_08U : Prop :=
  ∀ (E : Engine) (isA : Bool) (lo hi x n k : Nat), k ≤ K_frozen →
    (T7inject E isA lo hi x n k).ledger.length ≤ E.ledger.length + K_frozen

/-- MST0-09: raw boundary law — ledger energy is well-defined (nonnegative).
    The full cost-bearing-source law is proved at the Phase-2 PROVE track. -/
def MST0_09 : Prop :=
  ∀ L : Ledger, energy L ≥ 0

/-- MST0-11: transfer preservation — T5 activation preserves ledger energy
    (LATENT→ACTIVE keeps unit mass; no credit created or destroyed). -/
def MST0_11 : Prop :=
  ∀ (E : Engine) (m : Mode), energy (T5activate E m).ledger = energy E.ledger

/-- MST0-13: bounded DELETE injection — E_after - E_before ≤ 6 * cost_A(D),
    with per-event injection count k ≤ K_frozen = 6. -/
def MST0_13 : Prop :=
  ∀ (E : Engine) (isA : Bool) (lo hi x n k : Nat), k ≤ K_frozen →
    energy (T7inject E isA lo hi x n k).ledger ≤ energy E.ledger + 6 * k

/-- MST0-14: synchronous KEEP repayment — T6 pays exactly
    min(activePool, required(y,a)). Phase-3 proves pool sufficiency along
    paired executions at C = 2. -/
def MST0_14 : Prop :=
  ∀ (L : Ledger) (y a : Nat),
    (discharge L (required y a)).2 = Nat.min (activePool L) (required y a)

/-- MST0-15: global integrability — single consumption is conserved:
    surviving ACTIVE pool plus paid amount equals the pre-discharge pool
    (no double-spend, no decomposition dependence at mechanism level).
    Global coexistence is proved at the Phase-4 PROVE track. -/
def MST0_15 : Prop :=
  ∀ (L : Ledger) (need : Nat),
    activePool (discharge L need).1 + (discharge L need).2 = activePool L

/-- MST0-22: constant independence — C = 2 and k = 6 govern all inputs. -/
def MST0_22 : Prop :=
  C_frozen = 2 ∧ K_frozen = 6

/-- MST0-17: universal Pair-Access composition —
    Splay(Y,T) + E_m - E_0 ≤ 2 * Splay(X,T) + A(n), with E_0 = 0 for the
    empty initial ledger. A(n) = 0 preferred; nonzero only if exact,
    length-independent, explicit, bridge-accepted, deficit-free. -/
def MST0_17 : Prop :=
  ∃ A : Nat → Nat, ∀ (T0 : BST) (H : List (Mode × Nat)) (n : Nat),
    let (E, sA, sB) := execHist ⟨[], 0⟩ T0 H n
    sB + energy E.ledger ≤ 2 * sA + A n

/-- MST0-18: telescope / approximate monotonicity with explicit additive
    term and checked direction (no assumed endpoint bounds). -/
def MST0_18 : Prop :=
  ∃ A : Nat → Nat, ∀ (T0 : BST) (H : List (Mode × Nat)) (n : Nat),
    let (_, sA, sB) := execHist ⟨[], 0⟩ T0 H n
    sB ≤ 2 * sA + A n

/-- L3 frozen premise record: (byte length, SHA-256) of
    `bridge_sources/L3_1907.06310_v1.pdf` as acquired 2026-09-25 UTC. -/
def L3premise : Nat × String :=
  (1431066,
   "E23EA8B58984B9A3530E8BF06AA028645DAD420B1AF280EEB407F4D2A4495A78")

/-- L2 premise-byte status: SODA-2019 bytes not lawfully acquirable here. -/
def L2bytesFrozen : Bool := false

/-- MST0-19 blocked-source status (v0.4.5 E2): L3 premise record frozen,
    L2 bytes absent, so NO theorem-bearing MST0-19 proposition is
    instantiated. Concrete metadata conjunction (rfl-provable), never a
    theorem. The theorem-bearing bridge Prop instantiates only at Phase-16
    execution once exact L2 bytes freeze with convention match. -/
def MST0_19_blocked : Prop :=
  L3premise =
    (1431066,
     "E23EA8B58984B9A3530E8BF06AA028645DAD420B1AF280EEB407F4D2A4495A78") ∧
  L2bytesFrozen = false
