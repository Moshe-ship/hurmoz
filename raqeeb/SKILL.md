---
name: raqeeb
description: "فاحص RTL — اكتشف مشاكل الاتجاه من اليمين لليسار في HTML/CSS واحصل على تقييم RTL (0-100)"
version: 1.0.0
author: Mousa Abu Mazin
license: MIT
platforms: [linux, macos]
prerequisites:
  commands: [raqeeb]
  env_vars: []
metadata:
  hermes:
    tags: [arabic, rtl, html, css, accessibility, web, linter]
---

# raqeeb — فاحص RTL للمواقع العربية

أداة لاكتشاف مشاكل RTL في HTML/CSS مع تقييم من 0 إلى 100. استخدم لفحص المواقع العربية.

## الأوامر

### فحص ملفات محلية
```bash
raqeeb scan .
```

مثال — فحص مشروع Next.js:
```bash
raqeeb scan ./src/
```

النتيجة المتوقعة:
```
🔍 Scanning ./src/ (47 HTML/CSS files)...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 HIGH: src/components/Navbar.tsx:12
   Missing dir="rtl" on nav element
   Fix: <nav dir="rtl">

🔴 HIGH: src/app/layout.tsx:8
   <html> missing dir="rtl" and lang="ar"
   Fix: <html lang="ar" dir="rtl">

🟠 MEDIUM: src/styles/globals.css:45
   Using margin-left instead of margin-inline-start
   Line: .sidebar { margin-left: 20px; }
   Fix: .sidebar { margin-inline-start: 20px; }

🟠 MEDIUM: src/components/Card.tsx:23
   text-align: left found — should be text-align: start
   Fix: text-align: start;

🟡 LOW: src/styles/globals.css:89
   Using padding-right instead of padding-inline-end
   Fix: padding-inline-end: 16px;

🟡 LOW: src/components/Footer.tsx:5
   Float: left used — prefer logical properties
   Fix: float: inline-start;

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Issues: 6 (2 HIGH, 2 MEDIUM, 2 LOW)
RTL Score: 62/100
```

### فحص رابط
```bash
raqeeb url URL
```

مثال — فحص موقع حي:
```bash
raqeeb url "https://example.sa"
```

النتيجة المتوقعة:
```
🌐 Fetching https://example.sa ...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Page: الصفحة الرئيسية
HTML elements: 342
CSS rules: 1,247

Issues found: 8
  HIGH:   1 (missing dir attribute)
  MEDIUM: 4 (physical properties)
  LOW:    3 (minor alignment)

RTL Score: 71/100
```

### تقرير كامل
```bash
raqeeb report .
```

مثال:
```bash
raqeeb report ./src/ --format markdown
```

النتيجة المتوقعة:
```markdown
# تقرير جودة RTL

**المشروع**: ./src/
**التاريخ**: 2026-04-06
**التقييم**: 62/100

## ملخص

| الفئة | النتيجة | المشاكل |
|-------|---------|---------|
| Direction | 70/100 | 2 |
| CSS Layout | 55/100 | 4 |
| Text Rendering | 80/100 | 1 |
| Forms | 60/100 | 3 |
| Tables | 90/100 | 0 |
| Media | 75/100 | 1 |
| Navigation | 50/100 | 3 |
| Accessibility | 45/100 | 2 |

## التوصيات ذات الأولوية
1. أضف dir="rtl" و lang="ar" على <html>
2. استبدل الخصائص الفيزيائية بالمنطقية
3. أضف aria-label بالعربي للعناصر التفاعلية
```

### إصلاح تلقائي
```bash
raqeeb fix .
```

مثال عملي:
```bash
raqeeb fix ./src/
```

النتيجة المتوقعة:
```
🔧 Auto-fixing RTL issues...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. src/app/layout.tsx:8
   <html lang="en"> → <html lang="ar" dir="rtl">
   Apply? [y/N/a(ll)] y ✓

2. src/styles/globals.css:45
   margin-left: 20px → margin-inline-start: 20px
   Apply? [y/N/a(ll)] y ✓

3. src/styles/globals.css:67
   padding-right: 16px → padding-inline-end: 16px
   Apply? [y/N/a(ll)] a ✓ (applying all remaining)

Fixed: 6 issues
RTL Score: 62 → 89 (+27)
```

تطبيق بدون تأكيد:
```bash
raqeeb fix ./src/ --yes
```

### شرح الفحوصات
```bash
raqeeb explain
```

## أنماط CSS الشائعة التي يفحصها

### الخصائص الفيزيائية → المنطقية

| فيزيائي (خطأ) | منطقي (صح) | الوصف |
|----------------|-----------|-------|
| `margin-left` | `margin-inline-start` | هامش بداية السطر |
| `margin-right` | `margin-inline-end` | هامش نهاية السطر |
| `padding-left` | `padding-inline-start` | حشوة بداية السطر |
| `padding-right` | `padding-inline-end` | حشوة نهاية السطر |
| `text-align: left` | `text-align: start` | محاذاة النص |
| `text-align: right` | `text-align: end` | محاذاة النص |
| `float: left` | `float: inline-start` | تعويم |
| `float: right` | `float: inline-end` | تعويم |
| `border-left` | `border-inline-start` | حد بداية السطر |
| `border-right` | `border-inline-end` | حد نهاية السطر |
| `left: 0` | `inset-inline-start: 0` | موضع بداية |
| `right: 0` | `inset-inline-end: 0` | موضع نهاية |

### فحوصات HTML

```
✓ <html dir="rtl" lang="ar">
✓ <body> يرث dir من html
✓ <input> مع dir="auto" للحقول ثنائية اللغة
✓ <table> مع dir="rtl"
✓ <form> مع تسميات عربية
✓ <img> مع alt بالعربي
✓ <nav> مع ترتيب RTL
```

## الفئات الـ8 بالتفصيل

| الفئة | عدد الفحوصات | أمثلة |
|-------|-------------|-------|
| Direction | 3 | dir attribute, lang attribute, document flow |
| CSS Layout | 5 | logical properties, flexbox direction, grid |
| Text Rendering | 3 | text-align, unicode-bidi, writing-mode |
| Forms | 3 | input direction, label placement, placeholder |
| Tables | 2 | table direction, cell alignment |
| Media | 3 | image mirroring, icon direction, video controls |
| Navigation | 3 | menu order, breadcrumb direction, pagination |
| Accessibility | 2 | aria-label language, reading order |

## إعداد CI
```bash
raqeeb init --write
```

يولّد GitHub Actions workflow:
```yaml
# .github/workflows/rtl-check.yml
name: RTL Quality Check
on: [pull_request]
jobs:
  rtl-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install raqeeb
        run: pipx install raqeeb
      - name: Check RTL quality
        run: raqeeb ci --threshold 75
      - name: Upload report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: rtl-report
          path: rtl-report.md
```

خيار الحد الأدنى للتقييم:
```bash
# يفشل CI إذا التقييم أقل من 75
raqeeb ci --threshold 75

# يفشل فقط إذا فيه مشاكل HIGH
raqeeb ci --threshold 0 --fail-on high
```

## متى تستخدم
- المستخدم يبني موقع عربي ويريد فحص RTL
- مراجعة موقع قبل الإطلاق
- إعداد CI لفحص RTL تلقائي
- تحويل موقع LTR إلى RTL
- مراجعة pull request يحتوي تغييرات CSS
