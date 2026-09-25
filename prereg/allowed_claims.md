# Allowed claims (spec §33 + v0.4.1 A3) — enforced by run_phase18.py + human review.

- `BOUNDED_DELETE_INJECTION_PROVED`: DELETE-side injection universally bounded by proved constant times A-side cost. No Pair-Access claim.
- `UNIVERSAL_LOCALITY_PROVED`: reference modifications satisfy the proved arbitrary-n bound. No repayment claim.
- `TRANSFER_PRESERVATION_PROVED`: every legal primitive preserves all downstream invariants. No repayment claim.
- `RAW_BOUNDARY_LAW_PROVED`: boundary damage has exact cost-bearing sources with proved bound. No repayment claim.
- `SYNCHRONOUS_KEEP_TRANSFER_PROVED`: every legal KEEP satisfies the frozen repayment theorem. No global claim until integrability/composition.
- `GLOBAL_INTEGRABILITY_PROVED`: frozen local calculus admits the proved global accounting. Still requires composition/telescope.
- `UNIVERSAL_PAIR_ACCESS_LEMMA_PROVED`: exact universal Pair-Access inequality proved for all legal paired executions. No DOC claim before MST0-18/19.
- `APPROXIMATE_MONOTONICITY_PROVED`: only after telescope theorem and endpoint/additive-term audit.
- `DYNAMIC_OPTIMALITY_PROVED`: only after all ten positive critical nodes REVIEWED and Phase-18 bridge regeneration. Success S1.
- `DYNAMIC_OPTIMALITY_DISPROVED`: only after REVIEWED closed-form real-Splay/competitor divergence theorem. Success S2.
- No-claim levels (`POSITIVE_ROUTE_REFUTED_NO_DOC_NEGATIVE`, `POSITIVE_ROUTE_BLOCKED_UNRESOLVED_NO_CLAIM`, `BRIDGE_BLOCKED_NO_CLAIM`, `RESOURCE_LIMIT_NO_CLAIM`): exact first-wall localization; YES/NO forbidden.
- `POSITIVE_ROUTE_BLOCKED_UNRESOLVED_NO_CLAIM`: allowed — “positive route blocked at named unresolved theorem(s) (reviewer REJECT/BLOCKED or UNPROVED with open obligations); no refutation, no resource failure, no YES/NO.”
