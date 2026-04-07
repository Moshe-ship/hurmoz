---
name: bidi-guard
description: BiDi text validation and Trojan Source attack detection (CVE-2021-42574)
version: 1.0.0
author: Mousa Abu Mazin
license: MIT
platforms: [linux, macos]
prerequisites:
  commands: [bidi-guard]
  env_vars: []
metadata:
  hermes:
    tags: [nlp, security, bidi, unicode, arabic]
---
# bidi-guard — حماية من هجمات Bidi

أداة لاكتشاف حروف Unicode الاتجاهية المخفية التي تُستخدم في هجمات Trojan Source.

## خلفية الثغرة

**CVE-2021-42574** — ثغرة Trojan Source تستغل حروف Unicode الاتجاهية (BiDi control characters) لإخفاء كود خبيث داخل كود يبدو طبيعيا. الحروف الخطيرة:

| الحرف | الكود | الخطورة | الوصف |
|-------|-------|---------|-------|
| RLO | U+202E | عالية | يعكس اتجاه النص — يخفي كود خبيث |
| LRO | U+202D | عالية | يفرض اتجاه يسار-يمين |
| RLI | U+2067 | متوسطة | عزل نص من اليمين لليسار |
| LRI | U+2066 | متوسطة | عزل نص من اليسار لليمين |
| FSI | U+2068 | متوسطة | عزل اتجاه تلقائي |
| PDI | U+2069 | منخفضة | إنهاء العزل |
| PDF | U+202C | منخفضة | إنهاء التجاوز |

## الأوامر

### فحص ملفات
```bash
bidi-guard scan PATH
```

مثال — فحص مشروع كامل:
```bash
bidi-guard scan ./src/
```

النتيجة المتوقعة:
```
🔍 Scanning ./src/ ...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  src/auth/login.js:42
    Found: U+202E (RLO) — Right-to-Left Override
    Context: if (user === "admin‮ ⁦// Check role⁩ ⁦") {
    Risk: HIGH — Code appears different than what executes

⚠️  src/utils/format.py:18
    Found: U+2067 (RLI) — Right-to-Left Isolate
    Context: price = "⁧100⁩ SAR"
    Risk: MEDIUM — May be legitimate Arabic text

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Files scanned: 127
Issues found: 2 (1 HIGH, 1 MEDIUM)
```

مثال — فحص ملف واحد:
```bash
bidi-guard scan ./src/auth/login.js
```

### فحص سريع للحافظة
```bash
echo "النص المراد فحصه" | bidi-guard scan -
```

### وضع CI
```bash
bidi-guard ci
```

يرجع exit code غير صفري إذا وجد حروف خطيرة. مناسب لـ GitHub Actions.

مثال GitHub Actions workflow:
```yaml
name: BiDi Guard
on: [pull_request]
jobs:
  bidi-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install bidi-guard
        run: pipx install bidi-guard
      - name: Scan for BiDi attacks
        run: bidi-guard ci
```

### إصلاح تلقائي
```bash
bidi-guard fix PATH
```

مثال تفاعلي:
```bash
bidi-guard fix ./src/
```

النتيجة المتوقعة:
```
Found 2 BiDi characters:

1. src/auth/login.js:42 — U+202E (RLO)
   Remove? [y/N/a(ll)] y
   ✓ Removed

2. src/utils/format.py:18 — U+2067 (RLI)
   Remove? [y/N/a(ll)] n
   ⊘ Skipped (legitimate Arabic)

Fixed: 1 | Skipped: 1
```

إصلاح بدون تأكيد:
```bash
bidi-guard fix ./src/ --yes
```

### شرح الهجمة
```bash
bidi-guard explain
```

يوضح كل حرف bidi وكيف يُستغل مع أمثلة حية.

## تكامل مع pre-commit hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: bidi-guard
        name: BiDi character check
        entry: bidi-guard ci
        language: system
        pass_filenames: false
```

## ملاحظة للمشاريع العربية

المشاريع التي تحتوي نصوص عربية طبيعية ستظهر فيها حروف RLI/FSI بشكل مشروع. استخدم ملف `.bidiignore` لاستثناء ملفات الترجمة:

```bash
# .bidiignore
locales/
i18n/
*.po
*.xliff
```

## متى تستخدم
- المستخدم يفحص كود مفتوح المصدر
- إعداد CI/CD pipeline
- مراجعة pull request يحتوي نص عربي في الكود
- فحص أمني قبل دمج كود من مصدر خارجي
- التحقق من ملفات تهيئة (config) تحتوي نصوص عربية
