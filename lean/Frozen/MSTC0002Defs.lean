/-
Frozen MSTC-0002 ledger declarations for SPLAY-AM-DECIDE-v0.4 (normative).

Covers spec §5.2 ledger-side core objects for the frozen calculus
(P_all, k=6, C=2): credit types, support/scale/mass, T5/T6/T7 operations,
energy/flow quantities, block partition placeholder. Concrete where the
frozen rule is total (energy, regret, demand); opaque with tracked axiom
records where the operation needs ledger-state threading proved later.
No proofs live here; no sorry/admit.
-/

/-- Frozen constants: C = 2, k = 6 (literals, independent by construction). -/
def C_frozen : Nat := 2
def K_frozen : Nat := 6

/-- Access mode. -/
inductive Mode where
  | KEEP : Mode
  | DELETE : Mode
  deriving DecidableEq, Repr

/-- Frozen predicate P_all: fires on every KEEP and DELETE event. -/
def P_all : Mode → Bool
  | .KEEP => true
  | .DELETE => true

/-- Credit types of the unsigned Branch-A ledger. -/
inductive CreditType where
  | LATENT : CreditType
  | ACTIVE : CreditType
  | SPENT : CreditType
  deriving DecidableEq, Repr

/-- Boundary support (left, right, orientation). -/
structure BoundarySup where
  lo : Nat
  hi : Nat
  leftOriented : Bool
  deriving DecidableEq, Repr

/-- One unit-mass discrepancy credit. -/
structure Credit where
  ctype : CreditType
  sup : BoundarySup
  deriving DecidableEq, Repr

/-- Ledger: finite multiset modeled as a list (canonical order by decision). -/
abbrev Ledger := List Credit

/-- Scalar energy: |LATENT| + |ACTIVE| (SPENT carries none). -/
def energy : Ledger → Nat
  | [] => 0
  | c :: cs =>
    (match c.ctype with | .LATENT => 1 | .ACTIVE => 1 | .SPENT => 0) + energy cs

/-- Edge regret w = y - 2a (integers; may be negative). -/
def regret (y a : Nat) : Int := (y : Int) - 2 * (a : Int)

/-- Positive-regret demand: max(w, 0). -/
def required (y a : Nat) : Nat := (regret y a).toNat

/-- T7 injection (opaque: TRACKED AXIOM T7-SITES, discharged by Phase-03
    agreement against the frozen site-cycling rule). -/
opaque inject : Ledger → Nat → Ledger

/-- T5 activation LATENT → ACTIVE (opaque: TRACKED AXIOM T5-ACT). -/
opaque activate : Ledger → Ledger

/-- T6 discharge of ACTIVE against demand (opaque: TRACKED AXIOM T6-PAY). -/
opaque discharge : Ledger → Nat → Ledger × Nat

/-- Block partition placeholder (exact-once partition proved in MST0-17). -/
abbrev BlockId := Nat
