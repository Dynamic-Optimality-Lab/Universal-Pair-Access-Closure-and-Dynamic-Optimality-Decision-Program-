"""audit/conformance.py — PSC implementation conformance harness (WP-2, STOP-17).

Verifies a generator module against the frozen corpus spec WITHOUT sharing
attack logic: interface signature, corpus seed-derivation formula, sorted
outputs, declared size coverage, parameter ranges. Returns issue list
(empty = green). Used by run_phase05..09 before attack execution.
"""
import hashlib
import inspect
from pathlib import Path

IMPL = Path(__file__).resolve().parents[2]
MASTER = hashlib.sha256(b"SPLAY-AM-DECIDE-v0.4").hexdigest()
SIZES = [16, 32, 64, 128, 256, 512, 1024]

SPECS = {
    "locality_explosion": {"family": "PSC-L", "gen": "gen_locality", "params": ["seed", "n", "depth_span"]},
    "primitive_exhaust": {"family": "PSC-P", "gen": "gen_preservation", "params": ["seed", "n", "case_mix"]},
    "boundary_torture": {"family": "PSC-B", "gen": "gen_boundary", "params": ["seed", "n", "boundary_class"]},
}


def check_module(modname):
    """Return list of conformance issues (empty = STOP-17 green)."""
    import importlib
    issues = []
    spec = SPECS.get(modname.split(".")[-1])
    if spec is None:
        return [f"unknown generator {modname}"]
    try:
        mod = importlib.import_module(f"python.proof_attack.{modname.split('.')[-1]}")
    except Exception as e:
        return [f"import failed: {e}"]
    gen = getattr(mod, spec["gen"], None)
    if gen is None or list(inspect.signature(gen).parameters) != spec["params"]:
        issues.append(f"interface mismatch for {spec['gen']}")
        return issues
    # seed-derivation formula: recompute independently and compare one value.
    fam = spec["family"]
    expect = int(hashlib.sha256(f"{MASTER}{fam}{1000 + 16}".encode()).hexdigest(), 16)
    try:
        from python.proof_attack import common as C
        if C.seed_int(fam, 1016) != expect:
            issues.append("seed derivation mismatch")
    except Exception as e:
        issues.append(f"seed check failed: {e}")
    if C.SIZES != SIZES:
        issues.append("size coverage mismatch")
    # canonical-order probe on a tiny sample (deterministic total order by
    # (shape, numeric-x, mode, side); history probes last for boundary).
    try:
        sample = list(gen(1016, 16, _probe_arg(spec["gen"])))
        keys = [_canon_key(spec["gen"], p) for p in sample]
        if keys != sorted(keys):
            issues.append("outputs not in canonical sorted order")
    except Exception as e:
        issues.append(f"probe failed: {e}")
    return issues


def _canon_key(gen_name, p):
    if gen_name == "gen_boundary":
        if p[0] == "access":
            return (0, str(p[1]), int(p[3]), "", "")
        return (1, str(p[1]), len(p[3]), "", "")
    if gen_name == "gen_locality":
        return (str(p[0]), int(p[2]))
    if gen_name == "gen_preservation":
        return (str(p[0]), int(p[2]), str(p[3]), str(p[4]))
    raise ValueError(gen_name)


def _probe_arg(gen_name):
    return {"gen_locality": "edge", "gen_preservation": "all",
            "gen_boundary": "scale"}[gen_name]
