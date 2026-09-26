# MST0-14 — Layer-A proof skeleton: universal synchronous KEEP repayment (WP-3 PROVE track)

Status: PROOF IN PROGRESS (mechanism lemma proved in Lean; sufficiency argument
below is a genuine amortized skeleton with one explicit open obligation — NOT a
complete proof; truth stays UNPROVED per lifecycle). Frozen statement:
`math/theorem_MST14_keep_repayment.md` (G11 identity).

## Definitions invoked (frozen only)

`discharge` (fold), `activePool`, `required`, `T7inject`, `T5activate`,
`replayAccessA/B`, `execHist`/`execSuffices`. No integrability premise
(STOP-44 respected: local repayment never consumes MST0-15).

## Mechanism lemma (PROVED in Lean: `MST0_14_paid_identity`)

`paid = min(activePool, required)` holds for every discharge by fold induction:
the fold consumes ACTIVE credits in order while demand remains, so exactly the
first `min(pool, need)` ACTIVEs become SPENT. Binding use: any `min(pool,w)`-form
reduction in the evaluator is this proved lemma, never an assumption.

## Sufficiency argument (open — the K6 war's mathematical content)

Claim: along paired executions from the empty ledger, every KEEP discharge
pays in full (`execSuffices = true`).
Established firmly:
1. Per-step inflow/outflow accounting: each A-rotation injects ≤ 6 LATENT and
   activates ≤ 1 (first LATENT; T7-then-T5 order guarantees supply); each
   B-rotation activates ≤ 1; each KEEP discharge consumes exactly
   min(pool, need) ACTIVE (mechanism lemma).
2. LATENT-supply invariant: injections (6/rotation) dominate activations
   (1/rotation), so activation never starves for lack of LATENT.
3. DELETE-prefunding: DELETE accesses inject+activate with no discharge, so
   DELETE bursts build the ACTIVE pool that later KEEPs draw on.
4. Finite evidence: K6 war over 13 dimensions × 7 sizes × 6 seeds × 5 trees
   (worst residual 0, independently agreed) — diagnostic, never proof.
OPEN OBLIGATION (explicit, not hidden): the paired-depths coupling lemma —
for every paired prefix, pool covers the next KEEP's positive regret. In
spreadsheet form: need_k > inflow_k is possible exactly when B is much deeper
than A at the accessed key (y_k > 2·a_k + inflow_k); covering those spikes
from the DELETE-prefunded pool for ALL legal paired histories is unproven.
Finite survival is not a theorem (LOC-07/STOP-30/31); this file claims no
more than the mechanism lemma plus the skeleton above.

## Scope notes

Matching Lean development: `lean/Proofs/Repayment.lean` (mechanism identity
green; sufficiency conjunct open, correctly absent). Attack evidence: K6 war
(NO_WITNESS all shards, checker AGREE). Review package PENDING-HUMAN.
