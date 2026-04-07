---
name: safha
description: "كاشط محتوى عربي — اجمع محتوى عربي من الويب، نظّفه، واكتشف لهجته لتجهيز بيانات التدريب"
version: 1.0.0
author: Mousa Abu Mazin
license: MIT
platforms: [linux, macos]
prerequisites:
  commands: [safha]
  env_vars: []
metadata:
  hermes:
    tags: [arabic, scraping, web, data-collection, dialect-detection, nlp]
---

# safha — كاشط المحتوى العربي

أداة لجمع وتنظيف المحتوى العربي من الويب لتجهيز بيانات التدريب.

## الأوامر

### كشط صفحة واحدة
```bash
safha scrape URL
```

مثال — كشط مقال من الجزيرة:
```bash
safha scrape "https://www.aljazeera.net/news/2026/4/6/example-article"
```

النتيجة المتوقعة:
```
🌐 Scraping https://www.aljazeera.net/news/...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Title: عنوان المقال
Date: 2026-04-06
Language: Arabic (فصحى)
Words: 842
Tokens (GPT-4): 1,247

Saved: output.jsonl (1 record)
```

صيغة السجل المحفوظ:
```json
{
  "url": "https://www.aljazeera.net/news/...",
  "title": "عنوان المقال",
  "text": "نص المقال الكامل بعد التنظيف...",
  "date": "2026-04-06",
  "source": "aljazeera.net",
  "dialect": "msa",
  "word_count": 842,
  "scraped_at": "2026-04-06T14:30:00Z"
}
```

### كشط مصادر متعددة
```bash
safha scrape URL1 URL2 URL3
```

مثال — كشط عدة مواقع إخبارية عربية:
```bash
safha scrape \
  "https://www.aljazeera.net/news/article1" \
  "https://arabic.cnn.com/article2" \
  "https://www.bbc.com/arabic/article3" \
  --output news_corpus.jsonl
```

### كشط sitemap كامل
```bash
safha sitemap URL
```

مثال — كشط موقع كامل عبر sitemap:
```bash
safha sitemap "https://www.example.com/sitemap.xml" --output site_data.jsonl
```

النتيجة المتوقعة:
```
🗺️  Parsing sitemap: https://www.example.com/sitemap.xml
Found: 1,247 URLs

Scraping with 5 concurrent workers...
Rate limit: 2 req/sec

Progress: [████████████████████] 1,247/1,247 (100%)
Time: 10m 23s

Results:
  Scraped:   1,198 (96.1%)
  Failed:       31 (2.5%)
  No Arabic:    18 (1.4%)

Saved: site_data.jsonl (1,198 records)
Total words: 847,320
```

خيارات rate limiting:
```bash
# تحديد عدد الطلبات في الثانية
safha sitemap URL --rate 1

# تحديد عدد العمال المتوازين
safha sitemap URL --workers 3

# تحديد حد أقصى للصفحات
safha sitemap URL --max 500
```

### تنظيف البيانات
```bash
safha clean data.jsonl
```

مثال عملي:
```bash
safha clean raw_data.jsonl --output cleaned.jsonl
```

النتيجة المتوقعة:
```
🧹 Cleaning raw_data.jsonl (1,198 records)...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Cleaning steps applied:
  1. ✓ Remove URLs and emails
  2. ✓ Normalize alef (أ إ آ → ا)
  3. ✓ Normalize ya (ي ← ى)
  4. ✓ Remove tashkeel (diacritics)
  5. ✓ Remove tatweel (ـ)
  6. ✓ Normalize whitespace
  7. ✓ Remove HTML tags
  8. ✓ Remove social media handles (@, #)
  9. ✓ Remove duplicate paragraphs
  10. ✓ Remove non-Arabic content (< 50% Arabic)

Before: 1,198 records, 847,320 words
After:  1,142 records, 798,450 words
Removed: 56 records (4.7%)

Saved: cleaned.jsonl
```

مع الاحتفاظ بالتشكيل:
```bash
safha clean data.jsonl --keep-tashkeel --output cleaned.jsonl
```

### اكتشاف اللهجة
```bash
safha detect data.jsonl
```

مثال عملي:
```bash
safha detect cleaned.jsonl
```

النتيجة المتوقعة:
```
🗣️  Dialect Detection — cleaned.jsonl
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Records: 1,142

Distribution:
  فصحى (MSA):    782 (68.5%)  ████████████████████████████
  مصري (EGY):    134 (11.7%)  █████
  خليجي (GLF):    98 (8.6%)   ███▌
  شامي (LEV):     72 (6.3%)   ██▌
  مغاربي (MAG):   56 (4.9%)   ██

Confidence: avg 0.87

Saved dialect labels to: cleaned_with_dialect.jsonl
```

تقسيم البيانات حسب اللهجة:
```bash
safha detect data.jsonl --split
```

ينتج ملفات منفصلة:
```
data_msa.jsonl    (782 records)
data_egy.jsonl    (134 records)
data_glf.jsonl    (98 records)
data_lev.jsonl    (72 records)
data_mag.jsonl    (56 records)
```

### إحصائيات
```bash
safha stats data.jsonl
```

النتيجة المتوقعة:
```
📊 Corpus Statistics
━━━━━━━━━━━━━━━━━━━━

Records:     1,142
Total words: 798,450
Avg words:   699
Median:      542

Sources:
  aljazeera.net:    420 (36.8%)
  arabic.cnn.com:   312 (27.3%)
  bbc.com/arabic:   245 (21.5%)
  other:            165 (14.4%)

Word frequency (top 10):
  في: 12,340 | من: 11,230 | على: 9,870
  أن: 8,450 | إلى: 7,890 | التي: 6,540
```

## التصدير بصيغ مختلفة

```bash
# JSONL (الافتراضي)
safha scrape URL --format jsonl

# CSV
safha scrape URL --format csv

# Plain text (ملف نصي واحد)
safha scrape URL --format txt

# Parquet (لمعالجة البيانات الكبيرة)
safha scrape URL --format parquet
```

## أعلام مفيدة

| العلم | الوصف |
|-------|-------|
| `--output FILE` | ملف الخروج |
| `--keep-tashkeel` | لا تحذف التشكيل |
| `--min-words N` | حد أدنى لعدد الكلمات (الافتراضي 50) |
| `--max-words N` | حد أقصى لعدد الكلمات |
| `--rate N` | عدد الطلبات في الثانية |
| `--workers N` | عدد العمال المتوازين |
| `--format FMT` | صيغة الخروج (jsonl, csv, txt, parquet) |

## متى تستخدم
- المستخدم يريد جمع بيانات تدريب عربية
- تنظيف بيانات خام من الويب
- تصنيف بيانات حسب اللهجة
- بناء corpus عربي لمشروع NLP
- تجهيز بيانات fine-tuning لنموذج عربي
