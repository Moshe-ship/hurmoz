# Hurmoz narrowed demos

Three brutal workflows, each showing the full MTG reliability loop:

1. **failure without MTG** — advisory mode just detects
2. **repaired execution** — reconciled mode proposes concrete repairs
3. **signed ToolProof receipt** — chain captures both outcomes
4. **report output** — `mtg report` aggregates the chain into a scorecard

The demos are deliberately narrow. We are not trying to be comprehensive here — we are trying to make the failure and the repair pattern impossible to miss.

## Run all three

```bash
pip install mtg-guards toolproof
python demos/demo_send_message.py
python demos/demo_saudi_business.py
python demos/demo_quran_search.py

# Aggregate all three chains into one scorecard
cat ~/.toolproof/demos/*.ndjson > /tmp/all-demos.ndjson
mtg report /tmp/all-demos.ndjson --html /tmp/scorecard.html
```

## What each demo covers

| Demo | Tool | Failure modes demonstrated |
|---|---|---|
| `demo_send_message.py` | `send_message_gulf.json` | dialect drift, Arabizi transliteration |
| `demo_saudi_business.py` | `saudi_address.json` | Latin transliteration of a city, Arabic-Indic-digit homoglyph, BiDi RLO injection (Trojan Source) |
| `demo_quran_search.py` | `quran_search.json` | dialect drift in an MSA-bound slot, Arabizi query, zero-width-space padding attack |

Each demo is a narrow instrument. They're the proof surface — not the product.

## Reading the output

Each scenario runs twice: once in advisory mode (detection only), once in reconciled mode (detection + repair suggestions). The `advisory (no repair)` line shows MTG's detection rate; the `reconciled (with repair)` line shows what the agent would see if it read the repair suggestions before sending the call. A downstream agent with `needs_review=True` logic can refuse to ship the repaired value and prompt the user instead — or, for low-risk repairs like BiDi stripping, apply them silently.

## Why these three

- **send_message** is the canonical dialect surface. Every market binds to one.
- **saudi_business** is the canonical mixed-script surface. Real national APIs treat script as part of the contract.
- **quran_search** is the canonical content-correctness surface. MSA-only alignment against a fixed corpus is one of the few places MTG's MSA dialect check is load-bearing.

Three brutal cases. No breadth.
