# MST0-19 — Levy-Tarjan bridge: BLOCKED-NODE RECORD (frozen Phase 1; v0.4 §6, Phase-16 contract; v0.4.5 E2 representation)

This node carries NO source-dependent Statement/Negation (synthesizing bridge content
from prose is forbidden). Its machine form is the concrete metadata conjunction
`MST0_19_blocked` in `lean/Frozen/Statements.lean`, never a theorem-bearing Prop.

- Parent status: BLOCKED on 18 + exact L2/L3 premise bytes.
- v0.4 owner phase: Phase 5 (WorkPlan §8; 10-point convention checklist + independent reconstruction, spec PHASE 16).
- First consumer: Phase-18 decision gate (DEC-GATE-11..13 -> BRIDGE_READY_FOR_DECISION).
- Prerequisites (all unfrozen): MST0-18 REVIEWED + exact L2 bytes frozen + exact L3 bytes frozen + convention match.
- Premise-byte status: L3 FROZEN (`bridge_sources/L3_1907.06310_v1.pdf`, 1,431,066 bytes,
  SHA-256 `E23EA8B58984B9A3530E8BF06AA028645DAD420B1AF280EEB407F4D2A4495A78`,
  acquired 2026-09-25 UTC); L2 ABSENT (SODA-2019, no lawful open bytes obtainable here).
- Child-lemma namespace: `MST0-19/*` (opens only after premise freeze; nothing registered).
- Forbidden premises: consuming the bridge before source+convention freeze (STOP-11);
  prose-synthesized Levy-Tarjan; L2/L3 conflation (arXiv v1 title lineage noted, never substituted).
- Falsity consequence: SOURCE/CONVENTION MISMATCH -> BLOCKED, never REFUTED; only an exact
  bridge-negation witness under matched frozen conventions may REFUTE. Unavailable source ->
  `BRIDGE_BLOCKED_NO_CLAIM`, never consumed. Mismatch blocks per STOP-55..59.
- Proof artifact: `math/proofs/MST0-19_proof.md` (PENDING Phase 5; bridge-mapping argument after premise freeze).
- Formal artifact: `python/formal_bridge/bridge_audit.py` convention record (PENDING Phase 5; no Lean theorem module while blocked).
- Review artifact: `math/reviews/MST0-19.PACKAGE.md` + `math/reviews/MST0-19.review.json` (human verdict only).
- Refutation artifact: three mutually exclusive outcomes only (mismatch->BLOCKED / exact-witness->REFUTED-candidate / proof+cert+ACCEPT->REVIEWED); no source-dependent witness synthesized while blocked.
