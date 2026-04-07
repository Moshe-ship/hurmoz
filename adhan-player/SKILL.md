---
name: adhan-player
description: Adhan audio playback with multiple muezzin voices
version: 1.0.0
author: Mousa Abu Mazin
license: MIT
platforms: [linux, macos]
prerequisites:
  commands: [ffplay]
  env_vars: []
metadata:
  hermes:
    tags: [islamic, adhan, audio, arabic]
---
# مشغّل الأذان

## المؤذنون المتاحون

### من مكتبة الأذان المحلية
| المؤذن | الملف |
|--------|-------|
| مشاري العفاسي | `adhan_alafasi.mp3` |
| عبدالباسط عبدالصمد | `adhan_abdalbaset.mp3` |
| ماهر المعيقلي | `adhan_almajali.mp3` |
| أذان المسجد الأقصى | `adhan_alaqsa.mp3` |
| أذان عمّان | `adhan_amman.mp3` |
| أذان الجزيري | `adhan_aljazari.mp3` |
| أذان الزهراني | `adhan_alzahran.mp3` |
| أذان أفريقيا | `adhan_africa.mp3` |
| أذان النفيس | `adhan_alnafees.mp3` |
| أذان الأسلمي | `adhan_aslami.mp3` |

### من الإنترنت

#### islamcan.com (أذان كامل)
```bash
# أذان مكة — عبدالرحمن السديس
curl -sL "https://www.islamcan.com/audio/adhan/azan1.mp3" --output /tmp/adhan.mp3

# أذان المدينة
curl -sL "https://www.islamcan.com/audio/adhan/azan2.mp3" --output /tmp/adhan.mp3

# أذان مشاري العفاسي
curl -sL "https://www.islamcan.com/audio/adhan/azan8.mp3" --output /tmp/adhan.mp3
```

> **تنبيه**: إذا كانت الروابط غير متاحة، حمّل ملف أذان MP3 يدوياً واحفظه محلياً:
> ```bash
> # ضع ملف الأذان في مجلد ثابت
> mkdir -p ~/Audio/adhan
> cp /path/to/downloaded/adhan.mp3 ~/Audio/adhan/adhan_alafasi.mp3
>
> # ثم شغّله مباشرة
> afplay ~/Audio/adhan/adhan_alafasi.mp3
> ```

## التشغيل

### macOS
```bash
afplay /path/to/adhan.mp3
```

### Linux
```bash
ffplay -nodisp -autoexit /path/to/adhan.mp3
```

### مع مستوى الصوت
```bash
ffplay -nodisp -autoexit -volume 80 /path/to/adhan.mp3
```

### تشغيل من ملف محلي (الطريقة الأضمن)
```bash
# macOS
afplay ~/Audio/adhan/adhan_alafasi.mp3

# Linux
ffplay -nodisp -autoexit ~/Audio/adhan/adhan_alafasi.mp3
```

## متى تستخدم
- المستخدم يقول "شغّل أذان" أو "أبي أسمع أذان"
- يطلب أذان بصوت مؤذن معين
- وقت الصلاة حان ويريد تنبيه

## القواعد
- إذا ما حدد مؤذن، شغّل العفاسي (الأشهر)
- إذا طلب "أذان الفجر"، نبّه أن أذان الفجر مختلف (فيه "الصلاة خير من النوم")
- احترم الأذان — لا تقطعه أو تعدّل فيه
- إذا الرابط الخارجي ما اشتغل، استخدم الملفات المحلية مباشرة
