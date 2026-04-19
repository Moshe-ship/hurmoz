"""Smoke test for examples/dialect_router.py — the closed-loop reference."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "examples"))

try:
    import dialect_router  # type: ignore[import-not-found]
except ImportError as exc:  # pragma: no cover
    pytest.skip(f"mtg / toolproof not installed: {exc}", allow_module_level=True)


def test_gulf_clean_routes_to_gulf_variant_pass():
    receipt, repaired = dialect_router.route_and_execute("أبي أحجز فندق في دبي")
    assert receipt.dialect_expected == "gulf"
    assert receipt.outcome == "pass"
    assert repaired is None
    assert receipt.verify_integrity()


def test_egyptian_clean_routes_to_egy_variant_pass():
    receipt, _ = dialect_router.route_and_execute("عايز أبعت رسالة دلوقتي")
    assert receipt.dialect_expected == "egy"
    assert receipt.outcome == "pass"
    assert receipt.verify_integrity()


def test_levantine_clean_routes_to_lev_variant_pass():
    receipt, _ = dialect_router.route_and_execute("بدي احكي مع احمد")
    assert receipt.dialect_expected == "lev"
    assert receipt.outcome == "pass"


def test_arabizi_triggers_repair_suggestion():
    receipt, repaired = dialect_router.route_and_execute("abi a7jez funduq fi dubai")
    assert receipt.outcome == "fail"
    assert repaired is not None
    # Repair produced real Arabic script
    assert any("\u0600" <= ch <= "\u06FF" for ch in repaired)
    # Receipt carries the repair in mtg_repairs (evidence_hash-protected)
    assert any(r["action"] == "arabizi_to_arabic" for r in receipt.mtg_repairs)
    assert receipt.verify_integrity()
    # Tampering with the repair must break verify
    receipt.mtg_repairs = []
    assert not receipt.verify_integrity()


def test_english_falls_to_base_schema_script_violation():
    receipt, _ = dialect_router.route_and_execute("Book me a hotel in Dubai")
    # Base schema has dialect_expected=any — unset on the receipt
    assert receipt.dialect_expected is None
    assert receipt.outcome == "fail"


def test_receipts_form_a_hash_chain_when_prev_hash_threaded():
    r1, _ = dialect_router.route_and_execute("أبي أحجز فندق")
    r2, _ = dialect_router.route_and_execute("بدي احكي مع احمد", prev_hash=r1.hash)
    assert r2.hash_prev == r1.hash
    assert r1.hash != r2.hash
    assert r1.verify_integrity() and r2.verify_integrity()
