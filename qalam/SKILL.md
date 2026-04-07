---
name: qalam
description: "توثيق عربي من الكود — ولّد توثيق عربي تلقائي من كود Python/JS/TS مع قاموس تقني مدمج (300+ مصطلح)"
version: 1.0.0
author: Mousa Abu Mazin
license: MIT
platforms: [linux, macos]
prerequisites:
  commands: [qalam]
  env_vars: []
metadata:
  hermes:
    tags: [arabic, documentation, code, translation, technical-dictionary]
---

# qalam — مولّد التوثيق العربي

أداة لتوليد توثيق عربي تلقائي من الكود البرمجي. يعمل بدون إنترنت.

## الأوامر

### توليد توثيق لمجلد كامل
```bash
qalam generate src/
```

مثال — توليد توثيق لمشروع Python:
```bash
qalam generate ./app/
```

النتيجة المتوقعة:
```
📝 Scanning ./app/ ...
Found: 12 files, 34 functions, 8 classes, 3 modules

Generated docs:
  docs/ar/app/auth.md        — 3 دوال، 1 صنف
  docs/ar/app/models.md      — 5 أصناف
  docs/ar/app/utils.md       — 12 دالة
  docs/ar/app/api.md         — 14 نقطة نهاية

Total: 4 files, 2,340 words
```

مثال لملف توثيق مُولّد:
```markdown
# وحدة المصادقة (auth)

## صنف: مدير_الجلسات (SessionManager)

يدير جلسات المستخدمين وتوكنات الوصول.

### إنشاء_جلسة(معرّف_المستخدم، مدة_الصلاحية)

- **الوصف**: ينشئ جلسة جديدة للمستخدم ويرجع توكن وصول
- **المعاملات**:
  - `معرّف_المستخدم` (نص) — المعرّف الفريد للمستخدم
  - `مدة_الصلاحية` (عدد صحيح) — المدة بالثواني، الافتراضي 3600
- **القيمة المرجعة**: قاموس يحتوي `token` و`expires_at`
- **الاستثناءات**: `خطأ_المصادقة` إذا كان المعرّف غير صالح
```

### توليد توثيق لملف واحد
```bash
qalam generate src/auth.py
```

### مسح الكود بدون توليد
```bash
qalam scan src/
```

النتيجة المتوقعة:
```
📊 Code Analysis — src/
━━━━━━━━━━━━━━━━━━━━━━

Files:     12
Functions: 34
Classes:   8
Modules:   3

Coverage:
  Documented (EN): 22/34 functions (65%)
  Documented (AR): 0/34 functions (0%)

Top undocumented:
  1. src/utils.py:process_data() — 45 lines, no docstring
  2. src/api.py:handle_webhook() — 32 lines, no docstring
  3. src/models.py:validate_input() — 28 lines, no docstring
```

### ترجمة مصطلح تقني
```bash
qalam translate "function"
```

النتيجة المتوقعة:
```
function → دالّة
  السياق: "تُعرَّف الدالّة باستخدام الكلمة المفتاحية def في Python"
```

أمثلة أخرى:
```bash
qalam translate "class"          # → صنف
qalam translate "variable"       # → متغيّر
qalam translate "array"          # → مصفوفة
qalam translate "middleware"     # → وسيط (برمجية وسيطة)
qalam translate "deployment"     # → نشر (عملية النشر)
qalam translate "refactoring"    # → إعادة هيكلة
qalam translate "authentication" # → مصادقة (التحقق من الهوية)
```

### القاموس التقني الكامل
```bash
qalam dict
```

يعرض القاموس الكامل (300+ مصطلح) مرتبا أبجديا بالإنجليزية.

البحث في القاموس:
```bash
qalam dict --search "data"
```

النتيجة المتوقعة:
```
database        → قاعدة بيانات
data structure  → بنية بيانات
data type       → نوع بيانات
data binding    → ربط البيانات
data migration  → ترحيل البيانات
dataframe       → إطار بيانات
```

## صيغ الخروج

```bash
# Markdown (الافتراضي)
qalam generate src/ --format markdown

# Docstring — يضيف التوثيق مباشرة في الكود
qalam generate src/ --format docstring

# قسم README
qalam generate src/ --format readme

# HTML مع دعم RTL
qalam generate src/ --format html
```

مثال HTML RTL:
```bash
qalam generate src/ --format html --output docs/ar/index.html
```

ينتج صفحة HTML كاملة مع `dir="rtl"` و CSS مناسب للعربي.

## اللغات البرمجية المدعومة

| اللغة | الامتدادات | الدعم |
|-------|-----------|-------|
| Python | .py | كامل — docstrings, type hints, decorators |
| JavaScript | .js, .jsx | كامل — JSDoc, ES6 classes |
| TypeScript | .ts, .tsx | كامل — interfaces, generics, types |

## متى تستخدم
- المستخدم يريد توثيق مشروعه بالعربي
- يبحث عن ترجمة مصطلح تقني
- يريد README عربي لمشروعه
- يريد إضافة docstrings عربية في الكود
- فريق تطوير عربي يحتاج توثيق داخلي بالعربي
