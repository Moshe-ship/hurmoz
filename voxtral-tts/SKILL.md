---
name: voxtral-tts
description: "تحويل النص لصوت عربي — حوّل أي نص عربي لملف صوتي باستخدام Voxtral أو NAMAA TTS. استخدم عندما يريد المستخدم سماع نص أو توليد صوت عربي."
version: 1.0.0
author: Mousa Abu Mazin
license: MIT
platforms: [linux, macos]
prerequisites:
  commands: [curl, python3]
  env_vars: [MISTRAL_API_KEY, HF_TOKEN]
metadata:
  hermes:
    tags: [arabic, voxtral-tts]
---

# تحويل النص إلى صوت عربي

أداة لتحويل النصوص العربية إلى ملفات صوتية عالية الجودة. تدعم عدة محركات: Voxtral من Mistral كخيار أساسي سحابي، ومكتبة NAMAA TTS كبديل محلي سعودي يعمل بدون إنترنت. مفيدة لإنتاج محتوى صوتي عربي، بودكاست، تعليق صوتي، أو سماع النطق الصحيح للنصوص والآيات.

## الطريقة الأولى: Voxtral TTS (Mistral — الأساسية)

### عبر API
```bash
curl -s -X POST "https://api.mistral.ai/v1/audio/speech" \
  -H "Authorization: Bearer $MISTRAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "voxtral-mini-2025-12",
    "input": "النص العربي هنا",
    "voice": "aria",
    "language": "ar",
    "response_format": "mp3"
  }' \
  --output output.mp3
```

### الأصوات المتاحة
| الصوت | الوصف |
|-------|-------|
| `aria` | أنثوي، واضح |
| `dan` | ذكوري، هادئ |
| `nova` | أنثوي، حيوي |

### استنساخ الصوت (Voice Cloning)
يدعم Voxtral استنساخ الصوت من عينة أقل من 5 ثوانٍ.

## الطريقة الثانية: NAMAA TTS (محلي سعودي — بدون إنترنت)

NAMAA هو مشروع TTS سعودي مفتوح المصدر يدعم اللهجة السعودية والفصحى.

### التثبيت
```bash
pip install namaa-tts
```

### الاستخدام
```python
from namaa_tts import NamaaTTS

tts = NamaaTTS()
tts.synthesize("مرحبا، كيف حالك اليوم؟", output_path="output.wav")
```

> **ملاحظة**: NAMAA يعمل محلياً بالكامل ولا يحتاج مفتاح API أو إنترنت. مناسب لمن يفضل الخصوصية أو لا يملك اشتراك Mistral.

## الطريقة الثالثة: SILMA TTS عبر HuggingFace (قد لا يكون متاحاً)

> **تنبيه**: نقطة الوصول هذه قد تكون غير متاحة (HTTP 410). استخدم Voxtral أو NAMAA بدلاً منها.

```bash
curl -s -X POST "https://api-inference.huggingface.co/models/silma-ai/SILMA-TTS-v1" \
  -H "Authorization: Bearer $HF_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"inputs": "النص العربي هنا"}' \
  --output output.wav
```

## التشغيل بعد التوليد

```bash
# macOS
afplay output.mp3

# Linux
ffplay -nodisp -autoexit output.mp3
```

## متى تستخدم
- المستخدم يقول "اقرأ لي" أو "أبي أسمع"
- يريد تحويل نص لبودكاست أو فيديو
- يريد نطق صحيح لكلمة أو آية
- يطلب صوت عربي لمشروع

## القواعد
- تأكد من تشكيل النص قبل التحويل للحصول على نطق أفضل
- للآيات القرآنية، نبّه أن TTS ليس بديلاً عن القراءة الصحيحة
- احفظ الملف بالمسار الذي يحدده المستخدم
- جرّب Voxtral أولاً (أفضل جودة)، ثم NAMAA كبديل محلي
- HF_TOKEN مطلوب فقط إذا أردت استخدام SILMA عبر HuggingFace
