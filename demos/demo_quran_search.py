"""Demo 3 — Quran search (religious / content correctness).

find_quran_verse expects MSA-register Arabic queries that match the
Quranic corpus. Failure modes:

  - query written in Arabizi (won't match the corpus at all)
  - query in dialect (Egyptian / Gulf) — DIALECT_DRIFT fires because
    the schema declared dialect_expected=msa for corpus alignment
  - surface-corruption post-call: some APIs echo the query back
    transliterated; our post_call_contract catches that

For content / religious applications, surface corruption is worse than
a simple missed match — a wrong echo in a Quran-search UI is a quality
and trust failure. MTG catches it before the user sees it.
"""

from __future__ import annotations

from pathlib import Path

from _runner import DemoStep, run_scenario


HERE = Path(__file__).resolve().parent
TOOL = HERE.parent / "tool-schemas" / "quran_search.json"
CHAIN = Path.home() / ".toolproof" / "demos" / "quran_search.ndjson"


def main() -> int:
    run_scenario(
        title="Demo 3 — Quran search (MSA-bound content correctness)",
        tool_path=TOOL,
        steps=[
            DemoStep(
                label="clean MSA query",
                arguments={
                    "query": "الرحمن الرحيم",
                    "surah": 1,
                },
            ),
            DemoStep(
                label="Egyptian-dialect query (drift)",
                arguments={
                    "query": "عايز أدور على آيه فيها رحمه",
                    "surah": 1,
                },
            ),
            DemoStep(
                label="Arabizi query",
                arguments={
                    "query": "al-ra7man al-ra7im",
                    "surah": 1,
                },
            ),
            DemoStep(
                label="invisible-char padding attack",
                # ZWSP between Arabic letters can break text-match lookups
                arguments={
                    "query": "الرحمن\u200bالرحيم",
                    "surah": 1,
                },
            ),
        ],
        chain_path=CHAIN,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
