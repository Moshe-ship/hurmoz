---
name: hijri-calendar
description: Hijri date conversion and Islamic calendar events via Aladhan API
version: 1.0.0
author: Mousa Abu Mazin
license: MIT
platforms: [linux, macos]
prerequisites:
  commands: [curl]
  env_vars: []
metadata:
  hermes:
    tags: [islamic, hijri, calendar, arabic]
---
# التقويم الهجري

## تحويل التواريخ

### من ميلادي لهجري

```bash
curl -s "https://api.aladhan.com/v1/gToH/DD-MM-YYYY"
```

مثال — تحويل 6 أبريل 2026:
```bash
curl -s "https://api.aladhan.com/v1/gToH/06-04-2026" \
  | jq '{hijri_date: .data.hijri.date, day: .data.hijri.day, month: .data.hijri.month.ar, year: .data.hijri.year}'
```

النتيجة المتوقعة:
```json
{
  "hijri_date": "08-10-1448",
  "day": "8",
  "month": "شوّال",
  "year": "1448"
}
```

### من هجري لميلادي

```bash
curl -s "https://api.aladhan.com/v1/hToG/DD-MM-YYYY"
```

مثال — تحويل 1 رمضان 1448:
```bash
curl -s "https://api.aladhan.com/v1/hToG/01-09-1448" \
  | jq '{gregorian_date: .data.gregorian.date, day: .data.gregorian.day, month: .data.gregorian.month.en, year: .data.gregorian.year}'
```

### التاريخ الهجري اليوم

```bash
curl -s "https://api.aladhan.com/v1/gToH" \
  | jq '{day: .data.hijri.day, month: .data.hijri.month.ar, year: .data.hijri.year, weekday: .data.hijri.weekday.ar}'
```

النتيجة المتوقعة:
```json
{
  "day": "8",
  "month": "شوّال",
  "year": "1448",
  "weekday": "الإثنين"
}
```

## أسماء الأشهر الهجرية

| الرقم | الاسم بالعربي | الاسم بالإنجليزي | أيام مهمة |
|-------|---------------|-------------------|-----------|
| 1 | مُحَرَّم | Muharram | 1 رأس السنة، 10 عاشوراء |
| 2 | صَفَر | Safar | — |
| 3 | رَبيع الأوّل | Rabi al-Awwal | 12 المولد النبوي |
| 4 | رَبيع الثاني | Rabi al-Thani | — |
| 5 | جُمادى الأولى | Jumada al-Ula | — |
| 6 | جُمادى الآخرة | Jumada al-Thani | — |
| 7 | رَجَب | Rajab | 27 الإسراء والمعراج |
| 8 | شَعبان | Sha'ban | 15 ليلة النصف |
| 9 | رَمَضان | Ramadan | 1 بداية الصيام، 27 ليلة القدر |
| 10 | شَوّال | Shawwal | 1 عيد الفطر |
| 11 | ذو القَعدة | Dhul Qi'dah | — |
| 12 | ذو الحِجّة | Dhul Hijjah | 9 يوم عرفة، 10 عيد الأضحى |

## المناسبات الإسلامية الرئيسية

| المناسبة | التاريخ الهجري | الوصف |
|----------|---------------|-------|
| رأس السنة الهجرية | 1 محرم | بداية العام الهجري الجديد |
| يوم عاشوراء | 10 محرم | صيام مستحب، يُسنّ صيام 9 و10 |
| المولد النبوي | 12 ربيع الأول | ذكرى مولد النبي ﷺ |
| الإسراء والمعراج | 27 رجب | ذكرى رحلة الإسراء والمعراج |
| ليلة النصف من شعبان | 15 شعبان | ليلة مباركة |
| بداية رمضان | 1 رمضان | بداية شهر الصيام |
| ليلة القدر | 27 رمضان (تقريبا) | خير من ألف شهر، في العشر الأواخر |
| عيد الفطر | 1 شوال | ثلاثة أيام عيد |
| يوم عرفة | 9 ذو الحجة | صيام مستحب لغير الحاج |
| عيد الأضحى | 10 ذو الحجة | أربعة أيام عيد |

## حساب المناسبة القادمة

عند السؤال "كم باقي على رمضان؟" أو "متى العيد؟":

```bash
# 1. اجلب التاريخ الهجري الحالي
HIJRI=$(curl -s "https://api.aladhan.com/v1/gToH" | jq -r '.data.hijri')
echo $HIJRI | jq '{month: .month.number, day: .day, year: .year}'

# 2. حوّل تاريخ المناسبة القادمة لميلادي
# مثلا: 1 رمضان 1448
curl -s "https://api.aladhan.com/v1/hToG/01-09-1448" \
  | jq '.data.gregorian.date'
```

ثم احسب الفرق بالأيام بين التاريخ الميلادي الحالي وتاريخ المناسبة.

## الجدول الهجري الشهري

```bash
curl -s "https://api.aladhan.com/v1/gToHCalendar/MONTH/YEAR"
```

مثال — جدول شهر أبريل 2026 بالهجري:
```bash
curl -s "https://api.aladhan.com/v1/gToHCalendar/4/2026" \
  | jq '.data[] | {gregorian: .gregorian.date, hijri: "\(.hijri.day) \(.hijri.month.ar) \(.hijri.year)"}'
```

## تنسيق العرض

```
التاريخ الهجري اليوم:
الإثنين 8 شوّال 1448 هـ
الموافق 6 أبريل 2026 م
```

عند السؤال عن مناسبة، احسب كم باقي عليها بالأيام واعرض التاريخ الميلادي المقابل.
