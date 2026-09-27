# PSC-K6 clarification + compliance disposition (repair track, append-only)

Historical artifacts preserved untouched. This record clarifies two frozen
sub-specifications and dispositions them given the certified MST0-14R legal
refutation. Nothing below rewrites history or manufactures semantics.

## 1. `2048+` (proof_stress_corpus.yaml sizes)

Frozen bytes: `sizes: [16,32,64,128,256,512,1024,2048+]`. Implementation
(`common.SIZES`, all shards, FULL) stops at 1024. Gap confirmed (real).
Normative reading (spec s26.1): "any deterministic schedule within
resources, for example 16,24,32,...,1024,..." — the trailing `...`
continues past 1024; `2048+` therefore reads "2048 and beyond as resources
permit" (at least one n>=2048 representative; larger sizes
resource-conditioned with s26.5 failure records). `2048+ := exactly 2048`
alone would be arbitrary; the `+` keeps larger sizes in scope.
Disposition: on the repair track n=2048 WAS exercised (F2-repeat-del-n2048:
margins 1-2, no witness; see LEGAL_SWEEP_engineered record). A formal
shard-D campaign on the old K6 track is SUPERSEDED-BY-REFUTATION (reason:
finite evidence cannot revive a certified-refuted universal; further K6
runs on this track are scientific dead weight). Resource disposition, not
omission. No old artifact edited.

## 2. `regret_class` (gen_k6 third parameter; range "positive-regret-magnitudes")

Confirmed: implementation stores it as a label; `campaign()` always passes
`"positive"`. The frozen range defines NO bins in any normative byte (spec
s14.3's 13 search dimensions do not elaborate it).
Disposition: PREREG_INTERFACE_UNDERSPECIFIED. The only source-derived
stratification is the frozen `required` formula's own sign dichotomy
(positive vs nonpositive regret); any finer magnitude bins (small/medium/
large, numeric thresholds) would be invented post hoc and are refused.
The interface is RETIRED with the refuted track (no post-refutation bins
manufactured). Historical "positive"-label streams remain reproducible
byte-identically (rebinding verified worst-match on all 4 shards).

## 3. FULL checker provenance (Path R1-033 PENDING vs blob AGREE)

Resolved append-only: `artifacts/v04/audits/MST0-14_FULL_CHECKER_ATTESTATION.json`
(checker rerun on the exact historical blob: AGREE, recomputed=0 claimed=0).
Historical scientific result validated retroactively; the original blob's
provenance overclaim stands corrected without touching its bytes. R1-033's
contemporaneous PENDING note was accurate at commit time.

## 4. K6 rebinding (Sec 10A)

`artifacts/v04/audits/MST0-14R_K6_REBIND.jsonl`: all 4 historical shards
regenerated with unmodified PSC-K6/1.0 code — worst matches claimed 0/0/0/0;
5,880/5,880 regenerated inputs satisfy LegalPairInstance (0 violations).
Historical evidence is valid finite evidence about the legal subspace and is
preserved as such. (FULL-space stream regeneration is covered by the union
of the 4 shard regenerations — same space — plus the FULL checker rerun.)

## 5. REP-12 / REP-14 truthful semantics (Sec 14)

- REP-12-MECHANISM (`paid = min(pool,need)` in Lean, no sorry): SATISFIED
  (historical, build-green; reused unchanged).
- REP-12-UNIVERSAL (full sufficiency proof): NOT_SATISFIED — permanently
  unsatisfiable (sufficiency mathematically refuted). Never report satisfied.
- REP-14-PACKAGE (evidence assembled, PENDING-HUMAN, no verdict file):
  SATISFIED as packaging only.
- REP-14-HUMAN (actual hostile human review): NOT_SATISFIED (no verdict
  recorded, none generated or inferred). `REP 14/14 GREEN` must never be
  reported; the machine-readable split is `tests/repayment/test_rep_12_14_truthful.py`
  (12U/14H strict-xfail: green suite with NOT_SATISFIED statuses explicit;
  14H flips loudly if a human verdict ever lands).
