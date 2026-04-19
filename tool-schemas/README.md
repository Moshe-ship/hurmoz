# Hurmoz tool schemas

JSON Schema tool definitions for 10 Hurmoz skills, annotated with MTG (Morphological Type Guards) `x-mtg` blocks on Arabic-valued parameters.

## Why these files exist

The 60+ `SKILL.md` files at the repo root are Hermes-agent skill definitions in YAML-frontmatter + markdown form. They tell the Hermes agent *what* to do when a user asks for a capability.

These JSON Schema files are the **machine-readable companions** — they expose the same tools as OpenAI/Anthropic-compatible function-calling definitions, so any function-calling agent (not just Hermes) can invoke them. The `x-mtg` annotations enable linguistic validation via [mtg-guards](https://github.com/Moshe-ship/mtg).

## Using with MTG

```python
import json
from mtg.adapters.openai import guard_tool

tool = json.load(open("tool-schemas/send_message.json"))
wrapped = guard_tool(tool)

report = wrapped.validate_call({
    "arguments": {
        "recipient": "أحمد",
        "platform": "whatsapp",
        "message": "أبي أحجز فندق",
    }
})
for name, guard in report.per_param.items():
    if guard.violations:
        print(f"{name}: {[v.code for v in guard.violations]}")
```

## Using without MTG

The `x-mtg` keys are strictly additive. Consumers that don't understand them ignore per the JSON Schema extension rules — so these files are also valid OpenAI tool definitions without any MTG knowledge.

```python
import json, openai
tool = json.load(open("tool-schemas/prayer_times.json"))
response = openai.chat.completions.create(
    model="gpt-4o",
    messages=[...],
    tools=[{"type": "function", "function": tool}],
)
```

## Coverage

| File | Hurmoz skill | Primary MTG slots |
|---|---|---|
| `prayer_times.json` | `prayer-times` | city=named_entity, country=identifier |
| `quran_search.json` | `quran-search` | query=free_text MSA |
| `hijri_calendar.json` | `hijri-calendar` | date=temporal mixed-script |
| `calculate_zakat.json` | `islamic-finance` | amount=numeric, currency=identifier |
| `translate.json` | `translate` | text=free_text mixed-script |
| `dialect_detect.json` | `dialect-detect` | text=free_text ar any-dialect |
| `tashkeel.json` | `tashkeel` | text=free_text ar MSA |
| `send_message.json` | `unifonic` + `whisper-arabic` | message=free_text ar preserve |
| `saudi_address.json` | `saudi-address` | city=named_entity ar, codes=identifier latn |
| `arabic_grammar.json` | `arabic-grammar` | text=free_text ar productive-preserve |

## License

MIT, matching the parent repo.
