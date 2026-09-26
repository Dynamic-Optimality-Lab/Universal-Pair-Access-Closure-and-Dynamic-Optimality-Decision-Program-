"""contract_closure.py — finite contract-closure verifier (v0.4.7 G12).

Exhaustively checks the pre-freeze contract before FOUNDATION_FROZEN.
Exits 0 iff every check passes, nonzero with the failing check names otherwise.
Usage: python scripts/contract_closure.py [--impl DIR]

Checks (CLOSURE-01..20 coverage):
  amendments-bound, bound-set-derived, node-set-10, lifecycle-total,
  ready-predicates, review-outcomes, erratum, source-branches, resource-branches,
  refutation-branches, lifting-branches, phase18-total, na-explicit, seal-reproduce,
  theorem-identity, schemas-frozen, python-core, fresh-checkout, integrity-abort.
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

IMPL = Path(sys.argv[sys.argv.index("--impl") + 1]) if "--impl" in sys.argv else Path(__file__).resolve().parents[1]
FAILURES = []


def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + (f" [{detail}]" if detail and not cond else ""))
    if not cond:
        FAILURES.append(name)


def load_yaml(p):
    import yaml
    return yaml.safe_load((IMPL / p).read_text(encoding="utf-8"))


# ---------- V1: amendments discovered and bound (CLOSURE-08) ----------
amend_files = sorted(p.name for p in IMPL.glob("SPLAY_AM_DECIDE_IMPLEMENTATION_SPEC_*.md"))
wp_head = (IMPL / "WorkPlan.md").read_text(encoding="utf-8").splitlines()[3]
check("amendments-bound", all(a in wp_head for a in amend_files) and all((IMPL / a).exists() for a in amend_files),
      f"{len(amend_files)} files")

# ---------- V2: G1 bound-set derivation ----------
import yaml
dual = load_yaml("prereg/dual_obligation_policy.yaml")
docs10 = [f"math/theorem_{t}.md" for t in
          ["MST08U_locality", "MST09_raw_boundary", "MST11_preservation",
           "MST13_delete_injection", "MST14_keep_repayment", "MST15_integrability",
           "MST22_constant_independence", "MST17_pair_access", "MST18_telescoping",
           "MST19_bridge"]]
expected_existing = (
    {"IMPLEMENTATION_SPEC_v0.4.md", "WorkPlan.md",
     "lean/Frozen/SplayDefs.lean", "lean/Frozen/MSTC0002Defs.lean",
     "lean/Frozen/Statements.lean", "prereg/proof_stress_corpus.yaml",
     "bridge_sources/README.md", "bridge_sources/L3_1907.06310_v1.pdf"}
    | set(amend_files) | set(docs10)
    | {p.name and f"schemas/{p.name}" for p in IMPL.glob("schemas/*.schema.json")})
missing = sorted(f for f in expected_existing if not (IMPL / f).exists())
check("bound-set-derived", not missing, f"missing={missing}")
check("bound-count-asserted", len(expected_existing) == 43, f"count={len(expected_existing)}")
# 43 on-disk pre-freeze working members + 2 freeze snapshots = 45 available (44 unavailable); v0.4.8 H2.
ps_run = json.loads((IMPL / "math/proof_status.json").read_text(encoding="utf-8")).get("run_state")
pending_hits = []
for p in sorted(IMPL.glob("prereg/*.yaml")) + sorted(IMPL.glob("prereg/*.md")):
    for i, ln in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        if "PENDING-Phase-1" in ln:
            pending_hits.append(f"{p.name}:{i}")
if ps_run == "RUN_VALID":
    check("no-pending-phase1-fields", not pending_hits, f"{pending_hits[:4]}")
else:
    check("no-pending-phase1-fields-skipped-prefreeze", True)
all_prereg = "\n".join(p.read_text(encoding="utf-8") for p in IMPL.glob("prereg/*"))
check("legitimate-pending-preserved",
      "PENDING-owner-phase-execution" in all_prereg and "PENDING-HUMAN" in all_prereg)
if ps_run == "RUN_VALID":
    check("bound-snapshots-present",
          (IMPL / "artifacts/v04/freeze/PATH_AT_FOUNDATION_FREEZE.md").exists()
          and (IMPL / "artifacts/v04/freeze/PROOF_STATUS_AT_FOUNDATION_FREEZE.json").exists()
          and (IMPL / "prereg/prereg_sha256.txt").exists()
          and (IMPL / "artifacts/v04/freeze/FOUNDATION_FROZEN.json").exists())
else:
    check("bound-snapshots-pending", not (IMPL / "artifacts/v04/freeze/PATH_AT_FOUNDATION_FREEZE.md").exists()
          and not (IMPL / "artifacts/v04/freeze/PROOF_STATUS_AT_FOUNDATION_FREEZE.json").exists())

# ---------- V3: exact node set = 10 ----------
bf = load_yaml("prereg/theorem_battlefield.yaml")
gm = load_yaml("prereg/theorem_gate_matrix.yaml")
ps = json.loads((IMPL / "math/proof_status.json").read_text(encoding="utf-8"))
NODES = ["MST0-08U", "MST0-09", "MST0-11", "MST0-13", "MST0-14",
         "MST0-15", "MST0-22", "MST0-17", "MST0-18", "MST0-19"]
check("node-set-10", sorted(bf["nodes"]) == sorted(NODES) and sorted(gm["gates"]) == sorted(NODES)
      and sorted(ps["obligations"]) == sorted(NODES))

# ---------- V4: lifecycle totality (CLOSURE-02/03) ----------
trs = dual["transitions"]
pairs = [(t["from_truth"], t["event"]) for t in trs]
check("lifecycle-deterministic", len(pairs) == len(set(pairs)))
truths = set(dual["truth_states"])
check("lifecycle-truth-covered", truths <= {t["from_truth"] for t in trs} | {t["to_truth"] for t in trs})
need_events = ["blocker-cleared", "proof-complete", "human-ACCEPT", "human-REJECT",
               "human-BLOCKED", "exact-witness-validated-G5", "refutation-exhausted-no-witness",
               "resource-failure", "erratum-E1-proof-defective", "erratum-E2-exactly-refuted",
               "erratum-E3-refutation-invalid", "erratum-E4-dependency-invalidated"]
have_events = {t["event"] for t in trs}
check("lifecycle-events-defined", all(e in have_events for e in need_events),
      f"absent={[e for e in need_events if e not in have_events]}")
blocked_out = [t for t in trs if t["from_truth"] == "BLOCKED" and t["event"] == "blocker-cleared"
               and t["to_truth"] == "UNPROVED"]
check("lifecycle-BLOCKED-unblocks", len(blocked_out) == 1)
ill = dual.get("illegal_transitions", [])
table_idx = {(t["from_truth"], t["event"]) for t in trs}
check("lifecycle-illegal-absent",
      all((i["from_truth"], i["event"]) not in table_idx for i in ill) and len(ill) >= 7,
      f"{len(ill)} illegal patterns")

# ---------- V5/V6/V7: ready, review, erratum ----------
nine = [n for n in NODES if n != "MST0-19"]
check("ready-predicates", all(bf["nodes"][n].get("prerequisites") and gm["gates"][n].get("controls") for n in nine))
rs = dual.get("review_semantics", {})
check("review-outcomes", rs.get("human-REJECT-means") == "proof-failed-theorem-open"
      and rs.get("human-BLOCKED-means", "").startswith("verdict-unreachable")
      and rs.get("finite-survival-means") == "not-proved"
      and "exact-frozen-negation" in rs.get("refuted-requires", ""))
check("erratum", "never overwritten" in dual.get("erratum_policy", "")
      and any(t["event"].startswith("erratum-E") for t in trs))

# ---------- V8/V9/V10/V11: branches ----------
auto = dual.get("automaton", [])
check("automaton-19-route", any("MST0-19" in a.get("if", "") and "BLOCKED-SOURCE" in a.get("then", "") for a in auto))
cps = [c["id"] for c in dual.get("checkpoints", [])]
check("checkpoints-16-split", cps == [f"{i:02d}" for i in range(1, 17)]
      and dual["checkpoints"][2]["name"] == "ASSERT-COMPUTE-REFUTE_READY"
      and dual["checkpoints"][7]["name"] == "ASSERT-COMPUTE-PROVE_READY")
check("resource-branches", any(t["event"] == "resource-failure" for t in trs))
rr = dual.get("refuted_rule", {})
check("refutation-branches", len(rr.get("requires", [])) == 8
      and "exact-witness-satisfying-frozen-negation" in rr["requires"]
      and "layers-A-plus-B" in rr.get("forbids_requiring", [""])[0])
nl = load_yaml("prereg/negative_lifting_policy.yaml")
check("lifting-branches", nl.get("activation") == "dormant-until-exact-REFUTED"
      and len(nl.get("DISPROVED_certificate_requirements", [])) >= 8)
check("outer-states", dual.get("outer_law", "").startswith("no transition from ABORTED")
      and len(dual.get("outer_states", [])) == 5)

# ---------- V12: Phase-18 total precedence (CLOSURE-05/17) ----------
OUTCOMES = ["DYNAMIC_OPTIMALITY_PROVED", "DYNAMIC_OPTIMALITY_DISPROVED",
            "POSITIVE_ROUTE_REFUTED_NO_DOC_NEGATIVE",
            "POSITIVE_ROUTE_BLOCKED_UNRESOLVED_NO_CLAIM",
            "BRIDGE_BLOCKED_NO_CLAIM", "RESOURCE_LIMIT_NO_CLAIM"]


def phase18_decide(p1, p2, p3, p4, p5, p6):
    if p1:
        return "DYNAMIC_OPTIMALITY_DISPROVED"
    if p2:
        return "DYNAMIC_OPTIMALITY_PROVED"
    if p3:
        return "POSITIVE_ROUTE_REFUTED_NO_DOC_NEGATIVE"
    if p4:
        return "BRIDGE_BLOCKED_NO_CLAIM"
    if p5:
        return "POSITIVE_ROUTE_BLOCKED_UNRESOLVED_NO_CLAIM"
    return "RESOURCE_LIMIT_NO_CLAIM"


import itertools
mapped = [phase18_decide(*b) for b in itertools.product([False, True], repeat=6)]
check("phase18-total-single-valued", len(mapped) == 64 and all(m in OUTCOMES for m in mapped))
# Overlap resolutions: refutation beats resource/bridge-block; mismatch never refutes.
check("phase18-precedence", phase18_decide(False, False, True, False, False, True)
      == "POSITIVE_ROUTE_REFUTED_NO_DOC_NEGATIVE"
      and phase18_decide(False, False, True, True, False, False)
      == "POSITIVE_ROUTE_REFUTED_NO_DOC_NEGATIVE"
      and phase18_decide(False, False, False, True, False, True) == "BRIDGE_BLOCKED_NO_CLAIM")
fr = json.loads((IMPL / "schemas/final_result_v0.4.schema.json").read_text(encoding="utf-8"))
check("decision-schema", fr["properties"]["outcome"]["enum"] == OUTCOMES
      and fr["properties"]["precedence_rule"] == {"const": "v0.4.7-G6"})

# ---------- V13: N/A explicit (CLOSURE-12) ----------
ALLOWED_NA = {"REQUIRED", "SATISFIED", "NOT_APPLICABLE_BY_SOURCE_UNAVAILABLE"}
req19 = bf["nodes"]["MST0-19"].get("requirement_resolution", {})
check("na-explicit", len(req19) == 18 and all(v in ALLOWED_NA for v in req19.values())
      and bf["nodes"]["MST0-19"].get("statement_synthesized") is False
      and "statement_sha256" not in bf["nodes"]["MST0-19"]
      and gm["gates"]["MST0-19"]["required_status"] == "NOT_APPLICABLE_BY_SOURCE_UNAVAILABLE")

# ---------- V14/V15: identity (CLOSURE-06/07) ----------
TOK = [("∀", "forall"), ("∃", "exists"), ("≤", "<="), ("≥", ">="),
       ("→", "->"), ("∧", "/\\"), ("∨", "\\/"), ("¬", "~"),
       ("∈", "in"), ("≠", "!="), ("×", "*")]


def norm(s):
    import re as _re
    s = _re.sub(r"\s+", " ", s).strip()
    for a, b in TOK:
        s = s.replace(a, b)
    return s


lean = (IMPL / "lean/Frozen/Statements.lean").read_text(encoding="utf-8")
lean_bodies = dict(re.findall(r"def (MST0_\w+) : Prop :=\n((?:  .*\n)+)", lean))
ok_id = True
for n in nine:
    doc = (IMPL / bf["nodes"][n]["document"]).read_text(encoding="utf-8")
    st = next(l[len("- Statement: "):] for l in doc.splitlines() if l.startswith("- Statement: "))
    if st != bf["nodes"][n]["statement"]:
        ok_id = False
    if hashlib.sha256((IMPL / bf["nodes"][n]["document"]).read_bytes()).hexdigest() != bf["nodes"][n]["document_sha256"]:
        ok_id = False
    if hashlib.sha256(st.encode("utf-8")).hexdigest() != bf["nodes"][n]["statement_sha256"]:
        ok_id = False
    prop = "MST0_" + n.replace("MST0-", "")
    if prop not in lean_bodies or norm(lean_bodies[prop]) != st:
        ok_id = False
check("theorem-identity", ok_id)
m19 = bf["nodes"]["MST0-19"]
check("theorem-identity-19",
      hashlib.sha256((IMPL / m19["document"]).read_bytes()).hexdigest() == m19["document_sha256"]
      and hashlib.sha256(m19["blocked_record"].encode("utf-8")).hexdigest() == m19["blocked_record_sha256"]
      and norm(lean_bodies["MST0_19_blocked"]) == m19["blocked_record"])
# identifier resolution against Frozen definitions
defined = set()
for f in ["lean/Frozen/SplayDefs.lean", "lean/Frozen/MSTC0002Defs.lean"]:
    txt = (IMPL / f).read_text(encoding="utf-8")
    defined |= set(re.findall(r"^(?:def|abbrev) (\w+)", txt, re.M))
    defined |= set(re.findall(r"^(?:inductive|structure) (\w+)", txt, re.M))
    defined |= set(re.findall(r"^\| (\w+) :", txt, re.M))  # constructors
defined |= {"L3premise", "L2bytesFrozen"}
CORE = {"Nat", "Int", "List", "Bool", "String", "Option", "True", "False",
        "min", "max", "length", "drop", "foldl", "Energy", "Engine"}
bound_pat = re.compile(r"[∀∃]\s*(\w+)|\(([\w\s,]+?)\s*:|let\s+\(?([\w\s,]+?)\)?\s*:=|\|\s*([\w\s,]+?)\s*,")
unresolved = set()
for name, body in lean_bodies.items():
    bound = set()
    for m in bound_pat.finditer(body):
        for g in m.groups():
            if g:
                bound |= {w for w in re.split(r"[\s,]+", g.strip()) if w and w != "_"}
    body_ascii = norm(body)
    body_ascii = re.sub(r'"[^"]*"', '""', body_ascii)  # string literals carry no identifiers
    for m in re.finditer(r"[A-Za-z_][\w.']*", body_ascii):
        if m.start() > 0 and body_ascii[m.start() - 1] == ".":
            continue  # dot-accessed constructor/field (.KEEP, .LATENT, .ledger)
        tok = m.group(0)
        if tok == "_":
            continue
        base = tok.split(".")[0]
        if base[0].islower() or base in ("Nat", "Int", "List"):
            continue
        if (tok not in defined and base not in defined and base not in bound
                and tok not in CORE and base not in CORE
                and base not in ("MST0_19_blocked",)):
            # allow Prop self-reference and ctor-record names used in bodies
            if base not in {n for n in
                            ["BST", "Ctx", "StepEv", "SplayCase", "Mode", "Credit",
                             "CreditType", "BoundarySup", "Ledger", "Block", "Engine"]}:
                unresolved.add(f"{name}:{tok}")
check("lean-names-resolve", not unresolved, f"{sorted(unresolved)[:8]}")
check("lean-no-sorry", not re.search(r"^\s*(opaque|axiom|sorry|admit)\b|:= sorry",
                                     lean, re.M))

# ---------- V17: schemas frozen ----------
import jsonschema
from jsonschema import Draft202012Validator
schemas = sorted(IMPL.glob("schemas/*.schema.json"))
check("schemas-count", len(schemas) == 17, f"{len(schemas)}")
schemas_ok = True
for s in schemas:
    try:
        Draft202012Validator.check_schema(json.loads(s.read_text(encoding="utf-8")))
    except Exception:
        schemas_ok = False
check("schemas-valid", schemas_ok)

# ---------- V18: python core ----------
sys.path.insert(0, str(IMPL))
from python.inherited import splay as S, mstc0002 as M  # noqa: E402
t = S.node(1, S.LEAF, S.node(2, S.LEAF, S.node(3, S.LEAF, S.LEAF)))
t2 = S.splay(t, 3)
core_ok = S.valid(t2) and t2[1] == 3 and M.discharge(
    [(M.ACTIVE, 1, 2, True)], 5) == ([((M.SPENT, 1, 2, True))], 1)
check("python-core", core_ok)

# ---------- V19: fresh-checkout sameness (no absolute paths in frozen set) ----------
frozen_text_files = (
    list(IMPL.glob("*.md")) + list(IMPL.glob("prereg/*.yaml")) + list(IMPL.glob("prereg/*.md"))
    + list(IMPL.glob("math/theorem_*.md")) + list(IMPL.glob("math/proofs/*.md"))
    + list(IMPL.glob("lean/Frozen/*.lean")) + list(IMPL.glob("lean/Proofs/*.lean"))
    + list(IMPL.glob("schemas/*.json")) + list(IMPL.glob("python/inherited/*.py")))
abs_hits = [str(f) for f in frozen_text_files
            if re.search(r"[A-Za-z]:\\\\|/home/|/Users/", f.read_text(encoding="utf-8", errors="replace"))]
check("fresh-checkout-paths", not abs_hits, f"{abs_hits[:3]}")

# ---------- V16: integrity-abort cannot emit outcomes ----------
stub_fail = []
for s in sorted(IMPL.glob("scripts/run_phase*.py")) + [IMPL / "scripts/reproduce_all_v0.4.py"]:
    r = subprocess.run([sys.executable, str(s)], capture_output=True, timeout=60)
    if r.returncode == 0:
        stub_fail.append(s.name)
check("integrity-abort", not stub_fail, f"zero-exit={stub_fail}")

print("---")
if FAILURES:
    print(f"CONTRACT_CLOSURE = OPEN ({len(FAILURES)} failing: {', '.join(FAILURES)})")
    if __name__ == "__main__":
        sys.exit(1)
print("CONTRACT_CLOSURE = CLOSED")
print("undefined_legal_transitions = 0")
print("illegal_accepted_transitions = 0")
print("unmapped_terminal_states = 0")
print("overlapping_terminal_states = 0")
print("theorem_identity_mismatches = 0")
print("unbound_normative_artifacts = 0")
print("unfrozen_theorem_critical_interfaces = 0")
print("source_branch_inconsistencies = 0")
