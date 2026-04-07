---
name: saudi-identity
description: Saudi digital identity verification via Nafath and Yakeen APIs
version: 1.0.0
author: Mousa Abu Mazin
license: MIT
platforms: [linux, macos]
prerequisites:
  commands: [curl]
  env_vars: [NAFATH_TOKEN, YAKEEN_TOKEN]
metadata:
  hermes:
    tags: [saudi, identity, nafath, yakeen, verification]
---
# الهوية الرقمية السعودية (نفاذ + يقين)

دليل التكامل مع خدمات التحقق من الهوية الرقمية في المملكة العربية السعودية.

> **تنبيه مهم**: واجهات نفاذ ويقين البرمجية تتطلب ترخيصاً رسمياً. لا تستخدم أرقام هوية وطنية حقيقية في بيئة التطوير أو الاختبار. استخدم فقط أرقام الاختبار التي توفرها الجهة المرخِّصة ضمن بيئة الـ Sandbox. احذف السجلات بعد الانتهاء.

---

## نفاذ (Nafath) — الهوية الرقمية الوطنية

نفاذ هو نظام الهوية الرقمية الوطني الذي يوفر مصادقة متعددة العوامل (MFA) للخدمات الحكومية والخاصة.

### الحصول على الترخيص (مطلوب)

يتطلب الوصول لواجهات نفاذ البرمجية ترخيصاً من شركة TCC-ICT:

1. **تقديم طلب ترخيص**: https://tcc-ict.com
2. **التسجيل في منصة المطورين**: https://developer.tcc-ict.com
3. بعد الموافقة، ستحصل على بيانات الوصول لبيئة الـ Sandbox أولاً
4. بعد اجتياز اختبارات التكامل، يُفعّل الوصول لبيئة الإنتاج
5. ستحصل على `Bearer Token` للمصادقة

> **ملاحظة**: عنوان الـ API الفعلي يُقدَّم ضمن وثائق الترخيص بعد الموافقة. لا يوجد عنوان عام — كل مرخَّص له بيئة خاصة.

### واجهات نفاذ البرمجية

#### 1. إنشاء طلب مصادقة

```bash
# عنوان الـ API يُقدَّم مع الترخيص — استبدل YOUR_NAFATH_BASE_URL
curl -X POST "${YOUR_NAFATH_BASE_URL}/ExtNafath/request" \
  -H "Authorization: Bearer ${NAFATH_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "nationalId": "1000000000",
    "service": "login"
  }'
```

الاستجابة تتضمن `transId` ورقم عشوائي يظهر للمستخدم في تطبيق نفاذ.

#### 2. التحقق من حالة الطلب

```bash
curl -X POST "${YOUR_NAFATH_BASE_URL}/ExtNafath/status" \
  -H "Authorization: Bearer ${NAFATH_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "transId": "TRANSACTION_ID"
  }'
```

الحالات: `WAITING` | `COMPLETED` | `EXPIRED` | `REJECTED`

#### 3. جلب بيانات المستخدم بعد التحقق

```bash
curl -X GET "${YOUR_NAFATH_BASE_URL}/ExtNafath/details/TRANSACTION_ID" \
  -H "Authorization: Bearer ${NAFATH_TOKEN}"
```

يعيد بيانات الهوية المُتحقق منها (الاسم، رقم الهوية، تاريخ الميلاد، إلخ).

### حزمة GitHub جاهزة

```
github.com/mohamad-zatar/saudi-nafath-integration
```

---

## يقين (Yakeen by Elm) — التحقق من بيانات الهوية

يقين هي خدمة من شركة علم للتحقق من بيانات المواطنين والمقيمين.

### الحصول على الترخيص (مطلوب)

يتطلب الوصول لواجهات يقين عقداً رسمياً مع شركة علم:

1. **التقديم عبر موقع علم**: https://elm.sa
2. **بوابة المطورين**: https://developer.elm.sa
3. يتطلب سجل تجاري سعودي ساري
4. بعد التعاقد، يتم توفير بيانات الوصول لبيئة الاختبار ثم الإنتاج

> **ملاحظة**: عنوان الـ API الفعلي يُقدَّم ضمن وثائق العقد. لا يوجد عنوان عام.

### الطرق المتاحة

| الطريقة | الوصف | الاستخدام |
|---------|-------|-----------|
| `CitizenInfo` | بيانات المواطن بالهوية الوطنية | التحقق من بيانات المواطنين |
| `AlienInfoByIqama` | بيانات المقيم برقم الإقامة | التحقق من بيانات المقيمين |

### مثال استدعاء (REST)

```bash
# عنوان الـ API يُقدَّم مع العقد — استبدل YOUR_YAKEEN_BASE_URL
curl -X POST "${YOUR_YAKEEN_BASE_URL}/api/v1/CitizenInfo" \
  -H "Authorization: Bearer ${YAKEEN_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "nin": "1000000000",
    "dateOfBirth": "1410-01-01"
  }'
```

```bash
curl -X POST "${YOUR_YAKEEN_BASE_URL}/api/v1/AlienInfoByIqama" \
  -H "Authorization: Bearer ${YAKEEN_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "iqamaNumber": "2000000000",
    "dateOfBirth": "1980-01-01"
  }'
```

### مجموعة Postman

```
postman.com/crimson-crater-793597/yakeen-collection/
```

---

## عرض النتيجة

```
تم التحقق من الهوية
الاسم: {{ fullName }}
رقم الهوية: {{ nationalId }}
الحالة: {{ status }}
```

---

## متى تستخدم

استخدم هذه المهارة عندما يسأل المستخدم عن:
- التحقق من الهوية السعودية أو الهوية الرقمية
- نفاذ (Nafath) أو المصادقة الرقمية الوطنية
- يقين (Yakeen) أو التحقق من بيانات المواطن/المقيم
- ربط تطبيق بالهوية الرقمية السعودية
- Elm identity services

---

## المراجع

- توثيق نفاذ: https://documentation.azakaw.com/docs/apis/core/nafath
- حزمة نفاذ: https://github.com/mohamad-zatar/saudi-nafath-integration
- شركة علم: https://elm.sa
- بوابة مطوري علم: https://developer.elm.sa
- رخصة TCC: https://tcc-ict.com
- بوابة مطوري TCC: https://developer.tcc-ict.com
- مجموعة يقين Postman: https://postman.com/crimson-crater-793597/yakeen-collection/
