"""Shared demo runner — shows the failure / repair / receipt / report loop.

Each narrowed demo (demos/*.py) calls `run_scenario()` with its own tool
schema + before/after arguments. The runner prints a uniform three-column
report so all demos read the same way, and writes receipts to a
per-scenario NDJSON chain that `mtg report` can aggregate.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional


try:
    from mtg.adapters.openai import guard_tool
    from toolproof.mtg_bridge import receipt_from_mtg_run
    from toolproof.receipt import Receipt
except ImportError as exc:  # pragma: no cover
    print(
        "Missing dependency: install mtg-guards and toolproof first\n"
        f"  pip install mtg-guards toolproof\n\n{exc}",
        file=sys.stderr,
    )
    sys.exit(2)


@dataclass
class DemoStep:
    """A single before/after pair for a scenario."""

    label: str
    arguments: dict[str, Any]


def _load_tool(path: Path, reconciled: bool) -> dict:
    tool = json.loads(path.read_text(encoding="utf-8"))
    if reconciled:
        props = tool.get("parameters", {}).get("properties", {})
        for prop in props.values():
            if isinstance(prop, dict) and "x-mtg" in prop:
                prop["x-mtg"]["mode"] = "reconciled"
    return tool


def run_scenario(
    title: str,
    tool_path: Path,
    steps: list[DemoStep],
    chain_path: Path,
) -> list[Receipt]:
    """Run each step twice: once without MTG (advisory), once with
    reconciled-mode MTG. Emit signed receipts for both variants to
    `chain_path`, and print a uniform before/after report.
    """
    print(f"\n{'=' * 72}\n{title}\n{'=' * 72}")
    print(f"tool: {tool_path.name}\n")

    tool_advisory = _load_tool(tool_path, reconciled=False)
    tool_reconciled = _load_tool(tool_path, reconciled=True)

    if chain_path.exists():
        chain_path.unlink()
    chain_path.parent.mkdir(parents=True, exist_ok=True)
    prev_hash: Optional[str] = None

    receipts: list[Receipt] = []

    for step in steps:
        print(f"--- {step.label} ---")
        for arm_label, tool_def in [
            ("advisory (no repair)", tool_advisory),
            ("reconciled (with repair)", tool_reconciled),
        ]:
            wrapped = guard_tool(tool_def)
            report = wrapped.validate_call({"arguments": step.arguments})
            receipt = receipt_from_mtg_run(
                tool=f"{tool_def['name']}@{arm_label.split()[0]}",
                guards=report.to_dict()["per_param"],
                arguments=step.arguments,
                prev_receipt_hash=prev_hash,
            )
            prev_hash = receipt.hash
            receipts.append(receipt)
            with chain_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(receipt.to_dict(), ensure_ascii=False) + "\n")

            # Summary line
            viol_codes = sorted({v["code"] for v in receipt.mtg_violations})
            repair_actions = sorted({r["action"] for r in receipt.mtg_repairs})
            print(f"  {arm_label:30s} outcome={receipt.outcome:8s} "
                  f"violations={viol_codes or '—'} "
                  f"repairs={repair_actions or '—'}")

            # Print repaired surface delta when present
            for repair in receipt.mtg_repairs:
                if repair.get("proposed"):
                    print(
                        f"    → repair {repair['action']} on {repair['param']}: "
                        f"{repair['original']!r} → {repair['proposed']!r}"
                    )
        print()

    print(f"wrote {len(receipts)} signed receipts → {chain_path}")
    print(f"inspect: mtg report {chain_path} --html /tmp/scorecard.html\n")
    return receipts
