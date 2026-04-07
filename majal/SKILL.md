---
name: majal
description: "فاحص بيانات التدريب العربية — اكتشف مشاكل الترميز والمحتوى المخفي وخلط اللهجات في ملفات JSONL"
version: 1.0.0
author: Mousa Abu Mazin
license: MIT
platforms: [linux, macos]
prerequisites:
  commands: [majal]
  env_vars: []
metadata:
  hermes:
    tags: [arabic, data-quality, training-data, jsonl, encoding, nlp]
---

# majal — فاحص بيانات التدريب العربية

أداة لفحص جودة بيانات التدريب العربية عبر 16 فحص. استخدم لتنظيف بيانات التدريب.

## الأوامر

### فحص البيانات
```bash
majal scan data.jsonl
```

مثال عملي:
```bash
majal scan training_data.jsonl
```

النتيجة المتوقعة:
```
🔍 Scanning training_data.jsonl (12,450 records)...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

╔════════════════════╦══════════╦═══════════╦═════════╗
║ Check              ║ Severity ║ Found     ║ % Total ║
╠════════════════════╬══════════╬═══════════╬═════════╣
║ mojibake           ║ HIGH     ║ 234       ║ 1.9%    ║
║ invisible_chars    ║ HIGH     ║ 12        ║ 0.1%    ║
║ bidi_override      ║ HIGH     ║ 3         ║ 0.0%    ║
║ mixed_encoding     ║ MEDIUM   ║ 89        ║ 0.7%    ║
║ dialect_mixing     ║ MEDIUM   ║ 456       ║ 3.7%    ║
║ empty_arabic       ║ MEDIUM   ║ 67        ║ 0.5%    ║
║ latin_in_arabic    ║ LOW      ║ 1,203     ║ 9.7%    ║
║ excessive_tashkeel ║ LOW      ║ 321       ║ 2.6%    ║
╠════════════════════╬══════════╬═══════════╬═════════╣
║ TOTAL ISSUES       ║          ║ 2,385     ║ 19.2%   ║
╚════════════════════╩══════════╩═══════════╩═════════╝

Quality Score: 74/100 (مقبول — يحتاج تنظيف)
```

### إحصائيات شاملة
```bash
majal stats data.jsonl
```

النتيجة المتوقعة:
```
📊 Dataset Statistics — training_data.jsonl
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Records:        12,450
Total tokens:   1,847,320
Avg tokens/rec: 148

Language Distribution:
  Arabic:     89.2%  ████████████████████████████▊
  English:     7.3%  ██▎
  Mixed:       3.5%  █▏

Dialect Distribution:
  فصحى:      62.1%  ████████████████████
  مصري:      14.3%  ████▌
  خليجي:     11.8%  ███▊
  شامي:       7.2%  ██▎
  مغاربي:     4.6%  █▌

Field Analysis:
  instruction:  avg 23 tokens (all records)
  input:        avg 45 tokens (8,230 records)
  output:       avg 80 tokens (all records)

Token Distribution (P50/P90/P99):
  instruction: 18 / 45 / 120
  output:      62 / 180 / 450
```

### إصلاح تلقائي
```bash
majal fix data.jsonl
```

النتيجة المتوقعة:
```
🔧 Fixing training_data.jsonl ...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Proposed fixes:
  1. Fix mojibake (234 records)
     Example: "Ø§Ù„Ø³Ù„Ø§Ù…" → "السلام"
  2. Remove invisible chars (12 records)
     Example: "مر\u200bحبا" → "مرحبا"
  3. Remove bidi overrides (3 records)
  4. Normalize encoding to UTF-8 (89 records)

Apply all fixes? [y/N/diff]
```

عرض diff قبل التطبيق:
```bash
majal fix data.jsonl --diff
```

تطبيق بدون تأكيد:
```bash
majal fix data.jsonl --yes
```

حفظ في ملف جديد:
```bash
majal fix data.jsonl --output fixed_data.jsonl
```

### شرح الفحوصات
```bash
majal explain
```

### عيّنة عشوائية
```bash
majal sample data.jsonl
```

النتيجة المتوقعة:
```
📋 Random Sample (5 records)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Record #3,421:
  instruction: "اشرح مفهوم الذكاء الاصطناعي"
  output: "الذكاء الاصطناعي هو فرع من علوم الحاسوب..."
  tokens: 142
  dialect: فصحى
  quality: ✅ clean

Record #8,102:
  instruction: "ترجم الجملة التالية"
  output: "The quick brown fox..."
  tokens: 28
  dialect: —
  quality: ⚠️ latin_in_arabic (output is entirely English)
```

عيّنة مع فلتر:
```bash
# عيّنة من السجلات المشكوك فيها فقط
majal sample data.jsonl --filter issues

# عيّنة من لهجة محددة
majal sample data.jsonl --filter dialect:masri
```

## الفحوصات الـ16 بالتفصيل

### فئة الترميز (Encoding)
1. **mojibake** — نص مشوّه بسبب خطأ ترميز (مثل: "Ø§Ù„Ø³Ù„Ø§Ù…")
2. **mixed_encoding** — خلط UTF-8 مع Windows-1256 أو ISO-8859-6
3. **bom_marker** — وجود Byte Order Mark غير ضروري
4. **null_bytes** — بايتات فارغة داخل النص

### فئة الحروف المخفية (Invisible)
5. **invisible_chars** — حروف عرض صفري (zero-width)
6. **bidi_override** — حروف تجاوز اتجاه النص
7. **homoglyph** — حروف تشبه العربية لكنها من أبجديات أخرى
8. **control_chars** — حروف تحكم غير مرئية

### فئة المحتوى (Content)
9. **empty_arabic** — حقل يدّعي أنه عربي لكنه فارغ أو إنجليزي بالكامل
10. **duplicate** — سجلات مكررة تماما
11. **toxic_content** — محتوى مسيء أو سام
12. **pii_leak** — تسريب معلومات شخصية (أرقام هواتف، إيميلات)

### فئة العربي (Arabic)
13. **dialect_mixing** — خلط لهجات في نفس السجل
14. **latin_in_arabic** — حروف لاتينية مخلوطة بالعربي
15. **excessive_tashkeel** — تشكيل زائد أو خاطئ
16. **normalization** — ألف ممدودة/مقصورة، تاء مربوطة/مفتوحة

## مقاييس الجودة

| التقييم | النقاط | المعنى |
|---------|--------|--------|
| ممتاز | 90-100 | بيانات نظيفة جاهزة للتدريب |
| جيد | 75-89 | تحتاج تنظيف طفيف |
| مقبول | 60-74 | تحتاج تنظيف متوسط |
| ضعيف | أقل من 60 | تحتاج إعادة معالجة شاملة |

## متى تستخدم
- المستخدم يجهّز بيانات تدريب عربية
- يريد فحص جودة dataset
- يشك بمشاكل ترميز أو محتوى مخفي
- يريد تنظيف بيانات قبل fine-tuning
- يحتاج إحصائيات عن توزيع اللهجات في بياناته
