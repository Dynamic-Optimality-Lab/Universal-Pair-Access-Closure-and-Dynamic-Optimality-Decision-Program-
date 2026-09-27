# MST0-14R — Layer-A refutation analysis: intended synchronous KEEP repayment is FALSE

Status: UNIVERSAL PROOF ABANDONED (exact legal refutation certified;
mathematical refutation recorded, lifecycle REFUTED pending G5 human
validation). Frozen identity `MST0-14` preserved; successor `MST0-14R`
defined in `math/theorem_MST14R_legal_repayment.md`. Ledger:
`math/proof_status_MST14R.json`. Witness:
`artifacts/v04/counterexamples/MST0-14R/MST0-14R_LEGAL_WITNESS.json`.

## 1. What was reused (valid inner mechanism)

`MST0_14_paid_identity` (`paid = min(pool, need)`, fold induction,
`lean/Proofs/Repayment.lean`, build-green history) is pure discharge algebra,
domain-independent, reused unchanged. The failure is pool insufficiency, never
the discharge operator. Frozen `C=2/k=6/P_all/T5/T6/T7/discharge/required/
replay/cost-convention` untouched.

## 2. Exact structural laws (validated, assert-level, finite scope stated)

All validated on 573,734 exhaustive legal instances (n<=4, all shapes, all
histories len<=5) plus engineered/divergence/burst campaigns to n=2048, with
per-step asserts inside `python/audit/ledger_trace.py` (zero assert failures):
- Trace count: `(splayTrace T x).2.length = ceil(depth/2)` on present-key
  vine probes (e.g. d=15 -> 8 events); A-phase assert `L+=5rA, P+=rA` held
  everywhere legal (every legal A-event injected exactly 6 LATENT with
  successful T5 activation; zero site-empty legal events observed).
- Ledger recurrence (empty start): `L = 5RA - ActB`, `P = RA + ActB - D`,
  `E = 6RA - D`, with `ActA = RA` exactly (A-activation never fails legally),
  `ActB = min(rB, L+5rA)` per KEEP (B-activation can starve).
- Pre-discharge pool identity: `P_pre = P + rA + ActB`. Sufficiency is
  exactly `P_pre >= need` (mechanism lemma). No approximation anywhere.

## 3. Failed proof routes (retained with minimal counterexamples; do not retry)

- **I2a `P >= maxneed` at boundaries.** FALSE in general. Held on 3.3M
  n<=4 states by small-state luck. First breaks: DELETE-burst states, e.g.
  n=8 seeded `H=[DEL8,DEL8,DEL1,DEL5]`; one-step DELETE spikes widespread at
  n>=32. DELETE x spikes `need(x)` by `2dA(x)` while pool grows `ceil(dA/2)`.
- **J0 (J without L).** FALSE. E.g. n=128 vine 4-DELETE burst, slack -21.
  The LATENT term is load-bearing: B-activations draw on accumulated LATENT.
- **J (with L).** FALSE. Systematic burst grid: e.g. n=512 slack -122.
- **Splay-target monotonicity** (non-target depths never decrease). FALSE:
  917,438/6,576,822 violations. Preservation arguments must not use it.
- **Local reduction `rA + ActB >= need`.** Too strong (drops history reserves);
  fails where the theorem holds. Not a refutation path, just a dead end.

## 4. The obstruction: drain-then-diverge rate mismatch

Canonical closed-form family (falsifies MST0-14R for every n>=28):
`T0 = vine-right-n`, `H = [DEL(n-1), DEL(n), KEEP(n), KEEP(n-1)]`.
- `DEL(n-1)` (depth n-2, ~n/2 events) + `DEL(n)` prefund the pool.
- `KEEP(n)`: `a=1` (n at A-root), `y=n` (B still vine), `need=n-2` paid in
  full, pool drained to ~2 (margin 2 at n=28; exactly the F2 tight pattern).
- `KEEP(n-1)`: churn+strike pin `n-1` at A-depth 1 (`a=2` constant for all n)
  while B, which saw only `KEEP(n)`, keeps `n-1` at depth ~n/2 (`y~n/2+1`).
  `need ~ n/2`, pool `~ n/4` (P~2 + rA=1 + ActB~rB~n/4). Residual `~ -n/4`.
Measured: n=28: need=11 paid=10 (-1); n=512: need=253 paid=131 (-122).
Minimality: greedy-drop-minimal (all 4 single drops satisfy); family-minimal
n=28 (n=1..27 all satisfy; margin ladder 4,4,5,5,...,1,1,0,0 then -1).
Legality: `LegalPairInstance` holds (vine valid, keys 1..n, history in [n]).

## 5. Why K6 missed it

K6's `delete-bursts` dimension churns only keys `1..6` (`ks[:6]`) then KEEPs
the middle key: pool is always overfunded relative to divergence, and the
draining KEEP never precedes a strike at a B-deep/A-shallow key. The
refutation needs deep-key bursts + drain + strike at a third key — outside
all 13 frozen K6 dimension shapes. Finite survival was never proof; here the
gap is exhibited exactly.

## 6. Consequences

- MST0-14R sufficiency is mathematically refuted (lifecycle: UNPROVED pending
  human G5 validation; no transition invented here).
- MSTC-0002 at `C=2/k=6` cannot serve as a universal Pair-Access repayment
  mechanism. The positive route is obstructed at the repayment node.
- The closed-form family (linear residual divergence) is the preserved exact
  obstruction seeding Phase-6 negative-lifting candidacy (NOT a DOC disproof;
  lifting requires closed-form Splay lower + explicit competitor + ratio
  divergence, all open).
- Lean staging: `lean/Proofs/LegalDomain.lean` carries domain defs, repaired
  statement, and `by decide` witness evaluations (UNCHECKED, PENDING_TOOLCHAIN).
