"""proof_attack/pair_access_search.py (STUB) — dedicated REFUTE(MST0-17) battery; see WorkPlan Phase 5.

Exact negation (HARD fix v0.4-WP5 — endpoint terms mandatory): exists
(n,T,X,Y<=X, legal execution/ledger) with lhs > rhs where
lhs = Splay(Y,T) + E_m - E_0 and rhs = 2*Splay(X,T) + A(n), all exact.
The endpoint-free form belongs to MST0-18 downstream and MUST NOT be targeted
here: a negative E_m-E_0 could otherwise mask a missed MST0-17 violation.
Evaluator uses exact Fraction arithmetic via the inherited core + imported
ledger semantics; witnesses carry the 15-field reconstruction payload
(n,T,X,Y,Y<=X cert,paired execution,block decomposition,L_0,L_m,E_0,E_m,
SplayX,SplayY,A(n),lhs,rhs,residual) in
artifacts/v04/counterexamples/pair_access/ under the frozen canonical order
with inflation analysis + independent replay.
Clean-room counterpart: python/cleanroom/pair_access_check.py (share-nothing).
Startup SHA-guard: abort unless sha256(loaded statement) and sha256(loaded
negation) equal theorem_battlefield[MST0-17].statement/negation_sha256
(STOP-15/16); the evaluator is derived from that versioned obligation.
No theorem-facing execution before FOUNDATION_FROZEN; implementation must pass
the PSC conformance harness (STOP-17) before use."""
