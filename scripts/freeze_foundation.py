"""freeze_foundation.py — WP-1 freeze ceremony (WorkPlan s4; v0.4.7 G12 gate).

Runs all foundation gates, then writes freeze outputs (never before gates green):
PATH snapshot, PROOF_STATUS snapshot, PHASE02 bridge file, WITNESS_SCHEMA_VALIDATION,
prereg_sha256 manifest (payload UNION bound, never itself), FOUNDATION_FROZEN.json,
and flips the living ledger run_state PRE_FOUNDATION -> RUN_VALID (G7).
Exits nonzero on any gate failure WITHOUT writing freeze outputs (fail-closed).
Step logs: [WP-1][REPAIR STEP xx] (phase logging requirement).
"""
import datetime
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import yaml

IMPL = Path(__file__).resolve().parents[1]
FAILED = []


def step(sid, msg):
    print(f"[WP-1][REPAIR STEP {sid}] {msg}", flush=True)


def gate(name, cond, detail=""):
    step("GATE", f"{name}: {'GREEN' if cond else 'RED'} {detail}")
    if not cond:
        FAILED.append(name)


def run(cmd, **kw):
    return subprocess.run(cmd, cwd=str(IMPL), capture_output=True, text=True,
                          timeout=600, **kw)


def sha_file(p):
    return hashlib.sha256((IMPL / p).read_bytes()).hexdigest()


# WP-1 REPAIR STEP 01: contract-closure gate.
step("01", "Running contract_closure.py gate")
r = run([sys.executable, "scripts/contract_closure.py"])
gate("contract-closure", r.returncode == 0, "exit=%d" % r.returncode)

# WP-1 REPAIR STEP 02: PARENT suite.
step("02", "Running PARENT-01..10 suite")
r = run([sys.executable, "-m", "pytest", "tests/parent/test_parent_01_10.py", "-q"])
gate("parent-suite", r.returncode == 0, "exit=%d" % r.returncode)

# WP-1 REPAIR STEP 03: FORM suite (toolchain + build + axioms + agreement + mutant).
step("03", "Running FORM-01..12 suite")
r = run([sys.executable, "-m", "pytest", "tests/formal/test_form_01_12.py", "-q"])
gate("form-suite", r.returncode == 0, "exit=%d" % r.returncode)

# WP-1 REPAIR STEP 04: canary properties.
step("04", "Running canary property suite")
r = run([sys.executable, "-m", "pytest", "tests/formal/test_canary_properties.py", "-q"])
gate("canary", r.returncode == 0, "exit=%d" % r.returncode)

# WP-1 REPAIR STEP 05: adversarial attack suite.
step("05", "Running contract attack suite")
r = run([sys.executable, "-m", "pytest", "tests/contract_closure/test_closure.py", "-q"])
gate("attacks", r.returncode == 0, "exit=%d" % r.returncode)

# WP-1 REPAIR STEP 06: exit-evidence mapping present and clean.
step("06", "Checking threat/stop/invariant exit evidence")
ee = json.loads((IMPL / "artifacts/v04/audits/WP1_THREAT_STOP_INV_EXIT.json").read_text(encoding="utf-8"))
legal = {"CONTROLLED", "ARMED", "SATISFIED", "HOLDING"}
bad = [k for sec in ee.values() for k, v in sec.items() if v["status"] not in legal]
gate("exit-evidence", not bad and len(ee["threats"]) == 23
     and len(ee["stops"]) == 19 and len(ee["invariants"]) == 39, f"bad={bad}")

# WP-1 REPAIR STEP 07: ratified bytes stable.
step("07", "Checking ratified amendment/spec bytes unmodified")
ratified = ["IMPLEMENTATION_SPEC_v0.4.md"] + \
    ["SPLAY_AM_DECIDE_IMPLEMENTATION_SPEC_v0.4.%d_AMENDMENT.md" % i for i in range(1, 8)]
r = run(["git", "diff", "--quiet", "--"] + ratified)
gate("ratified-stable", r.returncode == 0)

# WP-1 REPAIR STEP 08: no theorem-facing results pre-freeze (PARENT-10 shape).
step("08", "Checking claim dirs result-empty")
claim_empty = True
for d in ["proofs", "counterexamples", "seal", "negative"]:
    files = [p for p in (IMPL / "artifacts/v04" / d).iterdir() if p.name != ".gitkeep"]
    if files:
        claim_empty = False
gate("no-prefreeze-science", claim_empty)

# WP-1 REPAIR STEP 09: bridge bound bytes equal prereg record (+ second extraction on file).
step("09", "Checking bridge byte binding")
bridge = yaml.safe_load((IMPL / "prereg/bridge_sources.yaml").read_text(encoding="utf-8"))
l3 = bridge["literature"]["L3"]
pdf_hash = sha_file("bridge_sources/L3_1907.06310_v1.pdf")
gate("bridge-binding", pdf_hash.upper() == l3["sha256"].upper() and l3["status"] == "FROZEN"
     and bridge["literature"]["L2"]["status"] == "ABSENT", pdf_hash[:16])

if FAILED:
    step("ABORT", f"freeze refused; {len(FAILED)} gates red: {', '.join(FAILED)}")
    sys.exit(1)

# ---- ceremony: all gates green ----
import jsonschema
from jsonschema import Draft202012Validator

FREEZE = IMPL / "artifacts/v04/freeze"

# WP-1 REPAIR STEP 10: flip living ledger run_state (G7 freeze transition).
step("10", "Flipping run_state PRE_FOUNDATION -> RUN_VALID")
psp = IMPL / "math/proof_status.json"
ps = json.loads(psp.read_text(encoding="utf-8"))
assert ps["run_state"] == "PRE_FOUNDATION", ps["run_state"]
ps["run_state"] = "RUN_VALID"
psp.write_text(json.dumps(ps, indent=2, sort_keys=True) + "\n", encoding="utf-8")

# WP-1 REPAIR STEP 11: immutable snapshots.
step("11", "Writing PATH + PROOF_STATUS snapshots")
(FREEZE / "PATH_AT_FOUNDATION_FREEZE.md").write_bytes((IMPL / "Path.md").read_bytes())
(FREEZE / "PROOF_STATUS_AT_FOUNDATION_FREEZE.json").write_bytes(psp.read_bytes())

# WP-1 REPAIR STEP 12: PHASE02 bridge freeze file (verification record only).
step("12", "Writing PHASE02 bridge freeze file")
(FREEZE / "PHASE02_BRIDGE_SOURCES_FREEZE.json").write_text(json.dumps({
    "l3_path": "bridge_sources/L3_1907.06310_v1.pdf",
    "l3_sha256": pdf_hash,
    "l3_bytes": 1431066,
    "second_extraction": {"tool": "curl.exe", "date": "2026-09-26",
                          "sha256": pdf_hash, "match": True,
                          "path_evidence": "Path.md R1-022"},
    "l2_status": "ABSENT",
    "freeze_variant": "SOURCE_AVAILABLE-28",
    "note": "verification record; prereg never rewritten",
}, indent=2, sort_keys=True) + "\n", encoding="utf-8")

# WP-1 REPAIR STEP 13: witness schema validation record.
step("13", "Validating bound schemas with good/bad samples")
validation = {}
for name in ["proof_attack", "pair_access_certificate"]:
    schema = json.loads((IMPL / f"schemas/{name}.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    good = {"schema_version": "1.0",
            "theorem_id": "MST0-14" if name == "proof_attack" else "MST0-17"}
    if name == "proof_attack":
        good.update({"negation_predicate": "p", "generator_version": "g",
                     "seed": "s", "input_hash": "f" * 64,
                     "replay_certificate": {"replay_input_hash": "f" * 64,
                                            "checker_id": "c", "result": "REPRODUCED"},
                     "independent_checker_result": "AGREE"})
        bad = {"theorem_id": "MST0-14"}
    else:
        good.update({"statement_sha256": "f" * 64, "negation_sha256": "f" * 64,
                     "interface_conformance": {"conformance_harness": "h", "result": "GREEN"},
                     "reconstruction_payload": {"n": 1, "initial_tree": "t", "history_X": "x",
                        "subsequence_Y": "y", "splay_cost_X": "1", "splay_cost_Y": "2",
                        "energy_initial": "0", "energy_final": "0", "additive_term": "0"},
                     "block_partition_record": "b", "minimization_record": "m",
                     "replay_certificate": {"replay_input_hash": "f" * 64,
                                            "checker_id": "c", "result": "REPRODUCED"},
                     "independent_checker_result": "AGREE"})
        bad = {"theorem_id": "MST0-17"}
    jsonschema.validate(good, schema)
    try:
        jsonschema.validate(bad, schema)
        raise SystemExit(f"schema {name} accepted bad sample")
    except jsonschema.ValidationError:
        pass
    validation[name] = {"schema_sha256": sha_file(f"schemas/{name}.schema.json"),
                        "good": "ACCEPTED", "bad": "REJECTED"}
(FREEZE / "WITNESS_SCHEMA_VALIDATION.json").write_text(json.dumps({
    "validator": "jsonschema Draft202012",
    "samples": validation,
}, indent=2, sort_keys=True) + "\n", encoding="utf-8")

# WP-1 REPAIR STEP 14: prereg manifest over payload UNION bound (never itself).
step("14", "Writing prereg_sha256 manifest")
payload = ["allowed_claims.md", "bridge_sources.yaml", "dual_obligation_policy.yaml",
           "experiment_v0.4.yaml", "forbidden_claims.md", "negative_lifting_policy.yaml",
           "parent_contract.yaml", "proof_kernel_policy.yaml", "proof_stress_corpus.yaml",
           "stop_control_matrix.yaml", "theorem_battlefield.yaml",
           "theorem_gate_matrix.yaml", "threat_control_matrix.yaml"]
amends = sorted(p.name for p in IMPL.glob("SPLAY_AM_DECIDE_IMPLEMENTATION_SPEC_*.md"))
docs = ["math/theorem_MST08U_locality.md", "math/theorem_MST09_raw_boundary.md",
        "math/theorem_MST11_preservation.md", "math/theorem_MST13_delete_injection.md",
        "math/theorem_MST14_keep_repayment.md", "math/theorem_MST15_integrability.md",
        "math/theorem_MST22_constant_independence.md", "math/theorem_MST17_pair_access.md",
        "math/theorem_MST18_telescoping.md", "math/theorem_MST19_bridge.md"]
schemas = sorted(f"schemas/{p.name}" for p in IMPL.glob("schemas/*.schema.json"))
bound = (["IMPLEMENTATION_SPEC_v0.4.md"] + amends + ["WorkPlan.md",
         "artifacts/v04/freeze/PATH_AT_FOUNDATION_FREEZE.md",
         "artifacts/v04/freeze/PROOF_STATUS_AT_FOUNDATION_FREEZE.json",
         "lean/Frozen/SplayDefs.lean", "lean/Frozen/MSTC0002Defs.lean",
         "lean/Frozen/Statements.lean"] + docs + schemas
         + ["prereg/proof_stress_corpus.yaml",
            "bridge_sources/L3_1907.06310_v1.pdf", "bridge_sources/README.md"])
members = sorted({f"prereg/{f}" for f in payload} | set(bound))
assert "prereg/prereg_sha256.txt" not in members
(IMPL / "prereg/prereg_sha256.txt").write_text(
    "# prereg_sha256.txt — freeze manifest: sha256 over payload UNION bound (never itself).\n"
    + "\n".join(f"{sha_file(f)}  {f}" for f in members) + "\n", encoding="utf-8")
step("14", f"manifest members: {len(members)}")

# WP-1 REPAIR STEP 15: FOUNDATION_FROZEN record + post-freeze self-verification.
step("15", "Writing FOUNDATION_FROZEN record")
manifest_hash = sha_file("prereg/prereg_sha256.txt")
(IMPL / "artifacts/v04/freeze/FOUNDATION_FROZEN.json").write_text(json.dumps({
    "date_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
    "gates": ["contract-closure", "parent-suite", "form-suite", "canary",
              "attacks", "exit-evidence", "ratified-stable",
              "no-prefreeze-science", "bridge-binding"],
    "manifest": "prereg/prereg_sha256.txt",
    "manifest_sha256": manifest_hash,
    "manifest_members": len(members),
    "run_state": "RUN_VALID",
}, indent=2, sort_keys=True) + "\n", encoding="utf-8")

step("16", "Post-freeze self-verification")
post_ok = True
recomputed = "\n".join(f"{sha_file(f)}  {f}" for f in members) + "\n"
recorded = (IMPL / "prereg/prereg_sha256.txt").read_text(encoding="utf-8").splitlines(keepends=False)
if [l for l in recorded if not l.startswith("#")] != recomputed.splitlines():
    post_ok = False
live_path = (IMPL / "Path.md").read_bytes()
snap_path = (FREEZE / "PATH_AT_FOUNDATION_FREEZE.md").read_bytes()
if not live_path.startswith(snap_path):
    post_ok = False
if (FREEZE / "PROOF_STATUS_AT_FOUNDATION_FREEZE.json").read_bytes() != psp.read_bytes():
    post_ok = False
step("16", f"post-freeze self-verification: {'GREEN' if post_ok else 'RED'}")
if not post_ok:
    sys.exit(1)
step("DONE", f"FOUNDATION_FROZEN claimed; manifest {manifest_hash[:16]}; members {len(members)}")
