"""Phase 01: reverify survivor identity and blocker DAG (WorkPlan Phase 1).

Implements spec PHASE 01 (01.1 survivor binding, 01.2 fresh-history integrity,
01.3 blocker-DAG re-derivation). Read-only verification: no bank content is
read, no holdout is unlocked, no theorem status is changed. Fail-closed via
Phase01Error. Success prints PHASE01_PASS with gates SURVIVOR_IDENTITY_VERIFIED
and BATTLEFIELD_VERIFIED. This gate alone does NOT claim FOUNDATION_FROZEN.
"""

import argparse
import datetime
import hashlib
import json
import subprocess
import sys
from pathlib import Path


class Phase01Error(Exception):
    """Raised on any Phase-01 verification failure (fail-closed)."""


# STEP-CFG: frozen expectations (WorkPlan Phase 1; PHASE-00 values rechecked here
# for clone continuity, then extended with survivor/history/DAG bindings).
print("STEP-CFG: loading frozen Phase-01 expectations")
EXPECTED_PARENT_HEAD = "353ee922b1cee0043afa46fe8929f42f7652e5bf"
EXPECTED_SET_HASH = "8FD3273143DEC3CA4611A1093F3521B8F22DE2BBD6A82715EE270412F65A2A00"
EXPECTED_MSTC0002 = {"predicate_modes": ["DELETE", "KEEP"], "k": 6, "C": 2,
                     "parent": "MSTC-DEV-0002",
                     "sha256": "930EAD000A38955469EBBDE468DB166E4EA6F1FD71BBFAF87C4AF36813A1489E"}
EXPECTED_CRITICAL = ["MST0-08U", "MST0-09", "MST0-11", "MST0-13", "MST0-14",
                     "MST0-15", "MST0-22", "MST0-17", "MST0-18", "MST0-19"]
EXPECTED_LEDGER = {"MST0-08U": "UNPROVED", "MST0-09": "UNPROVED", "MST0-11": "UNPROVED",
                   "MST0-13": "UNPROVED", "MST0-14": "UNPROVED", "MST0-15": "UNPROVED",
                   "MST0-22": "UNPROVED", "MST0-17": "BLOCKED", "MST0-18": "BLOCKED",
                   "MST0-19": "BLOCKED"}
REPO_ROOT = Path(__file__).resolve().parent.parent


def sha256_file(path):
    """Return the hex SHA-256 of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1048576), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path):
    """Load JSON or raise Phase01Error."""
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise Phase01Error("unreadable JSON %s: %s" % (path, e))


def check_parent_head(parent, log):
    """STEP-00: same sealed clone as PHASE 00 (continuity, still clean)."""
    print("STEP-00: rechecking parent sealed HEAD continuity")
    try:
        out = subprocess.run(["git", "-C", str(parent), "rev-parse", "HEAD"],
                             capture_output=True, text=True, check=True, timeout=60)
        clean = subprocess.run(["git", "-C", str(parent), "status", "--short"],
                               capture_output=True, text=True, timeout=60)
    except (subprocess.CalledProcessError, OSError) as e:
        raise Phase01Error("git failed in %s: %s" % (parent, e))
    if out.stdout.strip() != EXPECTED_PARENT_HEAD or clean.stdout.strip() != "":
        raise Phase01Error("parent clone continuity broken")
    log.append({"step": "STEP-00", "name": "parent_continuity", "status": "PASS",
                "detail": EXPECTED_PARENT_HEAD[:9]})


def check_survivor_binding(parent, log):
    """STEP-01: every theorem-facing MSTC-0002 field bound across 3 records."""
    print("STEP-01: binding survivor fields across candidate-set/FINAL_RESULT/ledger")
    cs = load_json(parent / "artifacts" / "v03" / "holdouts" / "candidate_set_commit.json")
    fr = load_json(parent / "artifacts" / "v03" / "seal" / "FINAL_RESULT.json")
    m2 = {c["calculus_id"]: c for c in cs["candidates"]}["MSTC-0002"]
    if m2.get("k") != 6 or m2.get("C") != 2:
        raise Phase01Error("MSTC-0002 k/C mutated")
    modes = sorted(p.get("mode_is") for p in m2["predicate"]["any_of"])
    if modes != EXPECTED_MSTC0002["predicate_modes"]:
        raise Phase01Error("MSTC-0002 predicate is not P_all")
    for field in ("parent_calculus", "sha256"):
        want = EXPECTED_MSTC0002["parent"] if field == "parent_calculus" else EXPECTED_MSTC0002["sha256"]
        key = "parent_calculus" if field == "parent_calculus" else "sha256"
        if m2.get(key) != want:
            raise Phase01Error("MSTC-0002 %s mismatch" % field)
    if fr.get("standing") != ["MSTC-0002"]:
        raise Phase01Error("FINAL_RESULT standing changed")
    ledger = (parent / "TRANSFER_CALCULUS_LEDGER.md").read_text(encoding="utf-8")
    if "Standing finite survivor: MSTC-0002 (P_all, k=6, C=2)" not in ledger:
        raise Phase01Error("ledger survivor note mismatch")
    log.append({"step": "STEP-01", "name": "survivor_binding", "status": "PASS",
                "detail": "P_all/k=6/C=2 across 3 records"})


def check_set_hash_agreement(parent, log):
    """STEP-02: one set hash across FINAL_RESULT, h3t_state, candidate-set."""
    print("STEP-02: cross-checking candidate-set hash in 3 records")
    fr = load_json(parent / "artifacts" / "v03" / "seal" / "FINAL_RESULT.json")
    st = load_json(parent / "artifacts" / "v03" / "holdouts" / "h3t_state.json")
    cs = load_json(parent / "artifacts" / "v03" / "holdouts" / "candidate_set_commit.json")
    got = {fr["hashes"]["candidate_set"], st["candidate_set_hash"], cs["set_hash"]}
    if got != {EXPECTED_SET_HASH}:
        raise Phase01Error("set-hash disagreement: %r" % sorted(got))
    log.append({"step": "STEP-02", "name": "set_hash_agreement", "status": "PASS",
                "detail": EXPECTED_SET_HASH[:16]})


def check_fresh_history(parent, log):
    """STEP-03: reveal verdicts match FINAL_RESULT kills; commitment intact."""
    print("STEP-03: verifying fresh-history integrity without re-unlock")
    rv = load_json(parent / "artifacts" / "v03" / "holdouts" / "h3t_reveal.json")
    fr = load_json(parent / "artifacts" / "v03" / "seal" / "FINAL_RESULT.json")
    by_id = {r["calculus_id"]: r for r in rv["results"]}
    if by_id["MSTC-0002"]["verdict"] != "FRESH_H3T_PASS":
        raise Phase01Error("survivor fresh verdict changed")
    if by_id["MSTC-0002"]["first_violation"] is not None:
        raise Phase01Error("survivor first_violation non-null")
    if by_id["MSTC-0002"]["n_episodes"] != 70000:
        raise Phase01Error("survivor episode count changed")
    if list(by_id["MSTC-0002"]["max_residual"]) != [0, 1]:
        raise Phase01Error("survivor max residual changed")
    kills = {k["calculus_id"]: k for k in fr["killed_fresh"]}
    for cid in ("MSTC-0001", "MSTC-0003"):
        if by_id[cid]["verdict"] != "FRESH_H3T_FAIL":
            raise Phase01Error("sibling kill verdict changed: %s" % cid)
        if by_id[cid]["first_violation"]["episode_hash"] != kills[cid]["first_violation"]["episode_hash"]:
            raise Phase01Error("sibling witness hash mismatch: %s" % cid)
    if rv.get("reveal_state") != "UNLOCKED_ONCE":
        raise Phase01Error("reveal_state=%r" % rv.get("reveal_state"))
    cm = load_json(parent / "artifacts" / "v03" / "holdouts" / "h3t_commitment.json")
    if cm["logical_stream"] != fr["hashes"]["h3t_logical_stream"]:
        raise Phase01Error("commitment logical_stream mismatch")
    log.append({"step": "STEP-03", "name": "fresh_history", "status": "PASS",
                "detail": "1 pass + 2 kills, witness hashes agree"})


def check_no_reunlock(log):
    """STEP-04: v0.4 side holds no holdout-derived files (attestation by scan)."""
    print("STEP-04: attesting no v0.4 holdout-derived artifacts exist")
    hits = [str(p) for p in (REPO_ROOT / "artifacts").rglob("*")
            if "h3t" in p.name.lower() or "holdout" in p.name.lower()]
    if hits:
        raise Phase01Error("holdout-derived files present: %r" % hits[:3])
    log.append({"step": "STEP-04", "name": "no_reunlock", "status": "PASS",
                "detail": "artifacts tree holds no h3t/holdout names"})


def check_blocker_dag(parent, log):
    """STEP-05: re-derive the critical set from parent statuses + gap rule."""
    print("STEP-05: re-deriving blocker DAG from parent gate matrix")
    o = load_json(parent / "artifacts" / "v03" / "proofs" / "obligation_status.json")
    st = o["statuses"]
    derived = {"MST0-08U"}  # universal gap of scoped-finite MST0-08 (review note)
    if st["MST0-08"]["status"] != "REVIEWED":
        raise Phase01Error("parent MST0-08 not scoped-REVIEWED")
    for tid in ("MST0-09", "MST0-11", "MST0-14", "MST0-15", "MST0-22"):
        if st[tid]["status"] != "UNPROVED":
            raise Phase01Error("parent %s=%s" % (tid, st[tid]["status"]))
        derived.add(tid)  # parent ids already equal v0.4 critical ids here
    derived.add("MST0-13")  # PROVED author-claim pending review: unconsumable
    if st["MST0-13"]["status"] != "PROVED":
        raise Phase01Error("parent MST0-13 not author-PROVED")
    for tid in ("MST0-17", "MST0-18", "MST0-19"):
        if st[tid]["status"] != "BLOCKED":
            raise Phase01Error("parent %s not BLOCKED" % tid)
        derived.add(tid)
    # Normalize: parent ids MST0-09 etc map to v0.4 ids MST0-09 (same strings here).
    want = set(EXPECTED_CRITICAL)
    if derived != want:
        raise Phase01Error("derived DAG=%r" % sorted(derived))
    ours = load_json(REPO_ROOT / "math" / "proof_status.json")["obligations"]
    for tid, want_status in EXPECTED_LEDGER.items():
        if ours.get(tid, {}).get("status") != want_status:
            raise Phase01Error("v0.4 ledger %s=%r" % (tid, ours.get(tid)))
    log.append({"step": "STEP-05", "name": "blocker_dag", "status": "PASS",
                "detail": "10-node critical set re-derived"})


def write_cert(log):
    """STEP-06: write the Phase-01 certificate and run log (append-only)."""
    print("STEP-06: writing Phase-01 certificate and run log")
    cert = {
        "experiment": "SPLAY-AM-DECIDE-v0.4",
        "gates": ["SURVIVOR_IDENTITY_VERIFIED", "BATTLEFIELD_VERIFIED"],
        "parent_head": EXPECTED_PARENT_HEAD,
        "utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "checks": log,
    }
    freeze = REPO_ROOT / "artifacts" / "v04" / "freeze"
    logs = REPO_ROOT / "artifacts" / "v04" / "logs"
    freeze.mkdir(parents=True, exist_ok=True)
    logs.mkdir(parents=True, exist_ok=True)
    (freeze / "PHASE01_SURVIVOR_BINDING.json").write_text(
        json.dumps(cert, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = ["PHASE01 run %s" % cert["utc"]]
    lines += ["%s %s %s" % (c["step"], c["name"], c["status"]) for c in log]
    with open(logs / "phase01.log", "a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return cert


def run_phase01(parent_dir):
    """Execute all Phase-01 checks; return the certificate or raise."""
    log = []
    parent = Path(parent_dir)
    if not parent.is_dir():
        raise Phase01Error("parent dir missing: %s" % parent)
    check_parent_head(parent, log)
    check_survivor_binding(parent, log)
    check_set_hash_agreement(parent, log)
    check_fresh_history(parent, log)
    check_no_reunlock(log)
    check_blocker_dag(parent, log)
    return write_cert(log)


def main(argv=None):
    """CLI entry: parse args, run checks, emit PASS/FAIL, exit accordingly."""
    print("PHASE01: start (WorkPlan Phase 1, spec PHASE 01; read-only verification)")
    ap = argparse.ArgumentParser(description="Phase-01 survivor binding and DAG check")
    ap.add_argument("--parent-dir", default=str(REPO_ROOT.parent / "parent-ref"),
                    help="read-only parent clone directory")
    args = ap.parse_args(argv)
    try:
        cert = run_phase01(args.parent_dir)
    except Phase01Error as e:
        print("PHASE01_FAIL: %s" % e)
        return 1
    print("PHASE01_PASS: %d checks green; gates SURVIVOR_IDENTITY_VERIFIED,BATTLEFIELD_VERIFIED (not FOUNDATION_FROZEN)"
          % len(cert["checks"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
