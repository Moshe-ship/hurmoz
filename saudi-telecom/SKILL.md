---
name: saudi-telecom
description: واجهات شركات الاتصالات السعودية -- STC وموبايلي وزين للرسائل والتحقق والدفع
version: 1.0.0
author: Mousa Abu Mazin
license: MIT
platforms: [linux, macos]
prerequisites:
  commands: [curl]
  env_vars: [STC_API_KEY, MOBILY_TOKEN, ZAIN_TOKEN]
metadata:
  hermes:
    tags: [saudi, telecom, stc, mobily, zain, sms, otp, carrier-billing]
---

# واجهات شركات الاتصالات السعودية

دليل شامل لواجهات المطورين لدى شركات الاتصالات الثلاث في المملكة العربية السعودية: STC وموبايلي وزين.

---

## مقارنة شاملة

| الميزة | STC | موبايلي | زين |
|--------|-----|---------|-----|
| البوابة | developers.stc.com.sa | developer.mobily.com.sa | developer.sa.zain.com |
| SMS | نعم | نعم | نعم (SPS) |
| OTP | نعم | نعم | نعم |
| الدفع | نعم | نعم | نعم (TABS) |
| IoT | نعم | لا | لا |
| بيئة تجريبية | نعم مجانية | نعم | نعم Sandbox |
| البريد الإلكتروني | لا | نعم | لا |
| QR Code | لا | نعم | لا |

---

## STC -- اتصالات السعودية

بوابة المطورين: https://developers.stc.com.sa

### الخدمات المتاحة

- **SMS API**: إرسال رسائل نصية فردية وجماعية
- **OTP API**: إرسال والتحقق من رموز التحقق
- **Identity API**: التحقق من هوية المشترك
- **Payment API**: الدفع عبر فاتورة STC
- **IoT API**: إدارة أجهزة إنترنت الأشياء
- **Network Events API**: أحداث الشبكة

### الإعداد

1. سجّل في https://developers.stc.com.sa
2. أنشئ تطبيقًا واحصل على `API Key`
3. بيئة تجريبية مجانية (Sandbox) متاحة مباشرة

### إرسال SMS عبر STC

```bash
curl -X POST "https://developers.stc.com.sa/api/sms/v1/send" \
  -H "Authorization: Bearer ${STC_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "مرحبًا من تطبيقنا",
    "recipients": ["+966500000000"],
    "sender": "MyApp"
  }'
```

### إرسال OTP عبر STC

```bash
curl -X POST "https://developers.stc.com.sa/api/otp/v1/send" \
  -H "Authorization: Bearer ${STC_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "mobile": "+966500000000",
    "template": "Your code is {otp}"
  }'
```

---

## موبايلي (Mobily)

بوابة المطورين: https://developer.mobily.com.sa

### الخدمات المتاحة

- **OTP API**: إرسال والتحقق من رموز التحقق
- **Payment API**: الدفع عبر فاتورة موبايلي
- **SMS API**: إرسال رسائل نصية
- **Email API**: إرسال بريد إلكتروني
- **QR Code API**: إنشاء رموز QR

### الإعداد

1. سجّل في https://developer.mobily.com.sa
2. احصل على `App ID` و `App Secret`

### إرسال SMS عبر موبايلي

```bash
curl -X POST "https://developer.mobily.com.sa/api/sms/send" \
  -H "Authorization: Bearer ${MOBILY_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "966550000000",
    "message": "مرحبًا من تطبيقنا",
    "sender": "MyApp"
  }'
```

### إرسال OTP عبر موبايلي

```bash
curl -X POST "https://developer.mobily.com.sa/api/otp/send" \
  -H "Authorization: Bearer ${MOBILY_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "mobile": "966550000000",
    "lang": "ar"
  }'
```

---

## زين السعودية (Zain KSA)

بوابة المطورين: https://developer.sa.zain.com

### الخدمات المتاحة

- **SPS (SMS Premium Service)**: رسائل نصية مدفوعة
- **TABS (Telecom Application Billing System)**: الدفع عبر الفاتورة
- **SDP (Service Delivery Platform)**: منصة تقديم الخدمات

### الإعداد

1. سجّل في https://developer.sa.zain.com
2. أنشئ تطبيقًا واحصل على بيانات الاعتماد
3. بيئة Sandbox متاحة للاختبار

### إرسال SMS عبر زين

```bash
curl -X POST "https://developer.sa.zain.com/api/sps/v1/send" \
  -H "Authorization: Bearer ${ZAIN_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "destinationAddress": "tel:+966590000000",
    "message": "مرحبًا من تطبيقنا",
    "senderAddress": "MyApp"
  }'
```

### الدفع عبر TABS

```bash
curl -X POST "https://developer.sa.zain.com/api/tabs/v1/charge" \
  -H "Authorization: Bearer ${ZAIN_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "msisdn": "+966590000000",
    "amount": "5.00",
    "currency": "SAR",
    "description": "اشتراك شهري"
  }'
```

---

## عرض النتيجة

```
تم إرسال الرسالة بنجاح
المزود: {{ provider }}
الرقم: {{ recipient }}
معرّف الرسالة: {{ messageId }}
الحالة: {{ status }}
```

---

## متى تستخدم

استخدم هذه المهارة عندما يسأل المستخدم عن:
- إرسال رسائل SMS في السعودية
- خدمات OTP ورموز التحقق عبر الاتصالات
- واجهات مطوري STC أو موبايلي أو زين
- الدفع عبر فاتورة الاتصالات (Carrier Billing)
- بوابات المطورين لشركات الاتصالات السعودية

---

## المراجع

- STC Developers: https://developers.stc.com.sa
- Mobily Developer: https://developer.mobily.com.sa
- Zain KSA Developer: https://developer.sa.zain.com
