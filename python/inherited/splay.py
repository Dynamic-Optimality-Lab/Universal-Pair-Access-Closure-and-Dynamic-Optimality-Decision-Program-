"""Ordinary bottom-up Splay + BST core for SPLAY-AM-DECIDE-v0.4.

Provenance (wrap, never mutate): faithful port of the sealed v0.3 canonical
implementation `python/splay_ref/splay.py` (Node/depth/cost/rotations/splay/
builders/serialize/inorder) plus the rotation-granular replay of
`python/transfer/branchA.py::stepwise_access` (local-keys affected interval).
Semantics frozen: keys [n]={1..n}; root depth 0; cost c(T,x)=depth+1; cases
ROOT/ZIG/LL/RR/LR/RL. v0.4 additions: frozen rotation-event dicts consumed by
the ledger engine (side/mode/a_edge/y_edge/nkeys/x) and BST-validity audit.
No floats. Deterministic. Exact integers throughout.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Node:
    """BST node with parent pointers (ported from v0.3 splay_ref)."""

    key: int
    left: "Node | None" = None
    right: "Node | None" = None
    parent: "Node | None" = None


def depth(root: "Node | None", x: int) -> int:
    """Depth of key x (root depth 0)."""
    d = 0
    cur = root
    while cur is not None:
        if x == cur.key:
            return d
        cur = cur.left if x < cur.key else cur.right
        d += 1
    raise KeyError("key %d not in tree" % x)


def cost(root: "Node | None", x: int) -> int:
    """Frozen cost convention: depth + 1."""
    return depth(root, x) + 1


def _rotate_right(p: Node) -> None:
    """Single right rotation at p (ported)."""
    x = p.left
    assert x is not None
    p.left = x.right
    if x.right is not None:
        x.right.parent = p
    x.parent = p.parent
    if p.parent is not None:
        if p.parent.left is p:
            p.parent.left = x
        else:
            p.parent.right = x
    x.right = p
    p.parent = x


def _rotate_left(p: Node) -> None:
    """Single left rotation at p (ported)."""
    x = p.right
    assert x is not None
    p.right = x.left
    if x.left is not None:
        x.left.parent = p
    x.parent = p.parent
    if p.parent is not None:
        if p.parent.left is p:
            p.parent.left = x
        else:
            p.parent.right = x
    x.left = p
    p.parent = x


def splay(root: Node, x: int) -> tuple[Node, list[dict]]:
    """Splay x to root. Returns (new_root, rotation events).

    Event: {case, index, keys_local}. Cases: ZIG/LL/RR/RL/LR (ROOT sidedoor:
    x already root yields zero events; callers record case ROOT).
    """
    cur: Node | None = root
    while cur is not None and cur.key != x:
        cur = cur.left if x < cur.key else cur.right
    if cur is None:
        raise KeyError("key %d not in tree" % x)
    node = cur
    events: list[dict] = []
    idx = 0
    while node.parent is not None:
        p = node.parent
        g = p.parent
        if g is None:
            if p.left is node:
                _rotate_right(p)
            else:
                _rotate_left(p)
            events.append({"case": "ZIG", "index": idx,
                           "keys_local": sorted([p.key, node.key])})
        elif p.left is node and g.left is p:
            _rotate_right(g)
            _rotate_right(p)
            events.append({"case": "LL", "index": idx,
                           "keys_local": sorted([g.key, p.key, node.key])})
        elif p.right is node and g.right is p:
            _rotate_left(g)
            _rotate_left(p)
            events.append({"case": "RR", "index": idx,
                           "keys_local": sorted([g.key, p.key, node.key])})
        elif p.left is node and g.right is p:
            _rotate_right(p)
            _rotate_left(g)
            events.append({"case": "RL", "index": idx,
                           "keys_local": sorted([g.key, p.key, node.key])})
        elif p.right is node and g.left is p:
            _rotate_left(p)
            _rotate_right(g)
            events.append({"case": "LR", "index": idx,
                           "keys_local": sorted([g.key, p.key, node.key])})
        else:
            raise AssertionError("splay parent/child inconsistency")
        idx += 1
    return node, events


def stepwise_access(root: Node, x: int, nkeys: int, side: str, mode: str) -> tuple[list[dict], Node]:
    """Replay one access rotation-by-rotation (ported site semantics).

    Affected interval = key range of the rotated nodes (local site), matching
    the sealed site-faithful reading. Each step emits a frozen v0.4 rotation
    event: {side, mode, splay_case, keys, interval, x, nkeys, a_edge, y_edge}.
    a_edge/y_edge are per-event edge costs attached by the paired driver
    (single-access replay: full access cost on the terminal rotation, else 0).
    """
    cur: Node | None = root
    while cur is not None and cur.key != x:
        cur = cur.left if x < cur.key else cur.right
    if cur is None:
        raise KeyError("key %d not in tree" % x)
    node = cur
    steps: list[dict] = []
    while node.parent is not None:
        p = node.parent
        g = p.parent
        if g is None:
            case = "ZIG"
        elif p.left is node and g.left is p:
            case = "LL"
        elif p.right is node and g.right is p:
            case = "RR"
        elif p.left is node and g.right is p:
            case = "RL"
        else:
            case = "LR"
        keys = sorted({node.key, p.key} | ({g.key} if g is not None else set()))
        steps.append({"side": side, "mode": mode, "splay_case": case,
                      "keys": keys, "interval": [min(keys), max(keys)],
                      "x": x, "nkeys": nkeys, "a_edge": 0, "y_edge": 0})
        if case == "ZIG":
            if p.left is node:
                _rotate_right(p)
            else:
                _rotate_left(p)
        elif case == "LL":
            _rotate_right(g)
            _rotate_right(p)
        elif case == "RR":
            _rotate_left(g)
            _rotate_left(p)
        elif case == "RL":
            _rotate_right(p)
            _rotate_left(g)
        else:
            _rotate_left(p)
            _rotate_right(g)
    top = node
    while top.parent is not None:
        top = top.parent
    return steps, top


def build_balanced(keys: list[int]) -> Node | None:
    """Deterministic balanced BST from sorted keys (median root, ported)."""
    if not keys:
        return None
    mid = len(keys) // 2
    root = Node(keys[mid])
    root.left = build_balanced(keys[:mid])
    if root.left is not None:
        root.left.parent = root
    root.right = build_balanced(keys[mid + 1:])
    if root.right is not None:
        root.right.parent = root
    return root


def build_spine(keys: list[int], left: bool = True) -> Node | None:
    """Deterministic spine (ported). left=True: decreasing chain, root=max."""
    root: Node | None = None
    seq = sorted(keys) if left else sorted(keys, reverse=True)
    for k in seq:
        n = Node(k)
        if root is None:
            root = n
        elif left:
            n.left = root
            root.parent = n
            root = n
        else:
            n.right = root
            root.parent = n
            root = n
    return root


def serialize(root: Node | None) -> str:
    """Canonical structural string (ported)."""
    if root is None:
        return "."
    return "(%d%s%s)" % (root.key, serialize(root.left), serialize(root.right))


def inorder(root: Node | None) -> list[int]:
    """Inorder key list (ported)."""
    out: list[int] = []

    def rec(n: Node | None) -> None:
        if n is None:
            return
        rec(n.left)
        out.append(n.key)
        rec(n.right)

    rec(root)
    return out


def is_valid_bst(root: Node | None) -> bool:
    """Audit: inorder sorted and parent pointers consistent (v0.4 addition)."""
    keys = inorder(root)
    if keys != sorted(keys):
        return False

    def rec(n: Node | None) -> bool:
        if n is None:
            return True
        if n.left is not None and n.left.parent is not n:
            return False
        if n.right is not None and n.right.parent is not n:
            return False
        return rec(n.left) and rec(n.right)

    return rec(root)


def clone(root: Node | None) -> Node | None:
    """Deep copy preserving parent pointers (v0.4 addition for drivers)."""
    if root is None:
        return None
    n = Node(root.key)
    n.left = clone(root.left)
    if n.left is not None:
        n.left.parent = n
    n.right = clone(root.right)
    if n.right is not None:
        n.right.parent = n
    return n
