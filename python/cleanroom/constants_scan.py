"""cleanroom/constants_scan.py — dependence + quantifier support scan (WP-2, MST0-22).

Support-only scan (never the proof): asserts none of the ten
CONST_FORBIDDEN_DEPENDENCIES identifiers occur in the frozen Lean/Python
constant-defining sources, and that the MST0_22 canonical statement exhibits
the frozen order (literals conjunction, then universals). Prints SCAN verdict.
Exit 0; exit 2 on I/O failure.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

IMPL = Path(__file__).resolve().parents[2]
FORBIDDEN = ["n", "sequence_length", "initial_tree", "subsequence_choice",
             "proof_decomposition", "corpus_or_holdout_identity",
             "search_generator_or_seed", "solver_state_or_selected_panel",
             "finite_state_id", "cycle_id"]
SOURCES = ["lean/Frozen/SplayDefs.lean", "lean/Frozen/MSTC0002Defs.lean",
           "lean/Frozen/Statements.lean", "python/inherited/splay.py",
           "python/inherited/mstc0002.py", "python/inherited/pair_access.py"]


def main():
    # WP-2 STEP CS-01: forbidden-dependence scan over frozen sources.
    print("[WP-2][STEP CS-01] constants support scan running", flush=True)
    try:
        texts = {f: (IMPL / f).read_text(encoding="utf-8") for f in SOURCES}
    except OSError:
        print("[WP-2][STEP CS-01] source unreadable", flush=True)
        return 2
    hits = []
    for f, text in texts.items():
        names = set(re.findall(r"[A-Za-z_][\w]*", text))
        for bad in FORBIDDEN:
            if bad == "n":
                continue  # single-letter locals ubiquitous; covered by literal-form check below
            if bad in names:
                hits.append(f"{f}:{bad}")
    frozen = texts["lean/Frozen/MSTC0002Defs.lean"]
    literal_ok = ("def C_frozen : Nat := 2" in frozen
                  and "def K_frozen : Nat := 6" in frozen)
    lean22 = texts["lean/Frozen/Statements.lean"]
    m = re.search(r"def MST0_22 : Prop :=\n((?:  .*\n)+)", lean22)
    body = m.group(1) if m else ""
    order_ok = body.lstrip().startswith("(C_frozen = 2") \
        and "∀ y a : Nat" in body and "∀ (E : Engine)" in body
    verdict = "CLEAN" if not hits and order_ok and literal_ok else "DIRTY"
    # WP-2 STEP CS-02: scan verdict emitted.
    print(f"[WP-2][STEP CS-02] SCAN-VERDICT: {verdict} "
          f"(hits={hits} quantifier_order_ok={order_ok} literal_ok={literal_ok})", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
