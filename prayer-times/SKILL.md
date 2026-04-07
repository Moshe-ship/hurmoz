---
name: prayer-times
description: Prayer time lookup via Aladhan API for any city worldwide
version: 1.0.0
author: Mousa Abu Mazin
license: MIT
platforms: [linux, macos]
prerequisites:
  commands: [curl]
  env_vars: []
metadata:
  hermes:
    tags: [islamic, prayer, aladhan, arabic]
---
# أوقات الصلاة

عندما يسأل المستخدم عن أوقات الصلاة:

1. اسأل عن المدينة إذا ما ذكرها
2. استخدم API أوقات الصلاة:

## جلب أوقات الصلاة بالمدينة

```bash
curl -s "https://api.aladhan.com/v1/timingsByCity?city=CITY&country=COUNTRY&method=4"
```

### أمثلة للمدن الرئيسية

الرياض:
```bash
curl -s "https://api.aladhan.com/v1/timingsByCity?city=Riyadh&country=SA&method=4" \
  | jq '.data.timings | {الفجر: .Fajr, الشروق: .Sunrise, الظهر: .Dhuhr, العصر: .Asr, المغرب: .Maghrib, العشاء: .Isha}'
```

القاهرة:
```bash
curl -s "https://api.aladhan.com/v1/timingsByCity?city=Cairo&country=EG&method=5" \
  | jq '.data.timings | {الفجر: .Fajr, الشروق: .Sunrise, الظهر: .Dhuhr, العصر: .Asr, المغرب: .Maghrib, العشاء: .Isha}'
```

دبي:
```bash
curl -s "https://api.aladhan.com/v1/timingsByCity?city=Dubai&country=AE&method=4" \
  | jq '.data.timings'
```

إسطنبول:
```bash
curl -s "https://api.aladhan.com/v1/timingsByCity?city=Istanbul&country=TR&method=3" \
  | jq '.data.timings'
```

ديترويت (أمريكا):
```bash
curl -s "https://api.aladhan.com/v1/timingsByCity?city=Detroit&country=US&method=2" \
  | jq '.data.timings'
```

## جلب أوقات الصلاة بالإحداثيات

```bash
curl -s "https://api.aladhan.com/v1/timings?latitude=LAT&longitude=LNG&method=METHOD"
```

مثال — مكة المكرمة:
```bash
curl -s "https://api.aladhan.com/v1/timings?latitude=21.4225&longitude=39.8262&method=4" \
  | jq '.data.timings'
```

## طرق الحساب (method)

| الرقم | الطريقة | المنطقة |
|-------|---------|---------|
| 1 | جامعة العلوم الإسلامية، كراتشي | باكستان، أفغانستان |
| 2 | ISNA | أمريكا الشمالية |
| 3 | رابطة العالم الإسلامي | أوروبا، تركيا، العراق |
| 4 | أم القرى | السعودية، الخليج |
| 5 | الهيئة المصرية | مصر، السودان، ليبيا |
| 7 | معهد المساحة، سنغافورة | جنوب شرق آسيا |
| 8 | فرنسا | فرنسا، غرب أفريقيا |
| 9 | وزارة الأوقاف، الكويت | الكويت |
| 10 | قطر | قطر |
| 15 | الأوقاف التركية (ديانت) | تركيا |

## الجدول الشهري

```bash
curl -s "https://api.aladhan.com/v1/calendarByCity/YEAR/MONTH?city=CITY&country=COUNTRY&method=METHOD"
```

مثال — جدول رمضان 2026 في الرياض:
```bash
curl -s "https://api.aladhan.com/v1/calendarByCity/2026/2?city=Riyadh&country=SA&method=4" \
  | jq '.data[] | {date: .date.readable, fajr: .timings.Fajr, maghrib: .timings.Maghrib}'
```

## حساب الصلاة القادمة

عند السؤال "متى الصلاة القادمة؟":

1. اجلب أوقات الصلاة لمدينة المستخدم
2. قارن الوقت الحالي مع أوقات الصلوات
3. الصلاة التي وقتها أكبر من الوقت الحالي هي القادمة
4. إذا كل الصلوات مرّت، الصلاة القادمة هي فجر الغد

```bash
# جلب الأوقات مع الوقت الحالي للمقارنة
curl -s "https://api.aladhan.com/v1/timingsByCity?city=Riyadh&country=SA&method=4" \
  | jq '{now: .data.date.timestamp, fajr: .data.timings.Fajr, dhuhr: .data.timings.Dhuhr, asr: .data.timings.Asr, maghrib: .data.timings.Maghrib, isha: .data.timings.Isha}'
```

## تعامل خاص مع رمضان

- في رمضان، أضف وقت الإمساك (قبل الفجر بـ10 دقائق)
- وقت الإفطار = وقت المغرب
- اعرض "الإمساك" و"الإفطار" بدل "الفجر" و"المغرب" إذا كان الشهر رمضان

```bash
# تحقق إذا كان الشهر الحالي رمضان
curl -s "https://api.aladhan.com/v1/gToH" | jq '.data.hijri.month.number'
# إذا الناتج = 9 فهو رمضان
```

## تنسيق العرض

```
أوقات الصلاة — [المدينة]
[التاريخ الهجري] | [التاريخ الميلادي]

🕌 الفجر:    04:32
🌅 الشروق:   05:58
☀️ الظهر:    12:09
🌤 العصر:    15:30
🌇 المغرب:   18:21
🌙 العشاء:   19:51
```

4. إذا سأل "متى صلاة [اسم]؟" اعطه وقت تلك الصلاة فقط
5. إذا سأل "كم باقي على المغرب؟" احسب الفرق بالدقائق
