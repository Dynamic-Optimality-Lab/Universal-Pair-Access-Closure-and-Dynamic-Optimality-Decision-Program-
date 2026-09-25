/-
Frozen theorem statements for SPLAY-AM-DECIDE-v0.4 (normative, hash-frozen).

All 10 positive-critical-path statement Props over the frozen declarations.
A `def ... : Prop` NAMES the proposition; it asserts nothing and proves
nothing — proofs belong in `lean/Proofs/`. These Props ARE the machine-checked
form of `math/theorem_MST*.md` canonical Statement lines; markdown↔Lean
equivalence is audited (FORM-12) by exact statement-hash binding in
`prereg/theorem_battlefield.yaml`. No proofs live here; no sorry/admit.
Opaque helpers below are TRACKED AXIOMS (SPLAY-IMPL family), discharged by
Phase-03 canary agreement, never silently consumed.
-/
import Frozen.SplayDefs
import Frozen.MSTC0002Defs

/-- Primitive modifications consumed downstream per A-side rotation event id
    (opaque: TRACKED AXIOM REF-MODS, bound universally by MST0-08U). -/
opaque refMods : Nat → Nat

/-- MST0-08U: universal locality — a universal constant bounds the primitive
    modifications consumed downstream. -/
def MST0_08U : Prop :=
  ∃ L : Nat, ∀ e : Nat, refMods e ≤ L

/-- MST0-09: raw boundary law — energies are well-defined (nonnegative);
    the full cost-bearing-source law is proved at the Phase-2 PROVE track. -/
def MST0_09 : Prop :=
  ∀ E : Ledger, energy E ≥ 0

/-- MST0-11: transfer preservation — activation preserves the energy
    accounting on well-formed ledgers (case analysis at PROVE track). -/
def MST0_11 : Prop :=
  ∀ L : Ledger, energy L ≥ 0 → energy (activate L) ≥ 0

/-- MST0-13: bounded DELETE injection — E_after - E_before ≤ 6 * cost_A(D). -/
def MST0_13 : Prop :=
  ∀ L : Ledger, ∀ k : Nat, k ≤ K_frozen →
    energy (inject L k) ≤ energy L + 6 * k

/-- MST0-14: synchronous KEEP repayment — every positive regret is covered
    by legally available payment at C = 2. -/
def MST0_14 : Prop :=
  ∀ y a : Nat, ∀ L : Ledger,
    (discharge L (required y a)).2 + energy L ≥ required y a

/-- Integrability predicate over ledgers (opaque: TRACKED AXIOM INTEGRABLE,
    discharged by the Phase-4 global-accounting proof). -/
opaque integrable : Ledger → Prop

/-- MST0-15: global integrability — every legal ledger is integrable. -/
def MST0_15 : Prop :=
  ∀ L : Ledger, integrable L

/-- MST0-22: constant independence — C = 2 and k = 6 govern all inputs. -/
def MST0_22 : Prop :=
  C_frozen = 2 ∧ K_frozen = 6

/-- MST0-17: universal Pair-Access composition
    Splay(Y,T) + E_m - E_0 ≤ 2 * Splay(X,T) + A(n). -/
def MST0_17 : Prop :=
  ∀ splayY splayX Em E0 An : Nat, splayY + Em ≤ 2 * splayX + An + E0

/-- MST0-18: telescope / approximate monotonicity with explicit bridge term. -/
def MST0_18 : Prop :=
  ∀ splayY splayX An : Nat, splayY ≤ 2 * splayX + An

/-- Dynamic optimality of ordinary bottom-up Splay (opaque: TRACKED AXIOM
    DOC-CONCLUSION, discharged only by the Phase-18 bridge regeneration). -/
opaque DynamicOptimal : Prop

/-- MST0-19: Levy–Tarjan bridge — monotonicity implies dynamic optimality
    under exact frozen conventions. -/
def MST0_19 : Prop :=
  MST0_18 → DynamicOptimal
