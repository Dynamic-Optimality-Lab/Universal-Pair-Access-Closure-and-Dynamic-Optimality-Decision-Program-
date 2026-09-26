import Frozen.Statements
-- Proofs/Boundary.lean: MST0-09 boundary cost-bearing-source law (WP-2 PROVE track).
-- Standalone (no inter-Proofs dependencies): T5-energy fact, per-step bound,
-- fold induction. Proof developments importing frozen declarations only.

/-- Energy distributes over append. -/
theorem bnd_energy_append : ∀ (l1 l2 : Ledger),
    energy (l1 ++ l2) = energy l1 + energy l2
  | [], _ => by simp [energy]
  | c :: cs, l2 => by
    cases c.ctype <;> simp [energy, List.cons_append, bnd_energy_append cs l2,
      Nat.add_assoc, Nat.add_comm, Nat.add_left_comm]

/-- Mapped LATENT credits carry unit energy each. -/
theorem bnd_energy_map_latent : ∀ (ss : List BoundarySup),
    energy (ss.map fun s => ({ ctype := .LATENT, sup := s } : Credit)) = ss.length := by
  intro ss
  induction ss with
  | nil => rfl
  | cons _ _ ih => simp [energy, ih, Nat.add_comm]

/-- T5 activation preserves ledger energy (ledger-level induction). -/
theorem bnd_act_energy : ∀ (L : Ledger),
    match activateFirst L with
    | none => True
    | some L' => energy L' = energy L
  | [] => by simp [activateFirst]
  | c :: cs => by
    by_cases hc : (c.ctype == .LATENT) = true
    · have heq : c.ctype = .LATENT := of_decide_eq_true hc
      simp only [activateFirst, hc]
      simp [energy, heq]
    · simp only [activateFirst, hc]
      cases h0 : activateFirst cs with
      | none => dsimp only; trivial
      | some rest =>
        dsimp only
        have ih := bnd_act_energy cs
        simp only [h0] at ih
        cases hct : c.ctype <;> simp [energy, ih]

/-- T5 activation preserves ledger energy (engine form). -/
theorem bnd_T5_energy : ∀ (L : Ledger) (m : Mode),
    energy (T5activate { ledger := L, cursor := 0 } m).ledger = energy L := by
  intro L m
  have hT5 : ∀ (E1 : Engine) (mm : Mode),
      (T5activate E1 mm).ledger = (match activateFirst E1.ledger with
        | none => E1
        | some ledger => { ledger := ledger, cursor := E1.cursor }).ledger := by
    intro E1 mm
    cases mm <;> rfl
  rw [hT5]
  cases h0 : activateFirst L with
  | none => simp
  | some L' =>
    have ih := bnd_act_energy L
    simp only [h0] at ih
    exact ih

/-- filterMap never lengthens a list. -/
theorem bnd_filterMap_length_le : ∀ (l : List α) (f : α → Option β),
    (l.filterMap f).length ≤ l.length
  | [], _ => Nat.le_refl _
  | _ :: xs, f => by
    simp only [List.filterMap]
    split
    · exact Nat.le_trans (bnd_filterMap_length_le xs f) (Nat.le_succ _)
    · exact Nat.succ_le_succ (bnd_filterMap_length_le xs f)

/-- T7 injection grows energy by at most k (all injected credits LATENT). -/
theorem bnd_T7_energy (E : Engine) (isA : Bool) (lo hi x nkeys k : Nat) :
    energy (T7inject E isA lo hi x nkeys k).ledger ≤ energy E.ledger + k := by
  unfold T7inject
  split
  · exact Nat.le_add_right _ _
  · next =>
    by_cases h : sites lo hi x nkeys = []
    · simp only [h]
      exact Nat.le_add_right _ _
    · obtain ⟨s0, ss, hss⟩ := List.exists_cons_of_ne_nil h
      rw [hss]
      dsimp only
      have hlen : (List.filterMap (fun j => (s0 :: ss)[(E.cursor + j) % (s0 :: ss).length]?) (List.range k)).length ≤ k := by
        have h1 := bnd_filterMap_length_le (List.range k) (fun j => (s0 :: ss)[(E.cursor + j) % (s0 :: ss).length]?)
        rw [List.length_range] at h1
        exact h1
      have hmap := bnd_energy_map_latent (List.filterMap (fun j => (s0 :: ss)[(E.cursor + j) % (s0 :: ss).length]?) (List.range k))
      have happ := bnd_energy_append E.ledger (List.map (fun s => ({ ctype := .LATENT, sup := s } : Credit)) (List.filterMap (fun j => (s0 :: ss)[(E.cursor + j) % (s0 :: ss).length]?) (List.range k)))
      omega

/-- Per-step energy growth ≤ 6. -/
theorem bnd_step_le (E : Engine) (isA : Bool) (m : Mode) (ev : StepEv)
    (x nkeys : Nat) :
    energy (replayStep E isA m ev x nkeys).ledger ≤ energy E.ledger + 6 := by
  unfold replayStep
  have hgen : ∀ (E1 : Engine) (mm : Mode),
      energy (T5activate E1 mm).ledger = energy E1.ledger := by
    intro E1 mm
    have hT5 : (T5activate E1 mm).ledger = (match activateFirst E1.ledger with
        | none => E1
        | some ledger => { ledger := ledger, cursor := E1.cursor }).ledger := by
      cases mm <;> rfl
    rw [hT5]
    cases h0 : activateFirst E1.ledger with
    | none => dsimp only
    | some L' =>
      dsimp only
      have ih := bnd_act_energy E1.ledger
      simp only [h0] at ih
      exact ih
  rw [hgen]
  have h7 := bnd_T7_energy E isA ev.lo ev.hi x nkeys K_frozen
  unfold K_frozen at h7
  exact h7

/-- Fold induction: whole-access growth ≤ 6 times event count. -/
theorem bnd_fold : ∀ (evs : List StepEv) (E : Engine) (isA : Bool) (m : Mode)
    (x nkeys : Nat),
    energy (evs.foldl (fun E ev => replayStep E isA m ev x nkeys) E).ledger
      ≤ energy E.ledger + 6 * evs.length
  | [], _, _, _, _, _ => by simp
  | ev :: evs, E, isA, m, x, nkeys => by
    simp only [List.foldl_cons, List.length_cons]
    have hstep := bnd_step_le E isA m ev x nkeys
    have ih := bnd_fold evs (replayStep E isA m ev x nkeys) isA m x nkeys
    omega

/-- MST0-09: raw boundary cost-bearing-source law. -/
theorem MST0_09_proved : MST0_09 := by
  refine ⟨6, fun A x nkeys E => ?_⟩
  unfold replayAccessA
  dsimp only
  exact bnd_fold (splayTrace A x).2 E true .KEEP x nkeys
