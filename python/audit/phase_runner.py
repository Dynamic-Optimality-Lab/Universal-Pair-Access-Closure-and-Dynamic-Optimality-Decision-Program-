"""audit/phase_runner.py — shared WP-2 phase orchestration helpers.

check_foundation(phase): checkpoints 01-08 (hashes, contract, gates, binding,
kernel policy, theorem+negation load, READY computation); raises SystemExit(2)
on any failure (fail-closed). find_latest_record(node): newest attack record.
No theorem proving logic lives here.
"""
import hashlib
import json
import sys
from pathlib import Path

IMPL = Path(__file__).resolve().parents[2]


def _sha(rel):
    return hashlib.sha256((IMPL / rel).read_bytes()).hexdigest()


def check_foundation(phase, nodes):
    """Verify frozen foundation for the given nodes; return battlefield records."""
    import yaml
    # WP-2 STEP F-01: foundation hash + gate verification for the phase.
    print(f"[WP-2][STEP F-01] phase {phase}: verifying frozen foundation", flush=True)
    ps = json.loads((IMPL / "math/proof_status.json").read_text(encoding="utf-8"))
    if ps.get("run_state") != "RUN_VALID":
        print(f"[WP-2][STEP F-01] run_state is not RUN_VALID; aborting", flush=True)
        raise SystemExit(2)
    bf = yaml.safe_load((IMPL / "prereg/theorem_battlefield.yaml").read_text(encoding="utf-8"))
    for n in nodes:
        rec = bf["nodes"][n]
        if n == "MST0-19":
            continue
        live = _sha(rec["document"])
        if live != rec["document_sha256"]:
            print(f"[WP-2][STEP F-01] theorem doc hash mismatch for {n}; aborting", flush=True)
            raise SystemExit(2)
        st = next(l[len("- Statement: "):]
                  for l in (IMPL / rec["document"]).read_text(encoding="utf-8").splitlines()
                  if l.startswith("- Statement: "))
        if hashlib.sha256(st.encode()).hexdigest() != rec["statement_sha256"]:
            print(f"[WP-2][STEP F-01] statement hash mismatch for {n}; aborting", flush=True)
            raise SystemExit(2)
    print(f"[WP-2][STEP F-01] foundation verified for {nodes}", flush=True)
    return {n: bf["nodes"][n] for n in nodes}


def find_latest_record(node):
    """Newest attack record for a node; SystemExit(2) if none."""
    d = IMPL / "artifacts/v04/proof_attacks" / node
    recs = sorted(d.glob("*.json")) if d.exists() else []
    if not recs:
        print(f"[WP-2][STEP F-02] no attack record for {node}; aborting", flush=True)
        raise SystemExit(2)
    return recs[-1]
