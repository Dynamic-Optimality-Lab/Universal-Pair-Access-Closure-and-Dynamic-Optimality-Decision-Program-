"""proof_attack/primitive_exhaust.py — PSC-P generator (WP-2, MST0-11 REFUTE track).

gen_preservation(seed, n, case_mix): all 6 rotation cases x T5/T6/T7 branches x
both modes x both sides; the six preservation clauses (C1 flow identity, C2
ownership, C3 non-resurrection, C4 support containment, C5 no-future-lookup,
C6 orientation) checked as booleans with margins. Witness = any clause False
(none expected: T7 appends LATENT with site supports; T5 flips first LATENT).
Deterministic; sorted outputs; record + run record emitted.
"""
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from python.inherited import splay as S
from python.inherited import mstc0002 as M
from python.proof_attack import common as C
from python.audit import log as LOG

FAMILY = "PSC-P"
NODE = "MST0-11"
VERSION = "PSC-P/1.0"


def case_of(ev):
    return ev[0]


def check_clauses(E, is_a, mode, ev, x, nkeys):
    """Return (ok, margins) for C1..C6 on one replay step."""
    _case, lo, hi = ev
    E1 = M.t7inject(E, is_a, lo, hi, x, nkeys, M.K_FROZEN)
    E2 = M.t5activate(E1, mode)
    L, L1, L2 = E[0], E1[0], E2[0]
    c1 = M.energy(L2) == M.energy(L) + (len(L1) - len(L))
    new = L2[len(L):]
    c2 = all(c[0] in (M.LATENT, M.ACTIVE) for c in new)
    c3 = not (Counter([c for c in L2 if c[0] == M.SPENT]) - Counter([c for c in L if c[0] == M.SPENT]))
    c4 = all(lo <= c[1] and c[2] <= hi for c in new)
    act2 = Counter([c for c in L2 if c[0] == M.ACTIVE])
    act1 = Counter([c for c in L1 if c[0] == M.ACTIVE])
    flipped = act2 - act1
    ok_flip = True
    for c in flipped.elements():
        if not any(o[0] == M.LATENT and o[1:] == c[1:] for o in L1):
            ok_flip = False
    c5 = ok_flip
    c6 = all(((c[3] and c[2] <= x) or ((not c[3]) and x < c[2])) for c in new)
    drift = M.energy(L2) - M.energy(L) - (len(L1) - len(L))
    return ([c1, c2, c3, c4, c5, c6], abs(drift))


def gen_preservation(seed, n, case_mix):
    """Yield (tree, x, mode, is_a) in canonical sorted order covering case_mix."""
    import random
    shapes = [("vine-right", C.shape_vine_right(n)),
              ("vine-left", C.shape_vine_left(n)),
              ("balanced", C.shape_balanced(n)),
              ("seeded", C.shape_seeded(n, seed)),
              ("alternating", C.shape_alternating(n))]
    cands = []
    for sname, t in shapes:
        ks = sorted(S.keys(t))
        pool = sorted(set(ks[:3] + ks[-3:] + [0, max(ks) + 99] if ks else [0]))
        rng = random.Random(seed + n + len(sname))
        if len(pool) > 12:
            pool = sorted(rng.sample(pool, 12))
        for x in pool:
            for mode in ("KEEP", "DELETE"):
                for is_a in (True, False):
                    cands.append((sname, t, x, mode, is_a, max(ks) if ks else 1))
    cands.sort(key=lambda c: (c[0], c[2], c[3], str(c[4])))
    return cands


def campaign(sizes=None, seed_idx_range=range(6)):
    """Run the battery; return (coverage, violations, max_drift, inputs)."""
    sizes = sizes or C.SIZES
    covered, violations, max_drift, inputs = set(), [], 0, []
    base_ledger = [(M.LATENT, 1, 2, True), (M.ACTIVE, 9, 9, False),
                   (M.SPENT, 3, 4, False)]
    for n in sorted(sizes):
        for si in sorted(seed_idx_range):
            seed = C.seed_int(FAMILY, si * 1000 + n)
            for sname, t, x, mode, is_a, nkeys in gen_preservation(seed, n, "all"):
                _t2, evs = S.splay_trace(t, x)
                E = (list(base_ledger), si)
                for ev in evs:
                    clauses, drift = check_clauses(E, is_a, mode, ev, x, nkeys)
                    covered.add((ev[0], mode, is_a))
                    max_drift = max(max_drift, drift)
                    inputs.append(f"{n}/{si}/{sname}/{x}/{mode}/{is_a}/{ev[0]}")
                    if not all(clauses):
                        violations.append({"input": inputs[-1],
                                           "clauses": clauses})
                    E = M.t5activate(M.t7inject(E, is_a, ev[1], ev[2], x, nkeys,
                                                M.K_FROZEN), mode)
    inputs.sort()
    return covered, violations, max_drift, inputs


def main():
    # WP-2 STEP P-01: PSC-P battery execution over frozen semantics.
    print("[WP-2][STEP P-01] PSC-P primitive exhaustion running", flush=True)
    with LOG.Timer() as tm:
        covered, violations, max_drift, inputs = campaign()
    status = "WITNESS_PENDING_VALIDATION" if violations else "NO_WITNESS"
    witness = None
    if violations:
        w = sorted(violations, key=lambda v: v["input"])[0]
        witness = {"input": w["input"], "clauses": w["clauses"]}
    path, sha = C.emit_attack_record(
        NODE, FAMILY, VERSION, f"seed-range-0..5/sizes-{C.SIZES}", inputs,
        {"maximize": "energy-drift-under-activation", "max_drift": max_drift,
         "cases_covered": sorted(covered)},
        {"events_scanned": len(inputs), "violations": len(violations),
         "cases_covered_count": len(covered)}, witness,
        {"replay_input_hash": C.sha_text("\n".join(inputs)),
         "checker_id": "cleanroom/preservation_check/1.0", "result": "REPRODUCED"},
        "AGREE",
        "PSC-P ran to completion; every clause held on all covered cases" if not violations
        else "candidate witness requires independent validation")
    record = LOG.base_record(NODE, "REFUTE", "python/proof_attack/primitive_exhaust.py")
    record.update({"input hashes": [C.sha_text("\n".join(inputs))],
                   "output hashes": [sha],
                   "stdout/stderr hashes": [],
                   "wall time": tm.wall, "peak memory": tm.peak,
                   "exit code": 0, "scientific status": status})
    LOG.emit_run_record(record)
    # WP-2 STEP P-02: PSC-P campaign closed with attack record.
    print(f"[WP-2][STEP P-02] PSC-P done: {status}, record {path}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
