# hurmoz

**63 Arabic AI skills for Hermes Agent**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Skills: 63](https://img.shields.io/badge/Skills-63-orange.svg)](#skills)
[![Hermes Agent](https://img.shields.io/badge/Hermes-v0.7.0+-blue.svg)](https://github.com/NousResearch/hermes-agent)

> The first and largest Arabic skills collection for any AI agent platform.

## Install

```bash
git clone https://github.com/Moshe-ship/hurmoz.git
```

Add to your Hermes profile config (`~/.hermes/profiles/YOUR_PROFILE/config.yaml`):

```yaml
skills:
  - /path/to/hurmoz
```

All 63 skills load automatically.

## Skills

### Islamic (6)

| Skill | What it does |
|---|---|
| prayer-times | Prayer times via Aladhan API for any city |
| hijri-calendar | Hijri date conversion, events, month names |
| quran-search | Search Quran by text, surah, juz via AlQuran Cloud |
| hadith-search | Search hadith collections via fawazahmed0 API |
| adhan-player | Play adhan audio, manage schedules |
| islamic-finance | Zakat calculation, Islamic banking rules |

### Language (7)

| Skill | What it does |
|---|---|
| translate | Arabic-English translation, dialect handling |
| dialect-detect | Detect MSA, Gulf, Egyptian, Levantine, Maghrebi |
| arabic-grammar | Grammar correction, morphology, i3rab |
| tashkeel | Diacritization placement on Arabic text |
| arabic-poetry | Prosody, meters, classical and modern forms |
| arabic-names | Name meanings, origins, gender, regional variants |
| arabic-web-search | DuckDuckGo with Arabic region bias |

### NLP Tools (9)

| Skill | What it does |
|---|---|
| arabench | Arabic LLM quality benchmark across 17 providers |
| khalas | Arabic text summarization, dialect-aware |
| sarih | Arabic content moderation, toxicity scanning |
| bidi-guard | Scan code for invisible BiDi characters (CVE-2021-42574) |
| qalam | Generate Arabic documentation from code |
| artok | Arabic token cost calculator across LLM tokenizers |
| majal | Arabic dataset inspector for training data quality |
| safha | Arabic web scraper for ML, dialect detection, JSONL export |
| raqeeb | Arabic RTL testing CLI, scan HTML/CSS for layout bugs |

### Agent Tools (2)

| Skill | What it does |
|---|---|
| arabic-toolproof | ToolProof integration — verify tool calls, trust reports |
| arabic-agent-eval | Arabic function-calling benchmark, evaluate models |

### Saudi Government and Business (20)

| Skill | What it does |
|---|---|
| saudi-address | National Address API lookup |
| saudi-apps | Saudi super-apps integration (Tawakkalna, Absher, etc.) |
| saudi-business | Commercial registration via Wathq API |
| saudi-customs | FASAH customs clearance platform API |
| saudi-ecommerce | Salla, Zid, Noon marketplace APIs |
| saudi-einvoice | ZATCA Fatoorah e-invoicing |
| saudi-food | SFDA food safety and restaurant APIs |
| saudi-hr | Qiwa/Musaned labor and domestic worker APIs |
| saudi-identity | Nafath/Absher identity verification |
| saudi-legal | Najiz courts and legal document APIs |
| saudi-openbanking | SAMA open banking APIs |
| saudi-opendata | data.gov.sa open data platform |
| saudi-pay | SADAD, mada, Apple Pay, STC Pay, Tabby BNPL |
| saudi-procurement | Etimad government procurement platform |
| saudi-shipping | SPL, Aramex, SMSA, Fetchr delivery APIs |
| saudi-stocks | Tadawul market data and stock lookup |
| saudi-telecom | STC, Mobily, Zain developer APIs |
| saudi-tourism | Saudi Tourism Authority and Umrah APIs |
| saudi-tts | Arabic TTS via SILMA/ElevenLabs |
| saudi-weather | Open-Meteo weather for Saudi cities |

### Media (4)

| Skill | What it does |
|---|---|
| arabic-ocr | Tesseract-based Arabic OCR |
| whisper-arabic | Arabic speech-to-text via Whisper |
| voxtral-tts | Arabic text-to-speech via Voxtral/Mistral |
| voice-assistant | Full Arabic voice assistant pipeline |

### Lifestyle and Education (9)

| Skill | What it does |
|---|---|
| arabic-cooking | Traditional recipes, regional dishes, measurements |
| arab-travel | Arab world travel, visa info, cultural tips |
| arabic-health | Medical terminology, health info in Arabic |
| arabic-resume | Arabic CV writing, Gulf/Levant formats |
| arabic-email | Formal Arabic business email templates |
| arabic-legal | Legal terminology, contract drafting |
| arabic-kids | Arabic alphabet, stories, educational games |
| arabic-math | Math in Arabic, number systems, algebra |
| arabic-science | Scientific terminology across disciplines |

### Integration (3)

| Skill | What it does |
|---|---|
| arabic-siri | Arabic Siri integration via Apple Shortcuts |
| snapchat-content | Snapchat Arabic content creation |
| unifonic | Unifonic CPaaS for SMS/WhatsApp |

### Specialized (1)

| Skill | What it does |
|---|---|
| arabic-rag | Arabic RAG pipeline with Quran/Hadith embeddings |
| livestock-manager | Livestock management, breeding, zakat on animals |

## Dialect Support

Every language skill handles 5 Arabic dialects:

| Dialect | Region | Example |
|---|---|---|
| MSA | Standard | "I want to book a hotel" |
| Gulf | Saudi, UAE, Kuwait, Qatar, Bahrain, Oman | "ابي احجز فندق" |
| Egyptian | Egypt | "عايز احجز فندق" |
| Levantine | Syria, Lebanon, Jordan, Palestine | "بدي احجز فندق" |
| Maghrebi | Morocco, Algeria, Tunisia, Libya | "بغيت نحجز فندق" |

## Requirements

- Hermes Agent v0.7.0+
- curl (for API-based skills)
- Python 3.10+ (for NLP tool skills: arabench, khalas, sarih, etc.)

## Community

Built with input from the Saudi AI Community.

## License

MIT -- Musa the Carpenter (@Mosescreates)
