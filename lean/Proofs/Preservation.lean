import Frozen.Statements
-- Proofs/Preservation.lean: MST0-11 six-clause rotation-case law (WP-2 PROVE track).
-- T7-facts + T5-facts proved separately, then composed (mirrors Layer-A).
-- Proof developments importing frozen declarations, never modifying them.

/-- Energy distributes over append. -/
theorem pres_energy_append : ∀ (l1 l2 : Ledger),
    energy (l1 ++ l2) = energy l1 + energy l2
  | [], _ => by simp [energy]
  | c :: cs, l2 => by
    cases c.ctype <;> simp only [energy, List.cons_append, pres_energy_append cs l2,
      Nat.add_assoc, Nat.add_comm, Nat.add_left_comm]

/-- A mapped LATENT-only list carries unit energy per credit. -/
theorem pres_energy_map_latent : ∀ (ss : List BoundarySup),
    energy (ss.map fun s => ({ ctype := .LATENT, sup := s } : Credit)) = ss.length := by
  intro ss
  induction ss with
  | nil => rfl
  | cons _ _ ih => simp [energy, ih, Nat.add_comm]

/-- BEq-true on credit types gives propositional equality. -/
theorem pres_beq_true {c : Credit} {t : CreditType} (h : (c.ctype == t) = true) :
    c.ctype = t :=
  of_decide_eq_true h

/-- Membership in a cons cell, either way. -/
theorem pres_mem_cons {a b : Credit} {l : Ledger} (h : a = b ∨ a ∈ l) : a ∈ b :: l :=
  List.mem_cons.mpr h

/-- activateFirst touches at most one position (the first LATENT), in place. -/
theorem pres_act_single : ∀ (L : Ledger),
    match activateFirst L with
    | none => True
    | some L' => L'.length = L.length ∧
        ∀ i : Nat, L'[i]? = L[i]? ∨
          ∃ c : Credit, L[i]? = some c ∧ c.ctype = .LATENT ∧
            L'[i]? = some { ctype := .ACTIVE, sup := c.sup }
  | [] => by simp [activateFirst]
  | c :: cs => by
    by_cases hc : (c.ctype == .LATENT) = true
    · have heq : c.ctype = .LATENT := of_decide_eq_true hc
      simp only [activateFirst, hc]
      refine ⟨by simp, fun i => ?_⟩
      cases i with
      | zero =>
        right
        exact ⟨c, rfl, heq, rfl⟩
      | succ j =>
        left
        rfl
    · simp only [activateFirst, hc]
      cases h0 : activateFirst cs with
      | none => dsimp only; trivial
      | some rest =>
        dsimp only
        have ih := pres_act_single cs
        simp only [h0] at ih
        obtain ⟨hlen, hsingle⟩ := ih
        refine ⟨by simp [hlen], fun i => ?_⟩
        cases i with
        | zero => exact Or.inl rfl
        | succ j =>
          simp only [List.getElem?_cons_succ] at ⊢
          have := hsingle j
          simp only [List.getElem?_cons_succ] at this ⊢
          cases this with
          | inl h => exact Or.inl h
          | inr h =>
            obtain ⟨c0, hc0, hc0l, hc0f⟩ := h
            exact Or.inr ⟨c0, hc0, hc0l, hc0f⟩

/-- Every site support lies in the interval with matching orientation. -/
theorem pres_site_ok : ∀ (lo hi x nkeys : Nat) (s : BoundarySup),
    s ∈ sites lo hi x nkeys →
    lo ≤ s.lo ∧ s.hi ≤ hi ∧
    ((s.leftOriented = true → s.hi ≤ x) ∧ (s.leftOriented = false → x < s.hi)) := by
  intro lo hi x nkeys s hs
  unfold sites at hs
  rw [List.mem_filterMap] at hs
  obtain ⟨i, himem, hsome⟩ := hs
  simp only [List.mem_range'] at himem
  obtain ⟨j, hjlt, rfl⟩ := himem
  split at hsome
  · next hcond =>
    have hc := of_decide_eq_true hcond
    obtain ⟨h1, h2, h3⟩ := hc
    cases hsome
    dsimp only
    refine ⟨by omega, by omega, ?_, ?_⟩
    · intro ho
      have hx := of_decide_eq_true ho
      omega
    · intro ho
      have hx : ¬ (lo + 1 * j + 1 ≤ x) := of_decide_eq_false ho
      omega
  · next hcond =>
    cases hsome

/-- T7 output shape: old prefix plus mapped picks drawn from sites. -/
theorem pres_T7_shape (E : Engine) (isA : Bool) (lo hi x nkeys k : Nat) :
    ∃ picks : List BoundarySup, (∀ s ∈ picks, s ∈ sites lo hi x nkeys)
      ∧ (T7inject E isA lo hi x nkeys k).ledger
        = E.ledger ++ picks.map (fun s => ({ ctype := .LATENT, sup := s } : Credit)) := by
  unfold T7inject
  split
  · exact ⟨[], by simp, by simp⟩
  · next =>
    by_cases h : sites lo hi x nkeys = []
    · simp only [h]
      exact ⟨[], by simp, by simp⟩
    · obtain ⟨s0, ss, hss⟩ := List.exists_cons_of_ne_nil h
      rw [hss]
      refine ⟨_, fun y hy => ?_, rfl⟩
      rw [List.mem_filterMap] at hy
      obtain ⟨j, _, hj⟩ := hy
      exact List.mem_of_getElem? hj

/-- activateFirst flips at most the first LATENT, preserving length, energy,
    SPENT-membership, and ACTIVE-provenance. -/
theorem pres_act_spec : ∀ (L : Ledger),
    match activateFirst L with
    | none => ∀ c ∈ L, c.ctype ≠ .LATENT
    | some L' => L'.length = L.length ∧ energy L' = energy L ∧
        (∀ c ∈ L', c.ctype = .SPENT → c ∈ L) ∧
        (∀ c ∈ L', c.ctype = .ACTIVE → c ∈ L ∨ ∃ c0 ∈ L, c0.ctype = .LATENT ∧ c.sup = c0.sup)
  | [] => by simp [activateFirst]
  | c :: cs => by
    simp only [activateFirst]
    by_cases hc : (c.ctype == .LATENT) = true
    · simp only [hc]
      have heq : c.ctype = .LATENT := pres_beq_true hc
      refine ⟨by simp, by simp [energy, heq], fun d hd hsp => ?_, fun d hd hac => ?_⟩
      · simp only [List.mem_cons] at hd
        cases hd with
        | inl hdd =>
          rw [hdd] at hsp
          simp at hsp
        | inr hdd => exact pres_mem_cons (Or.inr hdd)
      · simp only [List.mem_cons] at hd
        cases hd with
        | inl hdd =>
          right
          exact ⟨c, pres_mem_cons (Or.inl rfl), heq, by rw [hdd]⟩
        | inr hdd => exact Or.inl (pres_mem_cons (Or.inr hdd))
    · simp only [hc]
      have hne : c.ctype ≠ .LATENT := fun hcon => hc (by simp [hcon])
      cases hcs : activateFirst cs with
      | none =>
        have ih := (pres_act_spec cs)
        simp only [hcs] at ih
        intro d hd
        simp only [List.mem_cons] at hd
        cases hd with
        | inl hdd => rw [hdd]; exact hne
        | inr hdd => exact ih d hdd
      | some cs' =>
        have ih := (pres_act_spec cs)
        simp only [hcs] at ih
        obtain ⟨hlen, henergy, hspent, hact⟩ := ih
        refine ⟨by simp [hlen], by simp [energy, henergy], fun d hd hsp => ?_, fun d hd hac => ?_⟩
        · simp only [List.mem_cons] at hd
          cases hd with
          | inl hdd => rw [hdd]; exact pres_mem_cons (Or.inl rfl)
          | inr hdd => exact pres_mem_cons (Or.inr (hspent d hdd hsp))
        · simp only [List.mem_cons] at hd
          cases hd with
          | inl hdd => exact Or.inl (pres_mem_cons (Or.inl hdd))
          | inr hdd =>
            have h2 := hact d hdd hac
            cases h2 with
            | inl hdd2 => exact Or.inl (pres_mem_cons (Or.inr hdd2))
            | inr hdd2 =>
              obtain ⟨c0, hc0mem, hc0lat, hsup⟩ := hdd2
              exact Or.inr ⟨c0, pres_mem_cons (Or.inr hc0mem), hc0lat, hsup⟩

/-- P_all fires on both modes. -/
theorem pres_P_all : ∀ m : Mode, P_all m = true
  | .KEEP => rfl
  | .DELETE => rfl

/-- T5activate acts on the ledger only through activateFirst (engine-match form). -/
theorem pres_T5_ledger (E1 : Engine) (m : Mode) :
    (T5activate E1 m).ledger = (match activateFirst E1.ledger with
      | none => E1
      | some ledger => { ledger := ledger, cursor := E1.cursor }).ledger := by
  cases m <;> rfl

/-- C1 (flow identity) as a standalone lemma: T5 preserves energy, T7's
    growth is exactly the injected count. The full six-clause conjunction
    (MST0_11) remains open: C2/C4/C6 need positional drop-facts beyond the
    membership-level T5 characterization above. -/
theorem MST0_11_flow_identity : ∀ (E : Engine) (isA : Bool) (m : Mode)
    (ev : StepEv) (x nkeys : Nat),
    let E1 := T7inject E isA ev.lo ev.hi x nkeys K_frozen;
    let E2 := T5activate E1 m;
    energy E2.ledger = energy E.ledger + (E1.ledger.length - E.ledger.length) := by
  intro E isA m ev x nkeys
  dsimp only
  obtain ⟨picks, _, hpeq⟩ :=
    pres_T7_shape E isA ev.lo ev.hi x nkeys K_frozen
  have hmap : energy (picks.map (fun s => ({ ctype := .LATENT, sup := s } : Credit)))
      = picks.length := pres_energy_map_latent picks
  have hE1 : (T7inject E isA ev.lo ev.hi x nkeys K_frozen).ledger
      = E.ledger ++ picks.map (fun s => ({ ctype := .LATENT, sup := s } : Credit)) := hpeq
  have hlen : ((E.ledger ++ picks.map
      (fun s => ({ ctype := .LATENT, sup := s } : Credit))).length - E.ledger.length)
      = picks.length := by
    rw [List.length_append, List.length_map]
    exact Nat.add_sub_cancel_left _ _
  have henergy : energy (E.ledger ++ picks.map
      (fun s => ({ ctype := .LATENT, sup := s } : Credit)))
      = energy E.ledger + picks.length := by
    rw [pres_energy_append, hmap]
  rw [pres_T5_ledger, hE1]
  cases h0 : activateFirst
      (E.ledger ++ picks.map (fun s => ({ ctype := .LATENT, sup := s } : Credit))) with
  | none =>
    dsimp only
    rw [hE1]
    rw [hlen]
    exact henergy
  | some L' =>
    dsimp only
    have hact := pres_act_spec
      (E.ledger ++ picks.map (fun s => ({ ctype := .LATENT, sup := s } : Credit)))
    rw [h0] at hact
    obtain ⟨_, henergy', _, _⟩ := hact
    rw [hlen, henergy', henergy]


/-- MST0-11: six-clause rotation-case law, composed from T7-shape, site
    bounds, single-flip positions, and drop equations. -/
theorem MST0_11_proved : MST0_11 := by
  intro E isA m ev x nkeys
  dsimp only
  obtain ⟨picks, hpmem, hpeq⟩ :=
    pres_T7_shape E isA ev.lo ev.hi x nkeys K_frozen
  have hsup : ∀ s ∈ picks, ev.lo ≤ s.lo ∧ s.hi ≤ ev.hi
      ∧ ((s.leftOriented = true → s.hi ≤ x) ∧ (s.leftOriented = false → x < s.hi)) :=
    fun s hs => pres_site_ok ev.lo ev.hi x nkeys s (hpmem s hs)
  have hE1 : (T7inject E isA ev.lo ev.hi x nkeys K_frozen).ledger
      = E.ledger ++ picks.map (fun s => ({ ctype := .LATENT, sup := s } : Credit)) := hpeq
  have hlen : ((E.ledger ++ picks.map
      (fun s => ({ ctype := .LATENT, sup := s } : Credit))).length - E.ledger.length)
      = picks.length := by
    rw [List.length_append, List.length_map]
    exact Nat.add_sub_cancel_left _ _
  have henergy : energy (E.ledger ++ picks.map
      (fun s => ({ ctype := .LATENT, sup := s } : Credit)))
      = energy E.ledger + picks.length := by
    rw [pres_energy_append, pres_energy_map_latent picks]
  have hdropP : ∀ c : Credit,
      c ∈ (E.ledger ++ picks.map
        (fun s => ({ ctype := .LATENT, sup := s } : Credit))).drop E.ledger.length →
      (c.ctype = .LATENT ∨ c.ctype = .ACTIVE)
      ∧ (∃ s ∈ picks, c.sup = s) := by
    intro c hc
    rw [List.drop_left] at hc
    simp only [List.mem_map] at hc
    obtain ⟨s, hs, rfl⟩ := hc
    exact ⟨Or.inl rfl, s, hs, rfl⟩
  rw [pres_T5_ledger, hE1]
  cases h0 : activateFirst
      (E.ledger ++ picks.map (fun s => ({ ctype := .LATENT, sup := s } : Credit))) with
  | none =>
    dsimp only
    rw [hE1]
    refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
    · rw [hlen]; exact henergy
    · intro c hc
      exact (hdropP c hc).1
    · intro c hc hsp
      simp only [List.mem_append] at hc
      cases hc with
      | inl h => exact h
      | inr h =>
        simp only [List.mem_map] at h
        obtain ⟨s, _, heq⟩ := h
        rw [←heq] at hsp
        simp at hsp
    · intro c hc
      obtain ⟨_, hex⟩ := hdropP c hc
      obtain ⟨s, hs, hseq⟩ := hex
      rw [hseq]
      exact ⟨(hsup s hs).1, ((hsup s hs).2).1⟩
    · intro c hc hac
      exact Or.inl hc
    · intro c hc
      obtain ⟨_, hex⟩ := hdropP c hc
      obtain ⟨s, hs, hseq⟩ := hex
      rw [hseq]
      exact ((hsup s hs).2).2
  | some L' =>
    dsimp only
    have hsingle := pres_act_single
      (E.ledger ++ picks.map (fun s => ({ ctype := .LATENT, sup := s } : Credit)))
    simp only [h0] at hsingle
    obtain ⟨_, hpoint⟩ := hsingle
    have hact := pres_act_spec
      (E.ledger ++ picks.map (fun s => ({ ctype := .LATENT, sup := s } : Credit)))
    simp only [h0] at hact
    obtain ⟨_, _, hspentS, hactS⟩ := hact
    have hdropS : ∀ c : Credit, c ∈ L'.drop E.ledger.length →
        (c.ctype = .LATENT ∨ c.ctype = .ACTIVE)
        ∧ (∃ s ∈ picks, c.sup = s) := by
      intro c hc
      rw [List.mem_iff_getElem?] at hc
      obtain ⟨j, hj⟩ := hc
      rw [List.getElem?_drop] at hj
      have hpt := hpoint (E.ledger.length + j)
      cases hpt with
      | inl heq =>
        rw [heq] at hj
        have hge : E.ledger.length ≤ E.ledger.length + j := Nat.le_add_right _ _
        have happ := List.getElem?_append_right (l₁ := E.ledger)
          (l₂ := picks.map (fun s => ({ ctype := .LATENT, sup := s } : Credit)))
          (i := E.ledger.length + j) hge
        rw [happ] at hj
        have hmem : c ∈ picks.map (fun s => ({ ctype := .LATENT, sup := s } : Credit)) :=
          List.mem_iff_getElem?.mpr ⟨_, hj⟩
        simp only [List.mem_map] at hmem
        obtain ⟨s, hs, rfl⟩ := hmem
        exact ⟨Or.inl rfl, s, hs, rfl⟩
      | inr hfl =>
        obtain ⟨c0, hc0eq, hc0l, hc0f⟩ := hfl
        have hceq : c = ({ ctype := .ACTIVE, sup := c0.sup } : Credit) :=
          Option.some_inj.mp (hj.symm.trans hc0f)
        have hge : E.ledger.length ≤ E.ledger.length + j := Nat.le_add_right _ _
        have happ := List.getElem?_append_right (l₁ := E.ledger)
          (l₂ := picks.map (fun s => ({ ctype := .LATENT, sup := s } : Credit)))
          (i := E.ledger.length + j) hge
        rw [happ] at hc0eq
        have hc0mem : c0 ∈ picks.map (fun s => ({ ctype := .LATENT, sup := s } : Credit)) :=
          List.mem_iff_getElem?.mpr ⟨_, hc0eq⟩
        simp only [List.mem_map] at hc0mem
        obtain ⟨s, hs, rfl⟩ := hc0mem
        have hseq2 : c.sup = s := by simp [hceq]
        exact ⟨Or.inr (by simp [hceq]), s, hs, hseq2⟩
    refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
    · rw [hlen]
      have henergyS : energy L' = energy (E.ledger ++ picks.map (fun s => ({ ctype := .LATENT, sup := s } : Credit))) := by
        have h2 := pres_act_spec (E.ledger ++ picks.map (fun s => ({ ctype := .LATENT, sup := s } : Credit)))
        simp only [h0] at h2
        obtain ⟨_, he, _, _⟩ := h2
        exact he
      rw [henergyS, henergy]
    · intro c hc
      exact (hdropS c hc).1
    · intro c hc hsp
      have h2 := hspentS c hc hsp
      simp only [List.mem_append] at h2
      cases h2 with
      | inl h => exact h
      | inr h =>
        simp only [List.mem_map] at h
        obtain ⟨s, _, heq⟩ := h
        rw [←heq] at hsp
        simp at hsp
    · intro c hc
      obtain ⟨_, hex⟩ := hdropS c hc
      obtain ⟨s, hs, hseq⟩ := hex
      rw [hseq]
      exact ⟨(hsup s hs).1, ((hsup s hs).2).1⟩
    · intro c hc hac
      have h2 := hactS c hc hac
      cases h2 with
      | inl h => exact Or.inl h
      | inr h => exact Or.inr h
    · intro c hc
      obtain ⟨_, hex⟩ := hdropS c hc
      obtain ⟨s, hs, hseq⟩ := hex
      rw [hseq]
      exact ((hsup s hs).2).2
