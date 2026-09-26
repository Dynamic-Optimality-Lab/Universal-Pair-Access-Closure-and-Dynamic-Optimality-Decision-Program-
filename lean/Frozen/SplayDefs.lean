/-
Frozen Splay declarations for SPLAY-AM-DECIDE-v0.4 (normative, hash-frozen).

Covers spec §5.2 Splay-side core objects with ACTUAL total computable
definitions (v0.4.6 F3): finite key sets (Nat), BST validity (inorder-sorted
keys), ordinary bottom-up splay with ROOT/ZIG/LL/RR/LR/RL cases (zipper
implementation with derived rotation formulas; structural recursion, no
fuel, no sorry), per-rotation trace events (case + affected interval),
cost depth+1, KEEP/DELETE access semantics, subsequence relation.
Equivalence to the Python executable semantics is PROVED at Phase-03
execution (canary agreement is sanity-only and discharges nothing).
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

/-- Depth of a key (root depth 0; 0 default keeps the function total). -/
def BST.depth : BST → Nat → Nat
  | .leaf, _ => 0
  | .node k l r, x =>
    if x = k then 0
    else if x < k then (l.depth x) + 1
    else (r.depth x) + 1

/-- Frozen cost convention: depth + 1. -/
def splayCost (T : BST) (x : Nat) : Nat := T.depth x + 1

/-- Bottom-up splay rotation cases. -/
inductive SplayCase where
  | ROOT | ZIG | LL | RR | LR | RL
  deriving DecidableEq, Repr, Inhabited

/-- One rotation step: case plus affected key interval. -/
structure StepEv where
  scase : SplayCase
  lo : Nat
  hi : Nat
  deriving DecidableEq, Repr

/-- Ancestor context: each frame holds the parent key, the side of the
    focused subtree within the parent, and the sibling subtree. -/
inductive Ctx where
  | top : Ctx
  | leftOf : Nat → BST → Ctx → Ctx
  | rightOf : Nat → BST → Ctx → Ctx

/-- Descend to the node holding x; return its subtree and ancestor context.
    Returns none iff x is absent. The context is parent-first: the outermost
    frame is the parent, `.top` marks the root end. (A root-first order here
    would rotate the wrong pair in `splayWithT`; parent-first is load-bearing.) -/
def descendAcc : BST → Nat → Ctx → Option (BST × Ctx)
  | .leaf, _, _ => none
  | .node k l r, x, acc =>
    if x = k then some (.node k l r, acc)
    else if x < k then descendAcc l x (.leftOf k r acc)
    else descendAcc r x (.rightOf k l acc)

/-- Descend with an empty initial context. -/
def BST.descend (T : BST) (x : Nat) : Option (BST × Ctx) :=
  descendAcc T x .top

/-- Plug a focused subtree back into its context (dead-branch use only). -/
def plug : Ctx → BST → BST
  | .top, t => t
  | .leftOf k q outer, t => plug outer (.node k t q)
  | .rightOf k q outer, t => plug outer (.node k q t)

/-- Zig with x left child: p(kp, L=n(x,t1,t2), R=B) ↦ x(x, t1, node(kp,t2,B)).
    Leaf focus is dead on valid input; it rebuilds the parent unchanged. -/
def zigL (n : BST) (x kp : Nat) (B : BST) : BST :=
  match n with
  | .node _ t1 t2 => .node x t1 (.node kp t2 B)
  | .leaf => .node kp .leaf B

/-- Zig with x right child: mirror image. -/
def zigR (n : BST) (x kp : Nat) (B : BST) : BST :=
  match n with
  | .node _ t1 t2 => .node x (.node kp B t1) t2
  | .leaf => .node kp B .leaf

/-- Zig-zig left-left: two sequential right rotations, direct formula.
    g(kg, L=p(kp, L=n(x,t1,t2), R=B), R=C) ↦ x(x, t1, node(kp,t2,node(kg,B,C))). -/
def zigzigLL (n : BST) (x kp : Nat) (B : BST) (kg : Nat) (C : BST) : BST :=
  match n with
  | .node _ t1 t2 => .node x t1 (.node kp t2 (.node kg B C))
  | .leaf => .node kg (.node kp .leaf B) C

/-- Zig-zig right-right: mirror image.
    g(kg, L=C, R=p(kp, L=B, R=n(x,t1,t2))) ↦ x(x, node(kp,node(kg,C,B),t1), t2). -/
def zigzigRR (n : BST) (x kp : Nat) (B : BST) (kg : Nat) (C : BST) : BST :=
  match n with
  | .node _ t1 t2 => .node x (.node kp (.node kg C B) t1) t2
  | .leaf => .node kg C (.node kp B .leaf)

/-- Zig-zag left-right: x right child of p, p left child of g.
    g(kg, L=p(kp, L=A, R=n(x,t1,t2)), R=D) ↦ x(x, node(kp,A,t1), node(kg,t2,D)). -/
def zigzagLR (n : BST) (x kp : Nat) (A : BST) (kg : Nat) (D : BST) : BST :=
  match n with
  | .node _ t1 t2 => .node x (.node kp A t1) (.node kg t2 D)
  | .leaf => .node kg (.node kp A .leaf) D

/-- Zig-zag right-left: mirror image.
    g(kg, L=A, R=p(kp, L=n(x,t1,t2), R=D)) ↦ x(x, node(kg,A,t1), node(kp,t2,D)). -/
def zigzagRL (n : BST) (x kp : Nat) (D : BST) (kg : Nat) (A : BST) : BST :=
  match n with
  | .node _ t1 t2 => .node x (.node kg A t1) (.node kp t2 D)
  | .leaf => .node kg A (.node kp .leaf D)

/-- Interval endpoints of rotated keys. -/
def span3 (x kp kg : Nat) : Nat × Nat :=
  (Nat.min x (Nat.min kp kg), Nat.max x (Nat.max kp kg))

/-- Bottom-up splay loop with per-rotation trace events. Double-case
    patterns precede single-case patterns, so a length-1 context (outer
    necessarily `.top`) is the only route to a zig branch. Structural
    recursion on the context: no fuel, no sorry. Leaf-focus branches are
    dead on valid input and plug back unchanged. -/
def splayWithT : BST → Ctx → List StepEv → BST × List StepEv
  | n, .top, evs => (n, evs)
  | n, .leftOf kp q (.leftOf kg c outer), evs =>
      match n with
      | .node x _ _ =>
        let (lo, hi) := span3 x kp kg
        splayWithT (zigzigLL n x kp q kg c) outer
          (evs ++ [{ scase := .LL, lo := lo, hi := hi }])
      | .leaf => (plug (.leftOf kp q (.leftOf kg c outer)) n, evs)
  | n, .rightOf kp q (.rightOf kg c outer), evs =>
      match n with
      | .node x _ _ =>
        let (lo, hi) := span3 x kp kg
        splayWithT (zigzigRR n x kp q kg c) outer
          (evs ++ [{ scase := .RR, lo := lo, hi := hi }])
      | .leaf => (plug (.rightOf kp q (.rightOf kg c outer)) n, evs)
  | n, .rightOf kp q (.leftOf kg d outer), evs =>
      match n with
      | .node x _ _ =>
        let (lo, hi) := span3 x kp kg
        splayWithT (zigzagLR n x kp q kg d) outer
          (evs ++ [{ scase := .LR, lo := lo, hi := hi }])
      | .leaf => (plug (.rightOf kp q (.leftOf kg d outer)) n, evs)
  | n, .leftOf kp q (.rightOf kg a outer), evs =>
      match n with
      | .node x _ _ =>
        let (lo, hi) := span3 x kp kg
        splayWithT (zigzagRL n x kp q kg a) outer
          (evs ++ [{ scase := .RL, lo := lo, hi := hi }])
      | .leaf => (plug (.leftOf kp q (.rightOf kg a outer)) n, evs)
  | n, .leftOf kp q outer, evs =>
      match n with
      | .node x _ _ =>
        splayWithT (zigL n x kp q) outer
          (evs ++ [{ scase := .ZIG, lo := Nat.min x kp, hi := Nat.max x kp }])
      | .leaf => (plug (.leftOf kp q outer) n, evs)
  | n, .rightOf kp q outer, evs =>
      match n with
      | .node x _ _ =>
        splayWithT (zigR n x kp q) outer
          (evs ++ [{ scase := .ZIG, lo := Nat.min x kp, hi := Nat.max x kp }])
      | .leaf => (plug (.rightOf kp q outer) n, evs)

/-- Ordinary bottom-up splay: x absent leaves the tree unchanged. -/
def splay (T : BST) (x : Nat) : BST :=
  match T.descend x with
  | none => T
  | some (sub, ctx) => (splayWithT sub ctx []).1

/-- Splay with rotation trace (case + affected interval per step). -/
def splayTrace (T : BST) (x : Nat) : BST × List StepEv :=
  match T.descend x with
  | none => (T, [])
  | some (sub, ctx) => splayWithT sub ctx []

/-- Access modes. -/
inductive Mode where
  | KEEP : Mode
  | DELETE : Mode
  deriving DecidableEq, Repr, Inhabited

/-- KEEP step: both trees splayed; returns new trees and (a, y) costs. -/
def keepStep (A B : BST) (x : Nat) : BST × BST × Nat × Nat :=
  let a := splayCost A x
  let y := splayCost B x
  (splay A x, splay B x, a, y)

/-- DELETE step: only A splays; B is untouched; y = 0. -/
def deleteStep (A : BST) (x : Nat) : BST × Nat :=
  let a := splayCost A x
  (splay A x, a)

/-- Subsequence relation (Y retained from X). -/
def IsSubseq (Y X : List Nat) : Prop := Y.Sublist X
