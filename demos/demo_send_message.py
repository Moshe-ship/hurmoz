"""Demo 1 — send_message_gulf.

Three scenarios, each one is a message a Gulf-market product might see
from the LLM. The demo shows:

  - clean Gulf input → pass
  - Egyptian register → DIALECT_DRIFT, advisory-only repair suggestion
  - Arabizi → SCRIPT + TRANSLIT violation, reconciled repair proposes
    a naive Arabic reverse-transliteration

For each scenario, the same call runs in advisory (no repair) and
reconciled (with repair). The receipt chain captures both so `mtg report`
can quantify the drop-rate and repair-available-rate.
"""

from __future__ import annotations

from pathlib import Path

from _runner import DemoStep, run_scenario


HERE = Path(__file__).resolve().parent
TOOL = HERE.parent / "tool-schemas" / "send_message_gulf.json"
CHAIN = Path.home() / ".toolproof" / "demos" / "send_message.ndjson"


def main() -> int:
    run_scenario(
        title="Demo 1 — send_message (Gulf-bound market)",
        tool_path=TOOL,
        steps=[
            DemoStep(
                label="clean Gulf message",
                arguments={
                    "recipient": "أحمد",
                    "platform": "whatsapp",
                    "message": "أبي أحجز فندق في دبي",
                },
            ),
            DemoStep(
                label="Egyptian register in a Gulf-bound slot",
                arguments={
                    "recipient": "أحمد",
                    "platform": "whatsapp",
                    "message": "عايز أبعت رسالة دلوقتي",
                },
            ),
            DemoStep(
                label="Arabizi — model returned Romanized Arabic",
                arguments={
                    "recipient": "أحمد",
                    "platform": "whatsapp",
                    "message": "abi a7jez funduq fi dubai",
                },
            ),
        ],
        chain_path=CHAIN,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
