/-
Agree executable: canonical serialization of frozen-semantics samples for
Lean↔Python agreement (FORM-04/05/06/07). Deterministic fixed samples; the
Python mirror `tests/formal/agree_py.py` prints byte-identical lines.
Comparison tuple (authoritative): final_tree, search_path,
rotation_case_sequence (+intervals), splay_cost, ledger_energy+sums.
Diagnostic scale per G10 (samples, not proof); mismatch fails closed.
-/
import Frozen.SplayDefs
import Frozen.MSTC0002Defs

def showNats (xs : List Nat) : String :=
  String.intercalate "," (xs.map toString)

def showTree : BST → String
  | .leaf => "leaf"
  | .node k l r => s!"(node {k} {showTree l} {showTree r})"

def pathKeys : Ctx → List Nat
  | .top => []
  | .leftOf k _ outer => pathKeys outer ++ [k]
  | .rightOf k _ outer => pathKeys outer ++ [k]

def caseName : SplayCase → String
  | .ROOT => "ROOT"
  | .ZIG => "ZIG"
  | .LL => "LL"
  | .RR => "RR"
  | .LR => "LR"
  | .RL => "RL"

def showTrace (evs : List StepEv) : String :=
  String.intercalate ";" (evs.map fun ev => s!"{caseName ev.scase}:{ev.lo}-{ev.hi}")

def t1 : BST :=
  .node 4 (.node 2 (.node 1 .leaf .leaf) (.node 3 .leaf .leaf))
          (.node 6 (.node 5 .leaf .leaf) (.node 7 .leaf .leaf))

def t2 : BST :=
  .node 1 .leaf (.node 2 .leaf (.node 3 .leaf .leaf))

def t3 : BST :=
  .node 3 (.node 2 (.node 1 .leaf .leaf) .leaf) .leaf

def t4 : BST :=
  .node 3 (.node 1 .leaf (.node 2 .leaf .leaf))
          (.node 6 (.node 4 .leaf (.node 5 .leaf .leaf)) (.node 7 .leaf .leaf))

def h1 : List (Mode × Nat) :=
  [(.KEEP, 3), (.KEEP, 5), (.DELETE, 2), (.KEEP, 7)]

def h2 : List (Mode × Nat) :=
  [(.KEEP, 1), (.KEEP, 2), (.KEEP, 3), (.DELETE, 1)]

def emitAccess (tid : String) (t : BST) (x : Nat) : IO Unit := do
  IO.println s!"TREE {tid} {showTree (splay t x)}"
  match t.descend x with
  | none => IO.println s!"PATH {tid}:{x} ABSENT"
  | some (_, ctx) => IO.println s!"PATH {tid}:{x} {showNats (pathKeys ctx)}"
  let (_, evs) := splayTrace t x
  IO.println s!"TRACE {tid}:{x} {showTrace evs}"
  IO.println s!"COST {tid}:{x} {splayCost t x}"

def emitHist (hid : String) (t : BST) (h : List (Mode × Nat)) (n : Nat) : IO Unit := do
  let (E, sA, sB) := execHist { ledger := [], cursor := 0 } t h n
  IO.println s!"LEDGER {hid} {energy E.ledger} {sA} {sB}"

def main : IO Unit := do
  emitAccess "t1" t1 1
  emitAccess "t1" t1 4
  emitAccess "t1" t1 7
  emitAccess "t1" t1 0
  emitAccess "t2" t2 3
  emitAccess "t2" t2 1
  emitAccess "t2" t2 99
  emitAccess "t3" t3 1
  emitAccess "t3" t3 3
  emitAccess "t3" t3 0
  emitAccess "t4" t4 5
  emitAccess "t4" t4 2
  emitAccess "t4" t4 6
  emitAccess "t4" t4 99
  emitHist "h1" t1 h1 7
  emitHist "h2" t2 h2 3
