# Промпты: кадры стадий и видео

Промпты пиши на **английском** — все модели (Veo, Grok Imagine, FLUX) понимают его лучше всего.
Держи один «паспорт кадра» на весь эпизод и вставляй его в каждый промпт без изменений.

## ★ Статичная цепочка стадий (основной формат)
Один локальный объект, одна неподвижная камера, объект меняется в кадре стадия за стадией. Это формат,
который набирает миллионы у Bau Rausch, Structural.Aesthetics, Map Snap. Обычно достаточно **5–6 кадров
стадий → 4–5 клипов-переходов** на 60–90 секунд ролика — не нужно дробить на десятки мелких вставок.

**Железное правило: в статичных кадрах-стадиях НЕТ людей, техники и инструментов.** Кадр-стадия — это
редактирование ПРЕДЫДУЩЕГО кадра, а не новая генерация. Если на стадии 2 стоит рабочий в жёлтой каске,
модель при редактировании стадии 3 просто скопирует его пиксель в пиксель — рабочий «замрёт» в одной
позе на всех следующих кадрах, и это будет заметно и странно. Люди и техника появляются **только**
в видео-переходах между кадрами (раздел 3), и в каждом переходе — разное действие и разные позы,
не повтор. Первая стадия — это буквально только уборка территории (сняли плющ/мусор), ничего
конструктивного ещё не меняется; не смешивай несколько стадий в один шаг, иначе кадр останется
«грязным» и результат не будет читаться как прогресс.

## 0. Паспорт кадра (CAMERA LOCK)
```
Vertical 9:16, locked-off tripod camera, eye level from 30 m away, 35mm lens,
same framing in every image, overcast soft daylight, photorealistic, documentary photo,
no text, no watermark.
```
Меняются только: состояние объекта, время суток в финале, люди/техника.

## 1. Якорный кадр — разруха (text-to-image)
```
[CAMERA LOCK]
An abandoned {OBJECT} in {PLACE}, left to decay for {YEARS} years.
{INTRIGUE_DETAIL}. Broken windows, collapsed roof sections, rust streaks, moss, overgrown weeds,
piles of debris, graffiti fragments. Melancholic mood, realistic textures, high detail.
```
Примеры `{INTRIGUE_DETAIL}`: `a birch tree growing through the roof`, `the steam locomotive is sunk
to its wheels in the forest soil`, `a faded Soviet mosaic is still visible under peeling plaster`.

## 2. Цепочка стадий (image edit — подавай ПРЕДЫДУЩИЙ кадр на вход)
Общий префикс для каждого шага:
```
Edit this exact image. Keep the camera, framing, perspective, lighting, background and the
building's geometry EXACTLY the same. Change only the following:
```
Стадии (для 6-шаговой схемы). Колонка «Кадр» — без людей, идёт в промпт редактирования картинки.
Колонка «Видео-переход» — с людьми, идёт в промпт видео между этим кадром и следующим (раздел 3);
действие и позы должны отличаться от предыдущего перехода.

| # | Стадия | Кадр (без людей) | Видео-переход (с людьми) |
|---|---|---|---|
| 1 | Расчистка | `all vegetation and debris removed, ground cleared and leveled, path swept clean, building still damaged, no scaffolding yet, no people or tools in the shot` | `Workers arrive, strip ivy and vines off the walls by hand, rake debris into a pile and haul it away in a wheelbarrow` |
| 2 | Леса и демонтаж | `scaffolding covers the facade, damaged roof removed down to the beams, stacks of new bricks and timber sit neatly to one side, ground stays clean, no people or tools in the shot` | `A crew erects wooden scaffolding, climbs it, and pulls off the last damaged roof beams, tossing debris into a dumpster below` |
| 3 | Конструкция | `new roof structure and rafters installed, walls repaired with fresh brick patches, new window frames in place without glass, no people or tools in the shot` | `Workers on the scaffolding hammer new rafters into place while others below lay fresh bricks and set new window frames` |
| 4 | Закрытие контура | `new roof covering finished, windows glazed, scaffolding mostly gone, facade plastered but unpainted, no people or tools in the shot` | `A crew nails the final roof shingles into place, fits clear glass into each window, and takes the scaffolding down section by section` |
| 5 | Отделка | `facade painted in {COLOR}, decorative details restored, landscaping started with a fresh gravel path, no people or tools in the shot` | `One worker rolls fresh paint across the facade while another lays a gravel path and plants shrubs along it` |
| 6 | Финал | `fully restored and alive, golden hour / blue hour light, warm lights glowing in every window, lush garden, no people in the shot` | `As dusk falls the crew packs up and leaves; warm light switches on in each window one by one` |

Для **поездов/транспорта** замени стадии: расчистка вокруг → подъём на домкраты/кран → снятие ржавчины
(пескоструй) → грунт → покраска и хром → финал: едет/пар/огни. Тот же принцип: домкраты/кран/инструменты
на кадре — нет, только в видео.

Для **упадка (обратный порядок)** начни с нового объекта и иди в обратную сторону: трещины → облезлая
краска → разбитые стёкла → растения → обрушение.

### Где делать редактирование
- **FLUX Kontext** (подключено в этой сессии: `mcp__Bfl_ai__generate_image` с входным изображением) —
  лучше всех держит геометрию. Аспект 9:16.
- **Grok Imagine** → загрузить кадр → «Edit image» с промптом выше.
- **Google Flow** → создать изображение (Nano Banana / Imagen) → «Edit/Remix» с входным кадром.
Если геометрия «поплыла» — повтори шаг, добавив `Do not move or resize any windows or walls.`

## 3. Видео между стадиями

### Google Flow / Veo — Frames to Video (первый + последний кадр)
Загрузи кадр N как **start frame**, кадр N+1 как **end frame**, формат 9:16, 8 с:
```
Construction timelapse. Locked-off static camera, no camera movement.
Workers move fast in time-lapse, clouds race across the sky, shadows sweep across the ground.
{STAGE_ACTION}. Realistic physics, continuous transformation from the first frame to the last.
Audio: construction ambience — hammering, drills, angle grinder, distant voices, birds. No music.
```
`{STAGE_ACTION}` — одна фраза из таблицы стадий в прошедшем → настоящем времени
(«scaffolding rises around the facade and the old roof is torn down»).

Финальный клип (облёт):
```
Slow cinematic drone push-in and gentle orbit around the fully restored {OBJECT} at blue hour,
warm window lights, {LIFE_DETAIL}. Audio: calm evening ambience, soft wind, distant laughter.
```

### Grok Imagine — image to video
Загрузи кадр стадии, 6–10 с, режим Normal (не Spicy/Fun):
```
Fast time-lapse of a construction crew working on this building, static camera,
clouds moving quickly, realistic, no camera shake.
```
Grok не фиксирует последний кадр — используй его для живых вставок и для хука (рабочий входит в
разрушенный дом, фары поезда загораются).

### FLUX video (из этой сессии)
`mcp__Bfl_ai__generate_video` с двумя ключевыми кадрами = переход между стадиями без выхода из Claude.
Сначала делай `draft: true`, выбирай лучший, потом `enhance_video`.

## 4. Хук-тексты (≤ 6 слов, крупно в первые 1,5 с)
- `Бросили 40 лет назад`
- `Этому паровозу 90 лет`
- `Смотри на крышу 👀`
- `Left to rot since 1986`
- `Wait for the lights…`

## 5. Частые брак-факторы и как лечить
| Проблема | Лечение |
|---|---|
| Камера «плывёт» в Veo | Добавь `static tripod shot, absolutely no camera movement`; делай клипы короче (4–6 с) |
| Число окон меняется | Сгенерируй стадию заново от предыдущего кадра, а не от якоря |
| Люди-мутанты | Рабочие мелкие, вдалеке, в движении; финальных людей — со спины |
| Водяной знак | Не используй бесплатные тарифы для финала; кадрируй `assemble.sh` чуть с запасом |
| Мерцание между клипами | Берите последний кадр клипа N как старт клипа N+1 (а не исходную стадию) |
| Клип получился короче, чем нужно | Продолжи с его последнего кадра (стоп-кадр/скриншот) тем же промптом — не новый якорь |
| Рабочие в одинаковой позе на всех кадрах | Не описывай людей в промптах для статичных кадров-стадий — только в видео между ними, и каждый раз новое действие |
| Кадр всё ещё выглядит «грязным» после стадии 1 | Стадия 1 — только уборка (убрали плющ/мусор), больше ничего не меняй; не смешивай уборку со стройкой в одном шаге |

## Шот-лист действий (опционально, не по умолчанию)
Для канала, который хочет больше крупных планов рук/инструментов и ASMR-звука, вместо статичной
цепочки можно собрать ролик из 8–12 коротких экшн-сценок по 2–3 с — это отдельная стилистика, а не
замена основного формата. Общий префикс:
```
Vertical 9:16, photorealistic documentary footage, handheld but steady, natural light,
real construction work, realistic hands and tools, no text, no watermark.
Audio: only the real sound of the action, no music.
```
Типы шотов (чередуй общий → крупный → крупный → общий):
| Тип | Шаблон |
|---|---|
| Хук, общий «до» | `Wide shot of the abandoned {OBJECT}, {INTRIGUE}. Slow push-in.` |
| Демонтаж | `Close-up: a worker's gloved hands rip rotten {MATERIAL} off with a crowbar, dust and splinters fly.` |
| Резка | `Close-up: a chainsaw cuts through a fresh pine log, sawdust sprays toward the camera.` |
| Ручная работа | `Extreme close-up: an axe carves a notch in a log, wood chips fly, slow motion.` |
| Подъём | `Medium shot: two workers lift a heavy new {PART} into place and hammer it in.` |
| Кладка/заливка | `Close-up: a trowel spreads mortar and lays a red brick, excess mortar squeezes out.` |
| Отделка | `Macro: a paintbrush glides along carved wood trim, leaving a perfect glossy {COLOR} coat.` |
| Финал, общий «после» | `Same wide angle as the opening shot: the restored {OBJECT} at blue hour, warm windows, chimney smoke.` |
| Эмоция | `From behind: {PERSON} steps into the restored {ROOM}, pauses and touches {DETAIL}.` |
