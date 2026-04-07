---
name: arabench
description: Arabic LLM benchmarking across 8 quality categories
version: 1.0.0
author: Mousa Abu Mazin
license: MIT
platforms: [linux, macos]
prerequisites:
  commands: [arabench]
  env_vars: []
metadata:
  hermes:
    tags: [nlp, benchmark, arabic, evaluation]
---
# arabench — معيار جودة العربية للنماذج

أداة لتقييم جودة الذكاء الاصطناعي بالعربي عبر 8 فئات.

## الأوامر

### تشغيل المعيار الكامل
```bash
arabench run
```

النتيجة المتوقعة:
```
╔══════════════════════════════════════════════╗
║          arabench — Full Benchmark           ║
╠════════════════╦═══════╦═══════╦═════════════╣
║ Category       ║ GPT-4 ║ Claude║ Gemini      ║
╠════════════════╬═══════╬═══════╬═════════════╣
║ Translation    ║  82   ║  87   ║  79         ║
║ Grammar        ║  76   ║  84   ║  74         ║
║ Dialect        ║  68   ║  71   ║  65         ║
║ Diacritization ║  54   ║  62   ║  51         ║
║ Summarization  ║  78   ║  83   ║  76         ║
║ QA             ║  81   ║  85   ║  78         ║
║ Generation     ║  75   ║  80   ║  73         ║
║ Culture        ║  70   ║  77   ║  66         ║
╠════════════════╬═══════╬═══════╬═════════════╣
║ OVERALL        ║  73.0 ║  78.6 ║  70.3       ║
╚════════════════╩═══════╩═══════╩═════════════╝
```

### اختبار سريع لمزوّد واحد
```bash
arabench quick claude
arabench quick gpt4
arabench quick gemini
```

النتيجة — نتائج سريعة خلال 30 ثانية لأهم 3 فئات (translation, grammar, qa).

### مقارنة مزوّدين
```bash
arabench compare claude gpt4
```

النتيجة المتوقعة:
```
claude vs gpt4 — Arabic Quality Comparison
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Translation:    claude 87 ████████▋  vs  gpt4 82 ████████▏
Grammar:        claude 84 ████████▍  vs  gpt4 76 ███████▌
Dialect:        claude 71 ███████    vs  gpt4 68 ██████▊
Winner: claude (+5.6 avg)
```

### عرض لوحة النتائج
```bash
arabench leaderboard
```

يعرض ترتيب جميع المزوّدين المُقيّمين حسب المعدل العام.

### شرح فئة تقييم
```bash
arabench explain translation
arabench explain dialect
arabench explain diacritization
```

## الفئات الثمانية بالتفصيل

| الفئة | الوصف | أمثلة الاختبار |
|-------|-------|----------------|
| translation | دقة الترجمة عربي↔إنجليزي | مصطلحات تقنية، تعابير اصطلاحية |
| grammar | صحة القواعد النحوية والصرفية | إعراب، تصريف أفعال، جمع تكسير |
| dialect | فهم اللهجات الخمس | مصري، خليجي، شامي، مغاربي، عراقي |
| diacritization | دقة التشكيل | نصوص بدون تشكيل يُطلب تشكيلها |
| summarization | جودة التلخيص العربي | مقالات إخبارية، نصوص أكاديمية |
| qa | الإجابة على أسئلة بالعربي | ثقافية، تاريخية، علمية |
| generation | جودة توليد النصوص | مقالات، قصص، محتوى تسويقي |
| culture | الوعي الثقافي العربي | عادات، أمثال، سياق اجتماعي |

## نظام التقييم

- **90-100**: ممتاز — أداء يقارب المتحدث الأصلي
- **80-89**: جيد جدا — أخطاء نادرة وطفيفة
- **70-79**: جيد — يفهم السياق لكن فيه أخطاء ملحوظة
- **60-69**: مقبول — يحتاج تدقيق بشري
- **أقل من 60**: ضعيف — غير موثوق للاستخدام الإنتاجي

## متى تستخدم
- المستخدم يسأل "أي نموذج أفضل بالعربي؟"
- يريد مقارنة بين Claude و GPT أو غيرهم
- يريد يعرف نقاط ضعف نموذج معين بالعربي
- يختار نموذج لمشروع يتطلب عربي عالي الجودة
- يريد يفهم ليش نموذج معين ضعيف بالتشكيل أو اللهجات
