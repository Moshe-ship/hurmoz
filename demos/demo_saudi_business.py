"""Demo 2 — Saudi business address lookup.

The Saudi national address API expects:
  - 5-digit postal code (Latin digits only)
  - 4-digit additional number (Latin digits only)
  - city name (Arabic, preserved)

Failure modes we show:
  - city transliterated to Latin ("Riyadh" instead of "الرياض")
  - postal code smuggled with Arabic-Indic digits (٠١٢٣٤) — SCRIPT_HOMOGLYPH
  - BiDi control injection to reorder the code for display

Each scenario runs in both advisory and reconciled mode so you can see
MTG's detection rate AND what repair surfaces look like.
"""

from __future__ import annotations

from pathlib import Path

from _runner import DemoStep, run_scenario


HERE = Path(__file__).resolve().parent
TOOL = HERE.parent / "tool-schemas" / "saudi_address.json"
CHAIN = Path.home() / ".toolproof" / "demos" / "saudi_business.ndjson"


def main() -> int:
    run_scenario(
        title="Demo 2 — Saudi address lookup (mixed-script surface)",
        tool_path=TOOL,
        steps=[
            DemoStep(
                label="clean Saudi address",
                arguments={
                    "postal_code": "12345",
                    "additional_number": "6789",
                    "city": "الرياض",
                },
            ),
            DemoStep(
                label="city transliterated to Latin",
                arguments={
                    "postal_code": "12345",
                    "additional_number": "6789",
                    "city": "Riyadh",  # must flag SCRIPT_VIOLATION
                },
            ),
            DemoStep(
                label="postal code with Arabic-Indic digit homoglyphs",
                # "١٢٣٤٥" looks like "12345" but is U+0661..U+0665
                arguments={
                    "postal_code": "١٢٣٤٥",
                    "additional_number": "6789",
                    "city": "الرياض",
                },
            ),
            DemoStep(
                label="BiDi RLO override injected into postal code",
                # U+202E flips display of the digits — Trojan Source class
                arguments={
                    "postal_code": "12\u202e345",
                    "additional_number": "6789",
                    "city": "الرياض",
                },
            ),
        ],
        chain_path=CHAIN,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
