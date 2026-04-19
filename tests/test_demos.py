"""Smoke tests for the three narrowed demos.

Each demo is a runnable script. These tests verify the scripts produce
the expected outcome shape so they don't silently regress as MTG evolves.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "demos"))

try:
    import _runner  # type: ignore[import-not-found]
    import demo_send_message  # type: ignore[import-not-found]
    import demo_saudi_business  # type: ignore[import-not-found]
    import demo_quran_search  # type: ignore[import-not-found]
except ImportError as exc:  # pragma: no cover
    pytest.skip(f"mtg / toolproof not installed: {exc}", allow_module_level=True)


@pytest.fixture
def tmp_chain(tmp_path, monkeypatch):
    """Redirect HOME so each test gets a clean ~/.toolproof/demos dir."""
    monkeypatch.setenv("HOME", str(tmp_path))
    # The demos use Path.home() at module load time — re-exec via run fn
    return tmp_path


def test_send_message_demo_produces_expected_outcome_mix(tmp_chain):
    # Reload demo module under the new HOME so CHAIN resolves into tmp
    import importlib
    import demo_send_message as m  # noqa: F811
    importlib.reload(m)
    m.main()
    chain = Path(m.CHAIN)
    assert chain.exists()
    receipts = [json.loads(line) for line in chain.read_text(encoding="utf-8").splitlines() if line]
    # 3 scenarios × 2 arms = 6 receipts
    assert len(receipts) == 6
    outcomes = [r["outcome"] for r in receipts]
    assert outcomes.count("pass") >= 2   # clean pair
    assert outcomes.count("fail") >= 2   # Arabizi pair


def test_saudi_business_demo_catches_bidi_and_homoglyph(tmp_chain):
    import importlib
    import demo_saudi_business as m
    importlib.reload(m)
    m.main()
    receipts = [
        json.loads(line)
        for line in Path(m.CHAIN).read_text(encoding="utf-8").splitlines() if line
    ]
    # 4 scenarios × 2 arms = 8 receipts
    assert len(receipts) == 8
    codes = {c for r in receipts for c in (v["code"] for v in r.get("mtg_violations", []))}
    # The demo deliberately includes all three of these
    assert "BIDI_CONTROL_SMUGGLING" in codes
    assert "SCRIPT_HOMOGLYPH" in codes
    assert "SCRIPT_VIOLATION" in codes


def test_quran_search_demo_catches_dialect_and_invisible(tmp_chain):
    import importlib
    import demo_quran_search as m
    importlib.reload(m)
    m.main()
    receipts = [
        json.loads(line)
        for line in Path(m.CHAIN).read_text(encoding="utf-8").splitlines() if line
    ]
    assert len(receipts) == 8
    codes = {c for r in receipts for c in (v["code"] for v in r.get("mtg_violations", []))}
    assert "DIALECT_DRIFT" in codes
    assert "INVISIBLE_CONTENT" in codes


def test_demos_produce_signed_receipts_with_integrity(tmp_chain):
    """Every receipt must have a non-empty evidence_hash and verify_integrity."""
    from toolproof.receipt import Receipt
    import importlib
    import demo_send_message as m
    importlib.reload(m)
    m.main()
    for line in Path(m.CHAIN).read_text(encoding="utf-8").splitlines():
        if not line:
            continue
        r = Receipt.from_dict(json.loads(line))
        assert r.evidence_hash, "demo receipt missing evidence_hash"
        assert r.verify_integrity(), f"demo receipt failed verify: {r.id}"


def test_reconciled_mode_repairs_appear_in_receipts(tmp_chain):
    """Reconciled-mode arms must surface at least one concrete repair."""
    import importlib
    import demo_send_message as m
    importlib.reload(m)
    m.main()
    receipts = [
        json.loads(line)
        for line in Path(m.CHAIN).read_text(encoding="utf-8").splitlines() if line
    ]
    reconciled = [r for r in receipts if "reconciled" in r["tool_name"]]
    any_repair = any(
        r.get("mtg_repairs")
        for r in reconciled
    )
    assert any_repair, "no repairs surfaced in reconciled-mode receipts"
