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

### توليد توثيق
```bash
qalam generate src/
```
يولّد توثيق عربي من ملفات Python/JS/TS.

### مسح الكود
```bash
qalam scan src/
```
يعرض الدوال والكلاسات والموديولات المكتشفة.

### ترجمة مصطلح
```bash
qalam translate "function"
```
يترجم مصطلح برمجي واحد للعربي.

### القاموس التقني
```bash
qalam dict
```
يعرض القاموس الكامل (300+ مصطلح).

## صيغ الخروج
- Markdown
- Docstring
- README section
- HTML (RTL)

## متى تستخدم
- المستخدم يريد توثيق مشروعه بالعربي
- يبحث عن ترجمة مصطلح تقني
- يريد README عربي لمشروعه
