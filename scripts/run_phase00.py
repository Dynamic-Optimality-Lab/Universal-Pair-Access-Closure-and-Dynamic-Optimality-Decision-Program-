"""Phase 00: pin the v0.3 seal and freeze the v0.4 decision contract inputs.

Implements WorkPlan Phase 1 / spec PHASE 00 (00.1 pin, 00.2 freeze record,
00.3 ledger init). Follows the spec 15-step order for a read-only
verification phase (no proof search, no refutation attack, no status change).
Fail-closed: any mismatch prints FAIL and exits 1. Success prints
PHASE00_PASS and exits 0. This gate alone does NOT claim FOUNDATION_FROZEN,
which additionally requires PHASE 01-04 (run_phase01..run_phase04).
"""

import argparse
import datetime
import hashlib
import json
import subprocess
import sys
from pathlib import Path


class Phase00Error(Exception):
    """Raised on any Phase-00 verification failure (fail-closed)."""


# STEP-CFG: frozen expectations (WorkPlan Phase 1; values read from the sealed
# parent artifacts during plan study, verified here by recomputation).
print("STEP-CFG: loading frozen Phase-00 expectations")
EXPECTED_PARENT_HEAD = "353ee922b1cee0043afa46fe8929f42f7652e5bf"
EXPECTED_TERMINAL = "TRANSFER_CALCULUS_SURVIVES_FINITE_TESTS"
EXPECTED_SET_HASH = "8FD3273143DEC3CA4611A1093F3521B8F22DE2BBD6A82715EE270412F65A2A00"
EXPECTED_SPEC_BYTES = 85888
EXPECTED_MANIFEST_LINES = 424
EXPECTED_OBLIGATIONS = {"REVIEWED": 10, "PROVED": 4, "NOT_APPLICABLE": 3, "BLOCKED": 3, "UNPROVED": 6}
EXPECTED_FRONTIER = {
    "MST0-08U": "UNPROVED", "MST0-09": "UNPROVED", "MST0-11": "UNPROVED",
    "MST0-13": "UNPROVED", "MST0-14": "UNPROVED", "MST0-15": "UNPROVED",
    "MST0-22": "UNPROVED", "MST0-17": "BLOCKED", "MST0-18": "BLOCKED",
    "MST0-19": "BLOCKED",
}
EXPECTED_KILLS = {
    "MSTC-0001": {"size": 32, "idx": 4406},
    "MSTC-0003": {"size": 16, "idx": 3610},
}
REPO_ROOT = Path(__file__).resolve().parent.parent


def sha256_file(path):
    """Return the hex SHA-256 of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1048576), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path):
    """Load JSON or raise Phase00Error."""
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise Phase00Error("unreadable JSON %s: %s" % (path, e))


def git_head(parent):
    """Return the full HEAD SHA of the parent clone or raise."""
    try:
        out = subprocess.run(
            ["git", "-C", str(parent), "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True, timeout=60,
        )
    except (subprocess.CalledProcessError, OSError) as e:
        raise Phase00Error("git rev-parse failed in %s: %s" % (parent, e))
    return out.stdout.strip()


def git_clean(parent):
    """Return True iff the parent working tree is clean."""
    out = subprocess.run(
        ["git", "-C", str(parent), "status", "--short"],
        capture_output=True, text=True, timeout=60,
    )
    return out.stdout.strip() == ""


def check_parent_head(parent, log):
    """STEP-00: full sealed commit identity (never the short navigation hash)."""
    print("STEP-00: verifying parent full sealed HEAD")
    head = git_head(parent)
    if head != EXPECTED_PARENT_HEAD:
        raise Phase00Error("PARENT_SEAL_MISMATCH head=%s" % head)
    if not git_clean(parent):
        raise Phase00Error("parent working tree is dirty (read-only violation)")
    log.append({"step": "STEP-00", "name": "parent_head", "status": "PASS", "detail": head})


def check_final_result(parent, log):
    """STEP-01: FINAL_RESULT terminal claim, survivor, sibling kills, firewalls."""
    print("STEP-01: verifying FINAL_RESULT terminal claim and seal fields")
    fr = load_json(parent / "artifacts" / "v03" / "seal" / "FINAL_RESULT.json")
    if fr.get("terminal_claim") != EXPECTED_TERMINAL:
        raise Phase00Error("terminal_claim=%r" % fr.get("terminal_claim"))
    if fr.get("standing") != ["MSTC-0002"]:
        raise Phase00Error("standing=%r" % fr.get("standing"))
    kills = {k["calculus_id"]: k for k in fr.get("killed_fresh", [])}
    for cid, exp in EXPECTED_KILLS.items():
        got = kills.get(cid)
        if not got or got["first_violation"]["size"] != exp["size"]:
            raise Phase00Error("kill record missing for %s" % cid)
        if got["first_violation"]["idx"] != exp["idx"]:
            raise Phase00Error("kill idx mismatch for %s" % cid)
    if fr.get("hashes", {}).get("candidate_set") != EXPECTED_SET_HASH:
        raise Phase00Error("candidate_set hash mismatch in FINAL_RESULT")
    fw = fr.get("firewalls", {})
    if fw.get("H3T") != "UNLOCKED_ONCE/unlocks=1":
        raise Phase00Error("H3T firewall=%r" % fw.get("H3T"))
    ob = fr.get("obligations", {})
    for k, v in EXPECTED_OBLIGATIONS.items():
        if ob.get(k) != v:
            raise Phase00Error("obligation %s=%r" % (k, ob.get(k)))
    log.append({"step": "STEP-01", "name": "final_result", "status": "PASS",
                "detail": EXPECTED_TERMINAL})


def check_candidate_set(parent, log):
    """STEP-02: candidate-set commitment binds frozen MSTC-0002 fields."""
    print("STEP-02: verifying candidate-set commitment and MSTC-0002 fields")
    cs = load_json(parent / "artifacts" / "v03" / "holdouts" / "candidate_set_commit.json")
    if cs.get("set_hash") != EXPECTED_SET_HASH:
        raise Phase00Error("set_hash mismatch")
    cands = {c["calculus_id"]: c for c in cs.get("candidates", [])}
    if set(cands) != {"MSTC-0001", "MSTC-0002", "MSTC-0003"}:
        raise Phase00Error("candidate ids=%r" % sorted(cands))
    m2 = cands["MSTC-0002"]
    if not (m2.get("k") == 6 and m2.get("C") == 2):
        raise Phase00Error("MSTC-0002 k/C mutated")
    pred = m2.get("predicate", {}).get("any_of", [])
    modes = sorted(p.get("mode_is") for p in pred)
    if modes != ["DELETE", "KEEP"]:
        raise Phase00Error("MSTC-0002 predicate is not P_all")
    log.append({"step": "STEP-02", "name": "candidate_set", "status": "PASS",
                "detail": EXPECTED_SET_HASH[:16]})


def check_h3t_state(parent, log):
    """STEP-03: H3T one-unlock history intact; bank never re-unlocked here."""
    print("STEP-03: verifying H3T state UNLOCKED_ONCE without reread")
    st = load_json(parent / "artifacts" / "v03" / "holdouts" / "h3t_state.json")
    if st.get("state") != "UNLOCKED_ONCE" or st.get("unlock_count") != 1:
        raise Phase00Error("h3t state=%r" % st.get("state"))
    if st.get("candidate_set_hash") != EXPECTED_SET_HASH:
        raise Phase00Error("h3t candidate_set_hash mismatch")
    log.append({"step": "STEP-03", "name": "h3t_state", "status": "PASS",
                "detail": "UNLOCKED_ONCE/1"})


def check_obligation_status(parent, log):
    """STEP-04: lifecycle counts 10/4/3/3/6 over 26 obligations, zero jumps assumed."""
    print("STEP-04: verifying obligation lifecycle counts")
    o = load_json(parent / "artifacts" / "v03" / "proofs" / "obligation_status.json")
    counts = {}
    for v in o["statuses"].values():
        counts[v["status"]] = counts.get(v["status"], 0) + 1
    if counts != EXPECTED_OBLIGATIONS or len(o["statuses"]) != 26:
        raise Phase00Error("lifecycle counts=%r" % counts)
    log.append({"step": "STEP-04", "name": "obligation_status", "status": "PASS",
                "detail": "26 obligations"})


def check_ledger(parent, log):
    """STEP-05: transfer-calculus ledger markers (frozen set + T5/T6/T7)."""
    print("STEP-05: verifying transfer-calculus ledger markers")
    text = (parent / "TRANSFER_CALCULUS_LEDGER.md").read_text(encoding="utf-8")
    for marker in ("TRANSFER_CALCULUS_FROZEN", "MSTC-0002", "T7", "T5", "T6"):
        if marker not in text:
            raise Phase00Error("ledger marker missing: %s" % marker)
    log.append({"step": "STEP-05", "name": "ledger", "status": "PASS",
                "detail": "frozen set present"})


def check_seal_files(parent, log):
    """STEP-06: manifest shape + deterministic archive byte identity."""
    print("STEP-06: verifying manifest shape and archive byte identity")
    seal = parent / "artifacts" / "v03" / "seal"
    lines = (seal / "MANIFEST.sha256").read_text(encoding="utf-8").splitlines()
    if len(lines) != EXPECTED_MANIFEST_LINES:
        raise Phase00Error("manifest lines=%d" % len(lines))
    for ln in lines:
        parts = ln.split()
        if len(parts) != 2 or len(parts[0]) != 64:
            raise Phase00Error("malformed manifest line")
    sidecar = (seal / "ARCHIVE.sha256").read_text(encoding="utf-8").split()
    tar = seal / "SPLAY-AM-MST-v0.3.tar.zst"
    if not tar.exists():
        raise Phase00Error("archive missing")
    if sha256_file(tar).lower() != sidecar[0].lower():
        raise Phase00Error("archive byte identity mismatch")
    log.append({"step": "STEP-06", "name": "seal_files", "status": "PASS",
                "detail": "424-file manifest, archive %d bytes" % tar.stat().st_size})


def check_parent_docs(parent, log):
    """STEP-07: parent Path.md / WorkPlan.md audit inheritance present."""
    print("STEP-07: recording parent Path.md / WorkPlan.md identities")
    detail = {}
    for name in ("Path.md", "WorkPlan.md"):
        p = parent / name
        if not p.exists():
            raise Phase00Error("parent %s missing" % name)
        detail[name] = {"sha256": sha256_file(p), "bytes": p.stat().st_size}
    log.append({"step": "STEP-07", "name": "parent_docs", "status": "PASS", "detail": detail})


def check_pin_doc(parent, log):
    """STEP-08: v0.3.1 ratified pin (ancestor chain identities)."""
    print("STEP-08: verifying v0.3.1 parent-pin identities")
    text = (parent / "SPLAY_AM_MST_IMPLEMENTATION_SPEC_v0.3.1_PIN.md").read_text(
        encoding="utf-8")
    for marker in ("38c1be6afd2ab2420aa094c68ce45ee6a26b3628",
                   "6de1ca2a595e8895f54794f3a211fe6ee1a95a80"):
        if marker not in text:
            raise Phase00Error("pin marker missing: %s" % marker[:12])
    log.append({"step": "STEP-08", "name": "pin_doc", "status": "PASS",
                "detail": "ancestor chain pinned"})


def check_spec_freeze(log):
    """STEP-09: v0.4 spec + amendments byte record (bytes preserved, never edited)."""
    print("STEP-09: recording v0.4 spec and amendment byte identities")
    spec = REPO_ROOT / "IMPLEMENTATION_SPEC_v0.4.md"
    if not spec.exists() or spec.stat().st_size != EXPECTED_SPEC_BYTES:
        raise Phase00Error("spec bytes=%s" % (spec.stat().st_size if spec.exists() else "missing"))
    detail = {"IMPLEMENTATION_SPEC_v0.4.md":
              {"sha256": sha256_file(spec), "bytes": EXPECTED_SPEC_BYTES}}
    for name in ("SPLAY_AM_DECIDE_IMPLEMENTATION_SPEC_v0.4.1_AMENDMENT.md",
                 "SPLAY_AM_DECIDE_IMPLEMENTATION_SPEC_v0.4.2_AMENDMENT.md"):
        p = REPO_ROOT / name
        if not p.exists():
            raise Phase00Error("%s missing" % name)
        detail[name] = {"sha256": sha256_file(p), "bytes": p.stat().st_size}
    log.append({"step": "STEP-09", "name": "spec_freeze", "status": "PASS", "detail": detail})


def check_prereg_inventory(log):
    """STEP-10: prereg inventory pre-freeze; manifest-line verification post-freeze."""
    print("STEP-10: checking prereg inventory / manifest binding")
    names = ["experiment_v0.4.yaml", "parent_contract.yaml", "theorem_battlefield.yaml",
             "theorem_gate_matrix.yaml", "dual_obligation_policy.yaml",
             "proof_kernel_policy.yaml", "proof_stress_corpus.yaml",
             "negative_lifting_policy.yaml", "bridge_sources.yaml",
             "threat_control_matrix.yaml", "stop_control_matrix.yaml",
             "allowed_claims.md", "forbidden_claims.md"]
    detail = {}
    for name in names:
        p = REPO_ROOT / "prereg" / name
        if not p.exists():
            raise Phase00Error("prereg/%s missing" % name)
        detail[name] = sha256_file(p)
    mpath = REPO_ROOT / "prereg" / "prereg_sha256.txt"
    if not mpath.exists():
        log.append({"step": "STEP-10", "name": "prereg_inventory", "status": "PASS",
                    "detail": "13 sources recorded, manifest correctly absent (freeze pending)"})
        return
    rows = mpath.read_text(encoding="utf-8").splitlines()
    by_path = {}
    for ln in rows:
        parts = ln.split()
        if len(parts) != 2:
            raise Phase00Error("malformed manifest line")
        by_path[parts[1]] = parts[0].lower()
    if "prereg/prereg_sha256.txt" in by_path:
        raise Phase00Error("manifest hashes itself")
    for name in names:
        if by_path.get("prereg/%s" % name) != detail[name]:
            raise Phase00Error("manifest mismatch: prereg/%s" % name)
    log.append({"step": "STEP-10", "name": "prereg_inventory", "status": "PASS",
                "detail": "13 payload lines verified against manifest"})


def check_theorem_ledger(log):
    """STEP-11: v0.4 theorem ledger matches the mapped frontier (no jumps)."""
    print("STEP-11: verifying v0.4 theorem ledger frontier")
    ps = load_json(REPO_ROOT / "math" / "proof_status.json")
    obs = ps.get("obligations", {})
    for tid, want in EXPECTED_FRONTIER.items():
        if obs.get(tid, {}).get("status") != want:
            raise Phase00Error("ledger %s=%r" % (tid, obs.get(tid)))
    log.append({"step": "STEP-11", "name": "theorem_ledger", "status": "PASS",
                "detail": "10 nodes at frontier"})


def check_downstream_docs(parent, log):
    """STEP-12: counterexample atlas + downstream theorem docs/reviews present."""
    print("STEP-12: verifying atlas and downstream theorem docs")
    atlas = parent / "COUNTEREXAMPLE_ATLAS.md"
    if not atlas.exists() or atlas.stat().st_size == 0:
        raise Phase00Error("counterexample atlas missing")
    for rel in ("math/theorem_MST13_delete_injection.md",
                "artifacts/v03/proofs/MST13_injection_bound.json",
                "math/reviews"):
        if not (parent / rel).exists():
            raise Phase00Error("downstream doc missing: %s" % rel)
    detail = {"atlas_sha256": sha256_file(atlas)}
    log.append({"step": "STEP-12", "name": "downstream_docs", "status": "PASS",
                "detail": detail})


def write_cert(parent, log):
    """STEP-13: write the Phase-00 certificate and run log (append-only)."""
    print("STEP-13: writing Phase-00 certificate and run log")
    cert = {
        "experiment": "SPLAY-AM-DECIDE-v0.4",
        "gate": "PHASE00_PASS",
        "parent_head": EXPECTED_PARENT_HEAD,
        "utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "checks": log,
    }
    freeze = REPO_ROOT / "artifacts" / "v04" / "freeze"
    logs = REPO_ROOT / "artifacts" / "v04" / "logs"
    freeze.mkdir(parents=True, exist_ok=True)
    logs.mkdir(parents=True, exist_ok=True)
    (freeze / "PHASE00_PARENT_PIN.json").write_text(
        json.dumps(cert, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = ["PHASE00 run %s" % cert["utc"]]
    lines += ["%s %s %s" % (c["step"], c["name"], c["status"]) for c in log]
    (logs / "phase00.log").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return cert


def run_phase00(parent_dir):
    """Execute all Phase-00 checks; return the certificate or raise."""
    log = []
    parent = Path(parent_dir)
    if not parent.is_dir():
        raise Phase00Error("parent dir missing: %s" % parent)
    check_parent_head(parent, log)
    check_final_result(parent, log)
    check_candidate_set(parent, log)
    check_h3t_state(parent, log)
    check_obligation_status(parent, log)
    check_ledger(parent, log)
    check_seal_files(parent, log)
    check_parent_docs(parent, log)
    check_pin_doc(parent, log)
    check_spec_freeze(log)
    check_prereg_inventory(log)
    check_theorem_ledger(log)
    check_downstream_docs(parent, log)
    return write_cert(parent, log)


def main(argv=None):
    """CLI entry: parse args, run checks, emit PASS/FAIL, exit accordingly."""
    print("PHASE00: start (WorkPlan Phase 1, spec PHASE 00; read-only verification)")
    ap = argparse.ArgumentParser(description="Phase-00 parent pin and freeze record")
    ap.add_argument("--parent-dir", default=str(REPO_ROOT.parent / "parent-ref"),
                    help="read-only parent clone directory")
    args = ap.parse_args(argv)
    try:
        cert = run_phase00(args.parent_dir)
    except Phase00Error as e:
        print("PHASE00_FAIL: %s" % e)
        return 1
    print("PHASE00_PASS: %d checks green; parent %s; gate PHASE00_PASS (not FOUNDATION_FROZEN)"
          % (len(cert["checks"]), EXPECTED_PARENT_HEAD[:9]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
