import Frozen.Statements
-- Proofs/Constants.lean: MST0-22 uniformity law (WP-2 PROVE track).
-- Proof developments importing frozen declarations, never modifying them.

/-- filterMap never lengthens a list. -/
theorem filterMap_length_le : ∀ (l : List α) (f : α → Option β),
    (l.filterMap f).length ≤ l.length
  | [], _ => Nat.le_refl _
  | _ :: xs, f => by
    simp only [List.filterMap]
    split
    · exact Nat.le_trans (filterMap_length_le xs f) (Nat.le_succ _)
    · exact Nat.succ_le_succ (filterMap_length_le xs f)

/-- T7 injection grows the ledger by at most k credits. -/
theorem T7inject_length_le (E : Engine) (isA : Bool) (lo hi x nkeys k : Nat) :
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
        filterMap_length_le _ _
      rw [List.length_range] at h1
      exact Nat.add_le_add_left h1 _

/-- MST0-22: literals by definition, C-linkage by unfolding, K-uniformity by
    the injection bound with k ≤ K_frozen. -/
theorem MST0_22_proved : MST0_22 := by
  refine ⟨⟨rfl, rfl⟩, fun y a => rfl, fun E isA lo hi x nkeys k hk => ?_⟩
  calc (T7inject E isA lo hi x nkeys k).ledger.length
      ≤ E.ledger.length + k := T7inject_length_le E isA lo hi x nkeys k
    _ ≤ E.ledger.length + K_frozen := Nat.add_le_add_left hk _
