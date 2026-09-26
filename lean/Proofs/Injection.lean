import Frozen.Statements
-- Proofs/Injection.lean: MST0-13 bounded DELETE injection (WP-2 PROVE track).
-- Standalone: no inter-Proofs imports (no consumption before REVIEWED). The
-- per-step/fold energy-growth lemmas are proved locally here; the cost-link
-- half (trace events ≤ splay cost) is native. Proof developments importing
-- frozen declarations, never modifying them.

/-- Energy distributes over append. -/
theorem inj_energy_append : ∀ (l1 l2 : Ledger),
    energy (l1 ++ l2) = energy l1 + energy l2
  | [], _ => by simp [energy]
  | c :: cs, l2 => by
    cases c.ctype <;> simp [energy, List.cons_append, inj_energy_append cs l2,
      Nat.add_assoc, Nat.add_comm, Nat.add_left_comm]

/-- Mapped LATENT credits carry unit energy each. -/
theorem inj_energy_map_latent : ∀ (ss : List BoundarySup),
    energy (ss.map fun s => ({ ctype := .LATENT, sup := s } : Credit)) = ss.length
  | [] => rfl
  | _ :: ss => by
    simp only [List.map_cons, energy, List.length_cons]
    rw [inj_energy_map_latent ss]
    omega

/-- filterMap never lengthens a list. -/
theorem inj_filterMap_length_le : ∀ (l : List α) (f : α → Option β),
    (l.filterMap f).length ≤ l.length
  | [], _ => Nat.le_refl _
  | _ :: xs, f => by
    simp only [List.filterMap]
    split
    · exact Nat.le_trans (inj_filterMap_length_le xs f) (Nat.le_succ _)
    · exact Nat.succ_le_succ (inj_filterMap_length_le xs f)

/-- T5 activation preserves ledger energy (ledger-level induction). -/
theorem inj_act_energy : ∀ (L : Ledger),
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
        have ih := inj_act_energy cs
        simp only [h0] at ih
        cases hct : c.ctype <;> simp [energy, ih]

/-- T7 injection grows energy by at most k (all injected credits LATENT). -/
theorem inj_T7_energy (E : Engine) (isA : Bool) (lo hi x nkeys k : Nat) :
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
        have h1 := inj_filterMap_length_le (List.range k) (fun j => (s0 :: ss)[(E.cursor + j) % (s0 :: ss).length]?)
        rw [List.length_range] at h1
        exact h1
      have hmap := inj_energy_map_latent (List.filterMap (fun j => (s0 :: ss)[(E.cursor + j) % (s0 :: ss).length]?) (List.range k))
      have happ := inj_energy_append E.ledger (List.map (fun s => ({ ctype := .LATENT, sup := s } : Credit)) (List.filterMap (fun j => (s0 :: ss)[(E.cursor + j) % (s0 :: ss).length]?) (List.range k)))
      omega

/-- Per-step energy growth ≤ 6. -/
theorem inj_step_le (E : Engine) (isA : Bool) (m : Mode) (ev : StepEv)
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
      have ih := inj_act_energy E1.ledger
      simp only [h0] at ih
      exact ih
  rw [hgen]
  have h7 := inj_T7_energy E isA ev.lo ev.hi x nkeys K_frozen
  unfold K_frozen at h7
  exact h7

/-- Fold induction: whole-access growth ≤ 6 times event count. -/
theorem inj_fold : ∀ (evs : List StepEv) (E : Engine) (isA : Bool) (m : Mode)
    (x nkeys : Nat),
    energy (evs.foldl (fun E ev => replayStep E isA m ev x nkeys) E).ledger
      ≤ energy E.ledger + 6 * evs.length
  | [], _, _, _, _, _ => by simp
  | ev :: evs, E, isA, m, x, nkeys => by
    simp only [List.foldl_cons, List.length_cons]
    have hstep := inj_step_le E isA m ev x nkeys
    have ih := inj_fold evs (replayStep E isA m ev x nkeys) isA m x nkeys
    omega

/-- Ancestor-frame count (proof-local; T7/T5 ledgers never see it). -/
def injCtxLen : Ctx → Nat
  | .top => 0
  | .leftOf _ _ o => injCtxLen o + 1
  | .rightOf _ _ o => injCtxLen o + 1

/-- Descend builds exactly depth-many frames atop the accumulator. -/
theorem inj_descend_len : ∀ (T : BST) (x : Nat) (acc : Ctx) (sub : BST) (ctx : Ctx),
    descendAcc T x acc = some (sub, ctx) →
    injCtxLen ctx = injCtxLen acc + BST.depth T x
  | .leaf, _, _, _, _, h => by simp [descendAcc] at h
  | .node k l r, x, acc, sub, ctx, h => by
    simp only [descendAcc] at h
    by_cases hx : x = k
    · simp only [hx] at h
      obtain ⟨rfl, rfl⟩ := Option.some_inj.mp h
      simp [BST.depth, hx]
    · simp only [hx] at h
      by_cases hlt : x < k
      · simp only [hlt] at h
        have ih := inj_descend_len l x (Ctx.leftOf k r acc) sub ctx h
        simp [injCtxLen, BST.depth, hx, hlt] at ih ⊢
        omega
      · simp only [hlt] at h
        have ih := inj_descend_len r x (Ctx.rightOf k l acc) sub ctx h
        simp [injCtxLen, BST.depth, hx, hlt] at ih ⊢
        omega

/-- One loop iteration: either the trace is done, or it recurses with
    strictly fewer frames and exactly one more event. -/
theorem inj_step : ∀ (n : BST) (ctx : Ctx) (evs : List StepEv),
    (splayWithT n ctx evs).2 = evs ∨
    (∃ (n' : BST) (ctx' : Ctx) (ev : StepEv),
      injCtxLen ctx' < injCtxLen ctx ∧
      (splayWithT n ctx evs).2 = (splayWithT n' ctx' (evs ++ [ev])).2) := by
  intro n ctx evs
  cases ctx with
  | top => exact Or.inl rfl
  | leftOf kp q outer =>
    cases outer with
    | top =>
      cases n with
      | leaf => exact Or.inl rfl
      | node x t1 t2 =>
        refine Or.inr ⟨_, _, _, ?_, rfl⟩
        simp only [injCtxLen]
        omega
    | leftOf kg c outer' =>
      cases n with
      | leaf => exact Or.inl rfl
      | node x t1 t2 =>
        refine Or.inr ⟨_, _, _, ?_, rfl⟩
        simp only [injCtxLen]
        omega
    | rightOf kg a outer' =>
      cases n with
      | leaf => exact Or.inl rfl
      | node x t1 t2 =>
        refine Or.inr ⟨_, _, _, ?_, rfl⟩
        simp only [injCtxLen]
        omega
  | rightOf kp q outer =>
    cases outer with
    | top =>
      cases n with
      | leaf => exact Or.inl rfl
      | node x t1 t2 =>
        refine Or.inr ⟨_, _, _, ?_, rfl⟩
        simp only [injCtxLen]
        omega
    | leftOf kg d outer' =>
      cases n with
      | leaf => exact Or.inl rfl
      | node x t1 t2 =>
        refine Or.inr ⟨_, _, _, ?_, rfl⟩
        simp only [injCtxLen]
        omega
    | rightOf kg c outer' =>
      cases n with
      | leaf => exact Or.inl rfl
      | node x t1 t2 =>
        refine Or.inr ⟨_, _, _, ?_, rfl⟩
        simp only [injCtxLen]
        omega

/-- Loop bound by fuel induction over the step lemma. -/
theorem inj_loop_len : ∀ (f : Nat) (n : BST) (ctx : Ctx) (evs : List StepEv),
    injCtxLen ctx ≤ f →
    (splayWithT n ctx evs).2.length ≤ evs.length + injCtxLen ctx
  | 0, n, ctx, evs => by
    intro h
    cases ctx with
    | top => exact Nat.le_add_right _ _
    | leftOf _ _ _ => simp [injCtxLen] at h
    | rightOf _ _ _ => simp [injCtxLen] at h
  | f + 1, n, ctx, evs => by
    intro h
    have hs := inj_step n ctx evs
    cases hs with
    | inl heq =>
      rw [heq]
      exact Nat.le_add_right _ _
    | inr hex =>
      obtain ⟨n', ctx', ev, hlt, heq⟩ := hex
      rw [heq]
      have ih := inj_loop_len f n' ctx' (evs ++ [ev]) (by omega)
      have hlen : (evs ++ [ev]).length = evs.length + 1 := by simp
      omega

/-- Trace length never exceeds splay cost (depth+1). -/
theorem inj_trace_le_cost : ∀ (A : BST) (x : Nat),
    (splayTrace A x).2.length ≤ splayCost A x := by
  intro A x
  simp only [splayTrace, splayCost]
  cases h : BST.descend A x with
  | none =>
    simp
  | some pr =>
    obtain ⟨sub, ctx⟩ := pr
    dsimp only
    have hloop := inj_loop_len (injCtxLen ctx) sub ctx [] (Nat.le_refl _)
    simp only [List.length_nil, Nat.add_zero] at hloop
    have hdesc : injCtxLen ctx = BST.depth A x := by
      have hacc : descendAcc A x .top = some (sub, ctx) := by
        simp only [BST.descend] at h
        exact h
      have hlen := inj_descend_len A x .top sub ctx hacc
      simpa [injCtxLen] using hlen
    omega

/-- Per-access growth from the Boundary fold bound (mode-polymorphic reuse). -/
theorem inj_access_growth : ∀ (E : Engine) (A : BST) (m : Mode) (x nkeys : Nat),
    energy (replayAccessA E A m x nkeys).1.ledger
      ≤ energy E.ledger + 6 * (splayTrace A x).2.length := by
  intro E A m x nkeys
  unfold replayAccessA
  dsimp only
  exact inj_fold _ _ _ _ _ _

/-- MST0-13: bounded DELETE injection, E_after − E_before ≤ 6·cost_A(D). -/
theorem MST0_13_proved : MST0_13 := by
  intro E A x nkeys
  show energy (replayAccessA E A .DELETE x nkeys).1.ledger
    ≤ energy E.ledger + 6 * (replayAccessA E A .DELETE x nkeys).2.snd
  have hgrow := inj_access_growth E A .DELETE x nkeys
  have hcost := inj_trace_le_cost A x
  have hcost2 : (replayAccessA E A .DELETE x nkeys).2.snd = splayCost A x := rfl
  omega
