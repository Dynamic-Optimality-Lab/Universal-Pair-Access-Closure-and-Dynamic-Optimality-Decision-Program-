"""REP-12/REP-14 truthful split tests (repair track; historical file untouched).

REP-12-MECHANISM: SATISFIED (MST0_14_paid_identity present, no sorry/admit).
REP-12-UNIVERSAL: NOT_SATISFIED — MST0-14R sufficiency is mathematically
  refuted by an exact legal witness; a universal proof is impossible.
  strict-xfail records the status in-suite (can never XPASS while refuted).
REP-14-PACKAGE: SATISFIED as packaging only (PACKAGE.md PENDING-HUMAN, zero
  .review.json fabricated).
REP-14-HUMAN: NOT_SATISFIED — no human verdict recorded or inferred.
  strict-xfail flips loudly (suite failure) if a human verdict ever lands,
  forcing an honest test update at that time.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

IMPL = Path(__file__).resolve().parents[2]


def test_REP_12M_mechanism():
    txt = (IMPL / "lean/Proofs/Repayment.lean").read_text(encoding="utf-8")
    assert "theorem MST0_14_paid_identity" in txt
    assert "sorry" not in txt and "admit" not in txt


@pytest.mark.xfail(strict=True, reason="MST0-14R sufficiency mathematically "
                   "refuted (canonical legal witness n=28, margin -1); "
                   "universal proof impossible; see MST0-14R_LEGAL_WITNESS.json")
def test_REP_12U_universal():
    txt = (IMPL / "lean/Proofs/Repayment.lean").read_text(encoding="utf-8")
    assert "theorem MST0_14_sufficiency" in txt or \
        "theorem RepairedMST0_14_proved" in txt


def test_REP_14P_package():
    pkg = IMPL / "math/reviews/MST0-14.PACKAGE.md"
    assert pkg.exists()
    assert "PENDING-HUMAN" in pkg.read_text(encoding="utf-8")
    assert not list((IMPL / "math/reviews").glob("MST0-14.review.json"))


@pytest.mark.xfail(strict=True, reason="no human ACCEPT/REJECT/BLOCKED verdict "
                   "recorded for MST0-14 (or its successor); verdicts are "
                   "human-only and never generated")
def test_REP_14H_human():
    assert list((IMPL / "math/reviews").glob("MST0-14*.review.json")) or \
        list((IMPL / "math/reviews").glob("MST0-14R*.review.json"))
