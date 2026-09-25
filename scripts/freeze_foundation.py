"""Freeze orchestrator: repair Phase 00 against the current normative stack.

Executes the WP8 freeze-manifest contract end to end and fails closed on any
missing, extra, mismatching, or ambiguous freeze-bound input:
  F-00 rerun PHASE-00 checks (imported, read-only)
  F-01 materialize the immutable parent/ import package (10 named files)
  F-02 exact-identity verification of every downstream-consumed parent
      theorem/proof/review artifact against the sealed MANIFEST
  F-03 lifecycle legality: zero jumps, zero pointerless, counts agree
  F-04 bridge manifest check (L3 bytes + SHA; L2 UNAVAILABLE record)
  F-05 prereg completeness (13 sources real content; manifest correctly absent)
  F-06 immutable PATH_AT_FOUNDATION_FREEZE.md snapshot
  F-07 write prereg/prereg_sha256.txt over PREREG_PAYLOAD u FREEZE_BOUND
  F-08 byte-verify every manifest line
  F-09 prefix-verify living Path opens with the snapshot bytes
  F-10 emit FOUNDATION_FROZEN with scope + pending-execution list, or fail
Only F-10 success claims the gate. Pre-freeze planning files are untouched.
"""

import argparse
import datetime
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_phase00
import run_phase01

REPO_ROOT = Path(__file__).resolve().parent.parent
EXPECTED_HEAD = run_phase00.EXPECTED_PARENT_HEAD
EXPECTED_SET_HASH = run_phase00.EXPECTED_SET_HASH


class FreezeError(Exception):
    """Raised on any freeze-contract violation (fail-closed)."""


# F-CFG: frozen freeze-contract sets (WP8 manifest contract).
print("STEP-F-CFG: loading freeze-contract sets")
PREREG_PAYLOAD_FILES = [
    "prereg/experiment_v0.4.yaml", "prereg/parent_contract.yaml",
    "prereg/theorem_battlefield.yaml", "prereg/theorem_gate_matrix.yaml",
    "prereg/dual_obligation_policy.yaml", "prereg/proof_kernel_policy.yaml",
    "prereg/proof_stress_corpus.yaml", "prereg/negative_lifting_policy.yaml",
    "prereg/bridge_sources.yaml", "prereg/threat_control_matrix.yaml",
    "prereg/stop_control_matrix.yaml", "prereg/allowed_claims.md",
    "prereg/forbidden_claims.md",
]
FREEZE_BOUND_FILES = [
    "WorkPlan.md",
    "IMPLEMENTATION_SPEC_v0.4.md",
    "SPLAY_AM_DECIDE_IMPLEMENTATION_SPEC_v0.4.1_AMENDMENT.md",
    "SPLAY_AM_DECIDE_IMPLEMENTATION_SPEC_v0.4.2_AMENDMENT.md",
    "lean-toolchain", "lake-manifest.json",
    "schemas/proof_attack.schema.json",
    "schemas/pair_access_certificate.schema.json",
    "prereg/proof_stress_corpus.yaml",
    "bridge_sources/L3_1907.06310_v1.pdf",
    "bridge_sources/README.md",
    "math/theorem_MST08U_locality.md", "math/theorem_MST09_raw_boundary.md",
    "math/theorem_MST11_preservation.md", "math/theorem_MST13_delete_injection.md",
    "math/theorem_MST14_keep_repayment.md", "math/theorem_MST15_integrability.md",
    "math/theorem_MST22_constant_independence.md",
    "math/theorem_MST17_pair_access.md", "math/theorem_MST18_telescoping.md",
    "math/theorem_MST19_bridge.md",
    "parent/V03_SEAL.json", "parent/V03_FINAL_RESULT.json",
    "parent/V03_MANIFEST.sha256", "parent/V03_ARCHIVE.sha256",
    "parent/V03_PATH_FINAL.md", "parent/V03_WORKPLAN_FINAL.md",
    "parent/V03_MSTC_0002.json", "parent/V03_THEOREM_STATUS.json",
    "parent/V03_COUNTEREXAMPLE_INDEX.json", "parent/BOOTSTRAP_MANIFEST.sha256",
    "artifacts/v04/freeze/PATH_AT_FOUNDATION_FREEZE.md",
]
DOWNSTREAM_DOCS = [
    "math/theorem_MST01_parent_transport.md", "math/theorem_MST02_rotation_refinement.md",
    "math/theorem_MST03_l6_translation.md", "math/theorem_MST04_keep_reference_snapshot.md",
    "math/theorem_MST05_keep_heavy_path.md", "math/theorem_MST06_zigzig_pairing.md",
    "math/theorem_MST07_zigzag_bends.md",
    "math/theorem_MST08_reference_rotation_locality.md",
    "math/theorem_MST10_ledger_determinism.md",
    "math/theorem_MST11_transfer_preservation.md",
    "math/theorem_MST13_delete_injection.md",
    "math/theorem_MST16_block_partition.md",
]
DOWNSTREAM_REVIEWS_PRESENT = ["MST0-%02d.review.json" % i for i in (1, 2, 3, 4, 5, 6, 7, 8, 10, 16)]
DOWNSTREAM_BUNDLES = ["MST0-%02d.json" % i for i in (1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 13, 14, 15, 16)]
# Path.md/WorkPlan.md join the downstream identity set (audit inheritance).
DOWNSTREAM_TOP_DOCS = ["Path.md", "WorkPlan.md"]


def sha256_file(path):
    """Return the hex SHA-256 of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1048576), b""):
            h.update(chunk)
    return h.hexdigest()


def sealed_bytes(path):
    """Return parent-workdir bytes normalized to the sealed identity.

    The reference clone checks out with core.autocrlf=true, so text files
    carry CRLF while the sealed MANIFEST (and the parent's own audit hashes)
    were computed over LF bytes. For UTF-8-decodable content, CRLF is folded
    to LF and the normalization is reported; binary content passes through
    untouched. Returns (bytes, normalized_flag).
    """
    raw = Path(path).read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw, False
    if "\r\n" not in text:
        return raw, False
    return text.replace("\r\n", "\n").encode("utf-8"), True


def sha256_sealed(path):
    """SHA-256 over sealed-identity (normalized) bytes."""
    data, _ = sealed_bytes(path)
    return hashlib.sha256(data).hexdigest()


def load_json(path):
    """Load JSON or raise FreezeError."""
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise FreezeError("unreadable JSON %s: %s" % (path, e))


def utcnow():
    """Return current UTC timestamp in canonical form."""
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def freeze_parent_package(parent, log):
    """F-01: materialize the 10 named immutable parent/ files with provenance."""
    print("STEP-F-01: materializing parent/ import package")
    dest = REPO_ROOT / "parent"
    dest.mkdir(parents=True, exist_ok=True)
    seal = parent / "artifacts" / "v03" / "seal"
    hold = parent / "artifacts" / "v03" / "holdouts"
    proofs = parent / "artifacts" / "v03" / "proofs"
    exact_copies = {
        "V03_FINAL_RESULT.json": seal / "FINAL_RESULT.json",
        "V03_MANIFEST.sha256": seal / "MANIFEST.sha256",
        "V03_ARCHIVE.sha256": seal / "ARCHIVE.sha256",
        "V03_PATH_FINAL.md": parent / "Path.md",
        "V03_WORKPLAN_FINAL.md": parent / "WorkPlan.md",
        "V03_THEOREM_STATUS.json": proofs / "obligation_status.json",
    }
    for name, src in exact_copies.items():
        if not src.exists():
            raise FreezeError("parent source missing: %s" % src)
        data, normalized = sealed_bytes(src)
        (dest / name).write_bytes(data)
        if normalized:
            log.append({"step": "STEP-F-01", "name": "crlf-fold-%s" % name,
                        "status": "PASS", "detail": "CRLF folded to LF sealed bytes"})
    fr = load_json(dest / "V03_FINAL_RESULT.json")
    cs = load_json(hold / "candidate_set_commit.json")
    m2 = next(c for c in cs["candidates"] if c["calculus_id"] == "MSTC-0002")
    (dest / "V03_MSTC_0002.json").write_text(json.dumps({
        "provenance": "extracted-MSTC-0002-entry-from-sealed-candidate_set_commit.json",
        "candidate_set_hash": cs["set_hash"], "record": m2,
    }, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    rv = load_json(hold / "h3t_reveal.json")
    atlas = parent / "COUNTEREXAMPLE_ATLAS.md"
    (dest / "V03_COUNTEREXAMPLE_INDEX.json").write_text(json.dumps({
        "provenance": "first-violations-from-sealed-h3t_reveal.json",
        "first_violations": [
            {"calculus_id": r["calculus_id"],
             "episode_hash": (r["first_violation"] or {}).get("episode_hash"),
             "max_residual": r.get("max_residual"),
             "verdict": r.get("verdict")} for r in rv["results"]],
        "atlas_sha256": sha256_file(atlas),
    }, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (dest / "V03_SEAL.json").write_text(json.dumps({
        "experiment": "SPLAY-AM-MST-v0.3",
        "sealed_head": EXPECTED_HEAD,
        "terminal_claim": fr["terminal_claim"],
        "candidate_set_hash": EXPECTED_SET_HASH,
        "h3t_state": "UNLOCKED_ONCE/unlocks=1",
        "manifest_lines": 424,
        "archive_sha256": (seal / "ARCHIVE.sha256").read_text(encoding="utf-8").split()[0].lower(),
    }, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    manifest = []
    for name in ["V03_SEAL.json", "V03_FINAL_RESULT.json", "V03_MANIFEST.sha256",
                 "V03_ARCHIVE.sha256", "V03_PATH_FINAL.md", "V03_WORKPLAN_FINAL.md",
                 "V03_MSTC_0002.json", "V03_THEOREM_STATUS.json",
                 "V03_COUNTEREXAMPLE_INDEX.json"]:
        manifest.append("%s  parent/%s" % (sha256_file(dest / name), name))
    (dest / "BOOTSTRAP_MANIFEST.sha256").write_text("\n".join(manifest) + "\n",
                                                    encoding="utf-8")
    log.append({"step": "STEP-F-01", "name": "parent_package", "status": "PASS",
                "detail": "10 files materialized"})


def verify_downstream_identities(parent, log):
    """F-02: every downstream-consumed artifact hash-matches the sealed MANIFEST."""
    print("STEP-F-02: verifying downstream identities against sealed MANIFEST")
    table = {}
    for ln in (parent / "artifacts" / "v03" / "seal" / "MANIFEST.sha256").read_text(
            encoding="utf-8").splitlines():
        h, p = ln.split()
        table[p[2:] if p.startswith("./") else p] = h.lower()
    checked = 0
    for rel in DOWNSTREAM_DOCS + DOWNSTREAM_TOP_DOCS:
        want = table.get(rel)
        if want is None:
            raise FreezeError("downstream doc absent from MANIFEST: %s" % rel)
        if sha256_sealed(parent / rel) != want:
            raise FreezeError("downstream hash mismatch: %s" % rel)
        checked += 1
    for name in DOWNSTREAM_REVIEWS_PRESENT:
        rel = "math/reviews/%s" % name
        if table.get(rel) is None or sha256_sealed(parent / rel) != table[rel]:
            raise FreezeError("review identity failure: %s" % rel)
        checked += 1
    if (parent / "math" / "reviews" / "MST0-13.review.json").exists():
        raise FreezeError("MST0-13.review.json exists but review is pending")
    for name in DOWNSTREAM_BUNDLES:
        rel = "artifacts/v03/proofs/bundles/%s" % name
        if table.get(rel) is None or sha256_sealed(parent / rel) != table[rel]:
            raise FreezeError("bundle identity failure: %s" % rel)
        checked += 1
    for rel in ("math/reviews/MST0-13.REVIEW-PACKAGE.md",
                "artifacts/v03/proofs/MST13_injection_bound.json"):
        if table.get(rel) is None or sha256_sealed(parent / rel) != table[rel]:
            raise FreezeError("MST0-13 package identity failure: %s" % rel)
        checked += 1
    log.append({"step": "STEP-F-02", "name": "downstream_identities", "status": "PASS",
                "detail": "%d artifacts hash-matched" % checked})


def verify_lifecycle_legality(parent, log):
    """F-03: zero jumps, zero pointerless, counts agree (legality, not counts)."""
    print("STEP-F-03: verifying lifecycle legality (zero jumps)")
    audit = load_json(parent / "artifacts" / "v03" / "proofs" / "lifecycle_audit.json")
    status = load_json(parent / "artifacts" / "v03" / "proofs" / "obligation_status.json")
    if audit.get("jumps") not in ([], None) or audit.get("pointerless") not in ([], None):
        raise FreezeError("lifecycle jumps or pointerless present")
    from collections import Counter
    counts = dict(Counter(v["status"] for v in status["statuses"].values()))
    audit_counts = {k: v for k, v in audit["counts"].items()}
    if counts != audit_counts or len(status["statuses"]) != 26:
        raise FreezeError("lifecycle counts disagree")
    log.append({"step": "STEP-F-03", "name": "lifecycle_legality", "status": "PASS",
                "detail": "0 jumps, 0 pointerless, 26 bound"})


def verify_bridge_manifest(log):
    """F-04: L3 bytes bound; L2 UNAVAILABLE record bound; yaml agrees."""
    print("STEP-F-04: verifying bridge-source manifest")
    l3 = REPO_ROOT / "bridge_sources" / "L3_1907.06310_v1.pdf"
    if not l3.exists() or sha256_file(l3) != "f7aa79010984db5104c81846d7d0862bb4b83c1f13cbc84c922757e340c36f1c":
        raise FreezeError("L3 bytes mismatch")
    text = (REPO_ROOT / "prereg" / "bridge_sources.yaml").read_text(encoding="utf-8")
    if "BRIDGE_SOURCE_UNAVAILABLE" not in text or "f7aa79010984db5104c81846d7d0862bb4b83c1f13cbc84c922757e340c36f1c" not in text:
        raise FreezeError("bridge_sources.yaml disagrees with bytes")
    log.append({"step": "STEP-F-04", "name": "bridge_manifest", "status": "PASS",
                "detail": "L3 frozen, L2 unavailable-recorded"})


def verify_prereg_content(log):
    """F-05: all 13 sources carry real normative content (no stub-only files)."""
    print("STEP-F-05: verifying prereg content completeness")
    for rel in PREREG_PAYLOAD_FILES:
        p = REPO_ROOT / rel
        if not p.exists():
            raise FreezeError("prereg source missing: %s" % rel)
        lines = [ln for ln in p.read_text(encoding="utf-8").splitlines() if ln.strip()]
        if len(lines) < 5 or any(ln.startswith("# STUB") for ln in lines):
            raise FreezeError("prereg source is stub-only: %s" % rel)
    if (REPO_ROOT / "prereg" / "prereg_sha256.txt").exists():
        raise FreezeError("prereg_sha256.txt exists before freeze")
    log.append({"step": "STEP-F-05", "name": "prereg_content", "status": "PASS",
                "detail": "13 sources normative"})


def write_snapshot(log):
    """F-06: immutable PATH_AT_FOUNDATION_FREEZE.md snapshot (prefix rule)."""
    print("STEP-F-06: writing immutable Path freeze snapshot")
    live = (REPO_ROOT / "Path.md").read_bytes()
    snap = REPO_ROOT / "artifacts" / "v04" / "freeze" / "PATH_AT_FOUNDATION_FREEZE.md"
    snap.parent.mkdir(parents=True, exist_ok=True)
    snap.write_bytes(live)
    log.append({"step": "STEP-F-06", "name": "path_snapshot", "status": "PASS",
                "detail": "sha256=%s" % sha256_file(snap)})


def write_manifest(log):
    """F-07: write prereg_sha256.txt over PAYLOAD u BOUND (never itself)."""
    print("STEP-F-07: writing prereg_sha256.txt (payload u bound, never itself)")
    rows = []
    for rel in PREREG_PAYLOAD_FILES + FREEZE_BOUND_FILES:
        p = REPO_ROOT / rel
        if not p.exists():
            raise FreezeError("freeze-bound file missing: %s" % rel)
        rows.append("%s  %s" % (sha256_file(p), rel))
    (REPO_ROOT / "prereg" / "prereg_sha256.txt").write_text(
        "\n".join(rows) + "\n", encoding="utf-8")
    log.append({"step": "STEP-F-07", "name": "manifest", "status": "PASS",
                "detail": "%d lines" % len(rows)})


def verify_manifest(log):
    """F-08: byte-verify every manifest line against workdir bytes."""
    print("STEP-F-08: byte-verifying every manifest line")
    rows = (REPO_ROOT / "prereg" / "prereg_sha256.txt").read_text(
        encoding="utf-8").splitlines()
    if len(rows) != len(PREREG_PAYLOAD_FILES) + len(FREEZE_BOUND_FILES):
        raise FreezeError("manifest line count=%d" % len(rows))
    for ln in rows:
        parts = ln.split()
        if len(parts) != 2 or parts[1] == "prereg/prereg_sha256.txt":
            raise FreezeError("manifest self-reference or malformed line")
        if sha256_file(REPO_ROOT / parts[1]) != parts[0].lower():
            raise FreezeError("manifest mismatch: %s" % parts[1])
    log.append({"step": "STEP-F-08", "name": "manifest_verify", "status": "PASS",
                "detail": "%d lines byte-verified" % len(rows)})


def verify_prefix(log):
    """F-09: living Path opens with the frozen snapshot bytes."""
    print("STEP-F-09: verifying living Path opens with snapshot bytes")
    snap = (REPO_ROOT / "artifacts" / "v04" / "freeze" / "PATH_AT_FOUNDATION_FREEZE.md").read_bytes()
    live = (REPO_ROOT / "Path.md").read_bytes()
    if not live.startswith(snap):
        raise FreezeError("living Path prefix mismatch")
    log.append({"step": "STEP-F-09", "name": "prefix_verify", "status": "PASS",
                "detail": "%d snapshot bytes are a live prefix" % len(snap)})


def stash_pre_freeze():
    """Capture pre-freeze cert bytes before the rerun overwrites them."""
    print("STEP-F-00A: stashing pre-freeze outputs for comparison")
    stashed = {}
    freeze = REPO_ROOT / "artifacts" / "v04" / "freeze"
    logs = REPO_ROOT / "artifacts" / "v04" / "logs"
    for rel in ("freeze/PHASE00_PARENT_PIN.json", "freeze/PHASE01_SURVIVOR_BINDING.json",
                "logs/phase00.log", "logs/phase01.log"):
        p = REPO_ROOT / "artifacts" / "v04" / rel
        if p.exists():
            stashed[rel] = {"sha256": sha256_file(p), "bytes": p.read_bytes().decode("utf-8", "replace")}
        else:
            stashed[rel] = {"sha256": None, "bytes": None}
    return stashed


def write_superseded(stashed, log):
    """F-11: mark pre-freeze outputs non-authoritative; compare with rerun."""
    print("STEP-F-11: writing supersede record with pre/post comparison")
    freeze = REPO_ROOT / "artifacts" / "v04" / "freeze"
    comparison = {}
    for rel, old in stashed.items():
        p = REPO_ROOT / "artifacts" / "v04" / rel
        new_sha = sha256_file(p) if p.exists() else None
        if old["sha256"] is None:
            verdict = "absent-before"
        elif new_sha == old["sha256"]:
            verdict = "byte-identical"
        else:
            try:
                o = json.loads(old["bytes"])["checks"]
                n = json.loads(p.read_text(encoding="utf-8"))["checks"]
                same = [(c["step"], c["name"], c["status"]) for c in o] == \
                    [(c["step"], c["name"], c["status"]) for c in n]
                verdict = "semantically-identical-checks" if same else "divergent"
            except (KeyError, json.JSONDecodeError, OSError):
                verdict = "divergent-or-unparsable"
        comparison[rel] = {"old_sha256": old["sha256"], "new_sha256": new_sha,
                           "verdict": verdict}
    for rel in [r for r in comparison if r.endswith(".log")]:
        old_b = stashed[rel]["bytes"] or ""
        new_p = REPO_ROOT / "artifacts" / "v04" / rel
        new_b = new_p.read_text(encoding="utf-8", errors="replace") if new_p.exists() else ""
        if new_b == old_b:
            comparison[rel]["verdict"] = "byte-identical"
        elif old_b and new_b.startswith(old_b):
            comparison[rel]["verdict"] = "appended-to"
    rec = {
        "classification": "PRE_FREEZE_EXECUTION_NONAUTHORITATIVE",
        "reason": "ordering-provenance-defect: executed-before-corrected-FOUNDATION_FROZEN",
        "rule": "retained-for-provenance-forbidden-from-gates-and-downstream",
        "utc": utcnow(),
        "comparison": comparison,
        "authoritative": "post-freeze-rerun-outputs-only",
    }
    (freeze / "SUPERSEDED_PRE_FREEZE.json").write_text(
        json.dumps(rec, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    log.append({"step": "STEP-F-11", "name": "supersede", "status": "PASS",
                "detail": comparison})
    return rec


def emit_foundation(log):
    """F-10: emit FOUNDATION_FROZEN with scope + pending-execution list."""
    print("STEP-F-10: emitting FOUNDATION_FROZEN with explicit scope")
    cert = {
        "experiment": "SPLAY-AM-DECIDE-v0.4",
        "gate": "FOUNDATION_FROZEN",
        "utc": utcnow(),
        "scope": "freeze-contract-inputs-immutable: parent-package, bridge-bytes(L3)/L2-block-record, prereg-content, manifest, snapshot, PHASE-00/01-evidence",
        "gates_closed_here": ["FOUNDATION_FROZEN"],
        "gates_evidence_ready": ["SURVIVOR_IDENTITY_VERIFIED", "BATTLEFIELD_VERIFIED"],
        "pending_execution_gates": ["BRIDGE_SOURCES_VERIFICATION-PHASE02", "FORMAL_KERNEL_FROZEN-PHASE03",
                                    "PSC_DUAL_FREEZE-PHASE04", "proof-mutant-suite-execution",
                                    "PSC-implementation-conformance", "lean-toolchain-compile-agreement"],
        "no_theorem_facing_before": "all-pending-execution-gates-green",
        "checks": log,
    }
    out = REPO_ROOT / "artifacts" / "v04" / "freeze" / "FOUNDATION_FROZEN.json"
    out.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return cert


def run_freeze(parent_dir):
    """Execute the full freeze contract; return certs or raise."""
    log = []
    parent = Path(parent_dir)
    if not parent.is_dir():
        raise FreezeError("parent dir missing: %s" % parent)
    print("FREEZE: start (WorkPlan Phase 1 recovery; read-only + freeze writes)")
    print("STEP-F-00: rerunning PHASE-00 checks from current foundation")
    stashed = stash_pre_freeze()
    cert00 = run_phase00.run_phase00(str(parent))
    log.append({"step": "STEP-F-00", "name": "phase00_rerun", "status": "PASS",
                "detail": "%d checks" % len(cert00["checks"])})
    freeze_parent_package(parent, log)
    verify_downstream_identities(parent, log)
    verify_lifecycle_legality(parent, log)
    verify_bridge_manifest(log)
    verify_prereg_content(log)
    write_snapshot(log)
    write_manifest(log)
    verify_manifest(log)
    verify_prefix(log)
    print("STEP-F-00B: rerunning PHASE-01 checks from the frozen foundation")
    try:
        cert01 = run_phase01.run_phase01(str(parent))
    except run_phase01.Phase01Error as e:
        raise FreezeError("phase01 rerun failed: %s" % e)
    log.append({"step": "STEP-F-00B", "name": "phase01_rerun", "status": "PASS",
                "detail": "%d checks" % len(cert01["checks"])})
    cert = emit_foundation(log)
    write_superseded(stashed, log)
    return cert


def main(argv=None):
    """CLI entry: parse args, run freeze, emit PASS/FAIL, exit accordingly."""
    print("FREEZE_FOUNDATION: start")
    ap = argparse.ArgumentParser(description="Phase-00 freeze repair orchestrator")
    ap.add_argument("--parent-dir", default=str(REPO_ROOT.parent / "parent-ref"),
                    help="read-only parent clone directory")
    args = ap.parse_args(argv)
    try:
        cert = run_freeze(args.parent_dir)
    except (FreezeError, run_phase00.Phase00Error, run_phase01.Phase01Error) as e:
        print("FREEZE_FAIL: %s" % e)
        return 1
    print("FOUNDATION_FROZEN: %d freeze checks green; scope=%s"
          % (len(cert["checks"]), cert["scope"][:60]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
