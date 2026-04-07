---
name: quran-search
description: Quran verse search and lookup via AlQuran Cloud API
version: 1.0.0
author: Mousa Abu Mazin
license: MIT
platforms: [linux, macos]
prerequisites:
  commands: [curl, jq]
  env_vars: []
metadata:
  hermes:
    tags: [islamic, quran, arabic, search]
---
# بحث في القرآن الكريم

## جلب آية بالرقم

```bash
curl -s "https://api.alquran.cloud/v1/ayah/SURAH:AYAH/ar.alafasy"
```

مثال — الآية 255 من البقرة (آية الكرسي):
```bash
curl -s "https://api.alquran.cloud/v1/ayah/2:255/editions/quran-uthmani,ar.alafasy" | jq '.data[0].text'
```

النتيجة المتوقعة:
```
"اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ ۚ لَا تَأْخُذُهُ سِنَةٌ وَلَا نَوْمٌ ..."
```

## جلب سورة كاملة

```bash
curl -s "https://api.alquran.cloud/v1/surah/SURAH_NUMBER/quran-uthmani"
```

مثال — سورة الفاتحة:
```bash
curl -s "https://api.alquran.cloud/v1/surah/1/quran-uthmani" | jq '.data.ayahs[].text'
```

مثال — سورة يس (السورة 36):
```bash
curl -s "https://api.alquran.cloud/v1/surah/36/quran-uthmani" | jq '.data.name,.data.ayahs | length'
```

## جلب جزء كامل

```bash
curl -s "https://api.alquran.cloud/v1/juz/JUZ_NUMBER/quran-uthmani"
```

مثال — الجزء 30 (جزء عمّ):
```bash
curl -s "https://api.alquran.cloud/v1/juz/30/quran-uthmani" | jq '.data.ayahs | length'
```

## بحث بالكلمة

```bash
curl -s "https://api.alquran.cloud/v1/search/KEYWORD/all/ar"
```

مثال — البحث عن "الرحمن":
```bash
curl -s "https://api.alquran.cloud/v1/search/الرحمن/all/ar" | jq '.data.count, .data.matches[:3]'
```

مثال — البحث عن "صبر":
```bash
curl -s "https://api.alquran.cloud/v1/search/صبر/all/ar" | jq '.data.count'
```

## البحث في سورة محددة

```bash
curl -s "https://api.alquran.cloud/v1/search/KEYWORD/SURAH_NUMBER/ar"
```

مثال — البحث عن "نور" في سورة النور فقط:
```bash
curl -s "https://api.alquran.cloud/v1/search/نور/24/ar" | jq '.data.matches[]'
```

## جلب آية مع الترجمة

```bash
curl -s "https://api.alquran.cloud/v1/ayah/SURAH:AYAH/editions/quran-uthmani,en.sahih"
```

مثال — آية الكرسي مع الترجمة الإنجليزية:
```bash
curl -s "https://api.alquran.cloud/v1/ayah/2:255/editions/quran-uthmani,en.sahih" \
  | jq '{arabic: .data[0].text, english: .data[1].text}'
```

## الطبعات المتاحة

| الطبعة | الوصف |
|--------|-------|
| `quran-uthmani` | الرسم العثماني (الأساسي) |
| `quran-simple` | بدون تشكيل |
| `ar.alafasy` | تلاوة العفاسي (رابط صوتي) |
| `ar.husary` | تلاوة الحصري |
| `en.sahih` | ترجمة صحيح إنترناشيونال |
| `en.pickthall` | ترجمة بيكثال |
| `ur.ahmedali` | ترجمة أوردو |

لعرض جميع الطبعات المتاحة:
```bash
curl -s "https://api.alquran.cloud/v1/edition" | jq '.data | length'
```

## عرض النتيجة

عند عرض آية:

سورة [اسم السورة] — آية [رقم]

﴿ نص الآية ﴾

## قواعد شرعية مهمة

- ما تفسّر من عندك — قل "للتفسير المفصل ارجع لتفسير ابن كثير أو الطبري"
- إذا طلب تفسير مختصر، اعطِ المعنى العام المتفق عليه فقط
- لا تجتهد في أحكام فقهية
- عند ذكر آية، تأكد من دقة النص بمراجعة API
- استخدم الأقواس القرآنية ﴿ ﴾ دائما عند عرض الآيات
- إذا طلب المستخدم "سورة كذا" بدون تحديد آية، اعرض أول 5 آيات واسأل إذا يريد المزيد
