import Frozen.Statements
import Proofs.Boundary
-- Proofs/Injection.lean: MST0-13 bounded DELETE injection (WP-2 PROVE track).
-- Growth half reuses the proved Boundary fold bound (dependency-hashed
-- composition, acyclic); cost-link half (trace events ≤ splay cost) proved
-- natively here. Proof developments importing frozen declarations, never
-- modifying them.

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
  exact bnd_fold _ _ _ _ _ _

/-- MST0-13: bounded DELETE injection, E_after − E_before ≤ 6·cost_A(D). -/
theorem MST0_13_proved : MST0_13 := by
  intro E A x nkeys
  show energy (replayAccessA E A .DELETE x nkeys).1.ledger
    ≤ energy E.ledger + 6 * (replayAccessA E A .DELETE x nkeys).2.snd
  have hgrow := inj_access_growth E A .DELETE x nkeys
  have hcost := inj_trace_le_cost A x
  have hcost2 : (replayAccessA E A .DELETE x nkeys).2.snd = splayCost A x := rfl
  omega
