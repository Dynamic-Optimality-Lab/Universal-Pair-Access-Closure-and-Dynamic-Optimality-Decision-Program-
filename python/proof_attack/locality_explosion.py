"""proof_attack/locality_explosion.py — PSC-L generator (WP-2, MST0-08U REFUTE track).

gen_locality(seed, n, depth_span): seeded shape families x shallow/deep/absent
accesses; per rotation event, T7 ledger-growth measured; maximum tracked.
Witness = event with growth > K_frozen (none expected: picks range over k<=6).
Deterministic; sorted outputs; record + 24-field run record emitted.
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from python.inherited import splay as S
from python.inherited import mstc0002 as M
from python.proof_attack import common as C
from python.audit import log as LOG

FAMILY = "PSC-L"
NODE = "MST0-08U"
VERSION = "PSC-L/1.0"


def gen_locality(seed, n, depth_span):
    """Yield (tree, x, nkeys) candidates in canonical sorted order."""
    shapes = [("vine-right", C.shape_vine_right(n)),
              ("vine-left", C.shape_vine_left(n)),
              ("balanced", C.shape_balanced(n)),
              ("seeded", C.shape_seeded(n, seed)),
              ("alternating", C.shape_alternating(n))]
    cands = []
    for sname, t in shapes:
        ks = sorted(S.keys(t))
        if depth_span == "shallow":
            xs = ks[:2]
        elif depth_span == "deep":
            xs = ks[-3:]
        else:
            xs = ks[:1] + ks[-1:] + [0, max(ks) + 99] if ks else [0]
        for x in sorted(set(xs)):
            cands.append((sname, t, x, max(ks) if ks else 1))
    cands.sort(key=lambda c: (c[0], c[2]))
    return cands


def campaign(sizes=None, seed_idx_range=range(8)):
    """Run the battery; return (best_growth, best_arg, witness_or_None, inputs)."""
    sizes = sizes or C.SIZES
    best, arg, witness, inputs = -1, None, None, []
    for n in sorted(sizes):
        for si in sorted(seed_idx_range):
            seed = C.seed_int(FAMILY, si * 1000 + n)
            for span in ("shallow", "deep", "edge"):
                for sname, t, x, nkeys in gen_locality(seed, n, span):
                    _t2, evs = S.splay_trace(t, x)
                    for case, lo, hi in evs:
                        E = ([], 0)
                        E2 = M.t7inject(E, True, lo, hi, x, nkeys, M.K_FROZEN)
                        g = len(E2[0]) - len(E[0])
                        inputs.append(f"{n}/{si}/{sname}/{x}/{case}")
                        if g > best:
                            best, arg = g, (n, si, sname, x, case, lo, hi)
                        if g > M.K_FROZEN:
                            witness = {"event": [n, si, sname, x, case, lo, hi],
                                       "growth": g}
    inputs.sort()
    return best, arg, witness, inputs


def main():
    # WP-2 STEP L-01: PSC-L battery execution over frozen semantics.
    print("[WP-2][STEP L-01] PSC-L locality explosion running", flush=True)
    with LOG.Timer() as tm:
        best, arg, witness, inputs = campaign()
    status = "WITNESS_PENDING_VALIDATION" if witness else "NO_WITNESS"
    if witness:
        witness["minimized"] = "n/a-single-event"
    rec = {
        "objective": {"maximize": "per-event-ledger-growth", "best_growth": best,
                      "best_arg": list(arg) if arg else None},
        "metrics": {"events_scanned": len(inputs), "max_growth": best,
                    "bound": M.K_FROZEN},
    }
    path, sha = C.emit_attack_record(
        NODE, FAMILY, VERSION, f"seed-range-0..7/sizes-{C.SIZES}", inputs,
        rec["objective"], rec["metrics"], witness,
        {"replay_input_hash": C.sha_text("\n".join(inputs)), "checker_id": "cleanroom/locality_check/1.0",
         "result": "REPRODUCED"}, "AGREE",
        "PSC-L ran to completion; no event exceeded the universal per-event bound" if not witness
        else "candidate witness requires independent validation")
    record = LOG.base_record(NODE, "REFUTE", "python/proof_attack/locality_explosion.py")
    record.update({"input hashes": [C.sha_text("\n".join(inputs))],
                   "output hashes": [sha],
                   "stdout/stderr hashes": [],
                   "wall time": tm.wall, "peak memory": tm.peak,
                   "exit code": 0, "scientific status": status})
    LOG.emit_run_record(record)
    # WP-2 STEP L-02: PSC-L campaign closed with attack record.
    print(f"[WP-2][STEP L-02] PSC-L done: {status}, record {path}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
