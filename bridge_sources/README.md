# bridge_sources/ — L2/L3 byte store (manifest: `prereg/bridge_sources.yaml`)

## Acquisition outcome (recorded 2026-09-25 UTC, pre-freeze)

- **L3 ACQUIRED**: `L3_1907.06310_v1.pdf`
  - Identity: Levy & Tarjan, "A Foundation for Proving Splay is Dynamically Optimal",
    arXiv:1907.06310 v1 (submitted 15 Jul 2019). Identity verified against the
    arXiv abs metadata (title + authors + v1 submission date match).
  - Provenance: lawful open-access download from `https://arxiv.org/pdf/1907.06310v1.pdf`
    on 2026-09-25 UTC.
  - Bytes: 1,431,066; SHA-256:
    `E23EA8B58984B9A3530E8BF06AA028645DAD420B1AF280EEB407F4D2A4495A78`;
    magic `%PDF-`, trailer `%%EOF` present (complete as served).
  - Observation: arXiv's abs page lists v1 at 702 KB; the bytes served at the v1
    URL on 2026-09-25 are 1,431,066 bytes. Both the hash above and this size
    observation are frozen; Phase-02 execution performs the independent second
    extraction plus exact theorem-text capture, which confirms or disputes them.
- **L2 NOT ACQUIRED**: Levy & Tarjan, "A New Path from Splay to Dynamic Optimality",
  SODA 2019 (paywalled proceedings; no lawful open-access bytes obtainable from this
  environment). No L2 bytes are frozen; no L2 content is synthesized from prose.
  (Note: the arXiv record states v1 of 1907.06310 was titled "New Paths from Splay
  to Dynamic Optimality" — lineage noted, never conflated: L2 remains a separate
  unfrozen premise artifact.)

## Downstream disposition

- Freeze variant per v0.4.6 F1: **SOURCE_AVAILABLE (28-member set)** — the bound
  source PDF is present and bound above.
- `MST0-19` remains **BLOCKED**: spec requires exact L2/L3 premise bytes plus
  convention match; L2 bytes are absent, so no theorem-bearing MST0-19 proposition
  is instantiated (v0.4.5 E2 blocked-source representation). Inventing Levy–Tarjan
  from prose is forbidden.
- Phase-02 execution verifies these bytes and writes only the separate
  `artifacts/v04/freeze/PHASE02_BRIDGE_SOURCES_FREEZE.json` — never a post-freeze
  rewrite of this record.
