/-
Frozen MSTC-0002 ledger declarations for SPLAY-AM-DECIDE-v0.4 (normative).

Frozen calculus MSTC-0002 = (P_all, k=6, C=2): credit types, support/scale/
mass, T5/T6/T7 operations, energy/flow quantities, paired-execution driver,
block partition. Every operation below is an ACTUAL total computable
definition over explicit state (v0.4.6 F3) — no opaque theorem-bearing
operations, no sorry/admit. Finite canary agreement against the Python
executable semantics is a sanity check with zero discharge authority;
equivalence is proved at Phase-03 execution.
-/
import Frozen.SplayDefs

/-- Frozen constants: C = 2, k = 6 (literals, independent by construction). -/
def C_frozen : Nat := 2
def K_frozen : Nat := 6

/-- Frozen predicate P_all: fires on every KEEP and DELETE event. -/
def P_all : Mode → Bool
  | .KEEP => true
  | .DELETE => true

/-- Credit types of the unsigned Branch-A ledger. -/
inductive CreditType where
  | LATENT : CreditType
  | ACTIVE : CreditType
  | SPENT : CreditType
  deriving DecidableEq, Repr, Inhabited

/-- Boundary support (left, right, left-oriented?). -/
structure BoundarySup where
  lo : Nat
  hi : Nat
  leftOriented : Bool
  deriving DecidableEq, Repr, Inhabited

/-- One unit-mass discrepancy credit. -/
structure Credit where
  ctype : CreditType
  sup : BoundarySup
  deriving DecidableEq, Repr, Inhabited

/-- Ledger: finite multiset modeled as a list (canonical order by decision). -/
abbrev Ledger := List Credit

/-- Empty initial ledger (energy normalization). -/
def ledgerEmpty : Ledger := []

/-- Scalar energy: |LATENT| + |ACTIVE| (SPENT carries none). -/
def energy : Ledger → Nat
  | [] => 0
  | c :: cs =>
    (match c.ctype with | .LATENT => 1 | .ACTIVE => 1 | .SPENT => 0) + energy cs

/-- T7 injection sites: interior boundaries (i,i+1) of [lo,hi), restricted to
    1 ≤ i < nkeys, oriented LEFT iff i+1 ≤ x. -/
def sites (lo hi x nkeys : Nat) : List BoundarySup :=
  (List.range' lo (hi - lo)).filterMap fun i =>
    if decide (1 ≤ i ∧ i < nkeys ∧ i + 1 ≤ hi) then
      some { lo := i, hi := i + 1, leftOriented := decide (i + 1 ≤ x) }
    else none

/-- Engine state: ledger plus deterministic site-cycling cursor. -/
structure Engine where
  ledger : Ledger
  cursor : Nat

/-- T7 injection: up to k LATENT credits cycling over interior sites
    (A-side rotations only; other sides pass through unchanged). -/
def T7inject (E : Engine) (isA : Bool) (lo hi x nkeys k : Nat) : Engine :=
  if !isA then E
  else match sites lo hi x nkeys with
  | [] => E
  | ss =>
    let picks := (List.range k).filterMap fun j =>
      ss[(E.cursor + j) % ss.length]?
    { ledger := E.ledger ++ picks.map (fun s => { ctype := .LATENT, sup := s }),
      cursor := E.cursor + k }

/-- Convert the first LATENT credit to ACTIVE; none if no LATENT present.
    Structural recursion on the list: definitely terminating. -/
def activateFirst : Ledger → Option Ledger
  | [] => none
  | c :: cs =>
    if c.ctype == .LATENT then some ({ c with ctype := .ACTIVE } :: cs)
    else match activateFirst cs with
      | none => none
      | some rest => some (c :: rest)

/-- T5 activation: predicate-gated LATENT → ACTIVE (same support). -/
def T5activate (E : Engine) (m : Mode) : Engine :=
  if !P_all m then E
  else match activateFirst E.ledger with
    | none => E
    | some ledger => { E with ledger := ledger }

/-- Count ACTIVE credits available for repayment. -/
def activePool : Ledger → Nat
  | [] => 0
  | c :: cs => (if c.ctype == .ACTIVE then 1 else 0) + activePool cs

/-- T6 discharge: consume up to `need` ACTIVE credits into SPENT, returning
    the new ledger and the amount actually paid. Single left fold over the
    ledger (no general recursion): paid = min(activePool, need). -/
def discharge (L : Ledger) (need : Nat) : Ledger × Nat :=
  let step : Ledger × Nat × Nat → Credit → Ledger × Nat × Nat
    | (out, paid, rem), c =>
      if rem > 0 ∧ c.ctype = .ACTIVE then
        (out ++ [{ ctype := .SPENT, sup := c.sup }], paid + 1, rem - 1)
      else (out ++ [c], paid, rem)
  let (out, paid, _) := L.foldl step ([], 0, need)
  (out, paid)

/-- Edge regret w = y - 2a (integers; may be negative). -/
def regret (y a : Nat) : Int := (y : Int) - 2 * (a : Int)

/-- Positive-regret demand: max(w, 0). -/
def required (y a : Nat) : Nat := (regret y a).toNat

/-- A block is a contiguous history segment (exact-once partition proved at
    MST0-17; the partition theorem is not assumed here). -/
abbrev Block := List (Mode × Nat)

/-- Replay one rotation step through T7+T5 (A-side injects). -/
def replayStep (E : Engine) (isA : Bool) (m : Mode) (ev : StepEv)
    (x nkeys : Nat) : Engine :=
  T5activate (T7inject E isA ev.lo ev.hi x nkeys K_frozen) m

/-- Replay a full access on side A: splay, inject+activate per rotation. -/
def replayAccessA (E : Engine) (A : BST) (m : Mode) (x nkeys : Nat)
    : Engine × BST × Nat :=
  let a := splayCost A x
  let (A2, evs) := splayTrace A x
  let E2 := evs.foldl (fun E ev => replayStep E true m ev x nkeys) E
  (E2, A2, a)

/-- Replay a KEEP access on side B with mate cost a: activate per rotation,
    then discharge positive regret once (terminal-edge convention). -/
def replayAccessB (E : Engine) (B : BST) (x nkeys a : Nat)
    : Engine × BST × Nat × Nat :=
  let y := splayCost B x
  let (B2, evs) := splayTrace B x
  let E2 := evs.foldl (fun E ev => T5activate E .KEEP) E
  let need := required y a
  let (ledger, paid) := discharge E2.ledger need
  ({ ledger := ledger, cursor := E2.cursor }, B2, y, paid)

/-- Paired-execution loop: structural recursion on the history. -/
def execLoop : Engine → BST → BST → Nat → List (Mode × Nat) → Nat → Nat
    → Engine × Nat × Nat
  | E, _, _, _, [], sA, sB => (E, sA, sB)
  | E, A, B, n, (.KEEP, x) :: rest, sA, sB =>
    let (E1, A2, a) := replayAccessA E A .KEEP x n
    let (E2, B2, y, _) := replayAccessB E1 B x n a
    execLoop E2 A2 B2 n rest (sA + a) (sB + y)
  | E, A, B, n, (.DELETE, x) :: rest, sA, sB =>
    let (E1, A2, a) := replayAccessA E A .DELETE x n
    execLoop E1 A2 B n rest (sA + a) sB

/-- Paired execution from a common initial tree (Pair-Access precondition):
    A executes the full history, B executes KEEPs only. Returns final engine
    and summed Splay costs. -/
def execHist (E : Engine) (T0 : BST) (H : List (Mode × Nat)) (n : Nat)
    : Engine × Nat × Nat :=
  execLoop E T0 T0 n H 0 0
