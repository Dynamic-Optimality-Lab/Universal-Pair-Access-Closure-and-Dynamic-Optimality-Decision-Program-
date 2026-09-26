"""python/audit/log.py — canonical append-only run-record logger (spec s27, WP-2-REQ-020).

Exactly the 24 normative fields, in order, one JSON object per line, appended to
artifacts/v04/logs/WP2_RUN_RECORDS.jsonl. Key set asserted exactly (no more, no
fewer). Wall time via perf_counter; peak memory via tracemalloc (bytes, CPython
allocation peak). No theorem-facing logic lives here.
"""
import hashlib
import json
import subprocess
import time
import tracemalloc
from pathlib import Path

IMPL = Path(__file__).resolve().parents[2]
RECORDS = IMPL / "artifacts/v04/logs/WP2_RUN_RECORDS.jsonl"

FIELDS = ["experiment_id", "phase", "UTC timestamp", "local commit",
          "parent v0.3 commit", "spec SHA", "prereg SHA",
          "theorem battlefield SHA", "Lean toolchain hash",
          "bridge source manifest SHA", "MSTC-0002 SHA", "current theorem ID",
          "prove/refute track", "statement SHA", "negation SHA",
          "dependency SHAs", "command", "input hashes", "output hashes",
          "stdout/stderr hashes", "wall time", "peak memory", "exit code",
          "scientific status"]

SPEC_SHA = "30acc6f96abc35a9a4fc91ad159560888e54180f55be21f947b59dff8b62b5f9"
PARENT_PIN = "353ee922b1cee0043afa46fe8929f42f7652e5bf"


def _sha_file(rel):
    return hashlib.sha256((IMPL / rel).read_bytes()).hexdigest()


def _git_head():
    r = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(IMPL),
                       capture_output=True, text=True, timeout=60)
    return r.stdout.strip()


def _battlefield():
    import yaml
    return yaml.safe_load((IMPL / "prereg/theorem_battlefield.yaml").read_text(encoding="utf-8"))


def base_record(theorem_id, track, command):
    """Static-field scaffold for one run record (timing/outputs filled by caller)."""
    import re
    nodes = _battlefield()["nodes"]
    bf = nodes[theorem_id]
    pre = bf.get("prerequisites", "")
    if isinstance(pre, list):
        pre = " ".join(pre)
    deps = []
    for tok in sorted(set(re.findall(r"MST0-(?:08U|09|11|13|14|15|22|17|18|19)", pre))):
        key = "MST0-" + tok.split("-")[1]
        if key in nodes and "document_sha256" in nodes[key]:
            deps.append(nodes[key]["document_sha256"])
    if "frozen" in pre.lower():
        deps.append(_sha_file("lean/Frozen/SplayDefs.lean"))
        deps.append(_sha_file("lean/Frozen/MSTC0002Defs.lean"))
        deps.append(_sha_file("lean/Frozen/Statements.lean"))
    return {
        "experiment_id": "SPLAY-AM-DECIDE-v0.4",
        "phase": "WP-2",
        "UTC timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "local commit": _git_head(),
        "parent v0.3 commit": PARENT_PIN,
        "spec SHA": SPEC_SHA,
        "prereg SHA": _sha_file("prereg/prereg_sha256.txt"),
        "theorem battlefield SHA": _sha_file("prereg/theorem_battlefield.yaml"),
        "Lean toolchain hash": _sha_file("lean-toolchain"),
        "bridge source manifest SHA": _sha_file("prereg/bridge_sources.yaml"),
        "MSTC-0002 SHA": _sha_file("parent/V03_MSTC_0002.json"),
        "current theorem ID": theorem_id,
        "prove/refute track": track,
        "statement SHA": bf.get("statement_sha256", "N/A-BLOCKED"),
        "negation SHA": bf.get("negation_sha256", "N/A-BLOCKED"),
        "dependency SHAs": sorted(set(deps)),
        "command": command,
        "input hashes": [],
        "output hashes": [],
        "stdout/stderr hashes": [],
        "wall time": 0.0,
        "peak memory": 0,
        "exit code": 2,
        "scientific status": "NOT_RUN",
    }


class Timer:
    """Wall + peak-memory measurement context (tracemalloc peak, bytes)."""

    def __enter__(self):
        tracemalloc.start()
        self._t0 = time.perf_counter()
        return self

    def __exit__(self, *exc):
        self.wall = time.perf_counter() - self._t0
        _cur, self.peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()


def emit_run_record(record):
    """Append one record; key set must equal FIELDS exactly (fail-closed)."""
    if sorted(record.keys()) != sorted(FIELDS):
        raise ValueError(f"run-record field mismatch: {sorted(record.keys())}")
    ordered = {k: record[k] for k in FIELDS}
    with open(RECORDS, "a", encoding="utf-8") as f:
        f.write(json.dumps(ordered, sort_keys=False) + "\n")
    # WP-2 STEP LOG-01: run record appended (forensic reconstruction pointer).
    print(f"[WP-2][STEP LOG-01] appended run record {record['current theorem ID']}/"
          f"{record['prove/refute track']}/{record['scientific status']}", flush=True)
    return ordered
