# AI Influencer Studio — создай своего AI-инфлюенсера за выходные

> Живая панель + полный гид + пример персонажа **Амина (24, Владикавказ)**. Работает без ключей в DEMO и с ключами (Fal, ElevenLabs, HeyGen).

![Амина](assets/amina_reference.jpg)

## Что внутри

- 📖 **Полный гид 2026** → [`docs/GUIDE.md`](docs/GUIDE.md) — 17 разделов: от рынка ($11.7B, ER 5.7%) и сравнения инструментов (Flux, Higgsfield Soul ID, Kling 3.0, HeyGen, ElevenLabs, Midjourney) до пошагового плана на 7 шагов, бюджетов (2100₽–$200), закона (Instagram AI-label с 31.08.2026, FTC) и чек-листа «запустить за выходные».
- 👩‍🎤 **Example Character** → [`characters/amina.json`](characters/amina.json) — готовый Character Bible: ниша travel/lifestyle, 3 столпа контента, визуальный паспорт, 5 стартовых промптов, био, план монетизации.
- 🖼️ **Assets** → `assets/` — 3 референс-фото Амины (референс, кафе, горы).
- 🧠 **Библиотека** → `src/influencer/` — Python-модули для персонажа, промптов, генерации (Fal.ai Flux, Kling, ElevenLabs, HeyGen).
- 🖥️ **Веб-студия** → `app/` — FastAPI + UI (генератор промптов, подписей, контент-план 30 дней, инструкции для видео/голоса). Биндится на `0.0.0.0` — работает в preview.
- 🛠️ **CLI** → `scripts/create_influencer.py` — создай своего персонажа за 10 сек.

---

## Быстрый старт (2 минуты)

### 1. Установка
```bash
pip install -r requirements.txt
cp .env.example .env   # опционально — вставь ключи FAL_API_KEY / ELEVENLABS_API_KEY для реальной генерации
```

### 2. Запуск студии
```bash
python -m app.main
# или
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
Открой **http://localhost:8000** (в Arena preview — порт 8000 автоматически проксируется как `https://8000-...e2b.app`).

### 3. Что делать в студии
- **Генератор промптов:** введи сцену → получи готовый промпт (паспорт Амины уже вшит) → копируй в Leonardo AI / Fal Flux / syntx Nano Banana / APOB.
- **Подписи:** выбери столп (Кавказ/Город/Образы) → сгенерируй подпись с хештегами.
- **Контент-план:** таблица на 30 дней — каждый день промпт + подпись, всё копируется одним кликом.
- **Видео/голос:** без ключа — получаешь точную инструкцию для Kling / Higgsfield / HeyGen / Hedra; с ключом — прямой вызов API.

### 4. DEMO vs PRO
| Режим | Что нужно | Что получаешь |
|-------|-----------|---------------|
| **DEMO (без ключей)** | ничего | готовые промпты, подписи, планы, пошаговые инструкции куда их вставить |
| **PRO (с ключами)** | `FAL_API_KEY` (fal.ai), `ELEVENLABS_API_KEY`, `HEYGEN_API_KEY` | генерация прямо из панели |

Ключи добавляешь в `.env`. Без них всё равно полностью обучаешься и запускаешь ручную генерацию — этого достаточно для старта.

---

## Создать своего персонажа

### Вариант A — CLI (10 сек)
```bash
python scripts/create_influencer.py --name "Лера" --age 22 --city "Казань" --niche "фитнес и ПП"
# создаст characters/lera.json
```

### Вариант B — вручную
```bash
cp characters/amina.json characters/my.json
# открой my.json — поменяй name/city/niche/visual_identity/prompt_passport/bio
# перезапусти сервер
```

Затем:
1. Возьми `starter_prompts` из нового JSON.
2. Сгенерируй 20 вариантов лица в Leonardo AI (Flux.1 Dev) / syntx.ai (Nano Banana Pro) / Midjourney — выбери лучшее → сохрани как `assets/<name>_reference.jpg`.
3. Закрепи лицо: Higgsfield Soul ID (загрузи 20 фото, 3 мин) или Flux LoRA на fal.ai ($2).
4. Генерируй ленту через панель — каждый раз с референсом / LoRA.

Подробнее — [docs/GUIDE.md — шаг 7](docs/GUIDE.md#7-план).

---

## Инструменты — шпаргалка 2026

| Слой | Рекомендация новичкам | Альтернатива |
|------|----------------------|--------------|
| **Лицо** | Leonardo AI → Flux.1 Dev (бесплатно 150 токенов/день) | syntx.ai → Nano Banana Pro, APOB 80 кред/день |
| **Фиксация** | Higgsfield Soul ID ($9) | Fal.ai Flux LoRA ($1–5) |
| **Лента** | APOB / Morphed | OpenArt Omni Reference |
| **Видео** | KlingAI.com (Image→Video) | Higgsfield, Runway, Veo 3.1 |
| **Голос** | ElevenLabs (free 10 мин) | HeyGen (175 языков) |
| **Автопостинг** | Buffer / Later | — |

Для пользователей из РФ: syntx.ai, KADR (2100₽/мес за 30 фото+8 видео), GPTunneL для Midjourney.

---

## Структура проекта

```
.
├── docs/GUIDE.md              # полный гид (17 разделов)
├── characters/amina.json      # Character Bible примера
├── assets/                    # референс-фото
├── src/influencer/
│   ├── character.py           # загрузка Bible
│   ├── prompts.py             # build_prompt / build_caption / monthly_plan
│   └── generator.py           # обёртки Fal/Leonardo/ElevenLabs/HeyGen (DEMO+real)
├── app/
│   ├── main.py                # FastAPI
│   └── static/index.html      # UI студии
├── scripts/create_influencer.py
├── requirements.txt
└── .env.example
```

---

## Закон — не пропусти

- **Instagram (31.08.2026+):** включи `Настройки профиля → AI-generated profile` — без метки режут охваты в Reels/Explore.
- **Реклама:** ставь `#реклама` / `ERID` (РФ) и `AI-generated` (FTC/US) в каждом рекламном посте.
- **Не используй чужое лицо/голос** без письменного согласия.

См. раздел 12 в GUIDE.md.

---

## Обучение — с чего начать прямо сегодня

1. Прочитай `docs/GUIDE.md` (30 мин).
2. Открой студию `http://localhost:8000` — поиграй с генератором промптов и планом.
3. Сгенерируй 20 лиц Амины → выбери 1 → сделай 20 фото стартового пака (кафе/горы/селфи) с референсом.
4. Сделай 3 видео в Kling (фото→видео) + 1 talking в HeyGen.
5. Заведи Instagram + TikTok, залей 9 постов, включи AI-label, пости 1/день 30 дней.

Чек-лист на выходные — в GUIDE.md раздел 17.

---

## Деплой

```bash
# локально
python -m app.main
# docker (если нужен)
# docker build -t ai-influencer . && docker run -p 8000:8000 --env-file .env ai-influencer
```

---

## FAQ

**Нужна ли видеокарта?** Нет, если используешь облачные генераторы (Leonardo/Fal/syntx/Kling). Локальный Stable Diffusion — опционально.

**Сколько стоит старт?** От 0₽ (демо-лимиты) до 2100₽/мес (KADR) или $50–100 на западных сервисах.

**Это легально?** Да, если лицо вымышленное, голос синтезирован/лицензирован и есть disclosure (AI-label).

**Можно ли 18+?** Технически да, но Instagram/TikTok банят. Для этого — FanVue/Patreon + возрастная верификация.

---

*Собрано 16.10.2026 для Владикавказа. Удачного запуска! Вопросы — открывай issue или пиши.*

