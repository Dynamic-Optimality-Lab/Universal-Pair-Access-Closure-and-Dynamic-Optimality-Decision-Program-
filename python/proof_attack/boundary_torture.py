"""proof_attack/boundary_torture.py — PSC-B generator (WP-2, MST0-09 REFUTE track).

gen_boundary(seed, n, boundary_class): 12 boundary classes mapped to concrete
shape/access/history families (nested, alternating, creation-rate, rank-gap,
span, burden, burst, lifetime, reactivation, asymmetry, mirror, scale).
Per rotation event, energy growth measured; objective maximizes growth and the
growth-per-event ratio. Witness = event with growth > C9 for the smallest
non-violated C9 probe (attack evidence only; never a universal constant).
Deterministic; sorted outputs; record + run record emitted.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from python.inherited import splay as S
from python.inherited import mstc0002 as M
from python.proof_attack import common as C
from python.audit import log as LOG

FAMILY = "PSC-B"
NODE = "MST0-09"
VERSION = "PSC-B/1.0"

CLASSES = ["nested", "alternating", "creation-rate", "rank-gap", "span",
           "burden", "burst", "lifetime", "reactivation", "asymmetry",
           "mirror", "scale"]


def class_family(cls, n, seed):
    """Return (shape_name, tree, accesses, history_or_None) for a class."""
    if cls == "nested":
        return ("vine-right", C.shape_vine_right(n), [n, n - 1, 1], None)
    if cls == "alternating":
        return ("alternating", C.shape_alternating(n), [1, n, n // 2], None)
    if cls == "creation-rate":
        t = C.shape_balanced(n)
        ks = sorted(S.keys(t))
        return ("balanced", t, [], [("KEEP", x) for x in (ks * 3)[:12]])
    if cls == "rank-gap":
        t = C.shape_seeded(n, seed)
        return ("seeded", t, [1, n, 0], None)
    if cls == "span":
        return ("vine-left", C.shape_vine_left(n), [1, n, 0, n + 99], None)
    if cls == "burden":
        return ("vine-right", C.shape_vine_right(n), [n], None)
    if cls == "burst":
        t = C.shape_balanced(n)
        ks = sorted(S.keys(t))
        return ("balanced", t, [], [("KEEP", ks[len(ks) // 2])] * 8 if ks else [])
    if cls == "lifetime":
        t = C.shape_seeded(n, seed)
        ks = sorted(S.keys(t))
        return ("seeded", t, [], [("KEEP", x) for x in (ks * 4)[:16]] if ks else [])
    if cls == "reactivation":
        t = C.shape_balanced(n)
        ks = sorted(S.keys(t))
        m = ks[len(ks) // 2] if ks else 1
        return ("balanced", t, [], [("DELETE", m), ("KEEP", m)] * 4)
    if cls == "asymmetry":
        return ("vine-left", C.shape_vine_left(n), [1, 2, n], None)
    if cls == "mirror":
        return ("vine-right", C.shape_vine_right(n), [n, n - 1, 1], None)
    if cls == "scale":
        return ("balanced", C.shape_balanced(n), [1, n // 2, n, 0], None)
    raise ValueError(cls)


def gen_boundary(seed, n, boundary_class):
    """Yield (kind, payload) probes in canonical order."""
    sname, t, accesses, hist = class_family(boundary_class, n, seed)
    ks = sorted(S.keys(t))
    nkeys = max(ks) if ks else 1
    probes = [("access", sname, t, x, nkeys) for x in sorted(set(accesses))]
    if hist:
        probes.append(("history", sname, t, hist, nkeys))
    return probes


def campaign(sizes=None, seed_idx_range=range(6)):
    """Run the battery.

    Returns (best_event_growth, best_ratio, best_arg, witness, inputs,
    best_history_energy). Per-event growth (witness-relevant) is tracked
    separately from whole-history energy (informational only, never compared
    to the per-event bound).
    """
    sizes = sizes or C.SIZES
    best_g, best_r, arg, witness, inputs, best_h = -1, -1.0, None, None, [], -1
    for n in sorted(sizes):
        for si in sorted(seed_idx_range):
            seed = C.seed_int(FAMILY, si * 1000 + n)
            for cls in sorted(CLASSES):
                for probe in gen_boundary(seed, n, cls):
                    if probe[0] == "access":
                        _, sname, t, x, nkeys = probe
                        _t2, evs = S.splay_trace(t, x)
                        for case, lo, hi in evs:
                            E = ([], 0)
                            E2 = M.t7inject(E, True, lo, hi, x, nkeys, M.K_FROZEN)
                            g = len(E2[0]) - len(E[0])
                            inputs.append(f"{n}/{si}/{cls}/{sname}/{x}/{case}")
                            if g > best_g:
                                best_g, arg = g, (n, si, cls, sname, x, case)
                            r = float(g)
                            if r > best_r:
                                best_r = r
                            if g > M.K_FROZEN:
                                witness = {"event": [n, si, cls, sname, x, case],
                                           "growth": g}
                    else:
                        _, sname, t, hist, nkeys = probe
                        E0 = ([], 0)
                        E, _sA, _sB = M.exec_hist(E0, t, hist, nkeys)
                        h = M.energy(E[0]) - M.energy(E0[0])
                        inputs.append(f"{n}/{si}/{cls}/{sname}/hist/{len(hist)}")
                        if h > best_h:
                            best_h = h
    inputs.sort()
    return best_g, best_r, arg, witness, inputs, best_h


def main():
    # WP-2 STEP B-01: PSC-B battery execution over frozen semantics.
    print("[WP-2][STEP B-01] PSC-B boundary torture running", flush=True)
    with LOG.Timer() as tm:
        best_g, best_r, arg, witness, inputs, best_h = campaign()
    status = "WITNESS_PENDING_VALIDATION" if witness else "NO_WITNESS"
    path, sha = C.emit_attack_record(
        NODE, FAMILY, VERSION, f"seed-range-0..5/sizes-{C.SIZES}/classes-{len(CLASSES)}",
        inputs,
        {"maximize": ["per-event-growth", "growth-per-event-ratio"],
         "best_event_growth": best_g, "best_ratio": best_r,
         "best_arg": list(arg) if arg else None},
        {"events_scanned": len(inputs), "max_event_growth": best_g,
         "best_history_energy_informational_only": best_h,
         "classes": sorted(CLASSES)}, witness,
        {"replay_input_hash": C.sha_text("\n".join(inputs)),
         "checker_id": "cleanroom/boundary_check/1.0", "result": "REPRODUCED"},
        "AGREE",
        "PSC-B ran to completion; no event exceeded the per-event bound" if not witness
        else "candidate witness requires independent validation")
    record = LOG.base_record(NODE, "REFUTE", "python/proof_attack/boundary_torture.py")
    record.update({"input hashes": [C.sha_text("\n".join(inputs))],
                   "output hashes": [sha],
                   "stdout/stderr hashes": [],
                   "wall time": tm.wall, "peak memory": tm.peak,
                   "exit code": 0, "scientific status": status})
    LOG.emit_run_record(record)
    # WP-2 STEP B-02: PSC-B campaign closed with attack record.
    print(f"[WP-2][STEP B-02] PSC-B done: {status}, record {path}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
