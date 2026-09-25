"""Paired-Splay execution driver for SPLAY-AM-DECIDE-v0.4 (frozen semantics).

KEEP: (A,B) -> (S_xA, S_xB) with a = c(A,x), y = c(B,x).
DELETE: (A,B) -> (S_xA, B) with a = c(A,x), y = 0.
Cost: depth + 1. Edge regret: w = y - 2a. Single-access replay attaches the
full access cost to the terminal rotation event (per-access granularity);
block drivers may repartition per rotation. Deterministic. Exact integers.
"""
from __future__ import annotations

from python.inherited import splay as S


def build_tree(shape: str, nkeys: int) -> S.Node:
    """Deterministic initial tree: balanced | spine-left | spine-right."""
    keys = list(range(1, nkeys + 1))
    if shape == "balanced":
        return S.build_balanced(keys)
    if shape == "spine-left":
        return S.build_spine(keys, left=True)
    if shape == "spine-right":
        return S.build_spine(keys, left=False)
    raise ValueError("unknown shape %r" % (shape,))


def replay_access(tree: S.Node, x: int, nkeys: int, side: str, mode: str,
                  mate_a: int = 0, mate_y: int = 0) -> tuple[list[dict], S.Node]:
    """Replay one access; attach full costs to the terminal rotation event.

    Sealed edge convention (parent h3t_evaluate:episode_rotations +
    cycles/discovery:_edge_events): every A-side event carries zeroed
    (a_edge, y_edge); only the terminal B-rotation of a KEEP carries
    (a_edge, y_edge) = (mate A cost, own B cost). DELETE carries y_edge = 0
    everywhere. ROOT accesses (x already root) emit NO event at all (parent
    `if bevs:` guard): no rotation means no injection, no activation, and no
    repayment evaluation. Callers record case ROOT from empty step lists.
    Returns (events, new_root).
    """
    steps, new_root = S.stepwise_access(tree, x, nkeys, side, mode)
    if side == "B" and mode == "KEEP" and steps:
        steps[-1]["a_edge"] = mate_a
        steps[-1]["y_edge"] = mate_y
    if not S.is_valid_bst(new_root):
        raise AssertionError("BST invariant broken after access")
    return steps, new_root


def run_paired(nkeys: int, shape: str, program: list[tuple[str, int]]) -> dict:
    """Run a paired program: [(mode, x), ...] from a COMMON initial tree.

    Domain legality (theorem precondition): Pair Access compares Splay(Y,T)
    against Splay(X,T) from the SAME initial tree T. A and B therefore start
    identical; they diverge only through DELETE restructuring (B skips
    DELETE). Different-start batteries are outside the theorem domain and
    must fail closed, never refute.

    Returns {events, splay_A, splay_B, rotations_A, cases_covered}.
    splay_A/B are summed access costs (depth+1 per access).
    """
    tree_a = build_tree(shape, nkeys)
    tree_b = build_tree(shape, nkeys)
    events: list[dict] = []
    cost_a = 0
    cost_b = 0
    cases = set()
    for mode, x in program:
        if mode == "KEEP":
            a = S.cost(tree_a, x)
            y = S.cost(tree_b, x)
            cost_a += a
            cost_b += y
            sta, tree_a = replay_access(tree_a, x, nkeys, "A", "KEEP")
            stb, tree_b = replay_access(tree_b, x, nkeys, "B", "KEEP",
                                        mate_a=a, mate_y=y)
            events.extend(sta)
            events.extend(stb)
            if not sta:
                cases.add("ROOT")
            if not stb:
                cases.add("ROOT")
            cases.update(e["splay_case"] for e in sta + stb)
        elif mode == "DELETE":
            a = S.cost(tree_a, x)
            cost_a += a
            sta, tree_a = replay_access(tree_a, x, nkeys, "A", "DELETE")
            events.extend(sta)
            if not sta:
                cases.add("ROOT")
            cases.update(e["splay_case"] for e in sta)
        else:
            raise ValueError("mode must be KEEP or DELETE")
    rotations_a = sum(1 for e in events if e["side"] == "A" and e["splay_case"] != "ROOT")
    return {"events": events, "splay_A": cost_a, "splay_B": cost_b,
            "rotations_A": rotations_a, "cases_covered": sorted(cases)}
