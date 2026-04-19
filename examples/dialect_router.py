"""Closed-loop dialect router for send_message.

Detect the user's dialect → pick the matching send_message_<dialect>.json
variant → run MTG in reconciled mode → emit a ToolProof receipt carrying
original + repair delta. This is the pattern downstream products should
copy when they want strict dialect expectations bound at schema level.

Run:

    pip install mtg-guards toolproof
    python examples/dialect_router.py

Produces one receipt per sample message in a local NDJSON chain, then
prints an `mtg report` summary.

No network, no LLM calls. Everything deterministic and inspectable.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Optional

try:
    from mtg.adapters.openai import guard_tool
    from mtg.dialect import KeywordDialectClassifier
    from mtg.types import GuardSpec  # noqa: F401 — surfaces the public API
    from toolproof.mtg_bridge import receipt_from_mtg_run
    from toolproof.receipt import Receipt
except ImportError as exc:  # pragma: no cover
    print(
        "Missing dependency: install mtg-guards and toolproof first\n"
        f"  pip install mtg-guards toolproof\n\n{exc}",
        file=sys.stderr,
    )
    sys.exit(2)


HERE = Path(__file__).resolve().parent
SCHEMAS = HERE.parent / "tool-schemas"

# Map detected dialect → specialized variant. None falls back to the
# dialect-agnostic base schema.
DIALECT_TO_SCHEMA = {
    "gulf": SCHEMAS / "send_message_gulf.json",
    "egy":  SCHEMAS / "send_message_egy.json",
    "lev":  SCHEMAS / "send_message_lev.json",
    "msa":  SCHEMAS / "send_message_msa.json",
    None:   SCHEMAS / "send_message.json",
}


def load_tool(dialect: Optional[str], reconciled: bool = True) -> dict:
    """Load the send_message schema bound to `dialect` (or the base
    schema when dialect is None). When `reconciled=True`, flip the
    message slot's mode so MTG proposes repairs on violations."""
    path = DIALECT_TO_SCHEMA.get(dialect, DIALECT_TO_SCHEMA[None])
    tool = json.loads(path.read_text(encoding="utf-8"))
    if reconciled:
        props = tool.get("parameters", {}).get("properties", {})
        for prop in props.values():
            if isinstance(prop, dict) and "x-mtg" in prop:
                prop["x-mtg"]["mode"] = "reconciled"
    return tool


def detect_dialect(text: str, confidence_floor: float = 0.75) -> Optional[str]:
    """Classify the dialect of `text`. Returns None on low confidence so
    the caller can fall back to the dialect-agnostic base schema instead
    of pinning the wrong dialect."""
    classifier = KeywordDialectClassifier()
    detected, confidence = classifier.classify(text)
    if detected == "unknown" or confidence < confidence_floor:
        return None
    return detected


def route_and_execute(
    message: str,
    recipient: str = "أحمد",
    platform: str = "whatsapp",
    prev_hash: Optional[str] = None,
) -> tuple[Receipt, Optional[str]]:
    """Close the full loop: detect → variant → MTG → repair → receipt.

    Returns (receipt, repaired_surface_if_any).
    """
    dialect = detect_dialect(message)
    tool = load_tool(dialect, reconciled=True)
    wrapped = guard_tool(tool)
    arguments = {"recipient": recipient, "platform": platform, "message": message}
    report = wrapped.validate_call({"arguments": arguments})

    repaired: Optional[str] = None
    for name, guard in report.per_param.items():
        if name == "message" and guard.repaired_surface:
            repaired = guard.repaired_surface
            break

    tool_name = tool["name"]
    receipt = receipt_from_mtg_run(
        tool=tool_name,
        guards=report.to_dict()["per_param"],
        arguments=arguments,
        prev_receipt_hash=prev_hash,
    )
    return receipt, repaired


def _emit(receipt: Receipt, chain_path: Path) -> None:
    chain_path.parent.mkdir(parents=True, exist_ok=True)
    with chain_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(receipt.to_dict(), ensure_ascii=False) + "\n")


def demo(chain_path: Path) -> None:
    samples = [
        # (label, message) — each demonstrates a different router path
        ("Gulf (clean)",       "أبي أحجز فندق في دبي"),
        ("Egyptian (clean)",   "عايز أبعت رسالة دلوقتي"),
        ("Levantine (clean)",  "بدي احكي مع احمد"),
        ("MSA (clean)",        "أريد إرسال رسالة إلى أحمد"),
        ("Arabizi (needs repair)", "abi a7jez funduq fi dubai"),
        ("English (unknown → base)", "Book me a hotel in Dubai"),
    ]

    if chain_path.exists():
        chain_path.unlink()

    print(f"{'label':28s} {'detected':10s} {'outcome':8s}  message")
    print("-" * 100)
    prev_hash: Optional[str] = None
    for label, msg in samples:
        receipt, repaired = route_and_execute(msg, prev_hash=prev_hash)
        _emit(receipt, chain_path)
        prev_hash = receipt.hash
        detected = receipt.dialect_expected or "(none)"
        marker = " → repair:" if repaired else ""
        print(f"{label:28s} {detected:10s} {receipt.outcome:8s}  {msg!r}")
        if repaired:
            print(f"{' ':28s} {' ':10s} {' ':8s}    {marker} {repaired!r}")
        if receipt.mtg_violations:
            codes = sorted({v['code'] for v in receipt.mtg_violations})
            print(f"{' ':28s} {' ':10s} {' ':8s}    violations: {codes}")

    print()
    print(f"wrote {len(samples)} signed receipts → {chain_path}")
    print("inspect with:")
    print(f"  mtg report {chain_path} --html /tmp/scorecard.html")


def main() -> int:
    chain = Path.home() / ".toolproof" / "dialect_router_chain.ndjson"
    demo(chain)
    return 0


if __name__ == "__main__":
    sys.exit(main())
