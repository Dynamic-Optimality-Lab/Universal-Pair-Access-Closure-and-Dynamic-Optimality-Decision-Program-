"""audit/review_package.py — human review package assembler (WP-2).

Assembles math/reviews/<NODE>.PACKAGE.md evidence: frozen doc + hash, Layer-A
proof cert, Layer-B formal cert, Lean theorem/build status, attack/scan
evidence, mutant result, run records. Verdict section is always PENDING-HUMAN;
this module NEVER writes .review.json (human-only).
"""
import hashlib
import json
from pathlib import Path

IMPL = Path(__file__).resolve().parents[2]
REVIEWS = IMPL / "math/reviews"


def _h(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def assemble_package(node, proof_doc, formal_module, attack_records,
                     run_record_paths, extras=None):
    """Write PACKAGE.md evidence; return (path, sha256). No verdict asserted.

    extras (optional dict): layer_a_cert, formal_cert, lean_theorem,
    build_status, mutant_result, scan_artifact — each a path str (hashed) or
    a literal status str.
    """
    ex = extras or {}

    def fmt(label, val):
        if val is None:
            return None
        p = IMPL / val if (IMPL / val).exists() else None
        if p is not None and p.is_file():
            return f"- {label}: `{val}` sha256={_h(p)}"
        return f"- {label}: {val}"

    lines = [f"# {node} review package (evidence, PENDING-HUMAN)",
             "",
             f"Frozen theorem doc: `{proof_doc}`",
             f"sha256(doc): {_h(IMPL / proof_doc)}",
             f"Formal module: `{formal_module}` (proof developments import frozen declarations)",
             ""]
    for label in ["layer_a_cert", "formal_cert", "lean_theorem", "build_status",
                  "mutant_result", "scan_artifact"]:
        line = fmt(label, ex.get(label))
        if line is not None:
            lines.append(line)
    lines += ["", "## Attack evidence", ""]
    for rec in attack_records:
        lines.append(f"- `{rec}` sha256={_h(rec)}")
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
    return (str(path), _h(path))
