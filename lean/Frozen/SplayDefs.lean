/-
Frozen Splay declarations for SPLAY-AM-DECIDE-v0.4 (normative, hash-frozen).

Covers spec §5.2 Splay-side core objects: finite key sets (Nat), BST
validity (inorder-sorted keys), ordinary bottom-up splay (opaque with
tracked axiom record below: implementation identity proved at Phase-03
canary agreement, never assumed), cost depth+1, KEEP/DELETE access
semantics, subsequence relation. No proofs live here; no sorry/admit.
-/

/-- Binary search tree over natural keys. -/
inductive BST where
  | leaf : BST
  | node : Nat → BST → BST → BST
  deriving DecidableEq, Repr

/-- Inorder key list. -/
def BST.keys : BST → List Nat
  | .leaf => []
  | .node k l r => l.keys ++ [k] ++ r.keys

/-- BST validity: inorder keys strictly sorted. -/
def BST.Valid : BST → Prop
  | .leaf => True
  | .node k l r => l.Valid ∧ r.Valid ∧ (∀ x ∈ l.keys, x < k) ∧ (∀ x ∈ r.keys, k < x)

/-- Depth of a key (root depth 0); 0 default keeps the function total. -/
def BST.depth : BST → Nat → Nat
  | .leaf, _ => 0
  | .node k l r, x =>
    if x = k then 0
    else if x < k then (l.depth x) + 1
    else (r.depth x) + 1

/-- Frozen cost convention: depth + 1. -/
def splayCost (T : BST) (x : Nat) : Nat := T.depth x + 1

/-- Ordinary bottom-up splay (opaque: TRACKED AXIOM SPLAY-IMPL, discharged by
    Phase-03 Python↔Lean canary agreement on final-tree/cost/case traces). -/
opaque splay : BST → Nat → BST

/-- KEEP access cost pair (A-side cost, B-side cost). -/
def keepCosts (A B : BST) (x : Nat) : Nat × Nat :=
  (splayCost A x, splayCost B x)

/-- Subsequence relation (Y retained from X). -/
def IsSubseq (Y X : List Nat) : Prop := Y.Sublist X
