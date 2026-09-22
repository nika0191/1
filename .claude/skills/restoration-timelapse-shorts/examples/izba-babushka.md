# Episode: izba-babushka — «Избу бабушки восстановили за лето»

Формат: **шот-лист действий** (11 шотов × 2–3 с ≈ 28 с). Генерация: Google Flow (Veo), 9:16, 8 с на шот,
затем обрезка до лучших 2–3 с. Статичных «перетеканий» нет.

## Консистентность (Flow → Ingredients)
Сначала сделай во Flow две картинки-ингредиента и подключай их к шотам, где они в кадре:
- **HOUSE**: `Old Russian wooden log house (izba) in a northern village, dark grey weathered logs, three small windows with ornate carved wooden window frames (nalichniki), steep roof partly collapsed, a young birch growing through the roof, tall grass, a leaning fence. Vertical 9:16, photorealistic, overcast.`
- **GRANDMA**: `An elderly Russian village woman seen from behind, grey headscarf with small flowers, dark wool cardigan, leaning on a wooden cane. Vertical 9:16, photorealistic.` (лицо не показываем — меньше брака и сильнее эмоция)

## Общий префикс каждого шота
```
Vertical 9:16, photorealistic documentary footage, handheld but steady, natural light,
real construction work, realistic hands and tools, no text, no watermark.
Audio: only the real sound of the action, no music.
```

## Шоты
| # | Тип | Ингр. | Промпт (после префикса) | Оставить |
|---|---|---|---|---|
| 01 | Хук, общий «до» | HOUSE, GRANDMA | `Wide shot: the elderly woman from behind stands at the broken gate looking at her collapsed old log house, a birch grows through the roof, wind moves the tall grass. Slow push-in toward the house.` | 2,5 с |
| 02 | Демонтаж | HOUSE | `Close-up: gloved hands rip rotten roof planks off with a crowbar, dust and splinters fall, the birch is pulled out through the hole.` | 2 с |
| 03 | Резка | — | `Close-up: a chainsaw cuts through a fresh golden pine log, thick sawdust sprays toward the camera.` | 2 с |
| 04 | Ручная работа | — | `Extreme close-up: an axe carves a round notch into the end of a pine log, fresh wood chips fly, slow motion.` | 2,5 с |
| 05 | Подъём | HOUSE | `Medium shot: two workers lift a new golden pine log onto the old dark log wall and hammer it into place with a wooden mallet.` | 2,5 с |
| 06 | Таймлапс-связка | HOUSE | `Wide time-lapse from the same angle as the opening shot: new rafters rise and the roof is covered with fresh wooden shingles, clouds race across the sky, static camera.` | 3 с |
| 07 | Резьба | — | `Macro: a chisel and mallet carve an ornate floral pattern into a new wooden window frame, curls of wood peel away.` | 2,5 с |
| 08 | Покраска | — | `Macro: a paintbrush glides along the carved window frame, leaving a perfect glossy sky-blue coat on white wood.` | 2 с |
| 09 | Печь | — | `Close-up inside the house: a trowel spreads mortar and lays a red brick on a traditional Russian stove, excess mortar squeezes out.` | 2 с |
| 10 | Финал, общий «после» | HOUSE | `Same wide angle as the opening shot: the fully restored log house at blue hour, golden new logs, sky-blue carved window frames, warm light in all windows, smoke from the chimney, new fence with flowers.` | 3 с |
| 11 | Эмоция | GRANDMA | `From behind: the elderly woman steps into the warm restored room, pauses, and gently touches the white Russian stove; soft warm light, a cat on the bench.` | 3 с |

Петля: последний кадр (тёплая изба) → первый кадр (разрушенная) — резкий контраст «после → до» при повторе.

## Сборка
Сохрани обрезанные шоты как `episodes/izba-babushka/clips/01.mp4 … 11.mp4`, затем:
```bash
bash .claude/skills/restoration-timelapse-shorts/scripts/assemble.sh episodes/izba-babushka --speed 1.0
```
Хук-текст на 01: **«Бабушка 20 лет ждала этого»** / EN: **"She waited 20 years for this"**.

## Упаковка
- RU: `Избу бабушки восстановили за одно лето 😭 [ИИ-концепт]`
- EN: `We Rebuilt Grandma's Collapsed Log House by Hand ❤️ [AI concept]`
- DE: `Omas verfallenes Holzhaus komplett restauriert ❤️ [KI-Konzept]`
- Описание: «Эта изба на севере простояла без хозяина 20 лет. Что было бы, если её восстановить по-старому —
  с резными наличниками и настоящей печью? Концепт, созданный с помощью ИИ. Какой дом восстановить следующим? 👇»
- Хэштеги: `#restoration #beforeandafter #constructiontimelapse #woodworking #asmr`
- В Studio: «Altered or synthetic content» = Да.

## Проверка каждого шота (перед сборкой)
- [ ] Руки: 5 пальцев, инструмент держат правильно
- [ ] Изба в 01/06/10 — одна и та же (3 окна, та же форма крыши)
- [ ] В кадре есть действие с первой же секунды (обрезай «раскачку»)
- [ ] Звук действия есть и соответствует (пила звучит как пила)
