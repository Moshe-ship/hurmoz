---
name: artok
description: "حاسبة ضريبة التوكنات — قارن تكلفة التوكنات العربية عبر 18 محلل (tokenizer) واعرض كفاءة كل مزوّد"
version: 1.0.0
author: Mousa Abu Mazin
license: MIT
platforms: [linux, macos]
prerequisites:
  commands: [artok]
  env_vars: []
metadata:
  hermes:
    tags: [arabic, tokenizer, cost, benchmark, nlp, llm]
---

# artok — حاسبة ضريبة التوكنات العربية

أداة لمقارنة تكلفة التوكنات العربية عبر 18 محلل مختلف. استخدم لتحليل تكاليف API.

## الأوامر

### عدّ التوكنات
```bash
artok "النص العربي"
```

مثال عملي:
```bash
artok "بسم الله الرحمن الرحيم"
```

النتيجة المتوقعة:
```
╔═══════════════════════╦════════╦════════════╗
║ Tokenizer             ║ Tokens ║ Efficiency ║
╠═══════════════════════╬════════╬════════════╣
║ cl100k_base (GPT-4)   ║ 11     ║ 2.2x       ║
║ claude (Claude 3+)    ║ 9      ║ 1.8x       ║
║ o200k_base (GPT-4o)   ║ 8      ║ 1.6x       ║
║ gemini                ║ 10     ║ 2.0x       ║
║ llama3                ║ 14     ║ 2.8x       ║
║ mistral               ║ 12     ║ 2.4x       ║
║ jais (Arabic-native)  ║ 5      ║ 1.0x       ║
║ qwen2                 ║ 7      ║ 1.4x       ║
╠═══════════════════════╬════════╬════════════╣
║ English equivalent    ║ 5      ║ baseline   ║
╚═══════════════════════╩════════╩════════════╝

Arabic tax: العربي يكلف 1.6x - 2.8x أكثر من الإنجليزي
Best for Arabic: jais (1.0x) → qwen2 (1.4x) → GPT-4o (1.6x)
```

### مقارنة عربي vs إنجليزي
```bash
artok "النص العربي" -e "The English text"
```

مثال عملي:
```bash
artok "الذكاء الاصطناعي يغيّر مستقبل التعليم في العالم العربي" \
  -e "Artificial intelligence is changing the future of education in the Arab world"
```

النتيجة المتوقعة:
```
Text Comparison:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

              Arabic    English    Ratio
GPT-4:        28        15         1.87x
Claude:       24        13         1.85x
GPT-4o:       21        14         1.50x
Gemini:       26        14         1.86x
Qwen2:        16        13         1.23x

Winner for Arabic: Qwen2 (1.23x overhead)
Winner overall: GPT-4o (best balance)
```

### حساب التكلفة المالية
```bash
artok cost "النص" --provider claude --volume 100000
```

مثال — حساب تكلفة 100 ألف طلب:
```bash
artok cost "اشرح لي مفهوم الذكاء الاصطناعي بالتفصيل" \
  --provider all --volume 100000
```

النتيجة المتوقعة:
```
Cost Estimate (100K requests, avg 20 tokens/request):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Provider     Arabic Tokens  Cost/1M    Monthly Cost
GPT-4o       2,800K        $2.50      $7.00
Claude 3.5   2,400K        $3.00      $7.20
GPT-4        3,200K        $30.00     $96.00
Gemini 1.5   2,600K        $1.25      $3.25

Cheapest: Gemini 1.5 ($3.25/mo)
Best value: GPT-4o ($7.00/mo, better quality)
```

### معيار الكفاءة العربية
```bash
artok --benchmark
```

يشغّل معيار كفاءة التوكنات العربية عبر نصوص معيارية (أخبار، أدب، تقني، لهجات) لجميع الـ18 محلل.

النتيجة المتوقعة:
```
Arabic Tokenizer Benchmark
━━━━━━━━━━━━━━━━━━━━━━━━━━━

Test corpus: 5 categories × 100 samples

             News   Lit.   Tech   Dial.  Quran   AVG
jais         1.0x   1.1x   1.2x   1.0x   1.0x   1.06x
qwen2        1.3x   1.4x   1.2x   1.5x   1.3x   1.34x
o200k_base   1.5x   1.6x   1.4x   1.7x   1.5x   1.54x
claude       1.7x   1.8x   1.5x   1.9x   1.7x   1.72x
cl100k_base  2.1x   2.3x   1.8x   2.4x   2.1x   2.14x
llama3       2.6x   2.8x   2.2x   3.0x   2.7x   2.66x
```

### تأثير التشكيل
```bash
artok --tashkeel
```

النتيجة المتوقعة:
```
Tashkeel Impact Analysis:
━━━━━━━━━━━━━━━━━━━━━━━━━

Test: "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ"

                With Tashkeel  Without    Increase
GPT-4:         18             11         +63%
Claude:        15             9          +67%
GPT-4o:        14             8          +75%

Recommendation: احذف التشكيل إلا إذا كان ضروريا (قرآن، شعر)
Savings: حذف التشكيل يوفّر 40-75% من التوكنات
```

### مقارنة اللهجات
```bash
artok --dialects
```

النتيجة المتوقعة:
```
Dialect Token Comparison (same meaning):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"كيف حالك اليوم؟"

Dialect    Text                  GPT-4  Claude  GPT-4o
فصحى       كيف حالك اليوم؟       8      7       6
مصري       إزيك النهاردة؟         9      7       7
خليجي      شلونك اليوم؟          8      7       6
شامي       كيفك اليوم؟           8      7       6
مغاربي     لاباس عليك اليوم؟     10     8       8

الأرخص: الفصحى والخليجي
الأغلى: المغاربي (كلمات أقل شيوعا في بيانات التدريب)
```

## متى تستخدم
- المستخدم يسأل "ليش العربي أغلى؟"
- يختار بين مزوّدين ويريد يعرف الأرخص للعربي
- يريد يفهم تأثير التشكيل أو اللهجة على التكلفة
- يحسب ميزانية مشروع عربي
- يقارن بين محللات التوكنات لاختيار الأنسب
