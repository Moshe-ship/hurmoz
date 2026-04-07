---
name: sarih
description: Arabic sentiment analysis and content filtering across 5 dialects
version: 1.0.0
author: Mousa Abu Mazin
license: MIT
platforms: [linux, macos]
prerequisites:
  commands: [sarih]
  env_vars: []
metadata:
  hermes:
    tags: [nlp, sentiment, content-filter, arabic]
---
# sarih — فلتر المحتوى العربي

أداة لاكتشاف المحتوى السام بـ5 لهجات عربية، تعمل بالكامل بدون إنترنت.

## اللهجات المدعومة

| اللهجة | أمثلة كلمات مفلترة | ملاحظات |
|--------|---------------------|---------|
| فصحى | ألفاظ نابية، تحريض، كراهية | القاعدة الأساسية |
| مصري | شتائم بالعامية المصرية | يتعرف على "يا ابن..." وما شابه |
| خليجي | ألفاظ خليجية مسيئة | يفهم السياق الخليجي |
| شامي | إساءات بالشامي | يميّز بين الشتيمة والتعبير العادي |
| مغاربي | خلط عربي-فرنسي مسيء | يكتشف الإساءة حتى بالخلط |

## الأوامر

### فحص نص واحد
```bash
sarih check "النص المراد فحصه"
```

مثال — نص نظيف:
```bash
sarih check "شكرا على المساعدة، الله يعطيك العافية"
```

النتيجة المتوقعة:
```
✅ safe
   Dialect: خليجي
   Confidence: 0.94
   Flags: none
```

مثال — نص مسيء:
```bash
sarih check "يا حمار انت ما تفهم شي"
```

النتيجة المتوقعة:
```
⚠️ medium
   Dialect: فصحى/عام
   Confidence: 0.87
   Flags: [insult]
   Details: "حمار" — إهانة مباشرة
   Suggestion: حذف أو استبدال بـ "يا أخي"
```

### فحص ملف بيانات
```bash
sarih scan data.jsonl
```

مثال مع عرض التفاصيل:
```bash
sarih scan comments.jsonl --verbose
```

النتيجة المتوقعة:
```
Scanning comments.jsonl (4,230 records)...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total:    4,230
Safe:     3,891 (92.0%)
Low:        187 (4.4%)
Medium:     128 (3.0%)
High:        24 (0.6%)

Top flags:
  insult:        89
  hate_speech:   31
  harassment:    24
  profanity:     19
  threat:         8
```

### تنظيف البيانات
```bash
sarih clean data.jsonl --output cleaned.jsonl
```

خيارات التنظيف:
```bash
# حذف السجلات المخالفة بالكامل
sarih clean data.jsonl --output clean.jsonl --strategy remove

# استبدال الألفاظ المسيئة بـ [محذوف]
sarih clean data.jsonl --output clean.jsonl --strategy redact

# حذف فقط HIGH والاحتفاظ بـ medium و low
sarih clean data.jsonl --output clean.jsonl --threshold high
```

### إحصائيات الفحص
```bash
sarih stats
```

يعرض إحصائيات آخر فحص: توزيع المستويات، أكثر الفلاتر تفعيلا، توزيع اللهجات.

### شرح الفلاتر
```bash
sarih explain
```

النتيجة المتوقعة:
```
الفلاتر الـ13:
━━━━━━━━━━━━━━

فئة الإساءة المباشرة:
  1. profanity      — ألفاظ نابية صريحة
  2. insult         — إهانات شخصية
  3. slur           — ألفاظ عنصرية أو طائفية

فئة التحريض:
  4. hate_speech    — خطاب كراهية
  5. threat         — تهديد بالأذى
  6. incitement     — تحريض على العنف

فئة التحرش:
  7. harassment     — تحرش أو مضايقة
  8. sexual         — محتوى جنسي صريح
  9. doxxing        — نشر معلومات شخصية

فئة المعلومات الخطيرة:
  10. self_harm     — إيذاء النفس
  11. extremism     — محتوى متطرف
  12. spam          — رسائل مزعجة متكررة
  13. misinformation — معلومات مضللة

المستويات الثلاثة:
  🟢 safe    — لا مشاكل
  🟡 low     — ألفاظ عامية قد تكون مسيئة في سياق معين
  🟠 medium  — إساءة واضحة لكن ليست خطيرة
  🔴 high    — تهديد أو تحريض أو محتوى خطير
```

## الوعي باللهجات

sarih يفهم أن بعض الكلمات مسيئة في لهجة لكنها عادية في أخرى. أمثلة:
- "زفت" — في المصري شتيمة، في الشامي تعني "أسفلت"
- "حيوان" — في السياق العلمي طبيعي، كنعت إهانة

## متى تستخدم
- المستخدم يريد فحص محتوى قبل النشر
- تنظيف بيانات تدريب من المحتوى السام
- فحص تعليقات أو رسائل مستخدمين
- بناء نظام إشراف محتوى عربي (content moderation)
- فلترة مخرجات نموذج لغوي قبل عرضها للمستخدم
