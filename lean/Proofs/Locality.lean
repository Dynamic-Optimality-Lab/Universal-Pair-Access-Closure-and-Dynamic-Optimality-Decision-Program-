import Frozen.Statements
-- Proofs/Locality.lean: MST0-08U universal reference locality (WP-2 PROVE track).
-- Proof developments importing frozen declarations, never modifying them.

/-- filterMap never lengthens a list. -/
theorem loc_filterMap_length_le : ∀ (l : List α) (f : α → Option β),
    (l.filterMap f).length ≤ l.length
  | [], _ => Nat.le_refl _
  | _ :: xs, f => by
    simp only [List.filterMap]
    split
    · exact Nat.le_trans (loc_filterMap_length_le xs f) (Nat.le_succ _)
    · exact Nat.succ_le_succ (loc_filterMap_length_le xs f)

/-- T7 injection grows the ledger by at most k credits. -/
theorem loc_T7inject_length_le (E : Engine) (isA : Bool) (lo hi x nkeys k : Nat) :
    (T7inject E isA lo hi x nkeys k).ledger.length ≤ E.ledger.length + k := by
  unfold T7inject
  split
  · exact Nat.le_add_right _ _
  · next =>
    by_cases h : sites lo hi x nkeys = []
    · simp only [h]
      exact Nat.le_add_right _ _
    · obtain ⟨s, ss, hss⟩ := List.exists_cons_of_ne_nil h
      rw [hss]
      dsimp only
      rw [List.length_append, List.length_map]
      have h1 : ((List.range k).filterMap fun j =>
          (s :: ss)[(E.cursor + j) % (s :: ss).length]?).length
          ≤ (List.range k).length :=
        loc_filterMap_length_le _ _
      rw [List.length_range] at h1
      exact Nat.add_le_add_left h1 _

/-- MST0-08U: one universal constant (6) bounds downstream-consumed
    modifications per A-side rotation event, uniformly over all inputs. -/
theorem MST0_08U_proved : MST0_08U :=
  ⟨6, fun _A x nkeys E ev _ =>
    calc (T7inject E true ev.lo ev.hi x nkeys K_frozen).ledger.length
        ≤ E.ledger.length + K_frozen :=
          loc_T7inject_length_le E true ev.lo ev.hi x nkeys K_frozen
      _ = E.ledger.length + 6 := rfl⟩
