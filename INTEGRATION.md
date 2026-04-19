# Hurmoz integration

How Hurmoz (this repo) fits into the broader Arabic agent stack:

```
arabic-agent-eval  ─┐    (benchmark + canonical grader)
                    │
                    ├──▶ atropos/arabic_tool_calling  (RL environment)
                    │
                    ├──▶ mtg                          (type-system primitive)
                    │         │
                    │         ▼
                    │     toolproof 0.5               (evidence layer)
                    │
                    ▼
                  hurmoz                              (downstream consumer)
```

Hurmoz is the **downstream application layer**. It consumes the benchmark for coverage validation, MTG for tool-argument guards, and ToolProof for call-level auditing. None of those three depend on Hurmoz — the dependency flows one way.

## What Hurmoz is

**63 Arabic AI skills for the Hermes Agent.** Islamic services (prayer times, Hijri calendar, Quran search, Zakat), Saudi government APIs, Arabic NLP tools, communication, and dialect-aware helpers. Each skill is a YAML-frontmatter `SKILL.md` file that declares how the Hermes agent should invoke real APIs or local CLIs when the user requests the corresponding capability in Arabic.

## What Hurmoz is NOT

- Not the research flagship — that's [mtg](https://github.com/Moshe-ship/mtg).
- Not a benchmark — that's [arabic-agent-eval](https://github.com/Moshe-ship/arabic-agent-eval).
- Not a verification or receipt system — that's [ToolProof](https://github.com/Moshe-ship/toolproof).
- Not a wrapper around Hermes — it's a skill pack Hermes profiles load.

## Integration points

### 1. Coverage validation against `arabic-agent-eval`

Every Hurmoz skill that claims to support function-calling use cases is validated against the Arabic Agent Eval benchmark.

```bash
pip install arabic-agent-eval
export OPENROUTER_API_KEY=...
aae run --provider openrouter --model nousresearch/hermes-4-70b \
        --md-output reports/hurmoz-coverage.md
```

Rollout numbers for skills whose tools appear in `arabic_agent_eval/functions.py` (e.g. `send_message`, `get_prayer_times`, `calculate_zakat`, `find_quran_verse`, `search_restaurants`) should be tracked over time. A skill is considered "benchmarked" if at least one matching eval item exists upstream.

### 2. Tool-argument annotation via MTG

Tool schemas under `tool-schemas/` carry MTG `x-mtg` blocks on Arabic-valued parameters. Consumer frameworks that understand MTG (via [mtg-guards](https://github.com/Moshe-ship/mtg) adapters) will automatically validate arguments at pre-call and post-call time.

Example — `tool-schemas/send_message.json`:

```json
{
  "name": "send_message",
  "parameters": {
    "properties": {
      "message": {
        "type": "string",
        "x-mtg": {
          "slot_type": "free_text",
          "script": "ar",
          "dialect_expected": "any",
          "transliteration_allowed": false,
          "post_call_contract": ["script_match", "dialect_preserve"]
        }
      }
    }
  }
}
```

Consumers without MTG ignore the `x-mtg` field per JSON Schema extension rules — so the annotations are strictly additive.

> **⚠️ Dialect binding is a schema choice, not an MTG behavior.**
>
> The base `send_message.json` uses `dialect_expected: "any"` — a neutral default. If your product is bound to one dialect (Saudi → Gulf, Egyptian → Egy, etc.), register `send_message_gulf.json` / `_egy.json` / `_lev.json` / `_msa.json` at the router level. A product that expects strict dialect enforcement but registers the base schema will get `dialect_expected=None` on every receipt — that's a schema selection bug.
>
> See [tool-schemas/README.md#dialect-variants--when-to-use-which](tool-schemas/README.md#dialect-variants--when-to-use-which) for the full router pattern.

### 3. Call receipts via ToolProof 0.5

Skills that touch external APIs or user data emit ToolProof receipts on every call. MTG violations bridge into ToolProof via `toolproof.mtg_bridge.receipt_from_mtg_run`:

```python
from toolproof.mtg_bridge import receipt_from_mtg_run
from mtg.pipeline import validate_pre
from mtg.types import GuardSpec

# When a hurmoz skill tool fires, wrap the call:
spec = GuardSpec.from_dict({...})  # loaded from tool-schemas/*.json
guard = validate_pre(user_message, spec)
receipt = receipt_from_mtg_run(
    tool="send_message",
    guards={"message": guard.to_dict()},
    arguments={"message": user_message},
)
# receipt gets appended to ~/.toolproof/receipts.jsonl
```

### 4. Annotated tool schemas

`tool-schemas/` contains 10 JSON Schema tool definitions with `x-mtg` annotations, covering the highest-value Hurmoz skills, plus 4 dialect-specialized variants for `send_message`:

| File | Hurmoz skill | Why MTG matters here |
|---|---|---|
| `prayer_times.json` | `prayer-times` | City names in Arabic must not transliterate |
| `quran_search.json` | `quran-search` | Search query must stay Arabic to match Quran corpus |
| `hijri_calendar.json` | `hijri-calendar` | Date strings have dialect-aware variants |
| `calculate_zakat.json` | `islamic-finance` | Currency names often code-switch; must validate |
| `translate.json` | `translate` | Source text must preserve script |
| `dialect_detect.json` | `dialect-detect` | Entire skill is dialect-aware — core MTG use case |
| `tashkeel.json` | `tashkeel` | Diacritization must preserve base letters exactly |
| `send_message.json` | `unifonic` + `whisper-arabic` | Base: `dialect_expected=any` (no enforcement) |
| `send_message_gulf.json` | same | Gulf-bound: `dialect_expected=gulf`, DIALECT_DRIFT fires on non-Gulf |
| `send_message_egy.json` | same | Egyptian-bound: `dialect_expected=egy` |
| `send_message_lev.json` | same | Levantine-bound: `dialect_expected=lev` |
| `send_message_msa.json` | same | MSA-bound: `dialect_expected=msa` |
| `saudi_address.json` | `saudi-address` | Address fields are mixed script + named entities |
| `arabic_grammar.json` | `arabic-grammar` | Corrected text must stay in same register |

All schemas land at `tool-schemas/*.json`. Derived from the corresponding `*/SKILL.md` files' bash invocation surfaces — these are *machine-readable* companions to the human-readable skills.

## Dependency graph

Runtime (at skill invocation):

- `arabic_agent_eval` — optional, for validation tests
- `mtg` (mtg-guards) — optional, for argument guards
- `toolproof` — optional, for signed receipts
- Hermes Agent v0.7.0+ — required, for skill loading

None of these are hard dependencies of Hurmoz. The `hermes:` frontmatter and YAML metadata work without any Python package installed. The Python packages are additive improvements.

## Upstream roadmap

1. **arabic-agent-eval** → public GitHub + HF dataset mirror
2. **mtg** → public GitHub + arXiv note
3. **atropos env** → PR to NousResearch/atropos
4. **arabic-agent-eval** → discussion issue on NousResearch/Hermes-Function-Calling for dialect-split eval integration
5. **toolproof 0.5** → PyPI release with MTG bridge
6. **hurmoz** → continue as the downstream reference consumer

## References

- [arabic-agent-eval](https://github.com/Moshe-ship/arabic-agent-eval)
- [mtg](https://github.com/Moshe-ship/mtg)
- [toolproof](https://github.com/Moshe-ship/toolproof)
- [artok](https://github.com/Moshe-ship/artok) — Arabic token cost calculator (future MTG compression work)
- [NousResearch/Hermes-Function-Calling](https://github.com/NousResearch/Hermes-Function-Calling)
- [NousResearch/atropos](https://github.com/NousResearch/atropos)
