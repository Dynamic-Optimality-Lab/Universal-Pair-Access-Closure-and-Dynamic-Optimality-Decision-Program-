"""audit/review_package.py — human review package assembler (WP-2).

Assembles math/reviews/<NODE>.PACKAGE.md evidence from attack records,
certificates, hashes, Lean build status, and run records. Verdict section is
always PENDING-HUMAN; this module NEVER writes .review.json (human-only).
"""
import hashlib
import json
from pathlib import Path

IMPL = Path(__file__).resolve().parents[2]
REVIEWS = IMPL / "math/reviews"


def assemble_package(node, proof_doc, formal_module, attack_records, run_record_paths):
    """Write PACKAGE.md evidence; return (path, sha256). No verdict asserted."""
    lines = [f"# {node} review package (evidence, PENDING-HUMAN)",
             "",
             f"Frozen theorem doc: `{proof_doc}`",
             f"sha256(doc): {hashlib.sha256((IMPL / proof_doc).read_bytes()).hexdigest()}",
             f"Formal module: `{formal_module}` (proof developments import frozen declarations)",
             "",
             "## Attack evidence",
             ""]
    for rec in attack_records:
        lines.append(f"- `{rec}` sha256={hashlib.sha256(Path(rec).read_bytes()).hexdigest()}")
    lines += ["", "## Run records", ""]
    for rp in run_record_paths:
        lines.append(f"- `{rp}`")
    lines += ["",
              "## Human verdict",
              "",
              "PENDING-HUMAN. No assistant, review, or formal artifact substitutes.",
              "A human writes `<NODE>.review.json` with ACCEPT/REJECT/BLOCKED only.",
              ""]
    REVIEWS.mkdir(parents=True, exist_ok=True)
    path = REVIEWS / f"{node}.PACKAGE.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return (str(path), hashlib.sha256(path.read_bytes()).hexdigest())
