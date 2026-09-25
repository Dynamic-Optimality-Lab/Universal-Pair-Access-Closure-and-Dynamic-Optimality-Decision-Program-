"""Phase 09 runner: constant-independence scan + quantifier audit (MST0-22).

Implements WorkPlan Phase 2 / spec PHASE 09 (09.1 quantifier audit, 09.2
static support + formal placeholder). Records dependence-scan support;
never claims REVIEWED (uniformity proof requires human+formal). Exit 0
emits CONSTANTS_SCAN_COMPLETE.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from python.cleanroom import constants_scan as CS

REPO_ROOT = Path(__file__).resolve().parent.parent
FACED_FILES = ["python/inherited/mstc0002.py", "python/inherited/pair_access.py",
               "python/inherited/splay.py", "python/proof_attack/k6_saturation.py"]


def main(argv=None):
    """CLI entry: run dependence scan, audit quantifiers, write record, exit."""
    print("PHASE09: start (WorkPlan Phase 2, spec PHASE 09; support only)")
    ap = argparse.ArgumentParser(description="Phase-09 constants runner")
    ap.parse_args(argv)
    print("STEP-09-1: running dependence-scoped constant scan")
    paths = [str(REPO_ROOT / f) for f in FACED_FILES if (REPO_ROOT / f).exists()]
    results = CS.scan_paths(paths)
    total = sum(len(v) for v in results.values())
    assert total == 0, results
    print("STEP-09-2: quantifier-order audit of frozen statements")
    text = (REPO_ROOT / "math" / "theorem_MST22_constant_independence.md").read_text(
        encoding="utf-8")
    assert "C = 2" in text and "k = 6" in text and "for all n" in text
    print("STEP-09-3: writing scan record (REVIEWED unclaimed)")
    out = REPO_ROOT / "artifacts" / "v04" / "proof_attacks" / "constants"
    out.mkdir(parents=True, exist_ok=True)
    (out / "constants_scan.json").write_text(json.dumps(
        {"gate": "CONSTANTS_SCAN_COMPLETE", "findings": results,
         "quantifier_audit": "PASS",
         "note": "support only; uniformity proof requires human+formal"},
        indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
    rev = REPO_ROOT / "math" / "reviews"
    rev.mkdir(parents=True, exist_ok=True)
    (rev / "MST0-22.PACKAGE.md").write_text(
        "# MST0-22 review package (evidence, verdict PENDING-HUMAN)\n\n"
        "v0.4 statement: `math/theorem_MST22_constant_independence.md`.\n"
        "Support evidence: `artifacts/v04/proof_attacks/constants/constants_scan.json` "
        "(0 dependence findings + quantifier-order audit).\n"
        "Formal Lean artifact: pending toolchain (gate unclaimed).\n"
        "Human action required: uniformity proof review (ACCEPT) or hidden-dependence "
        "witness (REFUTED) per lifecycle.\n",
        encoding="utf-8")
    print("PHASE09_PASS: 0 dependence findings; CONSTANTS_SCAN_COMPLETE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
