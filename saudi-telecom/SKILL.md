---
name: saudi-telecom
description: "واجهات شركات الاتصالات السعودية — Saudi telecom developer APIs for SMS, OTP, and payments via STC, Mobily, Zain"
version: 1.0.0
author: Mousa Abu Mazin
license: MIT
platforms: [linux, macos]
prerequisites:
  commands: [curl]
  env_vars: []
metadata:
  hermes:
    tags: [arabic, saudi-telecom]
---


# واجهات شركات الاتصالات السعودية

دليل شامل لواجهات المطورين لدى شركات الاتصالات الثلاث في المملكة العربية السعودية: STC وموبايلي وزين.

## بوابة STC للمطورين (STC Dev Portal)

بوابة STC توفر واجهات لإرسال الرسائل القصيرة والتحقق من الهوية والمدفوعات.

### المصادقة — الحصول على توكن

```bash
curl -X POST "https://api.stc.com.sa/oauth2/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials&client_id=$STC_CLIENT_ID&client_secret=$STC_CLIENT_SECRET"
```

### إرسال رسالة SMS عبر STC

```bash
curl -X POST "https://api.stc.com.sa/sms/v1/send" \
  -H "Authorization: Bearer $STC_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "+966501234567",
    "message": "رمز التحقق: 4821",
    "sender": "MyApp"
  }'
```

### إرسال OTP عبر STC

```bash
curl -X POST "https://api.stc.com.sa/otp/v1/generate" \
  -H "Authorization: Bearer $STC_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "mobile": "+966501234567",
    "template": "رمز التحقق الخاص بك هو {otp}. صالح لمدة 5 دقائق.",
    "expiry_seconds": 300
  }'
```

### التحقق من OTP

```bash
curl -X POST "https://api.stc.com.sa/otp/v1/verify" \
  -H "Authorization: Bearer $STC_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"mobile": "+966501234567", "otp": "4821"}'
```

## واجهات موبايلي (Mobily API)

بوابة موبايلي للمطورين: https://developer.mobily.com.sa

### المصادقة

```bash
curl -X POST "https://api.mobily.com.sa/auth/token" \
  -H "Content-Type: application/json" \
  -d '{
    "apiKey": "$MOBILY_API_KEY",
    "apiSecret": "$MOBILY_API_SECRET"
  }'
```

### إرسال SMS عبر موبايلي

```bash
curl -X POST "https://api.mobily.com.sa/sms/v2/send" \
  -H "Authorization: Bearer $MOBILY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "recipients": ["+966551234567"],
    "body": "مرحبا! طلبك رقم 7723 جاهز للاستلام.",
    "sender": "MyBrand",
    "encoding": "UTF-8"
  }'
```

### الاستعلام عن رصيد SMS

```bash
curl -s "https://api.mobily.com.sa/sms/v2/balance" \
  -H "Authorization: Bearer $MOBILY_TOKEN"
```

## واجهات زين (Zain API)

بوابة زين للمطورين: https://developer.zain.com

### المصادقة

```bash
curl -X POST "https://api.zain.com/oauth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials&client_id=$ZAIN_CLIENT_ID&client_secret=$ZAIN_CLIENT_SECRET"
```

### إرسال SMS عبر زين

```bash
curl -X POST "https://api.zain.com/sms/v1/messages" \
  -H "Authorization: Bearer $ZAIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "+966591234567",
    "content": "تم تأكيد موعدك يوم الأحد الساعة 10 صباحا.",
    "from": "MyService"
  }'
```

### الاشتراك في خدمة

```bash
curl -X POST "https://api.zain.com/subscriptions/v1/subscribe" \
  -H "Authorization: Bearer $ZAIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "msisdn": "+966591234567",
    "service_id": "SVC001",
    "channel": "SMS"
  }'
```

## مقارنة بين الشركات الثلاث

| الميزة | STC | موبايلي | زين |
|--------|-----|---------|-----|
| بوابة المطورين | api.stc.com.sa | developer.mobily.com.sa | developer.zain.com |
| المصادقة | OAuth2 | API Key | OAuth2 |
| إرسال SMS | نعم | نعم | نعم |
| OTP | مدمج | عبر SMS | عبر SMS |
| الدفع عبر الفاتورة | STC Pay API | Mobily Pay | Zain Cash |
| بادئة الأرقام | 05x | 05x | 059 |

## ملاحظات مهمة

- جميع أرقام السعودية تبدأ بـ `+966` ثم `5` ثم 8 أرقام
- التسجيل في البوابات يتطلب سجل تجاري سعودي
- الرسائل العربية تستخدم ترميز UTF-8 وتحسب 70 حرف لكل رسالة (مقابل 160 للإنجليزية)
- يجب الالتزام بنظام هيئة الاتصالات وتقنية المعلومات (CITC) لإرسال الرسائل الجماعية
- ساعات الإرسال المسموحة: 8 صباحا - 9 مساء بتوقيت السعودية
