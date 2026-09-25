"""MSTC-0002 = (P_all, k=6, C=2) ledger engine for SPLAY-AM-DECIDE-v0.4.

Provenance (wrap, never mutate): faithful port of the sealed v0.3 Branch-A
machinery — `python/ledger/state.py` (credits, canonical form), `support.py`
(support hygiene + leakage blocklist), `update.py` (deterministic rule
application), `provenance/active.py` (predicate atoms P_all/T6 match), and
`python/transfer/branchA.py` (T7 site-cycling injection, T5 activation,
T6 repayment loop, evaluate()). Frozen values: predicate P_all =
any_of[KEEP, DELETE]; k=6; C=2; unit masses; scale (S0,0); E0=empty.

BINDING NOTE (WP2 imported-semantics rule): the sealed parent code discharges
repayment by looping T6 once per unit of positive regret while ACTIVE credit
exists (`evaluate`: `for _ in range(int(w))` with per-fire application
check). Hence the imported semantics PROVABLY reduce to
paid == min(active_pool, w) for w > 0 — recorded here as a binding lemma
derived from sealed code (`branchA.py::evaluate` + `update.py`), not assumed.
`imported_payment()` implements exactly that reduction.
"""
from __future__ import annotations

from fractions import Fraction

K_FROZEN = 6
C_FROZEN = 2
PREDICATE_ALL = {"any_of": [{"mode_is": "KEEP"}, {"mode_is": "DELETE"}]}
T6_MATCH = {"mode_is": "KEEP"}
ALLOWED_KINDS = {"key", "interval", "heavy_path", "heap_relation", "lazy_interval",
                 "boundary", "bend", "orientation"}
ORIENTATIONS = {"LEFT", "RIGHT", "MIXED"}
FORBIDDEN_SUBSTRINGS = ("state_id", "cycle", "holdout", "H1", "H2", "H3T",
                        "timestamp", "time_idx", "event_id", "future", "bellman",
                        "address", "U_b", "V_b", "/proc", "0x")


def check_support(support: tuple) -> None:
    """Support hygiene ported from v0.3 support.py (kinds + leakage blocklist)."""
    if not (isinstance(support, tuple) and support):
        raise ValueError("support must be a non-empty tuple")
    kind = support[0]
    if kind not in ALLOWED_KINDS:
        raise ValueError("forbidden support kind %r" % (kind,))
    for field in support[1:]:
        if isinstance(field, str):
            low = field.lower()
            if any(b.lower() in low for b in FORBIDDEN_SUBSTRINGS):
                raise ValueError("forbidden support content %r" % (field,))
        elif isinstance(field, bool) or not isinstance(field, int):
            raise ValueError("support fields must be ints/strings, got %r" % (field,))
    if kind == "boundary":
        if len(support) != 4 or support[3] not in ORIENTATIONS:
            raise ValueError("boundary support must be ('boundary', left, right, orientation)")


def make_credit(credit_type: str, support: tuple, scale: tuple,
                mass: Fraction, provenance: str) -> dict:
    """Frozen credit record (ported; mass must be exact Fraction)."""
    check_support(support)
    if not isinstance(mass, Fraction):
        raise TypeError("mass must be Fraction (exact arithmetic)")
    if not (isinstance(scale, tuple) and len(scale) == 2):
        raise ValueError("scale must be (system, level)")
    return {"type": credit_type, "support": support, "scale": scale,
            "mass": mass, "provenance": provenance}


def _key(credit: dict) -> tuple:
    """Canonical credit key (ported)."""
    return (credit["type"], credit["support"], credit["scale"],
            (credit["mass"].numerator, credit["mass"].denominator),
            credit["provenance"])


def canonical(ledger: list) -> tuple:
    """Canonical sorted tuple form (ported)."""
    return tuple(sorted((_key(c) for c in ledger)))


def empty() -> list:
    """Synchronized initial ledger (E0 = empty)."""
    return []


def energy(ledger: list) -> int:
    """E(L) = |LATENT| + |ACTIVE| (unsigned masses; SPENT carries no energy)."""
    return sum(1 for c in ledger if c["type"] in ("BOUNDARY_LATENT", "BOUNDARY_ACTIVE"))


def predicate_fires(pred: dict, event: dict) -> bool:
    """P_all match on rotation events (ported atom semantics)."""
    op, arg = next(iter(pred.items()))
    if op == "any_of":
        return any(predicate_fires(sub, event) for sub in arg)
    if op == "all_of":
        return all(predicate_fires(sub, event) for sub in arg)
    if op == "mode_is":
        return event.get("mode") == arg
    if op == "case_is":
        return event.get("splay_case") == arg
    if op == "side_is":
        return event.get("side") == arg
    raise ValueError("atom outside frozen menu: %r" % (op,))


def t7_inject(ledger: list, event: dict, k: int, cursor: int) -> tuple[list, int]:
    """T7: per A-side rotation inject up to k LATENT at cycling interior sites.

    Ported site semantics: interior boundaries (i,i+1) of the affected
    interval, oriented LEFT iff i+1 <= x; deterministic cycling cursor.
    Returns (new_ledger, new_cursor, injected_count).
    """
    out = list(ledger)
    injected = 0
    if event.get("side") == "A":
        lo, hi = event["interval"]
        nkeys = event["nkeys"]
        sites = [("boundary", i, i + 1, "LEFT" if i + 1 <= event["x"] else "RIGHT")
                 for i in range(lo, hi) if 1 <= i < nkeys]
        for _ in range(k):
            if not sites:
                break
            sup = sites[cursor % len(sites)]
            cursor += 1
            out.append(make_credit("BOUNDARY_LATENT", sup, ("S0", 0),
                                   Fraction(1), "A_ROTATION_CREATED"))
            injected += 1
    return out, cursor, injected


def t5_activate(ledger: list, event: dict) -> tuple[list, bool]:
    """T5: predicate-gated LATENT -> ACTIVE (same support; energy-neutral).

    P_all fires on every KEEP/DELETE event; converts one LATENT if present.
    Returns (new_ledger, fired).
    """
    if not predicate_fires(PREDICATE_ALL, event):
        return list(ledger), False
    out = list(ledger)
    for i, c in enumerate(out):
        if c["type"] == "BOUNDARY_LATENT":
            conv = dict(c)
            conv["type"] = "BOUNDARY_ACTIVE"
            conv["provenance"] = "B_ZIGZAG_EXPOSED"
            out[i] = conv
            return out, True
    return out, False


def active_pool(ledger: list) -> int:
    """Count of ACTIVE credits available for repayment."""
    return sum(1 for c in ledger if c["type"] == "BOUNDARY_ACTIVE")


def imported_payment(ledger: list, event: dict) -> tuple[list, int]:
    """T6: discharge ACTIVE against positive KEEP regret (imported semantics).

    Implements exactly the sealed reduction: loop while w units remain and an
    ACTIVE credit exists; each firing consumes one ACTIVE and produces one
    SPENT (provenance PAID_REGRET). Hence paid == min(active_pool, w).
    Returns (new_ledger, paid).
    """
    if event.get("mode") != "KEEP":
        return list(ledger), 0
    w = event.get("y_edge", 0) - C_FROZEN * event.get("a_edge", 0)
    if w <= 0:
        return list(ledger), 0
    out = list(ledger)
    paid = 0
    for _ in range(int(w)):
        hit = next((c for c in out if c["type"] == "BOUNDARY_ACTIVE"), None)
        if hit is None:
            break
        out.remove(hit)
        spent = dict(hit)
        spent["type"] = "SPENT"
        spent["provenance"] = "PAID_REGRET"
        out.append(spent)
        paid += 1
    return out, paid


def required(event: dict) -> int:
    """Positive-regret demand: max(w, 0) with w = y - 2a (integers)."""
    return max(0, event.get("y_edge", 0) - C_FROZEN * event.get("a_edge", 0))


def residual(event: dict, paid: int) -> int:
    """Exact residual: required - paid (refutes if > 0)."""
    return required(event) - paid


def evaluate(events: list[dict], k: int = K_FROZEN) -> dict:
    """Run the frozen calculus over rotation events; exact residual report.

    Ported evaluation order: T7 injection, then T5, then T6 repayment loop on
    burdened KEEP. Returns feasible flag, max residual, first violation,
    paid/injected totals (all exact integers).
    """
    ledger = empty()
    cursor = 0
    max_res = 0
    first = None
    paid_total = 0
    injected_total = 0
    for idx, ev in enumerate(events):
        ledger, cursor, injected = t7_inject(ledger, ev, k, cursor)
        injected_total += injected
        ledger, _ = t5_activate(ledger, ev)
        need = required(ev)
        if ev.get("mode") == "KEEP" and need > 0:
            ledger, paid = imported_payment(ledger, ev)
            paid_total += paid
            res = need - paid
            if res > max_res:
                max_res = res
                first = {"event_index": idx, "event": dict(ev),
                         "w": need, "paid": paid, "res": res}
    return {"feasible": max_res == 0, "max_residual": max_res,
            "first_violation": first, "paid_total": paid_total,
            "injected_total": injected_total, "terminal_energy": energy(ledger)}


def spent_count(ledger: list) -> int:
    """SPENT population (monotone audit helper: SPENT is never removed)."""
    return sum(1 for c in ledger if c["type"] == "SPENT")
