"""proof_attack/k6_saturation.py (STUB) — exact deterministic implementation; see WorkPlan Phase 3.

Payment-semantics binding (MAJOR fix, WorkPlan v0.4-WP2): the evaluator MUST call
`paid = imported_MSTC0002_payment(keep_event, ledger_state)` owned by the
hash-bound survivor record (`V03_MSTC_0002.json`), with `required = max(w, 0)`
for `w = y - 2a`. The plan-invented `paid = min(pool, w)` formula is FORBIDDEN
unless survivor binding proves that reduction for `w > 0` and records it as a
binding lemma. No theorem-facing execution before FOUNDATION_FROZEN."""
