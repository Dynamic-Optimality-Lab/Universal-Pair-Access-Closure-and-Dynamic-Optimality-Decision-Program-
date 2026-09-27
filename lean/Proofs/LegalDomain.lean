import Frozen.Statements
-- Proofs/LegalDomain.lean: MST0-14R repair-track legal domain (NEW FILE).
-- Staged UNCHECKED: no Lean toolchain in this environment (FORMAL_WITNESS_CERT
-- = PENDING_TOOLCHAIN). Alters no Frozen module. Follows Frozen naming/style.
-- The repaired successor proposition; the old MST0_14 bytes are preserved as-is.

/-- Minimal source-derived legal-domain predicate for paired executions.
    C1 BST validity (spec s4/s5.2). C2 tree keys within [n] (spec s4 universe,
    SUBSET reading: equality over-restricts without model mandate). C3 modes
    legal: vacuous in Lean (Mode has exactly KEEP/DELETE constructors).
    C4 history keys within [n] (spec s4 + validate_history). C5 common initial
    tree: structural (repaired statement passes T0 twice). No presence
    requirement (absent-key splay is a defined no-op); no Y-subsequence
    conjunct (lives at MST0-17). Mirrors python/audit/legal_domain.py. -/
def LegalPairInstance (T0 : BST) (H : List (Mode × Nat)) (n : Nat) : Prop :=
  T0.Valid ∧ (∀ k ∈ T0.keys, 1 ≤ k ∧ k ≤ n) ∧ (∀ e ∈ H, 1 ≤ e.2 ∧ e.2 ≤ n)

/-- Repaired successor proposition (NEW identity MST0-14R; old MST0_14 kept).
    Mechanism conjunct reused via MST0_14_paid_identity (domain-independent);
    sufficiency guarded by the minimal LegalPairInstance premise. -/
def RepairedMST0_14 : Prop :=
  (∀ (L : Ledger) (y a : Nat),
    (discharge L (required y a)).2 = Nat.min (activePool L) (required y a))
  ∧ (∀ (T0 : BST) (H : List (Mode × Nat)) (n : Nat),
    LegalPairInstance T0 H n →
    execSuffices { ledger := [], cursor := 0 } T0 T0 H n = true)

/-- Domain-defect witness tree: right vine over {1,2,3} (valid BST). -/
def witnessT0 : BST :=
  .node 1 .leaf (.node 2 .leaf (.node 3 .leaf .leaf))

/-- Domain-defect witness history with empty universe. -/
def witnessH : List (Mode × Nat) :=
  [(Mode.DELETE, 3), (Mode.KEEP, 3)]

/-- The old literal sufficiency conjunct is FALSE on the witness
    (expected kernel evaluation: false; run with the pinned toolchain). -/
#eval execSuffices { ledger := [], cursor := 0 } witnessT0 witnessT0 witnessH 0

/-- The witness is ILLEGAL under the repaired domain (expected: False).
    Bool mirror avoids Prop-Decidable synthesis (unverified without toolchain). -/
def legalPairInstanceB : BST → List (Mode × Nat) → Nat → Bool
  | T0, H, n =>
    T0.keys.all (fun k => 1 <= k && k <= n) &&
    H.all (fun e => 1 <= e.2 && e.2 <= n)

#eval legalPairInstanceB witnessT0 witnessH 0

/-- Machine-checkable witness claims (pinned toolchain: `lake env lean`). -/
example : execSuffices { ledger := [], cursor := 0 } witnessT0 witnessT0 witnessH 0 = false :=
  by decide

example : legalPairInstanceB witnessT0 witnessH 0 = false := by decide

/-- BST insertion (computable witness-family helper; mirrors the
    insertion-built test trees, not a Frozen semantic). -/
def bstInsert : BST → Nat → BST
  | .leaf, k => .node k .leaf .leaf
  | .node kk l r, k =>
    if k < kk then .node kk (bstInsert l k) r else .node kk l (bstInsert r k)

/-- Right vine over {1,..,n} by ascending insertion. -/
def vineRight : Nat → BST
  | 0 => .leaf
  | n + 1 => bstInsert (vineRight n) (n + 1)

/-- Canonical 4-access obstruction family history (n >= 28 falsifies). -/
def famHist (n : Nat) : List (Mode × Nat) :=
  [(Mode.DELETE, n - 1), (Mode.DELETE, n), (Mode.KEEP, n), (Mode.KEEP, n - 1)]

#eval execSuffices { ledger := [], cursor := 0 } (vineRight 28) (vineRight 28) (famHist 28) 28

#eval legalPairInstanceB (vineRight 28) (famHist 28) 28

/-- Canonical LEGAL witness: paid < need at the final KEEP
    (heavy kernel computation; `native_decide` compiles it first). -/
example : execSuffices { ledger := [], cursor := 0 } (vineRight 28) (vineRight 28) (famHist 28) 28 = false :=
  by native_decide

/-- The canonical witness is legal (Bool mirror). -/
example : legalPairInstanceB (vineRight 28) (famHist 28) 28 = true := by decide
