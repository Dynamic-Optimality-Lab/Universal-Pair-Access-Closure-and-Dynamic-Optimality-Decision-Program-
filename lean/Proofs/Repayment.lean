import Frozen.Statements
-- Proofs/Repayment.lean: MST0-14 KEEP repayment (WP-3 PROVE track).
-- Mechanism identity (paid = min(pool, demand)) proved here by fold induction.
-- Universal sufficiency (execSuffices over all paired histories) is OPEN (see
-- Layer-A open obligation) and correctly absent: no theorem asserted without
-- proof. Proof developments importing frozen declarations, never modifying them.

/-- T6 discharge step in top-level form (definitionally the frozen fold step). -/
def repStep : Ledger × Nat × Nat → Credit → Ledger × Nat × Nat
  | (out, paid, rem), c =>
    if rem > 0 ∧ c.ctype = .ACTIVE then
      (out ++ [{ ctype := .SPENT, sup := c.sup }], paid + 1, rem - 1)
    else (out ++ [c], paid, rem)

/-- The frozen discharge is the repStep fold (bridge lemma, no Frozen change). -/
theorem rep_disch_eq : ∀ (L : Ledger) (need : Nat),
    discharge L need =
      ((L.foldl repStep ([], 0, need)).1, (L.foldl repStep ([], 0, need)).2.1) := by
  intro L need
  rfl

/-- Arithmetic core of the discharge bound (min case analysis). -/
theorem rep_min_step : ∀ (paid P R : Nat), R > 0 →
    (paid + 1) + min P (R - 1) = paid + min (P + 1) R := by
  intro paid P R hr
  by_cases hle : P + 1 ≤ R
  · rw [Nat.min_eq_left hle, Nat.min_eq_left (show P ≤ R - 1 by omega)]
    omega
  · have h1 : R ≤ P + 1 := by omega
    have h2 : R - 1 ≤ P := by omega
    rw [Nat.min_eq_right h1, Nat.min_eq_right h2]
    omega

/-- Fold accounting: paid tracks min(pool, demand) from any start state. -/
theorem rep_pay_aux : ∀ (L : Ledger) (out : Ledger) (paid rem : Nat),
    (L.foldl repStep (out, paid, rem)).2.1
      = paid + min (activePool L) rem := by
  intro L
  induction L with
  | nil =>
    intro out paid rem
    rw [List.foldl_nil]
    show paid = paid + min 0 rem
    simp
  | cons c cs ih =>
    intro out paid rem
    simp only [List.foldl_cons]
    by_cases hcA : c.ctype = .ACTIVE
    · have hpool : activePool (c :: cs) = activePool cs + 1 := by
        simp [activePool, hcA, Nat.add_comm]
      by_cases hr : rem > 0
      · have hstep : repStep (out, paid, rem) c
            = (out ++ [{ ctype := .SPENT, sup := c.sup }], paid + 1, rem - 1) := by
          simp [repStep, hr, hcA]
        rw [hstep, hpool]
        have ih2 := ih (out ++ [{ ctype := .SPENT, sup := c.sup }]) (paid + 1) (rem - 1)
        have key := rep_min_step paid (activePool cs) rem hr
        omega
      · have hrem : rem = 0 := by omega
        have hstep : repStep (out, paid, rem) c
            = (out ++ [c], paid, rem) := by
          simp [repStep, hrem]
        rw [hstep, hrem, hpool]
        have ih2 := ih (out ++ [c]) paid 0
        have z1 : min (activePool cs + 1) 0 = 0 := Nat.min_eq_right (Nat.zero_le _)
        have z2 : min (activePool cs) 0 = 0 := Nat.min_eq_right (Nat.zero_le _)
        omega
    · have hpool : activePool (c :: cs) = activePool cs := by
        cases hct : c.ctype with
        | LATENT => simp [activePool, hct]
        | ACTIVE => exact absurd hct hcA
        | SPENT => simp [activePool, hct]
      have hstep : repStep (out, paid, rem) c
          = (out ++ [c], paid, rem) := by
        simp [repStep, hcA]
      rw [hstep, hpool]
      have ih2 := ih (out ++ [c]) paid rem
      exact ih2

/-- MST0-14 mechanism identity: discharge pays exactly min(pool, demand). -/
theorem MST0_14_paid_identity : ∀ (L : Ledger) (y a : Nat),
    (discharge L (required y a)).2 = Nat.min (activePool L) (required y a) := by
  intro L y a
  have h := rep_pay_aux L [] 0 (required y a)
  have h' : (L.foldl repStep ([], 0, required y a)).2.1
      = 0 + Nat.min (activePool L) (required y a) := h
  have h2 : (discharge L (required y a)).2
      = (L.foldl repStep ([], 0, required y a)).2.1 := by rw [rep_disch_eq]
  omega
